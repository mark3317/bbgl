"""Peer discovery and preflight on a selected private LAN/VPN; no game server.

The selected network is the trust boundary, as with a LAN game. Bootstrap offers
are exchanged only on that interface. Native gameplay remains on its own UDP port.
"""
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import secrets
import socket
import socketserver
import subprocess
import threading
import time

DISCOVERY_PORT, CONTROL_PORT, GAME_PORT = 37601, 37600, 37658
PROTOCOL = 'BBGL-P2P-1'
NO_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def write_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_bytes(encoded(value))
    os.replace(temp, path)


def choose_network(networks, mode='auto', custom=''):
    if mode == 'custom':
        ip = str(ipaddress.IPv4Address(custom.strip()))
        choices = [n for n in networks if ip in n['addresses']]
    elif mode in ('tailscale', 'radmin'):
        choices = [n for n in networks if mode == n.get('provider') or mode in n['text'].lower()]
    else:
        choices = [n for n in networks if n['vpn']] or networks
    if not choices:
        raise ValueError('Selected network is not connected. Check the VPN and refresh.')
    if len(choices) != 1 or len(choices[0]['addresses']) != 1 and mode != 'custom':
        raise ValueError('Several networks found. Choose Tailscale, Radmin or a custom local IPv4.')
    n = choices[0]
    address = ip if mode == 'custom' else n['addresses'][0]
    return address, n


def candidate_addresses(network, tailscale=None, extra=''):
    result = {str(ipaddress.IPv4Address(x)) for x in re.split(r'[,;\s]+', extra.strip()) if x}
    if (network.get('provider') == 'tailscale' or 'tailscale' in network['text'].lower()) and tailscale:
        reply = subprocess.run([str(tailscale), 'status', '--json'], capture_output=True,
                               text=True, timeout=5, creationflags=NO_WINDOW)
        if reply.returncode:
            raise ValueError('Tailscale is not connected.')
        status = json.loads(reply.stdout)
        if status.get('BackendState') != 'Running':
            raise ValueError('Tailscale is not connected.')
        for peer in (status.get('Peer') or {}).values():
            if peer.get('Online'):
                result.update(ip for ip in peer.get('TailscaleIPs', []) if ':' not in ip)
    else:
        for subnet in network['ranges']:
            net = ipaddress.IPv4Network(subnet, strict=False)
            if net.prefixlen < 31:
                result.add(str(net.broadcast_address))
    return result


def configuration(offers):
    if not 2 <= len(offers) <= 5:
        raise ValueError('Open the launcher on 2–5 players in the same network.')
    offers = sorted(offers, key=lambda p: p['id'])
    if len({p['host'] for p in offers}) != len(offers):
        raise ValueError('Each player needs a separate network address.')
    identity = [{k: p[k] for k in ('id', 'seed')} for p in offers]
    key = hashlib.sha256(encoded(identity)).hexdigest()
    # Address changes do not create a new group or reset its durable role journal.
    return {'version': 1, 'group': hashlib.sha256(('group:' + key).encode()).hexdigest()[:32],
            'secret': key, 'epoch': 1,
            'members': [{'id': p['id'], 'host': p['host'], 'port': CONTROL_PORT,
                         'p2p': GAME_PORT} for p in offers]}


def digest(cfg):
    return hashlib.sha256(encoded(cfg)).hexdigest()


class Discovery:
    def __init__(self, profile, address, targets, name, port=DISCOVERY_PORT):
        self.profile, self.address, self.port = Path(profile), address, port
        self.targets = set(targets)
        path = self.profile / 'coop/party/identity.json'
        if path.exists():
            identity = json.loads(path.read_text(encoding='utf-8'))
        else:
            identity = {'id': 'P' + secrets.token_hex(7), 'seed': secrets.token_hex(32)}
            write_json(path, identity)
        self.offer = dict(identity, host=address, name=str(name)[:32], protocol=PROTOCOL)
        self.lock, self.probes, self.peers = threading.RLock(), {}, {}
        self.closed, self.locked = threading.Event(), None
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp.settimeout(.2)
        try:
            self.udp.bind((address, port))
            outer = self

            class Server(socketserver.ThreadingTCPServer):
                daemon_threads = True
                allow_reuse_address = False
                request_queue_size = 16

            class Handler(socketserver.StreamRequestHandler):
                def handle(self):
                    self.request.settimeout(5)
                    try:
                        raw = self.rfile.readline(8193)
                        if len(raw) > 8192 or not raw.endswith(b'\n'):
                            return
                        body = json.loads(raw)
                        if body.get('protocol') != PROTOCOL:
                            return
                        answer = {'ok': True, 'offer': outer.offer}
                        if body.get('kind') == 'check':
                            cfg = configuration(outer.offers())
                            if body.get('digest') != digest(cfg) or outer.locked not in (None, digest(cfg)):
                                raise ValueError('Players see different groups. Refresh all launchers.')
                            outer.mesh_check(cfg)
                        self.wfile.write(encoded(answer) + b'\n')
                    except (OSError, ValueError, KeyError) as error:
                        try:
                            self.wfile.write(encoded({'ok': False, 'error': str(error)}) + b'\n')
                        except OSError:
                            pass

            self.tcp = Server((address, port), Handler)
        except Exception:
            self.udp.close()
            raise
        threading.Thread(target=self.tcp.serve_forever, daemon=True).start()
        threading.Thread(target=self._listen, daemon=True).start()
        threading.Thread(target=self._announce, daemon=True).start()

    def offers(self):
        with self.lock:
            now = time.monotonic()
            return [self.offer] + [p for p, seen in self.peers.values() if now - seen < 5]

    def _remember(self, offer, address):
        if (offer.get('protocol') != PROTOCOL or offer.get('host') != address or
                not re.fullmatch(r'[A-Za-z0-9]{1,16}', offer.get('id', '')) or
                not re.fullmatch(r'[a-f0-9]{64}', offer.get('seed', ''))):
            return
        if offer['id'] == self.offer['id']:
            return
        with self.lock:
            if len(self.peers) >= 16 and offer['id'] not in self.peers:
                return
            self.peers[offer['id']] = (offer, time.monotonic())

    def _listen(self):
        while not self.closed.is_set():
            try:
                raw, source = self.udp.recvfrom(8192)
                body = json.loads(raw)
                if body.get('protocol') != PROTOCOL:
                    continue
                if body.get('kind') == 'ping':
                    self.udp.sendto(encoded(dict(protocol=PROTOCOL, kind='pong', nonce=body.get('nonce'))), source)
                elif body.get('kind') == 'pong':
                    with self.lock:
                        event = self.probes.get((source[0], body.get('nonce')))
                    if event:
                        event.set()
                elif body.get('kind') in ('hello', 'reply'):
                    self._remember(body.get('offer', {}), source[0])
                    if body['kind'] == 'hello':
                        self.udp.sendto(encoded(dict(protocol=PROTOCOL, kind='reply', offer=self.offer)), source)
            except socket.timeout:
                pass
            except (OSError, ValueError, KeyError, TypeError):
                if self.closed.is_set():
                    return

    def _announce(self):
        while not self.closed.is_set():
            targets = self.targets | {p['host'] for p in self.offers() if p['host'] != self.address}
            for host in targets:
                try:
                    self.udp.sendto(encoded(dict(protocol=PROTOCOL, kind='hello', offer=self.offer)), (host, self.port))
                except OSError:
                    pass
            self.closed.wait(1)

    def request(self, host, kind='hello', **fields):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(4)
            sock.bind((self.address, 0))
            sock.connect((host, self.port))
            sock.sendall(encoded(dict(protocol=PROTOCOL, kind=kind, **fields)) + b'\n')
            with sock.makefile('rb') as stream:
                raw = stream.readline(8193)
            if len(raw) > 8192:
                raise ValueError('Invalid peer response')
            result = json.loads(raw)
            if not result.get('ok'):
                raise ValueError(result.get('error', 'Peer check failed'))
            return result

    def mesh_check(self, cfg):
        for peer in cfg['members']:
            if peer['id'] == self.offer['id']:
                continue
            reply = self.request(peer['host'])
            if reply['offer']['id'] != peer['id']:
                raise ValueError('Peer identity changed. Refresh the connection.')
            nonce, event = secrets.token_hex(16), threading.Event()
            with self.lock:
                self.probes[(peer['host'], nonce)] = event
            try:
                for _ in range(3):
                    self.udp.sendto(encoded(dict(protocol=PROTOCOL, kind='ping', nonce=nonce)), (peer['host'], self.port))
                    if event.wait(.4):
                        break
                if not event.is_set():
                    raise ValueError('UDP connection failed. Check the VPN and firewall on every PC.')
            finally:
                with self.lock:
                    self.probes.pop((peer['host'], nonce), None)

    def check(self):
        cfg = configuration(self.offers())
        key = digest(cfg)
        if self.locked not in (None, key):
            raise ValueError('The running game uses another group. Finish that session first.')
        self.mesh_check(cfg)
        for peer in cfg['members']:
            if peer['id'] != self.offer['id']:
                self.request(peer['host'], 'check', digest=key)
        # Never create a replacement group while the former owner/room is live.
        path = self.profile / 'coop/party/config.json'
        if path.exists():
            old = json.loads(path.read_text(encoding='utf-8'))
            journal = self.profile / 'coop/party/groups' / old['group'] / 'party-journal.json'
            if old['group'] != cfg['group'] and journal.exists():
                state = json.loads(journal.read_text(encoding='utf-8'))['state']
                if state.get('owner') or state.get('room'):
                    raise ValueError('The previous group has not finished its session. Reconnect those players first.')
        write_json(path, cfg)
        return cfg, path

    def close(self):
        self.closed.set()
        self.udp.close()
        self.tcp.shutdown()
        self.tcp.server_close()


def launch_environment(env, discovery):
    cfg, path = discovery.check()  # fresh check; UI readiness is never a cached permission
    discovery.locked = digest(cfg)
    env = dict(env)
    env.update(BB_PARTY_CONFIG=str(path), BB_PARTY_MEMBER=discovery.offer['id'],
               BBGL_PROFILE_DIR=str(discovery.profile), BB_DATA_DIR=str(discovery.profile),
               BB_FPS='60', BB_FPS_LIMIT='60', BB_COOP='1')
    patches = [p.strip() for p in env.get('BB_PATCHES', '').split(';') if p.strip()]
    if 'Skip Intro' not in patches:
        patches.append('Skip Intro')
    env['BB_PATCHES'] = ';'.join(patches)
    for key in ('BB_NET_BACKEND', 'BB_THD_TOKEN', 'BB_THD_ONLINE_ID', 'BB_THD_SERVER', 'BB_THD_AUTH', 'BB_THD_RULESET'):
        env.pop(key, None)
    return env

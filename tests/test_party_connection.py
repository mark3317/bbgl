"""Real discovery/preflight sockets; no game, production profile or VPN changes."""
import json
from pathlib import Path
import socket
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'launcher'))
import bbport_party as party


class PartyConnectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.nodes = []

    def tearDown(self):
        for node in self.nodes:
            node.close()
        self.temp.cleanup()

    def group(self, count=3):
        hosts = [f'127.0.0.{n+21}' for n in range(count)]
        for i, host in enumerate(hosts):
            self.nodes.append(party.Discovery(Path(self.temp.name)/str(i), host, set(hosts)-{host}, f'Player{i}'))
        deadline = time.monotonic()+5
        while time.monotonic()<deadline:
            if all(len(n.offers())==count for n in self.nodes):
                return self.nodes
            time.sleep(.05)
        self.fail('Discovery did not converge')

    def test_full_mesh_and_launch_without_server_or_invite_code(self):
        a,b,c = self.group()
        configs = [n.check()[0] for n in self.nodes]
        self.assertEqual(configs[0], configs[1]); self.assertEqual(configs[0], configs[2])
        env = party.launch_environment({'BB_NET_BACKEND':'old','BB_PATCHES':'Other'}, a)
        self.assertEqual(env['BB_FPS'], '60')
        self.assertEqual(env['BB_FPS_LIMIT'], '60')
        self.assertNotIn('BB_NET_BACKEND',env)
        self.assertEqual(env['BB_PARTY_MEMBER'], a.offer['id'])
        self.assertIn('Skip Intro',env['BB_PATCHES'])
        self.assertEqual(json.loads(Path(env['BB_PARTY_CONFIG']).read_text()), configs[0])
        self.assertEqual(a.locked,party.digest(configs[0]))

    def test_udp_failure_blocks_start(self):
        a,b = self.group(2)
        original = b.udp.sendto
        class NoUDPReplies:
            def __getattr__(self, name):
                return getattr(real, name)
            def sendto(self, data, target):
                if json.loads(data).get('kind') != 'pong':
                    return original(data,target)
        real = b.udp
        # Block only replies on the checked peer; leave discovery/TCP working.
        with patch.object(b, 'udp', NoUDPReplies()):
            with self.assertRaisesRegex(ValueError,'UDP connection failed'):
                a.mesh_check(party.configuration(a.offers()))
        b.udp = real

    def test_inconsistent_roster_and_stale_readiness_block_start(self):
        a,b = self.group(2)
        cfg,_ = a.check()
        b.locked = 'different-group'
        with self.assertRaisesRegex(ValueError,'different groups'):
            party.launch_environment({},a)
        b.locked=None
        with a.lock:
            a.peers.clear()
        with self.assertRaises(ValueError):
            party.configuration(a.offers())

    def test_old_live_group_cannot_be_replaced(self):
        a,b = self.group(2)
        old = {'group':'old-group'}
        party.write_json(a.profile/'coop/party/config.json',old)
        party.write_json(a.profile/'coop/party/groups/old-group/party-journal.json',
                         {'state':{'owner':'old-owner','room':None}})
        with self.assertRaisesRegex(ValueError,'previous group'):
            a.check()

    def test_network_selection_and_tailscale_peer_inventory(self):
        lan={'text':'Ethernet','vpn':False,'addresses':['192.168.1.3'],'ranges':['192.168.1.0/24']}
        ts={'text':'Tailscale','vpn':True,'addresses':['100.64.1.3'],'ranges':['100.64.1.3/32']}
        self.assertEqual(party.choose_network([lan,ts])[0],'100.64.1.3')
        self.assertEqual(party.choose_network([lan,ts],'custom','192.168.1.3')[0],'192.168.1.3')
        with self.assertRaises(ValueError): party.choose_network([lan],'radmin')
        with patch.object(party.subprocess,'run') as run:
            run.return_value.returncode=0
            run.return_value.stdout=json.dumps({'BackendState':'Running','Peer':{
                'a':{'Online':True,'TailscaleIPs':['100.64.1.4','fd7a::1']},
                'b':{'Online':False,'TailscaleIPs':['100.64.1.5']}}})
            self.assertEqual(party.candidate_addresses(ts,'tailscale.exe'),{'100.64.1.4'})


if __name__=='__main__':
    unittest.main()

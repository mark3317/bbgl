"""Local-three profile/port isolation; no production profiles or native games."""
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'launcher'))
sys.path.insert(0,str(ROOT/'mods-src/BBSC/party'))
import bbport_local_test as local
from engine import validate_invite, Engine
from compat import Compatibility


class LocalPartyTests(unittest.TestCase):
    def test_native_launch_uses_name_and_keeps_party_member_id(self):
        from engine import invite
        from compat import start_from_environment
        with socket.socket() as sock:
            sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
        cfg=invite([dict(id='StableMember',name='twin',host='127.0.0.1',port=port,p2p=3658)])
        path=self.root/'names.json';path.write_text(json.dumps(cfg))
        env=dict(BB_PARTY_CONFIG=str(path),BB_PARTY_MEMBER='StableMember',BBGL_PROFILE_DIR=str(self.root/'named-profile'))
        client=start_from_environment(env,self.root/'install')
        try:
            self.assertEqual(env['BB_SHADNET_NPID'],'twin')
            self.assertEqual(env['BB_PARTY_MEMBER'],'StableMember')
            self.assertEqual(client.e.state['roster'],['StableMember'])
        finally:client.close()

    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.game=self.root/'game';self.game.mkdir();(self.game/'eboot.bin').touch()
        for i in range(1,4):
            p=self.root/f'{local.PROFILE} Player {i}';(p/'user').mkdir(parents=True)
            (p/'settings.json').write_text(json.dumps({'game_dir':str(self.game),'player_name':f'Test{i}'}))

    def tearDown(self):
        self.tmp.cleanup()

    def test_three_real_embedded_clients_and_native_udp_ports(self):
        entries=local.profiles(self.root)
        cfg,path=local.configuration(self.root);validate_invite(cfg)
        local.reserve_ports(cfg)
        clients=[];udp=[]
        try:
            for entry,member in zip(entries,cfg['members']):
                clients.append(Compatibility(Engine(cfg,member['id'],entry['profile']/'state').start()).start())
                sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);sock.settimeout(1)
                sock.bind(('0.0.0.0',member['p2p']));udp.append(sock)
            for i in range(3):
                for j in range(3):
                    if i==j:continue
                    udp[i].sendto(b'local-datagram',('127.0.0.1',cfg['members'][j]['p2p']))
                    data,source=udp[j].recvfrom(1024)
                    self.assertEqual(data,b'local-datagram')
                    self.assertEqual(source,('127.0.0.1',cfg['members'][i]['p2p']))
            with self.assertRaisesRegex(ValueError,'already in use'):
                local.reserve_ports(cfg)
        finally:
            for sock in udp:sock.close()
            for client in clients:client.close()
        self.assertEqual(local.configuration(self.root)[0],cfg)

    def test_environment_uses_existing_profile_and_never_rewrites_settings(self):
        entries=local.profiles(self.root);cfg,path=local.configuration(self.root)
        class Core:
            def app_settings(self,value):return dict(value)
            def game_environment(self,value):return {'BB_PATCHES':'Other','BB_NET_BACKEND':'old'}
        for entry in entries:
            original=(entry['profile']/'settings.json').read_bytes()
            with patch.dict(os.environ,{'BBGL_PROFILE_DIR':str(entry['profile'])}):
                env=local.launch_environment(Core(),entry,path)
            self.assertEqual(env['BB_USER_DIR'],str(entry['user']))
            self.assertEqual(env['BB_PARTY_MEMBER'],f"LocalPlayer{entry['index']}")
            self.assertEqual(env['BB_CONFIG'],str(entry['profile']/'bbport.ini'))
            self.assertEqual(env['BB_FPS'],'60');self.assertEqual(env['BB_FULLSCREEN'],'0')
            self.assertIn('Skip Intro',env['BB_PATCHES']);self.assertNotIn('BB_NET_BACKEND',env)
            self.assertEqual((entry['profile']/'settings.json').read_bytes(),original)
        with patch.dict(os.environ,{'BBGL_PROFILE_DIR':str(self.root/'wrong')}):
            with self.assertRaisesRegex(ValueError,'wrong profile'):
                local.launch_environment(Core(),entries[0],path)

    def test_shared_user_dir_or_missing_profile_is_rejected_before_launch(self):
        p=self.root/f'{local.PROFILE} Player 3/settings.json'
        p.write_text(json.dumps({'game_dir':str(self.game),'user_dir':str(self.root/f'{local.PROFILE} Player 1/user')}))
        with self.assertRaisesRegex(ValueError,'separate saves'):
            local.profiles(self.root)
        p.unlink()
        with self.assertRaisesRegex(ValueError,'existing profile'):
            local.profiles(self.root)

    def test_child_cannot_inherit_another_players_paths(self):
        env=local.child_environment(self.root/'player',{'BB_CONFIG':'wrong','BB_P2P_PORT':'wrong',
                                                      'BBSC_SAVE_DIR':'wrong','BB_USER_DIR':'wrong'})
        self.assertEqual(env['BBGL_PROFILE_DIR'],str(self.root/'player'))
        self.assertNotIn('BB_USER_DIR',env);self.assertNotIn('BB_CONFIG',env)
        self.assertNotIn('BB_P2P_PORT',env);self.assertNotIn('BBSC_SAVE_DIR',env)

    def test_closed_native_games_keep_real_consensus_peers_until_owner_releases(self):
        cfg,_=local.configuration(self.root)
        clients=[];waiters=[]
        run=self.root/'run'
        local.write_json(run/'coordinator.json',{'heartbeat':time.time()})
        class Process:
            def poll(self): return None
        coordinator=threading.Thread(target=local.await_local_games,args=(run,[Process()]*3))
        try:
            for entry,member in zip(local.profiles(self.root),cfg['members']):
                clients.append(Compatibility(Engine(cfg,member['id'],entry['profile']/'state').start()).start())
            clients[2].e.command({'kind':'acquire'},12)
            self.assertFalse(local.local_party_drained(clients[2]))
            coordinator.start()
            def ended(i):
                env={'BB_LOCAL_PARTY_RUN':str(run),'BB_PARTY_MEMBER':cfg['members'][i]['id']}
                t=threading.Thread(target=local.keep_local_party_after_game,args=(clients[i],env,0))
                waiters.append(t);t.start()
            ended(0);ended(1)
            deadline=time.monotonic()+5
            while not (run/'LocalPlayer2-exited.json').exists() and time.monotonic()<deadline: time.sleep(.02)
            self.assertTrue(all(t.is_alive() for t in waiters))
            self.assertFalse((run/'stop-services.json').exists())
            # The last game's genuine release still has both early-exit peers.
            clients[2].e.command({'kind':'release'},12)
            ended(2)
            coordinator.join(8)
            self.assertFalse(coordinator.is_alive())
            self.assertTrue(json.loads((run/'stop-services.json').read_text())['drained'])
            for t in waiters:t.join(3);self.assertFalse(t.is_alive())
            self.assertTrue(all(local.local_party_drained(c) for c in clients))
        finally:
            local.write_json(run/'stop-services.json',{'drained':False})
            for t in waiters:t.join(3)
            if coordinator.ident:coordinator.join(3)
            for c in clients:c.close()

    def test_shutdown_deadline_reports_unresolved_state_without_granting_release(self):
        run=self.root/'timeout-run'
        for i in range(1,4):
            local.write_json(run/f'LocalPlayer{i}-exited.json',{'exit_code':0,'drained':False})
        class Process:
            def poll(self):return None
        # Only the local service barrier expires; no Engine operation or journal write.
        with patch.object(local.time,'monotonic',side_effect=[0,0,31]),patch.object(local.time,'sleep'):
            local.await_local_games(run,[Process()]*3)
        self.assertFalse(json.loads((run/'stop-services.json').read_text())['drained'])


if __name__=='__main__':unittest.main()

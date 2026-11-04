"""Network selection, firewall scope, and retained server endpoint compatibility."""
import base64,json,sys,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'launcher'))
import bbport_coop as coop
import bbport_party as party
class HostConnectionTests(unittest.TestCase):
 def networks(self):
  return [{'value':'radmin','text':'Radmin VPN','vpn':True,'addresses':['26.1.2.3'],'ranges':['26.0.0.0/8']},{'value':'lan','text':'Ethernet','vpn':False,'addresses':['192.168.1.5'],'ranges':['192.168.1.0/24']}]
 def test_auto_prefers_only_vpn_and_requires_choice_if_ambiguous(self):
  networks=self.networks()
  self.assertEqual(party.choose_network(networks),('26.1.2.3',networks[0]))
  networks.append(dict(networks[0],value='other',text='Other VPN'))
  with self.assertRaisesRegex(ValueError,'Several networks'):party.choose_network(networks)
 def test_multiple_addresses_require_local_selection_and_absent_provider_is_rejected(self):
  networks=self.networks();networks[0]['addresses'].append('26.1.2.4')
  with self.assertRaisesRegex(ValueError,'Several networks'):party.choose_network(networks,'radmin')
  self.assertEqual(party.choose_network(networks,'custom','26.1.2.4')[0],'26.1.2.4')
  with self.assertRaisesRegex(ValueError,'not connected'):party.choose_network(networks,'tailscale')
 def test_custom_ipv4_requires_an_active_local_address(self):
  self.assertEqual(party.choose_network(self.networks(),'custom',' 26.1.2.3 ')[0],'26.1.2.3')
  for address in ('','x','127.0.0.1','0.0.0.0','224.0.0.1','169.254.1.1','1.2.3.4;bad','203.0.113.10'):
   with self.subTest(address=address),self.assertRaises(ValueError):party.choose_network(self.networks(),'custom',address)
 def test_discovery_filters_disconnected_bad_addresses_and_groups_ipv4(self):
  rows=[dict(id='vpn',name='Radmin VPN',description='Radmin',address=ip,prefix=8) for ip in ('26.1.2.3','26.1.2.4','127.0.0.1','169.254.1.1')]
  with patch.object(coop.subprocess,'run',return_value=SimpleNamespace(returncode=0,stdout=json.dumps(rows))) as run:
   result=coop.network_candidates()
  self.assertIn("Status -eq 'Up'",run.call_args.args[0][-1])
  self.assertEqual(result[0]['addresses'],['26.1.2.3','26.1.2.4']);self.assertEqual(result[0]['ranges'],['26.0.0.0/8'])
 def test_firewall_scope_is_explicit_and_validated(self):
  self.assertIn("@('26.0.0.0/8','LocalSubnet')",coop._firewall_script('game.exe',('26.0.0.0/8','LocalSubnet')))
  self.assertIn("@('Any')",coop._firewall_script('game.exe',('Any',)))
  with self.assertRaises(ValueError):coop._firewall_script('game.exe',("bad';command",))
 def test_server_local_summon_address_does_not_leak_to_guests(self):
  server=Path(__file__).resolve().parents[1]/'mods-src/BBSC/server/gameserver';sys.path.insert(0,str(server))
  import bbsc_gameserver as gs
  args=SimpleNamespace(shadnet='203.0.113.10',local_shadnet='127.0.0.1',advertise='203.0.113.10',host='0.0.0.0',port=20443,summon_interval=None,level_range=None,no_playlog=True)
  with patch.object(gs,'ARGS',args):
   remote=base64.b64decode(gs.build_ss_info(quiet=True)).decode();local=base64.b64decode(gs.build_ss_info(local=True,quiet=True)).decode()
  self.assertIn('http://203.0.113.10:31315',remote);self.assertNotIn('http://127.0.0.1:31315',remote)
  self.assertIn('http://127.0.0.1:31315',local)
if __name__=='__main__':unittest.main()

"""Source/protobuf compatibility checks; deliberately does not build the server."""
import io
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CLIENT = ROOT / 'gpu/bbnet/vendor/shadps4/shadnet'


class LookupProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.server = Path(cls.temp.name)
        # Exactly the revision used by the packaging script, then every package patch.
        script = (ROOT / 'packaging/windows/build_coop_server.sh').read_text()
        revision = re.search(r'^COMMIT=(\w+)$', script, re.M)[1]
        archive = subprocess.check_output([
            'git', '-C', str(ROOT / 'out/shadnet-p2p'), 'archive', '--format=zip', revision])
        with zipfile.ZipFile(io.BytesIO(archive)) as source:
            source.extractall(cls.server)
        for patch in sorted((ROOT / 'packaging/windows/shadnet-p2p').glob('*.patch')):
            subprocess.run(['git', 'apply', '--whitespace=nowarn', str(patch)],
                           cwd=cls.server, check=True, capture_output=True)
        cls.handler = (cls.server / 'src/cmd_account.cpp').read_text().split(
            'ErrorType ClientSession::CmdLookupOnlineId', 1)[1]

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_dispatch_and_authentication(self):
        dispatch = (self.server / 'src/client_session.cpp').read_text()
        self.assertIn('LookupOnlineId = 41', (CLIENT / 'client.h').read_text())
        self.assertIn('LookupOnlineId = 41', (self.server / 'src/protocol.h').read_text())
        self.assertIn('case CommandType::LookupOnlineId:\n        return CmdLookupOnlineId(se, reply);', dispatch)
        pre_auth = dispatch.split('if (!m_authenticated)', 1)[1].split('// Attribute', 1)[0]
        self.assertNotIn('LookupOnlineId', pre_auth)
        self.assertIn('return ErrorType::Unauthorized;', pre_auth)

    def test_request_reply_wire_compatibility(self):
        protoc = shutil.which('protoc') or 'C:/msys64/clang64/bin/protoc.exe'
        def convert(schema, mode, message, data):
            return subprocess.check_output([protoc, '-I', str(schema.parent),
                                           f'--{mode}=shadnet.{message}', schema.name], input=data).replace(b'\r\n', b'\n')
        client = CLIENT / 'shadnet.proto'
        server = self.server / 'src/shadnet.proto'
        # Both directions, including case, maximum-length IDs and 64-bit account IDs.
        for name in ['Twin', 'guest_2', 'Abcdefghijklmn16']:
            request = f'npid: "{name}"\n'.encode()
            encoded = convert(client, 'encode', 'LookupOnlineIdRequest', request)
            self.assertEqual(convert(server, 'decode', 'LookupOnlineIdRequest', encoded), request)
            reply = f'account_id: 9007199254740993\nnpid: "{name}"\n'.encode()
            encoded = convert(server, 'encode', 'LookupOnlineIdReply', reply)
            self.assertEqual(convert(client, 'decode', 'LookupOnlineIdReply', encoded), reply)
        self.assertIn('decodeProto(req, data)', self.handler)
        self.assertIn('appendProto(reply, rep)', self.handler)
        self.assertIn('MakeProtoPayload(req)', (CLIENT / 'client.cpp').read_text().split(
            'ShadNetClient::LookupOnlineId', 1)[1].split('\n}', 1)[0])

    def test_lookup_query_preserves_identity_without_presence(self):
        sql = re.search(r'query.prepare\("([^"]+)"\)', self.handler)[1]
        with sqlite3.connect(':memory:') as db:
            db.execute('CREATE TABLE account (user_id INTEGER, username TEXT)')
            db.execute('INSERT INTO account VALUES (?, ?)', (9007199254740993, 'Twin'))
            self.assertEqual(db.execute(sql, ('tWiN',)).fetchone(), (9007199254740993, 'Twin'))
            self.assertIsNone(db.execute(sql, ('missing',)).fetchone())
            self.assertIsNone(db.execute(sql, ("' OR 1=1 --",)).fetchone())
        self.assertIn('query.addBindValue(npid)', self.handler)
        self.assertIn('rep.set_account_id(query.value(0).toULongLong())', self.handler)
        self.assertIn('rep.set_npid(query.value(1).toString().toStdString())', self.handler)

    def test_error_paths(self):
        for guard, result in [('!decodeProto(req, data) || data.error()', 'Malformed'),
                              ('!IsValidNpid(npid)', 'InvalidInput'),
                              ('!query.exec()', 'DbFail'), ('!query.next()', 'NotFound')]:
            self.assertRegex(self.handler, re.escape(guard) + r'\)\s*\{?[^{}]*?return ErrorType::' + result)
        self.assertLess(self.handler.index('!IsValidNpid'), self.handler.index('QSqlQuery'))
        self.assertLess(self.handler.index('!query.exec()'), self.handler.index('!query.next()'))


if __name__ == '__main__':
    unittest.main()

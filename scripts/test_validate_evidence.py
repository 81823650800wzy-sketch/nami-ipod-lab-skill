#!/usr/bin/env python3
"""Synthetic corruption/compatibility tests; no real device artifacts required."""
import copy
import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from validate_evidence import validate
from doctor import inspect


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.blob = self.root / 'app.hbapp'
        self.raw = struct.pack('<6I', 0x314c5248, 4, 8, 12, 1, 16) + struct.pack('<2I', 8, 0) + struct.pack('<I', 0)
        self.blob.write_bytes(self.raw)
        sha = hashlib.sha256(self.raw).hexdigest()
        self.data = {'deviceAccess': False, 'nanoAppsCommit': 'a'*40,
                     'sources': {'app.c': 'b'*64}, 'hbappConsecutiveBuildsEqual': True,
                     'blobAudit': {'sha256': sha, 'bytes': 36, 'entryOffset': 4,
                                   'imageBytes': 8, 'spanBytes': 12, 'bssBytes': 4,
                                   'arenaAllocationBytes': 28, 'relocations': 1},
                     'outputs': {'nami.hbapp': {'sha256': sha, 'bytes': 36}}}

    def run_manifest(self, data=None, blob=None):
        path = self.root / 'manifest.json'
        path.write_text(json.dumps(self.data if data is None else data), encoding='utf-8')
        return validate(path, blob)

    def package(self):
        return {'AllApps.pack': 'c'*64, 'Icons/NAMI.bin': 'd'*64,
                'Executables/NAMI.hbapp': self.data['blobAudit']['sha256']}

    def test_legacy_artifact(self):
        self.assertTrue(self.run_manifest(blob=self.blob)['artifactVerified'])

    def test_arcade_staging_is_reported(self):
        del self.data['outputs']
        self.data.update(package=self.package(), packageTreesEqual=True, managedHostAppStaged=True)
        self.assertTrue(self.run_manifest()['managedHostAppStaged'])

    def test_nested_player_package(self):
        self.data['package'] = {'package': self.package(), 'packageTreesEqual': True, 'deviceAccess': False}
        self.assertEqual(self.run_manifest()['profiles'], ['outputs', 'package'])

    def test_invalid_claims_and_types(self):
        mutations = [('deviceAccess', True), ('deviceAccess', 0),
                     ('hardwareGatesAdvanced', ['G1']), ('hbappConsecutiveBuildsEqual', 1),
                     ('sources', []), ('sources', {}), ('nanoAppsCommit', 'latest'),
                     ('managedHostAppStaged', 'false'), ('blobAudit', [])]
        for key, value in mutations:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                data = copy.deepcopy(self.data)
                data[key] = value
                self.run_manifest(data)

    def test_invalid_audit_and_output(self):
        for key, value in [('sha256', 'z'*64), ('bytes', True), ('bytes', -1),
                           ('entryOffset', 3), ('spanBytes', 13), ('arenaAllocationBytes', 999)]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                data = copy.deepcopy(self.data)
                data['blobAudit'][key] = value
                self.run_manifest(data)
        self.data['outputs']['nami.hbapp']['sha256'] = 'e'*64
        with self.assertRaises(ValueError):
            self.run_manifest()

    def test_package_hash_and_equality(self):
        self.data.update(package=self.package(), packageTreesEqual=False)
        with self.assertRaises(ValueError):
            self.run_manifest()
        self.data['packageTreesEqual'] = True
        self.data['package']['Executables/NAMI.hbapp'] = 'e'*64
        with self.assertRaises(ValueError):
            self.run_manifest()

    def test_corrupt_blob_hash(self):
        self.blob.write_bytes(self.raw[:-1])
        with self.assertRaises(ValueError):
            self.run_manifest(blob=self.blob)

    def test_forged_hash_cannot_hide_bad_relocation(self):
        raw = self.raw[:-4] + struct.pack('<I', 7)
        self.blob.write_bytes(raw)
        sha = hashlib.sha256(raw).hexdigest()
        self.data['blobAudit']['sha256'] = self.data['outputs']['nami.hbapp']['sha256'] = sha
        with self.assertRaisesRegex(ValueError, 'relocation offset'):
            self.run_manifest(blob=self.blob)

    def test_duplicate_keys(self):
        path = self.root / 'duplicate.json'
        path.write_text('{"deviceAccess":true,"deviceAccess":false}')
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            validate(path)

    def test_cli_malformed_json_fails_without_traceback(self):
        path = self.root / 'bad.json'
        path.write_text('[]')
        result = subprocess.run([sys.executable, str(Path(__file__).with_name('validate_evidence.py')), str(path)], capture_output=True, text=True, cwd=self.root)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stdout)['result'], 'FAILED')
        self.assertEqual(result.stderr, '')

    def test_doctor_missing_bundle(self):
        self.assertEqual(inspect(self.root)['result'], 'FAILED')


if __name__ == '__main__':
    unittest.main()

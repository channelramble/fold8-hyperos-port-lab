from pathlib import Path
import importlib.util
import hashlib
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('verify', ROOT / 'tools/verify_repository.py')
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


class RepositoryTests(unittest.TestCase):
    def test_source_pins_and_overlay_paths(self):
        inputs = json.loads((ROOT / 'inputs/manifest.json').read_text())
        for source in inputs['upstream'].values():
            self.assertRegex(source['commit'], r'^[0-9a-f]{40}$')
        mapping = json.loads((ROOT / 'integration/hyperos-overlays.json').read_text())
        self.assertFalse(mapping['launch_authorized'])
        self.assertEqual(len(mapping['files']), 6)
        for item in mapping['files']:
            self.assertTrue(item['guest_target'].startswith(('/system/', '/apex/')))
            self.assertNotIn('..', Path(item['guest_target']).parts)

    def test_tampered_inventory_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'a.txt').write_text('changed')
            digest = hashlib.sha256(b'original').hexdigest()
            (root / 'SHA256SUMS').write_text(digest + '  a.txt\n')
            with self.assertRaisesRegex(ValueError, 'Content differs'):
                verify.verify(root)

    def test_runtime_claim_cannot_hide_missing_boot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            p = root / 'status.json'
            p.write_text(json.dumps({'install_ready': True, 'hyperos_boot_verified': False,
                                    'return_to_oneui_verified_for_hyperos': False}))
            (root / 'SHA256SUMS').write_text(hashlib.sha256(p.read_bytes()).hexdigest() + '  status.json\n')
            with self.assertRaisesRegex(ValueError, 'Install-ready'):
                verify.verify(root)


if __name__ == '__main__':
    unittest.main()

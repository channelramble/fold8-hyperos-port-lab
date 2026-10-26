import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest


def load(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


native = load('hyperos-native-candidate')
methods = load('apply-port-method-guards')


class CandidateTests(unittest.TestCase):
    def test_native_preserves_all_unpatched_bytes(self):
        data = b'abc\0vold\0tail'
        out = native.patch(data, hashlib.sha256(data).hexdigest(), [(3, b'\0vold\0', b'\0gvld\0')])
        self.assertEqual(out, b'abc\0gvld\0tail')
        with self.assertRaises(ValueError):
            native.patch(data + b'?', hashlib.sha256(data).hexdigest(), [])
        with self.assertRaises(ValueError):
            native.patch(data, hashlib.sha256(data).hexdigest(), [(0, b'WRONG', b'STUFF')])

    def test_invalid_second_method_leaves_all_files_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            old = '.method public f()V\n    .locals 0\n    return-void\n.end method'
            (root / 'a.smali').write_text(old)
            (root / 'b.smali').write_text(old)
            rules = [dict(file=f, header='.method public f()V', before_sha256=sha,
                          replacement=old.replace('.locals 0', '.locals 1'))
                     for f, sha in [('a.smali', hashlib.sha256(old.encode()).hexdigest()), ('b.smali', 'bad')]]
            with self.assertRaises(ValueError):
                methods.prepare(root, {'methods': rules})
            self.assertEqual((root / 'a.smali').read_text(), old)
            self.assertEqual((root / 'b.smali').read_text(), old)
            rules[1]['before_sha256'] = rules[0]['before_sha256']
            prepared = methods.prepare(root, {'methods': rules})
            self.assertEqual(len(prepared), 2)
            self.assertIn('.locals 1', prepared[root / 'a.smali'])

    def test_method_path_escape_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                methods.prepare(Path(tmp), {'methods': [{'file': '../outside'}]})


if __name__ == '__main__':
    unittest.main()

"""The DEX verifier must not report success when its parser/tool did no work."""
from pathlib import Path
import os
import subprocess
import tempfile
import unittest
import zipfile


class DexChecks(unittest.TestCase):
    def run_check(self, dump, exit_code=0, empty=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tool = root / 'build-tools/37/dexdump'
            tool.parent.mkdir(parents=True)
            tool.write_text('#!/usr/bin/env python3\nimport sys\nprint(' + repr(dump) + ')\nsys.exit(' + str(exit_code) + ')\n')
            tool.chmod(0o755)
            jar = root / 'test.jar'
            with zipfile.ZipFile(jar, 'w') as z:
                z.writestr('note.txt' if empty else 'classes.dex', b'fixture')
            return subprocess.run(['python3', str(Path(__file__).with_name('check-dex.py')), str(jar)],
                                  env=dict(os.environ, ANDROID_HOME=str(root)), capture_output=True, text=True)

    def test_failed_tool_cannot_pass(self):
        self.assertNotEqual(self.run_check('Class descriptor', 1).returncode, 0)

    def test_empty_parser_output_cannot_pass(self):
        self.assertNotEqual(self.run_check('').returncode, 0)
        self.assertNotEqual(self.run_check('Class descriptor', empty=True).returncode, 0)

    def test_long_addresses_checked(self):
        r = self.run_check("Class descriptor : 'LExample;'\n|[0000] Example.f:()V\n|10000: nop\n|10001: move-result v0")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('move-result', r.stdout)

    def test_valid_result_sequence(self):
        r = self.run_check("Class descriptor : 'LExample;'\n|[0000] Example.f:()V\n|0000: invoke-static\n|0003: move-result v0\n|0004: return-void")
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == '__main__':
    unittest.main()

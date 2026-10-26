"""Regression: unsupported storage binaries must stop before framework patching."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class PortBuildGuard(unittest.TestCase):
    def test_unknown_vold_stops_before_framework_and_guards(self):
        builder = Path(__file__).with_name("make-overlays.sh").resolve()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sdk = root / "sdk"
            (sdk / "build-tools/36.0.0").mkdir(parents=True)
            (sdk / "platforms/android-37.0").mkdir(parents=True)
            (sdk / "platforms/android-37.0/android.jar").touch()
            image = root / "unknown.img"
            image.write_bytes(b"unrecognized guest")
            log = root / "debugfs.log"
            debugfs = root / "debugfs"
            debugfs.write_text('#!/bin/sh\nprintf "%s\\n" "$*" >> "$PORT_TEST_LOG"\nexit 0\n')
            debugfs.chmod(0o755)
            output = root / "overlays"
            env = dict(os.environ, ANDROID_HOME=str(sdk), DEBUGFS=str(debugfs),
                       APKTOOL=str(root / "unused.jar"), PORT_TEST_LOG=str(log))
            result = subprocess.run(["sh", str(builder), str(image), str(output)],
                                    env=env, capture_output=True, text=True, timeout=30)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Port blocked", result.stderr)
            self.assertNotIn("/system/framework/services.jar", log.read_text())
            self.assertFalse((output / "guards.txt").exists())
            self.assertFalse((output / "vold_patched").exists())


if __name__ == "__main__":
    unittest.main()

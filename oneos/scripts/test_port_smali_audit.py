import importlib.util
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('audit', Path(__file__).with_name('audit-port-smali.py'))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AuditTests(unittest.TestCase):
    def test_oem_jar_is_scanned_and_comments_are_ignored(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            p = root / 'miui-services/smali/com/miui/Storage.smali'
            p.parent.mkdir(parents=True)
            p.write_text(''' .class public Lcom/miui/Storage;
.method public wipe()V
    invoke-interface/range {v0 .. v3}, Landroid/os/IInstalld;->destroyUserData(Ljava/lang/String;II)V
    # invoke-interface {v0}, Landroid/os/IVold;->format()V
    const-string v0, "Landroid/os/IVold;->format()V"
    invoke-interface {v0}, Landroid/os/IVold;->getUnlockedUsers()[I
.end method
''')
            report = audit.scan(root)
            self.assertEqual(report['files_scanned'], 1)
            self.assertEqual(len(report['review_required']), 1)
            self.assertEqual(report['review_required'][0]['method'], '.method public wipe()V')
            self.assertEqual(report['review_required'][0]['line'], 3)

    def test_lock_and_wipe_paths(self):
        self.assertTrue(audit.sensitive('Landroid/hardware/weaver/V1_0/IWeaver;', 'write'))
        self.assertTrue(audit.sensitive('Landroid/os/RecoverySystem;', 'rebootWipeUserData'))
        self.assertFalse(audit.sensitive('Landroid/service/gatekeeper/IGateKeeperService;', 'verifyChallenge'))
        self.assertTrue(audit.sensitive('Landroid/os/IVold;', 'abortChanges'))
        self.assertTrue(audit.sensitive('Lvendor/xiaomi/hardware/oldcredential/IOldCredentialService;', 'setFile'))

    def test_control_property_sites_are_not_silent(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'TradeIn.smali'
            p.write_text('.method public reboot()V\n    const-string v0, "sys.powerctl"\n.end method\n')
            report = audit.scan(Path(d))
            self.assertEqual(report['control_strings_review_required'][0]['string'], 'sys.powerctl')

    def test_empty_input_does_not_claim_reviewed(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(audit.scan(Path(d))['files_scanned'], 0)


if __name__ == '__main__':
    unittest.main()

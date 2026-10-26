#!/usr/bin/env python3
"""Inventory sensitive calls in ALL decoded guest jars, including OEM jars.

Read-only review aid: absence of findings is not a proof of guest isolation.
Native code, reflection and raw Binder transactions need separate review.
Exit 1 means call sites require review; exit 2 means no smali was inspected.
"""
import argparse
import json
from pathlib import Path
import re

CALL = re.compile(r'^\s*invoke-[\w/-]+\s+\{[^}]*\},\s+(L[^;]+;)->([^\s(]+)\(')
METHODS = {
    'Landroid/os/IVold;': {'destroyUserStorage', 'prepareUserStorage', 'format',
        'partition', 'forgetPartition', 'moveStorage', 'onUserRemoved',
        'startCheckpoint', 'abortChanges', 'shutdown', 'sdlockErase'},
    'Landroid/os/IInstalld;': {'destroyUserData', 'destroyAppData', 'clearAppData',
        'clearAppDataWithPreservedCacheEntries', 'destroyAppDataSnapshot',
        'destroyCeSnapshotsNotSpecified', 'destroyPccData', 'rmPackageDir',
        'cleanupInvalidPackageDirs', 'moveCompleteApp', 'moveAppDataPath',
        'copyAppDataPath', 'migrateAppData', 'restoreAppDataSnapshot',
        'onPrivateVolumeRemoved', 'freeCache', 'reconcileSdkData'},
    'Landroid/security/AndroidKeyStoreMaintenance;': {'clearNamespace',
        'onUserRemoved', 'onUserLskfRemoved', 'onUserAdded',
        'migrateKeyNamespace', 'initUserSuperKeys', 'deleteAllKeys'},
    'Landroid/service/gatekeeper/IGateKeeperService;': {'enroll',
        'clearSecureUserId', 'reportDeviceSetupComplete'},
    'Landroid/hardware/weaver/IWeaver;': {'write'},
    'Lvendor/xiaomi/hardware/oldcredential/IOldCredentialService;':
        {'deleteOldCredential', 'setFile', 'resetOldCredentialTimer'},
}
CONTROL = re.compile(r'^\s*const-string(?:/jumbo)? [vp]\d+, "(sys\.powerctl|ctl\.start|setup-bcb|clear-bcb)"')


def sensitive(owner, method):
    if method in METHODS.get(owner, set()):
        return True
    if owner.startswith('Landroid/hardware/weaver/') and method == 'write':
        return True
    if owner == 'Landroid/os/RecoverySystem;' and ('Wipe' in method or 'wipe' in method):
        return True
    return False


def scan(root):
    findings, controls, count = [], [], 0
    for path in sorted(root.rglob('*.smali')):
        if path.is_symlink():
            raise ValueError(f'Refusing symlink: {path}')
        count += 1
        current_method = None
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if line.startswith('.method '):
                current_method = line
            elif line.startswith('.end method'):
                current_method = None
            match = CALL.match(line)
            if match and sensitive(*match.groups()):
                findings.append({'file': str(path.relative_to(root)), 'line': number,
                    'method': current_method, 'target': '->'.join(match.groups()),
                    'instruction': line.strip()})
            control = CONTROL.match(line)
            if control:
                controls.append({'file': str(path.relative_to(root)), 'line': number,
                    'method': current_method, 'string': control.group(1)})
    return {'files_scanned': count, 'review_required': findings,
            'control_strings_review_required': controls,
            'scope': 'Direct invokes and control-string sites; reachability, native code and reflection are not proven. Not a launch authorization.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('decoded', type=Path)
    args = parser.parse_args()
    report = scan(args.decoded)
    print(json.dumps(report, indent=2))
    raise SystemExit(2 if not report['files_scanned'] else bool(report['review_required'] or report['control_strings_review_required']))

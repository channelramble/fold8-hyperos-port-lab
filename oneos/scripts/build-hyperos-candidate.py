#!/usr/bin/env python3
"""Reproduce offline HyperOS framework candidates. No staging or device access.

Requires extracted inputs from inspect-port-image.py, service-crashrecovery.jar
extracted from the pinned CAPEX payload, apktool 3.0.3, and Android dexdump.
Outputs are NOT a flashable ROM or a launch-approved OneOS package.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

INPUTS = {
    'services': ('system/framework/services.jar', 'c7e5901633e6dc7e21eb2b0058494e0fe584d7d0942ea00daeda299281e9ae38'),
    'miui-services': ('system/system_ext/framework/miui-services.jar', '835056db4962a274c3567b1a329b166b47ed6ab5fd1c408b04e7b1cb5332e8b9'),
    'tradeinmode': ('system/framework/tradeinmode.jar', '6ebb258ed22de9ad27f57470b351f85470bd0ae45d17369679c8119b7db023b2'),
}
COMMON = ['guest_no_vold_keys', 'skip_host_apex_services', 'guest_power_guards',
          'guest_storage_guards', 'guest_installd_abi', 'guest_no_sysrq_crash',
          'guest_no_weaver', 'guest_no_biometric_cleanup', 'guest_no_gatekeeper',
          'guest_pdb_readonly', 'guest_no_apex_installs', 'guest_app_id_offset']
CRASH_JAR_SHA256 = '4533611de83fa462db64b2bacab2c0e497535f4acd96c0ba4444db0e44b1f193'


def sha(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--extracted', required=True, type=Path)
    p.add_argument('--crash-jar', required=True, type=Path)
    p.add_argument('--host-installd', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    a = p.parse_args()
    if a.output.exists():
        p.error('Use a new output directory')
    if not os.environ.get('ANDROID_HOME'):
        p.error('ANDROID_HOME is required for DEX checks')
    repo = Path(__file__).resolve().parents[1]
    patches = repo / 'switcher/patches'
    scripts = repo / 'scripts'
    for _, (rel, digest) in INPUTS.items():
        if sha(a.extracted / rel) != digest:
            p.error('Unsupported input: ' + rel)
    if sha(a.crash_jar) != CRASH_JAR_SHA256:
        p.error('Crash recovery input differs from the reviewed digest')
    def table(path):
        return [l for l in path.read_text().splitlines() if l and not l.startswith('#')]
    if table(a.host_installd) != table(patches / 'host_installd.txt'):
        p.error('Host installd layout differs; audit before building')
    a.output.mkdir(parents=True)
    decoded = a.output / 'decoded'
    products = a.output / 'candidate'
    products.mkdir()
    log = (a.output / 'build.log').open('w')
    def run(*args):
        args = [str(v) for v in args]
        log.write(json.dumps(args) + '\n'); log.flush()
        subprocess.run(args, check=True, stdout=log, stderr=subprocess.STDOUT)
    def patch(name, *args):
        run(sys.executable, '-I', patches / (name + '.py'), decoded / 'services', *args)
    for name, (rel, _) in INPUTS.items():
        run('apktool', 'd', '-f', '-r', a.extracted / rel, '-o', decoded / name)
    run('apktool', 'd', '-f', '-r', a.crash_jar, '-o', decoded / 'crashrecovery')
    for name in COMMON:
        patch(name, *([a.host_installd] if name == 'guest_installd_abi' else []))
    run(sys.executable, scripts / 'apply-port-method-guards.py', decoded,
        patches / 'hyperos-17-method-guards.json')
    for name in ['guest_no_new_users', 'guest_own_idmap', 'guest_own_vold']:
        patch(name)
    display = list((decoded / 'services').glob('smali*/com/android/server/display/LocalDisplayAdapter.smali'))
    if len(display) != 1:
        raise ValueError('Ambiguous display adapter')
    run(sys.executable, '-I', patches / 'display_mode_specs.py', display[0])
    jars = []
    for name, dest in [('services', 'services_patched.jar'),
                       ('miui-services', 'miui-services_patched.jar'),
                       ('tradeinmode', 'tradeinmode_patched.jar'),
                       ('crashrecovery', 'service-crashrecovery_patched.jar')]:
        out = products / dest
        run('apktool', 'b', decoded / name, '-o', out)
        jars.append(out)
    run(sys.executable, scripts / 'hyperos-native-candidate.py', a.extracted, products)
    run(sys.executable, scripts / 'check-dex.py', *jars)
    with (a.output / 'remaining-direct-calls.json').open('w') as f:
        result = subprocess.run([sys.executable, str(scripts / 'audit-port-smali.py'), str(decoded)], stdout=f)
        if result.returncode not in (0, 1):
            raise RuntimeError('Review scanner failed')
    report = {'launch_ready': False, 'flashable': False, 'device_modified': False,
              'stage': 'offline structural validation only',
              'inputs': {rel: digest for rel, digest in INPUTS.values()},
              'crash_jar_sha256': sha(a.crash_jar),
              'host_table_sha256': sha(a.host_installd),
              'files': {f.name: sha(f) for f in products.iterdir() if f.is_file()},
              'remaining': ['HyperOS runtime/mount and OneOS packaging integration',
                            'Full native, reflection, Binder and OEM service reachability review',
                            'Privileged IMS signing/integration and carrier provisioning',
                            'Device boot, return-to-One-UI and call tests']}
    (a.output / 'candidate-status.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'structural_build': 'passed', 'launch_ready': False}))


if __name__ == '__main__':
    main()

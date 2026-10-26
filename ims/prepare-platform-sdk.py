#!/usr/bin/env python3
"""Create a local SDK view for compiling privileged Android platform code.

The installed SDK is never modified. Remove duplicate public class stubs from
the local android.jar so the compile-only full platform jar supplies those APIs.
This changes the compiler's inputs only, not the guest's runtime permissions.
"""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--sdk', type=Path, required=True)
p.add_argument('--platform-jar', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--platform', default='android-37.0')
a = p.parse_args()
sdk, framework, out = a.sdk.resolve(), a.platform_jar.resolve(), a.output.resolve()
if out.exists():
    p.error('Output must not already exist')
if not (sdk / 'platforms' / a.platform / 'android.jar').is_file():
    p.error('Requested SDK platform is absent')
with zipfile.ZipFile(framework) as z:
    full_classes = {n for n in z.namelist() if n.endswith('.class')}
if 'android/telephony/ims/feature/MmTelFeature.class' not in full_classes:
    p.error('Platform jar does not contain IMS system APIs')
out.mkdir(parents=True)
for item in sdk.iterdir():
    if item.name != 'platforms':
        (out / item.name).symlink_to(item, target_is_directory=item.is_dir())
(out / 'platforms').mkdir()
for item in (sdk / 'platforms').iterdir():
    target = out / 'platforms' / item.name
    if item.name != a.platform:
        target.symlink_to(item, target_is_directory=item.is_dir())
        continue
    target.mkdir()
    for entry in item.iterdir():
        if entry.name != 'android.jar':
            (target / entry.name).symlink_to(entry, target_is_directory=entry.is_dir())
    removed = 0
    with zipfile.ZipFile(item / 'android.jar') as original, zipfile.ZipFile(
            target / 'android.jar', 'x', compression=zipfile.ZIP_DEFLATED) as patched:
        for info in original.infolist():
            # AGP's PlatformAttrTransform requires android.R$attr in the SDK.
            # Keep SDK resource/permission constants; they expose no IMS API.
            constants = (info.filename in ('android/R.class', 'android/Manifest.class')
                         or info.filename.startswith(('android/R$', 'android/Manifest$')))
            if info.filename in full_classes and not constants:
                removed += 1
            else:
                patched.writestr(info, original.read(info))
with framework.open('rb') as f:
    digest = hashlib.file_digest(f, 'sha256').hexdigest()
report = {'source_sdk': str(sdk), 'platform_jar': str(framework),
          'platform_jar_sha256': digest, 'duplicate_stubs_removed': removed,
          'runtime_modified': False}
(out / 'port-sdk-provenance.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

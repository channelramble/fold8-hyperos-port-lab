#!/usr/bin/env python3
"""Read-only ext4 guest inventory and extraction for a new OneOS port.

Does not mount, patch, execute, or deploy anything from the guest image.
The destination must be new. debugfs is never invoked with its write flag.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('image', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--debugfs', required=True)
    args = parser.parse_args()
    image = args.image.resolve()
    with image.open('rb') as f:
        f.seek(1080)
        if f.read(2) != bytes.fromhex('53ef'):
            parser.error('Expected an unpacked ext4 image, not sparse/EROFS/compressed input')
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    if any(c in str(out) for c in '\n\r"\\'):
        parser.error('Output path contains unsupported debugfs quoting characters')
    report = {'image': str(image), 'bytes': image.stat().st_size,
              'artifacts': [], 'directories': {}, 'launch_ready': False}

    def run(command):
        p = subprocess.run([args.debugfs, '-R', command, str(image)],
                           capture_output=True, text=True, timeout=90)
        return p.stdout

    def dump(source):
        dest = out / source.lstrip('/')
        dest.parent.mkdir(parents=True, exist_ok=True)
        run(f'dump {source} "{dest}"')
        if not dest.is_file() or dest.stat().st_size == 0:
            return
        with dest.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        report['artifacts'].append({'source': source, 'file': str(dest.relative_to(out)),
                                    'bytes': dest.stat().st_size, 'sha256': digest})

    for source in ['/system/build.prop', '/build.prop',
                   '/system/system_ext/build.prop', '/system/product/build.prop',
                   '/system/system_ext/etc/build.prop', '/system/product/etc/build.prop',
                   '/system/bin/vold', '/system/bin/surfaceflinger',
                   '/system/lib64/service.incremental.so',
                   '/system/framework/framework-res.apk']:
        dump(source)
    for directory in ['/system/framework', '/system/system_ext/framework',
                      '/system/product/framework', '/system/apex',
                      '/system/system_ext/apex', '/system/product/apex']:
        listing = run(f'ls -p {directory}')
        names = []
        for line in listing.splitlines():
            fields = line.split('/')
            if len(fields) > 5 and re.fullmatch(r'[A-Za-z0-9_.+-]+', fields[5]):
                name = fields[5]
                if name not in ('.', '..'):
                    names.append(name)
        report['directories'][directory] = names
        for name in names:
            if name.endswith('.jar') or ('crashrecovery' in name and name.endswith(('.apex', '.capex'))):
                dump(directory + '/' + name)
    if not any(a['source'] == '/system/framework/services.jar' for a in report['artifacts']):
        report['blocker'] = 'No /system/framework/services.jar; layout requires manual inspection'
    (out / 'inventory.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'artifacts': len(report['artifacts']), 'report': str(out / 'inventory.json'),
                      'launch_ready': False}, indent=2))


if __name__ == '__main__':
    main()

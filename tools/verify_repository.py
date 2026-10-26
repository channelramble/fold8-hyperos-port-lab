#!/usr/bin/env python3
"""Check the committed inventory and ensure status does not overclaim results."""
from pathlib import Path
import hashlib
import json
import re


def verify(root):
    rows = (root / 'SHA256SUMS').read_text().splitlines()
    if not rows:
        raise ValueError('Empty repository inventory')
    seen = set()
    for row in rows:
        digest, name = row.split('  ', 1)
        rel = Path(name)
        if not re.fullmatch('[0-9a-f]{64}', digest) or rel.is_absolute() or '..' in rel.parts or name in seen:
            raise ValueError('Invalid inventory entry')
        seen.add(name)
        path = root / rel
        if path.is_symlink() or not path.is_file():
            raise ValueError('Missing or linked file: ' + name)
        path.resolve().relative_to(root.resolve())
        if hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError('Content differs: ' + name)
    status = json.loads((root / 'status.json').read_text())
    if status['install_ready'] and not all(status[x] for x in ['hyperos_boot_verified', 'return_to_oneui_verified_for_hyperos']):
        raise ValueError('Install-ready claim without required runtime results')
    if status['volte_verified'] and not status['hyperos_boot_verified']:
        raise ValueError('VoLTE claim without a verified guest boot')
    for path in root.rglob('*'):
        if any(x in path.relative_to(root).parts for x in ['.git', 'build', '__pycache__']):
            continue
        if path.is_file() and path.name != 'SHA256SUMS' and str(path.relative_to(root)) not in seen:
            raise ValueError('File omitted from inventory: ' + str(path.relative_to(root)))
        if path.is_file() and path.suffix in ['.img', '.apk', '.jks', '.keystore', '.pk8', '.key']:
            raise ValueError('Unexpected binary/key in repository')
    return len(seen)


if __name__ == '__main__':
    print('Verified', verify(Path(__file__).resolve().parents[1]), 'repository files; runtime status remains explicit.')

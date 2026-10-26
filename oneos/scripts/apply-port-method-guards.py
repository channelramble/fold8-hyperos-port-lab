#!/usr/bin/env python3
"""Apply reviewed, hash-pinned method replacements to a decoded candidate only.

This does not approve an image for launch. Every method is checked before any
file is written; an unknown or already-patched method causes a closed failure.
The original image and framework jars are never opened for writing.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re


def prepare(root, spec):
    pending = {}
    seen = set()
    for rule in spec['methods']:
        rel = Path(rule['file'])
        path = root / rel
        if rel.is_absolute() or '..' in rel.parts or path.is_symlink():
            raise ValueError('unsafe target path')
        path.resolve().relative_to(root.resolve())
        ident = (str(rel), rule['header'])
        if ident in seen:
            raise ValueError('duplicate method rule')
        seen.add(ident)
        text = pending.get(path, path.read_text())
        pattern = re.compile('^' + re.escape(rule['header']) + r'\n.*?^\.end method$', re.M | re.S)
        hits = list(pattern.finditer(text))
        if len(hits) != 1:
            raise ValueError(f'{rel}: expected exactly one {rule["header"]}')
        hit = hits[0]
        if hashlib.sha256(hit.group().encode()).hexdigest() != rule['before_sha256']:
            raise ValueError(f'{rel}: method differs from reviewed input')
        replacement = rule['replacement']
        if not replacement.startswith(rule['header'] + '\n') or not replacement.endswith('\n.end method'):
            raise ValueError('replacement changes method signature or boundary')
        pending[path] = text[:hit.start()] + replacement + text[hit.end():]
    return pending


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('decoded', type=Path)
    p.add_argument('spec', type=Path)
    p.add_argument('--check-only', action='store_true')
    a = p.parse_args()
    spec = json.loads(a.spec.read_text())
    pending = prepare(a.decoded, spec)
    if not a.check_only:
        for path, text in pending.items():
            path.write_text(text)
    print(json.dumps({'methods_checked': len(spec['methods']), 'files': len(pending),
                      'applied': not a.check_only, 'launch_ready': False}))


if __name__ == '__main__':
    main()

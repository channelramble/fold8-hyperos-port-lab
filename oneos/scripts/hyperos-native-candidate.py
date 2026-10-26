#!/usr/bin/env python3
"""Build offline HyperOS storage-service patches; never authorize deployment.

Reviewed using this image's .gnu_debugdata and AArch64 disassembly. Each ELF
LOAD segment containing a patch has matching file offsets and virtual addresses.
vold start() uses the string at 0xf45d; try_start()'s 0x6ce00 TBZ targets
the not-declared return at 0x6ced4. IncrementalService's two String16 lookups
reference 0x64786 (0xc005c ADR and 0xc2710/14 ADRP+ADD).
"""
import argparse
import hashlib
import json
from pathlib import Path

FILES = {
    'system/bin/vold': ('vold_patched', 'f93d8d75894dacf39842fd349c7c271f18794dec0a3a450d56b39464b89273e4',
                        [(0xf45c, b'\0vold\0', b'\0gvld\0'),
                         (0x6ce00, bytes.fromhex('b3060036'), bytes.fromhex('35000014'))]),
    'system/lib64/service.incremental.so': ('service.incremental_patched.so',
        '2a8a3ff60d47b438acef3338d2f28ea13cc54cce1cad5d8bd55aa68f4adb7caa',
        [(0x64785, b'\0vold\0', b'\0gvld\0')]),
}


def patch(data, expected_hash, changes):
    if hashlib.sha256(data).hexdigest() != expected_hash:
        raise ValueError('unknown binary: no patch written')
    out = bytearray(data)
    occupied = set()
    for offset, before, after in changes:
        if len(before) != len(after) or out[offset:offset + len(before)] != before:
            raise ValueError('unexpected patch bytes or length')
        locations = set(range(offset, offset + len(before)))
        if locations & occupied:
            raise ValueError('overlapping patches')
        occupied |= locations
        out[offset:offset + len(before)] = after
    return bytes(out)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('extracted', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    result = {}
    for src, (name, sha, changes) in FILES.items():
        result[name] = patch((a.extracted / src).read_bytes(), sha, changes)
    a.output.mkdir(parents=True, exist_ok=True)
    if any((a.output / name).exists() for name in result):
        raise ValueError('refusing to overwrite candidate binaries')
    for name, data in result.items():
        (a.output / name).write_bytes(data)
    (a.output / 'native-candidate.json').write_text(json.dumps({
        'launch_ready': False,
        'reason': 'Requires framework, OEM, APEX, mount and runtime integration review.',
        'sha256': {n: hashlib.sha256(d).hexdigest() for n, d in result.items()},
    }, indent=2) + '\n')


if __name__ == '__main__':
    main()

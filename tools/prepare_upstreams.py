#!/usr/bin/env python3
"""Retrieve exact upstream commits and apply the reviewed local patches. No ADB."""
from pathlib import Path
import argparse
import json
import subprocess


def run(*args, cwd=None):
    subprocess.run([str(x) for x in args], cwd=cwd, check=True)


def main():
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=repo / 'build/upstreams')
    args = parser.parse_args()
    sources = json.loads((repo / 'inputs/manifest.json').read_text())['upstream']
    targets = {name: args.output.resolve() / name.lower() for name in sources}
    if any(path.exists() for path in targets.values()):
        parser.error('Checkout destinations must not already exist; nothing overwritten')
    for name, source in sources.items():
        path = targets[name]
        path.mkdir(parents=True)
        run('git', 'init', path)
        run('git', 'remote', 'add', 'origin', source['url'], cwd=path)
        run('git', 'fetch', '--depth=1', 'origin', source['commit'], cwd=path)
        run('git', 'checkout', '--detach', 'FETCH_HEAD', cwd=path)
        actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=path, text=True).strip()
        if actual != source['commit']:
            raise RuntimeError('Unexpected fetched commit')
        patch = repo / 'patches' / (name + '.patch')
        run('git', 'apply', '--check', patch, cwd=path)
        run('git', 'apply', patch, cwd=path)
        if name == 'IMS':
            run('git', 'submodule', 'update', '--init', '--recursive', cwd=path)
            actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=path / 'app/jni/rnnoise', text=True).strip()
            if actual != source['rnnoise_commit']:
                raise RuntimeError('Unexpected RNNoise commit')
    print('Pinned source prepared. No build, installation or device command was executed.')


if __name__ == '__main__':
    main()

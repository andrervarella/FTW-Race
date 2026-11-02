#!/usr/bin/env python3
"""Materialize authorized public FTW asset Git blobs in this same repository."""
import base64
import hashlib
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

REPOSITORY = 'andrervarella/FTW-Race'
ROOT = Path(__file__).resolve().parent


def reconstruct(entry):
    text = ''.join((ROOT / part['path']).read_text(encoding='ascii') for part in entry['parts'])
    raw = base64.b64decode(text, validate=True)
    if len(raw) != entry['size']:
        raise ValueError('Unexpected byte count for ' + entry['path'])
    digest = hashlib.sha1(('blob ' + str(len(raw)) + '\0').encode() + raw).hexdigest()
    if digest != entry['sha']:
        raise ValueError('Unexpected Git blob SHA for ' + entry['path'])
    return text


def publish(text, token):
    request = urllib.request.Request(
        'https://api.github.com/repos/' + REPOSITORY + '/git/blobs',
        data=json.dumps({'content': text, 'encoding': 'base64'}).encode(),
        headers={'Authorization': 'Bearer ' + token,
                 'Accept': 'application/vnd.github+json',
                 'X-GitHub-Api-Version': '2022-11-28',
                 'User-Agent': 'FTW-V4-authorized-asset-materialization'},
        method='POST')
    with urllib.request.urlopen(request, timeout=90) as response:
        return json.load(response)['sha']


def main():
    if os.environ.get('GITHUB_REPOSITORY') != REPOSITORY:
        raise RuntimeError('This workflow is restricted to its own FTW repository')
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    token = os.environ['GITHUB_TOKEN']
    results = {'repository': REPOSITORY, 'run_id': os.environ.get('GITHUB_RUN_ID'), 'blobs': []}
    result_path = ROOT / 'result.json'
    try:
        for entry in manifest['blobs']:
            text = reconstruct(entry)
            actual = publish(text, token)
            result = {'path': entry['path'], 'size': entry['size'], 'expected': entry['sha'], 'actual': actual}
            results['blobs'].append(result)
            result_path.write_text(json.dumps(results, indent=2) + '\n')
            if actual != entry['sha']:
                raise RuntimeError('GitHub returned a mismatched blob SHA')
            print('Verified ' + entry['path'] + ': ' + actual, flush=True)
    except urllib.error.HTTPError as error:
        results['error'] = 'GitHub API HTTP ' + str(error.code)
        raise
    finally:
        result_path.write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()

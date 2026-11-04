"""Publish an immutable runtime tree so cached HTML/modules cannot mix releases.

No bundler or asset transformations: the whole existing relative URL graph moves
under a content-derived directory. Older releases and legacy Pages stay intact.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

GAME = Path(__file__).resolve().parents[1]
PUBLIC = 'https://andrervarella.github.io/FTW-Race/teste-v4/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def runtime_files():
    files = {name: GAME / name for name in ['index.html', 'styles.css', 'podium.css']}
    for directory in ['src', 'assets', 'cars']:
        for path in sorted((GAME / directory).rglob('*')):
            if path.is_symlink():
                raise ValueError(f'Symlink cannot enter release: {path}')
            if path.is_file():
                files[path.relative_to(GAME).as_posix()] = path
    files['tests/marquinhos-render.html'] = GAME / 'tests/marquinhos-render.html'
    return files


def page(html, base, share_url, release_id):
    metadata = (
        f'<meta name="ftw-runtime-base" content="{base}">\n'
        f'<meta name="ftw-release" content="{release_id}">\n'
        f'<link rel="canonical" href="{share_url}">\n'
        '<meta property="og:type" content="website">\n'
        '<meta property="og:title" content="FTW Race — Daniel, Felipe e Marquinhos">\n'
        '<meta property="og:description" content="Escolha seu piloto e corra em Cascavel. Marquinhos e seu caminhão também estão na pista.">\n'
        f'<meta property="og:url" content="{share_url}">\n'
    )
    html = html.replace('</head>', metadata + '</head>', 1)
    if base != './':
        for name in ['styles.css', 'podium.css', 'src/main.js', 'assets/legacy/ftw.png']:
            old = f'"{name}"'
            if html.count(old) != 1:
                raise ValueError(f'Expected one HTML entry reference: {name}')
            html = html.replace(old, f'"{base}{name}"', 1)
    return html.encode()


def package(output, public_base=PUBLIC):
    output = Path(output).resolve()
    files = runtime_files()
    inputs = {name: path.read_bytes() for name, path in sorted(files.items())}
    graph = hashlib.sha256()
    for name, raw in inputs.items():
        graph.update(name.encode() + b'\0' + str(len(raw)).encode() + b'\0' + raw)
    runtime_sha = graph.hexdigest()
    release_id = runtime_sha[:16]
    relative = f'releases/{release_id}/'
    share = public_base.rstrip('/') + '/' + relative
    destination = output / relative
    destination.mkdir(parents=True, exist_ok=True)
    records = []
    for name, raw in inputs.items():
        published = page(raw.decode(), './', share, release_id) if name == 'index.html' else raw
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != published:
            raise ValueError(f'Refusing to mutate existing immutable release: {target}')
        target.write_bytes(published)
        records.append({'path': name, 'bytes': len(published), 'sha256': digest(published), 'inputSha256': digest(raw)})
    manifest = {'version': 1, 'release': release_id, 'runtimeSha256': runtime_sha,
                'shareUrl': share, 'files': records}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    manifest_path = destination / 'release.json'
    if manifest_path.exists() and manifest_path.read_bytes() != manifest_bytes:
        raise ValueError('Refusing to change an existing release manifest')
    manifest_path.write_bytes(manifest_bytes)
    # Only the V4 entry and its metadata change; no legacy page is rewritten.
    (output / 'index.html').write_bytes(page(inputs['index.html'].decode(), relative, share, release_id))
    version_path = output / 'version.json'
    version = json.loads(version_path.read_text()) if version_path.exists() else {}
    version.update({'version': 'V4 Marquinhos · immutable runtime', 'runtimeRelease': release_id,
                    'runtimeSha256': runtime_sha, 'runtimeBase': relative, 'shareUrl': share,
                    'sourceLocalCommit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=GAME, text=True).strip()})
    version_path.write_text(json.dumps(version, ensure_ascii=False, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--public-base', default=PUBLIC)
    args = parser.parse_args()
    result = package(args.output, args.public_base)
    print(json.dumps({'release': result['release'], 'files': len(result['files']), 'shareUrl': result['shareUrl']}))

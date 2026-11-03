"""Copy accepted Marquinhos artwork into runtime without changing a single pixel.

The prepared source trees remain authoritative. This step records native atlas
layout, common display scale, exact owner statements and byte-for-byte copies.
Felipe's accepted jaw/neck retouch is deliberately limited to the opening image.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
PREPARED = ROOT / 'assets/sprites/v4'
RUNTIME = ROOT / 'game/assets/v4'
FELIPE_HASH = '98832d1d00feb8f628d76172ad2ace8dcacf75a4a6ea2e7c8af88faf4f7a236b'
ACCEPTANCE = {
    'status': 'owner-requested-integration',
    'date': '2026-11-03',
    'quote': 'Otimo o que mais precisamos para aplicar tudo isso no game? Inclusive também ter esse novo piloto que se chama Marquinhos na capa do game e telefone como personagem jogavel',
    'scope': 'prepared master + six derivative podium poses + truck views; cover and playable character',
    'interpretation': 'latest integration request accepts the prepared artwork for this use; no invented approval quote',
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def write_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def copy(source, target):
    source, target = PREPARED / source, RUNTIME / target
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(target) == sha(source), target
    with Image.open(target) as image:
        size = list(image.size)
    return {'file': relative(target), 'source': relative(source), 'sha256': sha(target),
            'sourceSha256': sha(source), 'size': size,
            'transformation': 'byte-identical copy of prepared source',
            'approval': ACCEPTANCE['status']}


def prepare():
    driver_source = PREPARED / 'truck-driver/frames.json'
    driver = json.loads(driver_source.read_text())
    driver_copies = [
        copy('truck-driver/neutral.png', 'drivers/marquinhos-neutral.png'),
        copy('truck-driver/portrait.png', 'drivers/marquinhos-portrait.png'),
        copy('truck-driver/portrait.webp', 'drivers/marquinhos-portrait.webp'),
    ]
    title_copies = [copy(f'truck-driver/portrait.{ext}', f'title/marquinhos-front-portrait.{ext}') for ext in ['png', 'webp']]
    podium_copies = [copy(f'truck-driver/podium-{i}.png', f'podium/marquinhos-{i}.png') for i in range(6)]
    write_json(RUNTIME / 'drivers/marquinhos.json', {
        'version': 1, 'displayName': 'Marquinhos', 'key': 'marquinhos', 'number': None,
        'sourceMetadata': relative(driver_source), 'sourceMetadataSha256': sha(driver_source),
        'masterApproval': driver['masterApproval'], 'integrationAcceptance': ACCEPTANCE,
        'frameSize': driver['frameSize'], 'ground': driver['ground'], 'pivot': driver['pivot'],
        'portrait': driver['portrait'], 'effects': driver['effects'],
        'assets': driver_copies + title_copies + podium_copies,
    })

    vehicle_source = PREPARED / 'truck-vehicle/frames.json'
    vehicle = json.loads(vehicle_source.read_text())
    vehicle_copies = [copy(f'truck-vehicle/{view}.png', f'cars/marquinhos-{view}.png') for view in vehicle['frameOrder']]
    vehicle_copies += [copy('truck-vehicle/truck-atlas.png', 'cars/marquinhos.png'),
                       copy('truck-vehicle/front-menu.png', 'cars/marquinhos-front.png')]
    write_json(RUNTIME / 'cars/marquinhos.json', {
        'version': 1, 'key': 'marquinhos', 'vehicleType': 'truck',
        'sourceMetadata': relative(vehicle_source), 'sourceMetadataSha256': sha(vehicle_source),
        'integrationAcceptance': ACCEPTANCE, 'configuration': vehicle['configurationProposal'],
        'frameSize': vehicle['frameSize'], 'frameOrder': vehicle['frameOrder'],
        'sheetGrid': vehicle['sheetGrid'], 'atlasSize': vehicle['atlasSize'],
        'pivot': vehicle['pivot'], 'ground': vehicle['ground'],
        'renderScale': vehicle['scale']['futureUniformDisplayMultiplierForProposedWidth'],
        'displayPolicy': 'one uniform multiplier on width and height, plus native 560/512 aspect; common fleet camera budget preserves equal-depth ratios',
        'scaleMeasurements': vehicle['scale'], 'assets': vehicle_copies,
    })

    podium_path = RUNTIME / 'podium/frames.json'
    podium = json.loads(podium_path.read_text())
    podium['assets'] = [row for row in podium['assets'] if row.get('key') != 'marquinhos' and '/marquinhos-' not in row['file']]
    for i, row in enumerate(podium_copies):
        original = next(item for item in driver['assets'] if item['file'] == f'podium-{i}.png')
        podium['assets'].append({**row, 'key': 'marquinhos', 'name': driver['stages'][i], 'frame': i,
                                 'pivot': driver['pivot'], 'ground': driver['ground'],
                                 'sourceCrop': original['sourceCrop'], 'sourceAnchor': original['sourceAnchor'],
                                 'scale': [original['scale'], original['scale']], 'rotationDegrees': 0})
    write_json(podium_path, podium)
    return title_copies


def title_metadata(title_copies, felipe_source):
    target_png = RUNTIME / 'title/felipe-front-portrait.png'
    target_webp = target_png.with_suffix('.webp')
    if felipe_source.is_file():
        assert sha(felipe_source) == FELIPE_HASH, 'Unexpected Felipe retouch source'
        shutil.copyfile(felipe_source, target_png)
        shutil.copyfile(felipe_source.with_suffix('.webp'), target_webp)
    assert sha(target_png) == FELIPE_HASH, 'Missing accepted Felipe title retouch; pass --felipe-source'

    path = RUNTIME / 'title/approval.json'
    title = json.loads(path.read_text())
    title['integrationAcceptance'] = ACCEPTANCE
    title['composition'] = 'layered DOM/CSS; original official logo PNGs, preserved Daniel/Felipe art, accepted title-only Felipe retouch and prepared Marquinhos portrait; no mirroring'
    row = next(item for item in title['assets'] if item['file'] == relative(target_png))
    row.update({'source': str(felipe_source), 'sha256': sha(target_png),
                'approval': 'owner-requested-integration of accepted title-only less-chin retouch',
                'scope': 'opening portrait PNG/WebP only; other Felipe sprites preserved'})
    title['assets'] = [item for item in title['assets'] if '/marquinhos-' not in item['file']] + title_copies
    title['felipeRetouch'] = {'date': '2026-11-03', 'status': 'owner-requested-integration',
                             'request': 'Deixe o rosto do Felipe com menos papada e um pouco mais magro ajuste novamente',
                             'scope': 'opening portrait only', 'sha256': FELIPE_HASH}
    write_json(path, title)

    path = RUNTIME / 'title/web-encodings.json'
    encodings = json.loads(path.read_text())
    for key, png, webp in [('felipe', target_png, target_webp),
                           ('marquinhos', RUNTIME / 'title/marquinhos-front-portrait.png', RUNTIME / 'title/marquinhos-front-portrait.webp'),
                           ('marquinhos-driver', RUNTIME / 'drivers/marquinhos-portrait.png', RUNTIME / 'drivers/marquinhos-portrait.webp')]:
        row = next((item for item in encodings if item['file'] == relative(webp)), None)
        if row is None:
            row = {}; encodings.append(row)
        with Image.open(png) as im: original_size = list(im.size)
        with Image.open(webp) as im: web_size = list(im.size)
        row.update({'file': relative(webp), 'source': relative(png), 'sourceSha256': sha(png), 'sha256': sha(webp),
                    'originalSize': original_size, 'size': web_size, 'bytes': webp.stat().st_size,
                    'method': 'byte-identical prepared WebP delivery; source PNG preserved at native size',
                    'approval': 'owner-requested-integration; technical delivery encoding'})
    write_json(path, encodings)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--felipe-source', type=Path, default=Path('/workspace/work/felipe-chin-fix/felipe-front-portrait-proposal.png'))
    args = parser.parse_args()
    title_metadata(prepare(), args.felipe_source)
    print('Copied 19 Marquinhos runtime images byte for byte; applied accepted Felipe title-only retouch and recorded provenance.')

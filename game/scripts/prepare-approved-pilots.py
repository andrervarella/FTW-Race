"""Prepare owner-approved pilot views without changing art or existing NPCs.

Requires Pillow, NumPy and SciPy, already used by the repository's NPC pipeline.
Raw sheets/portraits are preserved byte for byte. A nominal grid cell selects its
largest overlapping 8-connected person in the full row, retaining connected
hands/props that cross a cell boundary. Every pose gets the same exact .70 affine
scale, no rotation, and the midpoint of both feet at (128, 500).
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
PRESERVED = ROOT / 'assets/previews/v4/approved-pilots'
DRIVERS = ROOT / 'game/assets/v4/drivers'
PODIUM = ROOT / 'game/assets/v4/podium'
FRAME = (256, 512)
GROUND = 500
SCALE = .70
COLS = [0, 314, 627, 940, 1254]
ROWS = [0, 627, 1254]
NAMES = ['neutral', 'helmet', 'entry', 'receive', 'raise', 'open', 'spray', 'final']
SOURCE_NAMES = ['daniel-full-sprites-corrected.png', 'felipe-full-sprites-corrected.png',
                'daniel-face-v2.png', 'felipe-face-v2.png', 'felipe-face-cap.png']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(path):
    return str(path.relative_to(ROOT))


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def preserve_sources(source_dir):
    records = []
    previous = PRESERVED / 'sources.json'
    saved = {item['file']: item for item in json.loads(previous.read_text())} if previous.exists() else {}
    for name in SOURCE_NAMES:
        original = source_dir / name
        target = PRESERVED / name
        if original.is_file():
            if target.exists():
                assert digest(target) == digest(original), f'Refusing to overwrite preserved source: {name}'
            else:
                shutil.copyfile(original, target)
        assert target.is_file(), f'Missing preserved source and original: {name}'
        if relative(target) in saved:
            assert digest(target) == saved[relative(target)]['sha256'], f'Changed preserved bytes: {name}'
        with Image.open(target) as image:
            size = list(image.size)
        scope = ('eight full-body poses including corrected open bottles' if 'sprites' in name else
                 'face anchor and cap cover variant' if name == 'felipe-face-cap.png' else 'face anchor')
        records.append({'file': relative(target), 'sha256': digest(target), 'size': size,
                        'originalPath': str(original), 'approval': 'approved-by-owner',
                        'approvalScope': scope,
                        'approvalReference': ('Owner explicitly selected “Aprovar a capa” on 2026-11-02'
                                              if name == 'felipe-face-cap.png' else
                                              'Owner approved shown artwork (“Aprovado”) on 2026-11-02')})
    write_json(previous, records)
    return records


def preserve_npc_baseline(frames):
    path = PRESERVED / 'npc-baseline.json'
    records = [record for record in frames['assets'] if '/npc-' in record['file']]
    files = {relative(file): digest(file) for file in sorted(PODIUM.glob('npc-*'))}
    baseline = {'records': records, 'files': files}
    if path.exists():
        assert json.loads(path.read_text()) == baseline, 'NPC baseline changed; preparation will not replace it'
    else:
        write_json(path, baseline)
    return baseline


def prepare_view(sheet, key, index):
    col, row = index % 4, index // 4
    cell = [COLS[col], ROWS[row], COLS[col + 1], ROWS[row + 1]]
    raw = np.array(sheet.crop((0, cell[1], sheet.width, cell[3])))
    labels, count = ndimage.label(raw[:, :, 3] >= 80, structure=np.ones((3, 3), dtype=int))
    assert count > 0, f'Empty source row: {key}/{index}'
    overlap = np.bincount(labels[:, cell[0]:cell[2]].ravel(), minlength=count + 1)
    overlap[0] = 0
    person = int(overlap.argmax())
    assert overlap[person] > 10000, f'No complete person in source cell: {key}/{index}'
    mask = labels == person
    yy, xx = np.where(mask)
    bounds = [int(xx.min()), int(yy.min()), int(xx.max() + 1), int(yy.max() + 1)]
    ground = bounds[3]
    feet_y, feet_x = np.where(mask[max(0, ground - 90):ground])
    feet = [int(feet_x.min()), int(ground - 90 + feet_y.min()),
            int(feet_x.max() + 1), int(ground - 90 + feet_y.max() + 1)]
    foot_center = (feet[0] + feet[2]) / 2
    raw[:, :, 3] = np.where(mask, 255, 0)
    raw[~mask] = 0
    tight = Image.fromarray(raw).crop(bounds)
    inverse = [1 / SCALE, 0, foot_center - bounds[0] - FRAME[0] / 2 / SCALE,
               0, 1 / SCALE, ground - bounds[1] - GROUND / SCALE]
    assert FRAME[0] / 2 + (bounds[0] - foot_center) * SCALE > 0
    assert FRAME[0] / 2 + (bounds[2] - foot_center) * SCALE < FRAME[0]
    assert GROUND + (bounds[1] - ground) * SCALE > 0, 'Full body must fit without pose-specific resizing'
    image = tight.transform(FRAME, Image.Transform.AFFINE, inverse, resample=Image.Resampling.NEAREST)
    path = DRIVERS / f'{key}-{NAMES[index]}.png' if index < 2 else PODIUM / f'{key}-{index - 2}.png'
    image.save(path, optimize=True)
    global_bounds = [bounds[0], bounds[1] + cell[1], bounds[2], bounds[3] + cell[1]]
    return {'key': key, 'name': NAMES[index], 'file': relative(path),
            'source': relative(PRESERVED / f'{key}-full-sprites-corrected.png'),
            'sourceIndex': index, 'sourceCell': cell, 'sourceCrop': global_bounds,
            'sourceUsefulBounds': [0, 0, tight.width, tight.height],
            'sourceFootBounds': [feet[0], feet[1] + cell[1], feet[2], feet[3] + cell[1]],
            'sourceFootAnchor': [foot_center, ground + cell[1]],
            'retainedSourcePixels': int(mask.sum()),
            'excludedCellPixels': int(overlap.sum() - overlap[person]),
            'recoveredOutsideCellPixels': int(mask.sum() - overlap[person]),
            'size': list(FRAME), 'usefulBounds': list(image.getbbox()),
            'scale': [SCALE, SCALE], 'rotationDegrees': 0, 'pivot': [.5, GROUND / FRAME[1]],
            'approval': 'approved-by-owner', 'sha256': digest(path)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', type=Path, default=Path('/workspace/work/pilot-art-review'))
    options = parser.parse_args()
    PRESERVED.mkdir(parents=True, exist_ok=True)
    DRIVERS.mkdir(parents=True, exist_ok=True)
    frames_file = PODIUM / 'frames.json'
    frames = json.loads(frames_file.read_text())
    npc_baseline = preserve_npc_baseline(frames)
    sources = preserve_sources(options.source_dir)
    views, portraits = [], []
    for key in ['daniel', 'felipe']:
        with Image.open(PRESERVED / f'{key}-full-sprites-corrected.png') as source:
            sheet = source.convert('RGBA')
        assert sheet.size == (1254, 1254), f'Unexpected source dimensions: {key}'
        views.extend(prepare_view(sheet, key, index) for index in range(8))
        source = PRESERVED / ('daniel-face-v2.png' if key == 'daniel' else 'felipe-face-cap.png')
        destination = DRIVERS / f'{key}-portrait.png'
        shutil.copyfile(source, destination)
        approved_anchor = PRESERVED / f'{key}-face-v2.png'
        with Image.open(source) as portrait:
            size = list(portrait.size)
        portraits.append({'key': key, 'file': relative(destination), 'source': relative(source),
                          'size': size, 'sha256': digest(destination), 'operation': 'byte-for-byte copy',
                          'approval': 'approved-by-owner',
                          'approvalScope': ('approved face anchor' if key == 'daniel' else
                                            'approved face anchor and explicitly approved cap cover variant'),
                          'approvedFaceAnchor': relative(approved_anchor),
                          'approvedFaceAnchorSha256': digest(approved_anchor),
                          'approvedFaceAnchorStatus': 'approved-by-owner'})

    replacements = {}
    for view in views:
        if view['sourceIndex'] >= 2:
            record = dict(view)
            record['frame'] = view['sourceIndex'] - 2
            record['transformation'] = 'alpha>=80; largest cell-seeded connected person; exact common .70 scale; feet midpoint at128,500'
            replacements[view['file']] = record
    assert len(replacements) == 12
    assert all(file in {record['file'] for record in frames['assets']} for file in replacements)
    frames['assets'] = [replacements.get(record['file'], record) for record in frames['assets']]
    assert [record for record in frames['assets'] if '/npc-' in record['file']] == npc_baseline['records']
    write_json(frames_file, frames)
    meta = {'version': 'approved-pilots-1', 'frameSize': list(FRAME), 'ground': GROUND,
            'pivot': [.5, GROUND / FRAME[1]], 'commonScale': SCALE, 'alphaThreshold': 80,
            'columnBoundaries': COLS, 'rowBoundaries': ROWS,
            'componentConnectivity': 8, 'footAnchorMethod': 'midpoint of both feet in bottom90 source pixels',
            'sourceSelection': 'largest full-row component overlapping nominal sourceCell; sourceCrop is its tight global bounds',
            'approval': 'approved-by-owner',
            'sheetApproval': 'Owner approved both shown corrected sheets (“Aprovado”), 2026-11-02',
            'coverApproval': 'Owner explicitly selected “Aprovar a capa”, 2026-11-02',
            'sources': sources, 'views': views, 'portraits': portraits,
            'npcBaseline': relative(PRESERVED / 'npc-baseline.json')}
    write_json(DRIVERS / 'approved-pilots.json', meta)
    print('Prepared 16 approved 256x512 views at uniform scale .70 / ground500, '
          '2 unchanged portrait copies, 5 preserved raw sources; NPCs untouched.')


if __name__ == '__main__':
    main()

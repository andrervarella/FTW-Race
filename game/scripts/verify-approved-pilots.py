"""Verify approved pilot derivatives against raw sheets and the preserved NPC baseline."""
from pathlib import Path
import hashlib
import json

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[2]
SOURCES = ROOT / 'assets/previews/v4/approved-pilots'
MANIFEST = ROOT / 'game/assets/v4/drivers/approved-pilots.json'
COLS = [0, 314, 627, 940, 1254]
ROWS = [0, 627, 1254]
NAMES = ['neutral', 'helmet', 'entry', 'receive', 'raise', 'open', 'spray', 'final']


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check():
    assert MANIFEST.is_file(), 'Approved pilot preparation has not produced its manifest'
    meta = json.loads(MANIFEST.read_text())
    assert meta['frameSize'] == [256, 512]
    assert meta['ground'] == 500 and meta['pivot'] == [.5, 500 / 512]
    assert meta['commonScale'] == .70 and meta['alphaThreshold'] == 80
    assert meta['columnBoundaries'] == COLS and meta['rowBoundaries'] == ROWS
    assert len(meta['views']) == 16
    for source in meta['sources']:
        path = ROOT / source['file']
        assert source['approval'] == 'approved-by-owner'
        assert digest(path) == source['sha256'], f'Changed preserved source: {path}'
        with Image.open(path) as image:
            assert list(image.size) == source['size']
        original = Path(source['originalPath'])
        if original.is_file():
            assert digest(original) == source['sha256'], f'Original/copy mismatch: {path}'

    frames = json.loads((ROOT / 'game/assets/v4/podium/frames.json').read_text())
    records = {record['file']: record for record in frames['assets']}
    baseline = json.loads((SOURCES / 'npc-baseline.json').read_text())
    actual_npcs = [record for record in frames['assets'] if '/npc-' in record['file']]
    assert actual_npcs == baseline['records'], 'NPC metadata was modified'
    actual_files = sorted(str(path.relative_to(ROOT)) for path in
                          (ROOT / 'game/assets/v4/podium').glob('npc-*'))
    assert actual_files == sorted(baseline['files']), 'NPC file set was modified'
    for file, expected in baseline['files'].items():
        assert digest(ROOT / file) == expected, f'NPC bytes changed: {file}'

    for key in ['daniel', 'felipe']:
        views = sorted((view for view in meta['views'] if view['key'] == key),
                       key=lambda view: view['sourceIndex'])
        assert [view['sourceIndex'] for view in views] == list(range(8))
        assert [view['name'] for view in views] == NAMES
        assert len({view['sha256'] for view in views}) == 8
        for view in views:
            index = view['sourceIndex']
            box = [COLS[index % 4], ROWS[index // 4],
                   COLS[index % 4 + 1], ROWS[index // 4 + 1]]
            assert view['sourceCell'] == box
            assert view['approval'] == 'approved-by-owner'
            assert view['scale'] == [.70, .70] and view['rotationDegrees'] == 0
            assert view['pivot'] == [.5, 500 / 512]
            assert digest(ROOT / view['file']) == view['sha256']

            # Reconstruct independently from the preserved raw sheet, never from
            # a pre-cleaned intermediate or the preparation script's functions.
            row_box = [0, box[1], 1254, box[3]]
            raw = np.array(Image.open(ROOT / view['source']).convert('RGBA').crop(row_box))
            mask = raw[:, :, 3] >= 80
            labels, count = ndimage.label(mask, structure=np.ones((3, 3), dtype=int))
            assert count > 0
            areas = np.bincount(labels.ravel())
            areas[0] = 0
            overlap = np.bincount(labels[:, box[0]:box[2]].ravel(), minlength=count + 1)
            overlap[0] = 0
            selected = int(overlap.argmax())
            mask = labels == selected
            yy, xx = np.where(mask)
            bounds = [int(xx.min()), int(yy.min()), int(xx.max() + 1), int(yy.max() + 1)]
            global_bounds = [bounds[0], bounds[1] + box[1], bounds[2], bounds[3] + box[1]]
            assert view['sourceCrop'] == global_bounds
            assert view['sourceUsefulBounds'] == [0, 0, bounds[2] - bounds[0], bounds[3] - bounds[1]]
            assert view['retainedSourcePixels'] == int(mask.sum())
            assert view['excludedCellPixels'] == int(overlap.sum() - overlap[selected])
            assert view['recoveredOutsideCellPixels'] == int(mask.sum() - overlap[selected])
            ground = bounds[3]
            foot_y, foot_x = np.where(mask[max(0, ground - 90):ground])
            foot_bounds = [int(foot_x.min()), int(ground - 90 + foot_y.min()),
                           int(foot_x.max() + 1), int(ground - 90 + foot_y.max() + 1)]
            foot_center = (foot_bounds[0] + foot_bounds[2]) / 2
            global_feet = [foot_bounds[0], foot_bounds[1] + box[1],
                           foot_bounds[2], foot_bounds[3] + box[1]]
            assert view['sourceFootBounds'] == global_feet
            assert view['sourceFootAnchor'] == [foot_center, ground + box[1]]
            raw[:, :, 3] = np.where(mask, 255, 0)
            raw[~mask] = 0
            tight = Image.fromarray(raw).crop(bounds)
            inverse = [1 / .70, 0, foot_center - bounds[0] - 128 / .70,
                       0, 1 / .70, ground - bounds[1] - 500 / .70]
            expected = tight.transform((256, 512), Image.Transform.AFFINE,
                                       inverse, resample=Image.Resampling.NEAREST)
            image = Image.open(ROOT / view['file']).convert('RGBA')
            pixels = np.array(image)
            assert image.size == (256, 512)
            assert np.array_equal(pixels, np.array(expected)), f'Crop/scale mismatch: {view["file"]}'
            assert set(np.unique(pixels[:, :, 3])) == {0, 255}, 'Alpha must be binary'
            assert np.count_nonzero(pixels[pixels[:, :, 3] == 0]) == 0, 'Hidden RGB residue'
            bounds_out = image.getbbox()
            assert list(bounds_out) == view['usefulBounds']
            assert 0 < bounds_out[0] < bounds_out[2] < 256
            assert 0 < bounds_out[1] and bounds_out[3] == 500, 'Clipped body or unstable ground'
            assert 128 + (bounds[0] - foot_center) * .70 > 0
            assert 128 + (bounds[2] - foot_center) * .70 < 256
            assert 500 + (bounds[1] - ground) * .70 > 0
            if index >= 2:
                record = records[view['file']]
                for field in ['source', 'sourceCell', 'sourceCrop', 'sourceIndex', 'sourceUsefulBounds',
                              'sourceFootAnchor', 'size', 'pivot', 'sha256', 'approval']:
                    assert record[field] == view[field], f'Podium metadata mismatch: {field}'
                assert record['frame'] == index - 2

    assert len(meta['portraits']) == 2
    for portrait in meta['portraits']:
        assert digest(ROOT / portrait['file']) == portrait['sha256']
        assert digest(ROOT / portrait['source']) == portrait['sha256'], 'Portrait changed source pixels'
        assert digest(ROOT / portrait['approvedFaceAnchor']) == portrait['approvedFaceAnchorSha256']
        assert portrait['approvedFaceAnchorStatus'] == 'approved-by-owner'
        assert portrait['approval'] == 'approved-by-owner'
        if portrait['key'] == 'felipe':
            assert portrait['approvalScope'] == 'approved face anchor and explicitly approved cap cover variant'
    print(f'PASS: 16 approved views (8 per pilot), 2 byte-identical portraits, '
          f'{len(meta["sources"])} preserved source hashes, clean binary alpha, '
          f'uniform .70 scale, feet at y500, exact crop mapping, '
          f'{len(baseline["files"])} NPC files/records unchanged. '
          'Felipe cap cover variant explicitly approved.')


if __name__ == '__main__':
    check()

#!/usr/bin/env python3
"""Prepare the approved truck-driver art; never synthesize or articulate a pose.

Requires Python 3.10+, Pillow, NumPy and SciPy. See README-preparation.md.
Original files are read only; a byte-for-byte copy of each is included in sources/.
Exit 2 means a source boundary/component needs an explicit reviewed crop/anchor.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import json
import math
from pathlib import Path
import platform
import shutil
import sys
import zipfile

import numpy as np
import PIL
from PIL import Image, ImageDraw, ImageFont
import scipy
from scipy import ndimage


SIZE = (256, 512)
GROUND = 500
PIVOT = [0.5, 0.9765625]
STAGES = ["entry", "receive", "raise", "open", "spray", "final"]
STAGE_LABELS = ["Entrada", "Receber taça", "Erguer taça", "Abrir garrafa", "Champanhe", "Comemorar"]
DURATIONS = [1200, 1400, 1300, 1400, 2200, None]
OWNER_APPROVAL = "Ótimo. Essa última ficou perfeita. Ela é a referência."
APPROVED_MASTER_SHA256 = "3a02874d742a7c70382d3bc6a1da9a4896882aa68d458248b83cbcdb49773c10"
ALPHA_FLOOR = 8
MIN_MARGIN = 6


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def bbox(mask: np.ndarray) -> list[int]:
    yy, xx = np.nonzero(mask)
    if len(xx) == 0:
        raise ValueError("No visible pixels remain")
    return [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1]


def font(size: int) -> ImageFont.ImageFont:
    for name in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def checker(size: tuple[int, int], tile: int = 16) -> Image.Image:
    im = Image.new("RGBA", size, "#e9ebed")
    draw = ImageDraw.Draw(im)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill="#d5d9dc")
    return im


class ManualReview(Exception):
    pass


def cleanup(im: Image.Image, spec: dict, key: str, issues: list[str]) -> tuple[Image.Image, dict]:
    """Remove only nearly invisible matte and demonstrably tiny detached noise.

    A hue rule would destroy real cap/polo/skin/denim. In the approved master the
    colored fringe is alpha 1–8. Opaque colors are never keyed or recolored here.
    Larger disconnected components are ambiguous: require reviewed component IDs.
    """
    arr = np.asarray(im.convert("RGBA")).copy()
    original = arr.copy()
    low = (arr[:, :, 3] > 0) & (arr[:, :, 3] <= ALPHA_FLOOR)
    arr[low] = 0
    labels, count = ndimage.label(arr[:, :, 3] > ALPHA_FLOOR, structure=np.ones((3, 3)))
    sizes = np.bincount(labels.ravel())
    if count == 0:
        raise ManualReview(f"{key}: no character component found")
    main = int(np.argmax(sizes[1:]) + 1)
    tiny_limit = max(8, min(32, int(sizes[main] * 0.0005)))
    explicit = spec.get("keep_components")
    keep = {main} if explicit is None else {int(item) for item in explicit}
    if main not in keep or any(item < 1 or item > count for item in keep):
        raise ManualReview(f"{key}: keep_components must include body {main} and valid IDs")
    components = []
    for component in range(1, count + 1):
        mask = labels == component
        area = int(sizes[component])
        box = bbox(mask)
        decision = "keep-body" if component == main else "keep-reviewed-component" if component in keep else "remove-reviewed-component" if explicit is not None else "remove-tiny-detached-noise"
        if component not in keep and area > tiny_limit and explicit is None:
            decision = "ambiguous-needs-manual-crop"
            issues.append(f"{key}: detached component {component}, area {area}, bbox {box}; review prop/drop/noise and set keep_components explicitly")
        components.append({"id": component, "area": area, "bbox": box, "decision": decision})
    selected = np.isin(labels, list(keep))
    arr[~selected] = 0
    arr[arr[:, :, 3] == 0, :3] = 0
    significant = original[:, :, 3] > ALPHA_FLOOR
    removed = significant & ~selected
    # Exact preservation of all retained visible source pixels: no hue processing.
    assert np.array_equal(arr[selected], original[selected]), f"{key}: retained pixel mutation"
    return Image.fromarray(arr), {
        "alphaFloorInclusive": ALPHA_FLOOR,
        "removedLowAlphaPixels": int(low.sum()),
        "removedDetachedPixels": int(removed.sum()),
        "tinyComponentAreaLimit": tiny_limit,
        "preservedVisiblePixelsUnchanged": True,
        "components": components,
        "visibleBBox": bbox(selected),
    }


def grid_boxes(im: Image.Image, columns: int, rows: int, issues: list[str]) -> tuple[list[list[int]], dict]:
    """Find transparent gutters near equal cell boundaries, in any source size."""
    visible = np.asarray(im)[:, :, 3] > ALPHA_FLOOR
    boundaries = []
    diagnostics = {}
    for axis, count, dimension in ((0, columns, im.width), (1, rows, im.height)):
        projection = visible.sum(axis=0 if axis == 0 else 1)
        edges = [0]
        axis_log = []
        for i in range(1, count):
            ideal = dimension * i / count
            radius = max(2, round(dimension / count * 0.15))
            start, stop = max(1, round(ideal) - radius), min(dimension - 1, round(ideal) + radius)
            clear = np.flatnonzero(projection[start:stop] == 0) + start
            groups = np.split(clear, np.where(np.diff(clear) != 1)[0] + 1) if len(clear) else []
            groups = [group for group in groups if len(group) >= 3]
            if not groups:
                edge = round(ideal)
                issues.append(f"grid {'x' if axis == 0 else 'y'} boundary {i}: no transparent gutter near {edge}; provide all six explicit cell boxes")
                axis_log.append({"ideal": ideal, "selected": edge, "status": "ambiguous"})
            else:
                group = min(groups, key=lambda group: abs((int(group[0]) + int(group[-1])) / 2 - ideal))
                edge = int(round((int(group[0]) + int(group[-1])) / 2))
                axis_log.append({"ideal": ideal, "selected": edge, "gutter": [int(group[0]), int(group[-1]) + 1], "status": "transparent-gutter"})
            edges.append(edge)
        edges.append(dimension)
        boundaries.append(edges)
        diagnostics["x" if axis == 0 else "y"] = axis_log
    xx, yy = boundaries
    boxes = [[xx[c], yy[r], xx[c + 1], yy[r + 1]] for r in range(rows) for c in range(columns)]
    return boxes, diagnostics


def recover_row_components(im: Image.Image, nominal_boxes: list[list[int]], columns: int,
                           rows: int, issues: list[str]) -> tuple[list[list[int]], list[dict]]:
    """Recover whole bodies across nominal vertical dividers, without cutting props.

    Row boundaries require transparent gutters. Vertical boundaries are selection
    hints only: each row's connected body is selected by overlap with its nominal
    cell, then recovered in full. Six distinct components must be unambiguous.
    """
    alpha = np.asarray(im)[:, :, 3]
    recovered, diagnostics = [], []
    for row in range(rows):
        row_boxes = nominal_boxes[row * columns:(row + 1) * columns]
        y0, y1 = row_boxes[0][1], row_boxes[0][3]
        labels, count = ndimage.label(alpha[y0:y1] > ALPHA_FLOOR, structure=np.ones((3, 3)))
        sizes = np.bincount(labels.ravel())
        selected = set()
        for col, nominal in enumerate(row_boxes):
            x0, _, x1, _ = nominal
            overlap = np.bincount(labels[:, x0:x1].ravel(), minlength=count + 1)
            overlap[0] = 0
            order = np.argsort(overlap)[::-1]
            component = int(order[0])
            if component == 0 or overlap[component] < 200 or component in selected:
                raise ManualReview(f"row {row}, column {col}: missing/duplicate body; supply explicit boxes")
            if len(order) > 1 and overlap[order[1]] > overlap[component] * 0.25:
                issues.append(f"row {row}, column {col}: two substantial overlapping bodies; supply explicit boxes")
            selected.add(component)
            local = bbox(labels == component)
            # Preserve enough empty space for meaningful source-edge QA.
            box = [max(0, local[0] - 12), max(y0, y0 + local[1] - 12),
                   min(im.width, local[2] + 12), min(y1, y0 + local[3] + 12)]
            recovered.append(box)
            diagnostics.append({"nominalCell": nominal, "sourceCrop": box, "rowComponent": component,
                                "componentArea": int(sizes[component]), "selectionOverlapPixels": int(overlap[component]),
                                "method": "whole-row-connected-component-recovered-across-vertical-cell-boundaries"})
        unassigned = []
        for component in range(1, count + 1):
            if component in selected:
                continue
            area = int(sizes[component])
            entry = {"id": component, "area": area, "bboxInRow": bbox(labels == component)}
            unassigned.append(entry)
            if area > 32:
                issues.append(f"row {row}: unassigned component {component}, area {area}; possible detached prop/drop; provide reviewed explicit cell boxes")
        diagnostics.append({"row": row, "unassignedComponents": unassigned,
                            "unassignedRule": "only detached components of at most 32 pixels may be treated as technical speckle; larger requires review"})
    return recovered, diagnostics


def anchor(im: Image.Image, spec: dict, key: str, issues: list[str], require_cap: bool = False) -> dict:
    alpha = np.asarray(im)[:, :, 3]
    mask = alpha > ALPHA_FLOOR
    box = bbox(mask)
    left, top, right, bottom = box
    if "root" in spec:
        root_x, ground_y = map(float, spec["root"])
        origin = "reviewed-explicit-foot-anchor"
    else:
        # Bottom contact band avoids arm/prop extents influencing the root.
        band = max(3, round((bottom - top) * 0.12))
        contacts = (alpha >= 64)[max(top, bottom - band):bottom]
        xx = np.nonzero(contacts)[1]
        if not len(xx):
            raise ManualReview(f"{key}: no opaque sole/contact band; supply root")
        root_x = (float(xx.min()) + float(xx.max()) + 1) / 2
        ground_y = float(bottom)
        origin = "midpoint-of-both-feet-extents-in-bottom-12-percent-band"
        # At least two separated support clusters are expected for standing poses.
        support = np.any(contacts, axis=0)
        groups = ndimage.label(support)[1]
        if groups != 2:
            issues.append(f"{key}: expected two sole supports, found {groups}; supply reviewed root [x, groundY]")
    if not (left <= root_x <= right and bottom <= ground_y <= bottom + 3):
        issues.append(f"{key}: root must lie between soles with baseline at/below visible bottom {bottom}")
    if bottom >= im.height - 1 or left <= 1 or right >= im.width - 1 or top <= 1:
        issues.append(f"{key}: visible body/prop touches source crop edge {box}; expand/review crop (source may be clipped)")
    cap_top = spec.get("cap_top")
    if cap_top is None and require_cap:
        # Only neutral/entry may use their highest point as cap. Raised poses never do.
        cap_top = top
        cap_origin = "entry-or-neutral-highest-visible-point-assumed-cap-requires-visual-review"
    else:
        cap_origin = "reviewed-explicit-cap-crown" if cap_top is not None else None
    height = None if cap_top is None else ground_y - float(cap_top)
    if height is not None and height <= 0:
        raise ManualReview(f"{key}: invalid cap_top / root")
    return {"root": [root_x, ground_y], "rootMethod": origin, "capTop": cap_top,
            "capTopMethod": cap_origin, "anatomicalHeight": height,
            "anatomicalMeasurement": "measured-cap-to-sole" if height is not None else "unmeasured-requires-visual-review; shared-scale-only",
            "visibleBBox": box}


def normalize(im: Image.Image, info: dict, scale: float) -> Image.Image:
    root_x, root_y = info["root"]
    # A single affine scale+translation of the complete authentic pose. No limbs,
    # rotations, deformation, shape filling, or independently fitted pose sizes.
    inverse = (1 / scale, 0, root_x - SIZE[0] / (2 * scale), 0, 1 / scale, root_y - GROUND / scale)
    result = im.convert("RGBa").transform(SIZE, Image.Transform.AFFINE, inverse,
                                        resample=Image.Resampling.BICUBIC).convert("RGBA")
    arr = np.asarray(result).copy()
    arr[arr[:, :, 3] <= 1] = 0
    arr[arr[:, :, 3] == 0, :3] = 0
    return Image.fromarray(arr)


def verify_frame(im: Image.Image, key: str) -> dict:
    assert im.mode == "RGBA" and im.size == SIZE, f"{key}: RGBA / frame size"
    arr = np.asarray(im)
    box = bbox(arr[:, :, 3] > 0)
    left, top, right, bottom = box
    assert left > 0 and top > 0 and right < SIZE[0] and bottom <= GROUND + 1, f"{key}: clipping / ground {box}"
    assert not np.any(arr[arr[:, :, 3] == 0, :3]), f"{key}: RGB leakage under alpha"
    assert np.any(arr[:, :, 3] == 0) and np.any(arr[:, :, 3] >= 128), f"{key}: alpha invalid"
    assert PIVOT == [SIZE[0] / 2 / SIZE[0], GROUND / SIZE[1]], "pivot mismatch"
    return {"rgba": True, "size": list(SIZE), "visibleBBox": box,
            "marginsPx": [left, top, SIZE[0] - right, SIZE[1] - bottom],
            "ground": GROUND, "pivot": PIVOT, "noOutputClipping": True,
            "zeroRgbUnderTransparentPixels": True}


def source_overlay(sheet: Image.Image, boxes: list[list[int]], specs: list[dict], output: Path) -> None:
    view = checker(sheet.size)
    view.alpha_composite(sheet)
    draw = ImageDraw.Draw(view)
    for index, box in enumerate(boxes):
        draw.rectangle(box, outline="#ff4da6", width=3)
        draw.text((box[0] + 8, box[1] + 8), f"{index}: {STAGES[index]}", font=font(24), fill="#ffe200", stroke_width=2, stroke_fill="#111111")
        if "root" in specs[index]:
            x, y = specs[index]["root"]
            x, y = x + box[0], y + box[1]
            draw.line((x - 16, y, x + 16, y), fill="#00e5ff", width=3)
            draw.line((x, y - 16, x, y + 16), fill="#00e5ff", width=3)
    view.thumbnail((1600, 1600), Image.Resampling.LANCZOS)
    view.convert("RGB").save(output)


def portrait(master: Image.Image, info: dict, spec: dict) -> tuple[Image.Image, list[int]]:
    left, top, right, bottom = info["visibleBBox"]
    crop_box = spec.get("portrait_box", [left, max(0, top - 8), right, round(top + info["anatomicalHeight"] * 0.50)])
    if len(crop_box) != 4 or not (0 <= crop_box[0] < crop_box[2] <= master.width and 0 <= crop_box[1] < crop_box[3] <= master.height):
        raise ManualReview("master: portrait_box must lie inside the approved master")
    crop = master.crop(crop_box)
    scale = min(496 / crop.width, 624 / crop.height)
    crop = crop.resize((round(crop.width * scale), round(crop.height * scale)), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (512, 640))
    canvas.alpha_composite(crop, ((512 - crop.width) // 2, 8))
    return canvas, list(crop_box)


def contact_sheet(frames: list[Image.Image], portrait_im: Image.Image, name: str) -> Image.Image:
    tile_w, tile_h = 280, 584
    result = Image.new("RGB", (tile_w * 4, tile_h * 2), "#f5f6f7")
    draw = ImageDraw.Draw(result)
    all_images = frames + [portrait_im]
    labels = ["Neutro · referência aprovada"] + [f"{i} · {stage} · {str(duration) + ' ms' if duration else 'parado'}" for i, (stage, duration) in enumerate(zip(STAGE_LABELS, DURATIONS))] + ["Retrato · referência aprovada"]
    for index, (im, label) in enumerate(zip(all_images, labels)):
        x, y = index % 4 * tile_w, index // 4 * tile_h
        panel = checker(SIZE)
        if index == 7:
            small = im.copy()
            small.thumbnail(SIZE, Image.Resampling.LANCZOS)
            panel.alpha_composite(small, ((256 - small.width) // 2, 0))
        else:
            panel.alpha_composite(im)
        result.paste(panel.convert("RGB"), (x + 12, y + 36))
        draw.text((x + 12, y + 9), name[:32], font=font(16), fill="#13171c")
        draw.text((x + 12, y + 552), label, font=font(12), fill="#13171c")
    return result


def data_uri(im: Image.Image) -> str:
    stream = io.BytesIO()
    im.save(stream, format="PNG")
    return "data:image/png;base64," + base64.b64encode(stream.getvalue()).decode("ascii")


def preview_html(frames: list[Image.Image], portrait_im: Image.Image, name: str) -> str:
    payload = json.dumps({"neutral": data_uri(frames[0]), "frames": [data_uri(im) for im in frames[1:]], "portrait": data_uri(portrait_im), "stages": STAGES, "labels": STAGE_LABELS, "durations": DURATIONS}).replace("<", "\\u003c")
    return """<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="icon" href="data:,"><title>Revisão de sprites — NAME</title>
<style>body{font:16px system-ui;background:#171b20;color:#f4f5f6;margin:0;padding:24px}main{max-width:1100px;margin:auto}h1{font-size:24px}p{line-height:1.5}button{font:inherit;padding:8px 12px;margin:3px;cursor:pointer}button[aria-pressed=true]{background:#b82031;color:white}section{display:flex;gap:24px;flex-wrap:wrap}.panel{background:#e9ebed;background-image:conic-gradient(#d5d9dc 25%,transparent 0 50%,#d5d9dc 0 75%,transparent 0);background-size:32px 32px;position:relative;width:256px;height:512px}.panel:after{position:absolute;content:'';left:0;right:0;top:500px;border-top:1px solid #b82031;pointer-events:none}.panel img{display:block;width:256px;height:512px}.light{background:white;background-image:none}.dark{background:#242b31;background-image:none}figcaption{margin:8px 0}figure{margin:0}.portrait img{width:256px;height:320px;object-fit:contain}.portrait:after{display:none}.portrait{height:320px}small{color:#c8d0d7}#status{min-height:24px}</style>
<main><h1>NAME — revisão técnica</h1><p>Apenas a referência original foi aprovada pelo proprietário. As seis poses derivadas aguardam revisão. Boné vermelho Mercedes, óculos pretos, polo FTW vermelha e jeans devem manter a referência. Não há efeitos de champanhe adicionados.</p>
<div><button id="play">Reproduzir</button><button id="restart">Reiniciar</button><button id="bg">Fundo: quadriculado</button></div><div id="steps" aria-label="Selecionar pose"></div><p id="status" role="status"></p>
<section><figure><div class="panel"><img id="pose" alt="Pose de pódio"></div><figcaption>Seis poses · 256 × 512 · chão 500</figcaption></figure><figure><div class="panel"><img id="neutral" alt="Referência aprovada normalizada"></div><figcaption>Neutro a partir da referência aprovada</figcaption></figure><figure><div class="panel portrait"><img id="portrait" alt="Retrato recortado da referência aprovada"></div><figcaption>Retrato — recorte da referência aprovada</figcaption></figure></section><p><small>Uma escala fixa para as seis poses. Neutro com a mesma altura anatômica da entrada. A linha vermelha marca o chão. O quadro final permanece parado; movimento reduzido inicia em pausa.</small></p></main>
<script>const data=PAYLOAD;let current=0,playing=false,started=0,timer=0;const pose=document.getElementById('pose'),status=document.getElementById('status'),play=document.getElementById('play');document.getElementById('neutral').src=data.neutral;document.getElementById('portrait').src=data.portrait;
function render(){pose.src=data.frames[current];pose.alt='Pose '+data.labels[current];status.textContent=current+' · '+data.labels[current]+' · '+(data.durations[current]===null?'final parado':data.durations[current]+' ms')+' · aguardando revisão';document.querySelectorAll('[data-step]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.step)===current));play.textContent=playing?'Pausar':'Reproduzir'}
function stop(){clearTimeout(timer);playing=false;render()}function schedule(){clearTimeout(timer);render();if(playing&&data.durations[current]!==null)timer=setTimeout(()=>{current++;if(current===5)playing=false;schedule()},data.durations[current]);else if(current===5){playing=false;render()}}
data.labels.forEach((stage,i)=>{let b=document.createElement('button');b.textContent=i+' '+stage;b.dataset.step=i;b.onclick=()=>{stop();current=i;render()};document.getElementById('steps').append(b)});play.onclick=()=>{if(playing)stop();else{if(current===5)current=0;playing=true;schedule()}};document.getElementById('restart').onclick=()=>{current=0;playing=true;schedule()};let bg=0;document.getElementById('bg').onclick=()=>{bg=(bg+1)%3;document.querySelectorAll('.panel').forEach(p=>{p.classList.toggle('light',bg===1);p.classList.toggle('dark',bg===2)});document.getElementById('bg').textContent='Fundo: '+['quadriculado','claro','escuro'][bg]};if(matchMedia('(prefers-reduced-motion: reduce)').matches)current=5;render();</script></html>""".replace("NAME", html.escape(name)).replace("PAYLOAD", payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True, help="owner-approved full-body master PNG")
    parser.add_argument("--sheet", type=Path, required=True, help="one generated six-pose sheet PNG")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--display-name", default="Piloto do caminhão")
    parser.add_argument("--grid", default="3x2", help="column×row layout, exactly six cells (default 3x2)")
    parser.add_argument("--anchors", type=Path, help="reviewed JSON overrides; coordinates are local to each crop")
    parser.add_argument("--standing-height", type=float, default=410, help="desired entry cap-to-ground pixels; common fit may reduce it")
    args = parser.parse_args()
    try:
        columns, rows = map(int, args.grid.lower().split("x"))
        assert columns > 0 and rows > 0 and columns * rows == 6
    except (ValueError, AssertionError):
        parser.error("--grid must be CxR with exactly six cells")
    if not (100 <= args.standing_height <= GROUND - MIN_MARGIN):
        parser.error("--standing-height must be 100–494")
    for source in (args.base, args.sheet):
        if not source.is_file() or source.suffix.lower() != ".png":
            parser.error(f"source PNG missing: {source}")
    output = args.output.resolve()
    if any(source.resolve().is_relative_to(output) for source in (args.base, args.sheet)):
        parser.error("output must not contain either original source")
    output.mkdir(parents=True, exist_ok=True)
    # An unsuccessful repeat must never leave a stale ZIP that appears approved.
    for name in ("truck-driver-art.zip", "truck-driver-art.zip.sha256"):
        (output / name).unlink(missing_ok=True)
    before_hashes = {"master": sha(args.base), "sheet": sha(args.sheet)}
    if before_hashes["master"] != APPROVED_MASTER_SHA256:
        parser.error("--base does not match the exact owner-approved MASTER hash; this script must not transfer approval to another image")
    overrides = json.loads(args.anchors.read_text(encoding="utf-8")) if args.anchors else {}
    if overrides.get("sourceSheetSha256", before_hashes["sheet"]) != before_hashes["sheet"] or overrides.get("sourceMasterSha256", before_hashes["master"]) != before_hashes["master"]:
        parser.error("reviewed anchors belong to different source hashes")
    master_spec = overrides.get("master", {})
    specs = overrides.get("cells", [{} for _ in range(6)])
    if len(specs) != 6:
        parser.error("anchors JSON must have exactly six cells")
    if any("box" in spec for spec in specs) and not all("box" in spec for spec in specs):
        parser.error("provide explicit boxes for all six cells, or for none")
    master_source = Image.open(args.base).convert("RGBA")
    sheet_source = Image.open(args.sheet).convert("RGBA")
    issues: list[str] = []
    qa: dict = {"status": "in-progress", "sourceHashes": before_hashes, "issues": issues,
                "assertions": {}, "preparationScriptSha256": sha(Path(__file__)),
                "anchorsFileSha256": sha(args.anchors) if args.anchors else None,
                "software": {"python": platform.python_version(), "Pillow": PIL.__version__, "numpy": np.__version__, "scipy": scipy.__version__}}
    auto_boxes, gutter_report = grid_boxes(sheet_source, columns, rows, issues)
    explicit_boxes = all("box" in spec for spec in specs)
    if explicit_boxes:
        issues.clear()  # Explicit reviewed boxes replace gutter inference.
    boxes = [list(spec.get("box", auto_boxes[i])) for i, spec in enumerate(specs)]
    qa["grid"] = {"layout": [columns, rows], "sourceSize": list(sheet_source.size), "gutters": gutter_report, "explicitBoxes": explicit_boxes, "nominalBoxes": boxes}
    try:
        if not explicit_boxes:
            # Horizontal row cuts must be transparent. Whole-row recovery makes
            # a missing vertical gutter harmless, so retain only y-cut issues.
            issues[:] = [issue for issue in issues if issue.startswith("grid y ")]
            boxes, recovery = recover_row_components(sheet_source, boxes, columns, rows, issues)
            qa["grid"]["componentRecovery"] = recovery
        qa["grid"]["boxes"] = boxes
        for box in boxes:
            if len(box) != 4 or not (0 <= box[0] < box[2] <= sheet_source.width and 0 <= box[1] < box[3] <= sheet_source.height):
                raise ManualReview(f"Invalid cell box {box}")
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    raise ManualReview("Cell boxes overlap; a genuine pose must occur once")
        source_overlay(sheet_source, boxes, specs, output / "source-crop-review.png")
        master, master_cleanup = cleanup(master_source, master_spec, "master", issues)
        master_anchor = anchor(master, master_spec, "master", issues, require_cap=True)
        qa["master"] = {"cleanup": master_cleanup, "anchor": master_anchor}
        poses, pose_anchors, pose_reports = [], [], []
        for index, (box, spec) in enumerate(zip(boxes, specs)):
            pose, clean_report = cleanup(sheet_source.crop(box), spec, STAGES[index], issues)
            info = anchor(pose, spec, STAGES[index], issues, require_cap=index == 0)
            poses.append(pose)
            pose_anchors.append(info)
            pose_reports.append({"stage": STAGES[index], "sourceCrop": box, "cleanup": clean_report, "anchor": info})
        qa["poses"] = pose_reports
        if issues:
            raise ManualReview("Ambiguous source components, feet, or crop boundaries")
        entry_height = pose_anchors[0]["anatomicalHeight"]
        target_scale = args.standing_height / entry_height
        constraints = []
        for info in pose_anchors:
            left, top, right, bottom = info["visibleBBox"]
            rx, ry = info["root"]
            constraints += [(128 - MIN_MARGIN) / max(1, rx - left), (128 - MIN_MARGIN) / max(1, right - rx), (GROUND - MIN_MARGIN) / max(1, ry - top)]
        # Include neutral extents at equivalent anatomical height; its scale is
        # derived only from master/entry anatomy, never independently fitted.
        master_ratio = entry_height / master_anchor["anatomicalHeight"]
        left, top, right, bottom = master_anchor["visibleBBox"]
        rx, ry = master_anchor["root"]
        constraints += [(128 - MIN_MARGIN) / max(1, (rx - left) * master_ratio), (128 - MIN_MARGIN) / max(1, (right - rx) * master_ratio), (GROUND - MIN_MARGIN) / max(1, (ry - top) * master_ratio)]
        scale = min([target_scale] + constraints)
        qa["scale"] = {"sheetScale": scale, "masterScale": scale * master_ratio, "requestedEntryHeight": args.standing_height,
                       "actualEntryHeight": entry_height * scale, "neutralAnatomicalHeight": master_anchor["anatomicalHeight"] * scale * master_ratio,
                       "commonFitReducedForBodyOrProps": scale < target_scale - 1e-9, "independentPoseFit": False,
                       "allSixSheetTransformsShareScale": True}
        assert math.isclose(qa["scale"]["actualEntryHeight"], qa["scale"]["neutralAnatomicalHeight"], abs_tol=1e-6)
        for index, info in enumerate(pose_anchors):
            if info["anatomicalHeight"] is not None and not 0.90 <= info["anatomicalHeight"] / entry_height <= 1.10:
                issues.append(f"{STAGES[index]}: source anatomy differs by more than 10% from entry; do not independently rescale; revise sheet")
        if issues:
            raise ManualReview("Source character scale drift")
        neutral = normalize(master, master_anchor, scale * master_ratio)
        frames = [neutral] + [normalize(im, info, scale) for im, info in zip(poses, pose_anchors)]
        names = ["neutral.png"] + [f"podium-{i}.png" for i in range(6)]
        frame_qa = {name: verify_frame(im, name) for name, im in zip(names, frames)}
        qa["frames"] = frame_qa
        for name, im in zip(names, frames):
            im.save(output / name, optimize=True)
        portrait_im, portrait_box = portrait(master, master_anchor, master_spec)
        portrait_im.save(output / "portrait.png", optimize=True)
        portrait_im.save(output / "portrait.webp", format="WEBP", lossless=True, exact=True)
        assert Image.open(output / "portrait.webp").convert("RGBA").tobytes() == portrait_im.tobytes(), "portrait WebP must be pixel exact"
        atlas = Image.new("RGBA", (SIZE[0] * 7, SIZE[1]))
        atlas_frames = {}
        for index, (name, im) in enumerate(zip(names, frames)):
            atlas.alpha_composite(im, (index * SIZE[0], 0))
            atlas_frames[name] = {"frame": {"x": index * 256, "y": 0, "w": 256, "h": 512}, "rotated": False, "trimmed": False,
                                  "spriteSourceSize": {"x": 0, "y": 0, "w": 256, "h": 512}, "sourceSize": {"w": 256, "h": 512}, "pivot": {"x": PIVOT[0], "y": PIVOT[1]}}
        atlas.save(output / "full-body-atlas.png", optimize=True)
        reloaded_atlas = Image.open(output / "full-body-atlas.png").convert("RGBA")
        assert all(reloaded_atlas.crop((i * 256, 0, (i + 1) * 256, 512)).tobytes() == im.tobytes()
                   for i, im in enumerate(frames)), "Atlas must preserve every frame pixel exactly"
        write_json(output / "full-body-atlas.json", {"frames": atlas_frames, "meta": {"image": "full-body-atlas.png", "format": "RGBA8888", "size": {"w": atlas.width, "h": atlas.height}, "scale": "1"}})
        contact_sheet(frames, portrait_im, args.display_name).save(output / "contact-sheet.png", optimize=True)
        (output / "preview.html").write_text(preview_html(frames, portrait_im, args.display_name), encoding="utf-8")
        sources = output / "sources"
        sources.mkdir(exist_ok=True)
        shutil.copyfile(args.base, sources / "approved-master.png")
        shutil.copyfile(args.sheet, sources / "generated-podium-sheet.png")
        if args.anchors:
            shutil.copyfile(args.anchors, sources / "reviewed-anchors.json")
        else:
            (sources / "reviewed-anchors.json").unlink(missing_ok=True)
        assert sha(sources / "approved-master.png") == before_hashes["master"]
        assert sha(sources / "generated-podium-sheet.png") == before_hashes["sheet"]
        assert {"master": sha(args.base), "sheet": sha(args.sheet)} == before_hashes, "Original source changed"
        assets = []
        for index, name in enumerate(names):
            assets.append({"file": name, "sha256": sha(output / name), "size": list(SIZE), "pivot": PIVOT, "ground": GROUND,
                           "stage": "neutral" if index == 0 else STAGES[index - 1], "durationMs": None if index == 0 else DURATIONS[index - 1],
                           "source": "sources/approved-master.png" if index == 0 else "sources/generated-podium-sheet.png",
                           "sourceCrop": [0, 0, master.width, master.height] if index == 0 else boxes[index - 1],
                           "sourceAnchor": master_anchor if index == 0 else pose_anchors[index - 1],
                           "scale": scale * master_ratio if index == 0 else scale,
                           "approval": "technical-normalization-of-approved-master; no-separate-owner-approval" if index == 0 else "pending-owner-review"})
        metadata = {"schemaVersion": 1, "displayName": args.display_name, "characterId": "truck-driver", "masterApproval": {"status": "owner-approved-MASTER-only", "quote": OWNER_APPROVAL, "sha256": before_hashes["master"]},
                    "derivativePoseApproval": "pending-owner-review", "portraitApproval": "technical-crop-of-approved-master; no-separate-owner-approval",
                    "identity": {"headwear": "red Mercedes cap; never helmet", "eyewear": "black sunglasses", "shirt": "new red FTW polo with black collar", "legs": "slim jeans", "arms": "moderate", "belly": "small"},
                    "frameSize": list(SIZE), "ground": GROUND, "pivot": PIVOT, "stages": STAGES, "frameDurationsMs": DURATIONS,
                    "finalFrameHolds": True, "poseCount": 6, "fullBodyFileCount": 7, "sheetGrid": [columns, rows], "scale": qa["scale"],
                    "sources": {"approvedMaster": {"file": "sources/approved-master.png", "sha256": before_hashes["master"], "size": list(master_source.size)}, "derivativeSheet": {"file": "sources/generated-podium-sheet.png", "sha256": before_hashes["sheet"], "size": list(sheet_source.size)}},
                    "assets": assets, "portrait": {"png": "portrait.png", "webp": "portrait.webp", "sourceCrop": portrait_box, "size": [512, 640], "sha256Png": sha(output / "portrait.png"), "sha256Webp": sha(output / "portrait.webp")},
                    "transformPolicy": "Whole authentic bodies only; one shared sheet scale and foot anchors; neutral equivalent to entry anatomy. No generated limbs, part rotations, deformation, recoloring, helmet, champagne drops, or effects.",
                    "visualReviewRequired": ["all six derivative poses and identity", "entry highest point is cap crown if no explicit cap_top", "cap/sole anchors", "source proportions", "genuine trophy/bottle and absence of generated champagne drops"]}
        metadata["effects"] = {}
        for effect_name, effect in overrides.get("effects", {}).items():
            index = STAGES.index(effect["stage"])
            box, info = boxes[index], pose_anchors[index]
            sx, sy = effect["sourcePoint"]
            px = SIZE[0] / 2 + (sx - box[0] - info["root"][0]) * scale
            py = GROUND + (sy - box[1] - info["root"][1]) * scale
            assert 0 <= px < SIZE[0] and 0 <= py < SIZE[1], "Effect anchor outside frame"
            assert frames[index + 1].getpixel((round(px), round(py)))[3] > ALPHA_FLOOR, "Effect anchor must touch visible prop"
            dx, dy = effect["sourceDirection"]
            length = (dx * dx + dy * dy) ** .5
            assert length > 0
            metadata["effects"][effect_name] = {"file": names[index + 1], "sourcePoint": [sx, sy],
                "pixelOrigin": [px, py], "normalizedOrigin": [px / SIZE[0], py / SIZE[1]],
                "direction": [dx / length, dy / length], "coordinateSystem": "image x-right, y-down",
                "review": "manually located on source prop; runtime effect not integrated"}
        write_json(output / "frames.json", metadata)
        portable_script = output / "prepare.py"
        if Path(__file__).resolve() != portable_script.resolve():
            shutil.copyfile(__file__, portable_script)
        (output / "README.md").write_text("""# Sprites do piloto do caminhão

Abra `preview.html` para conferir as seis poses, o retrato e a referência em fundos diferentes. O arquivo funciona sem conexão. `contact-sheet.png` reúne as oito imagens.

`neutral.png` e `podium-0.png` a `podium-5.png`: PNGs transparentes 256×512, chão500 e pivô(0.5,0.9765625). O atlas contém os sete corpos sem alterar seus pixels. Retrato em PNG/WebP sem perdas. Estados e tempos em `frames.json`.

A referência original foi aprovada pelo proprietário. As seis poses novas aguardam revisão visual. O boné vermelho Mercedes permanece em todas. Não há caminhão ou integração jogável neste pacote. Gotas de champanhe são efeitos separados; `effects` registra a boca da garrafa e sua direção.

Os originais estão em `sources/`, intactos. `SHA256SUMS` permite conferir os arquivos. Para reproduzir tecnicamente (Pillow, NumPy e SciPy), use outra pasta de saída:

```sh
python prepare.py --base sources/approved-master.png --sheet sources/generated-podium-sheet.png --anchors sources/reviewed-anchors.json --output ../truck-driver-rebuilt
```
""", encoding="utf-8")
        qa["status"] = "technical-checks-passed; derivative-poses-pending-owner-review"
        qa["assertions"] = {"noOutputClipping": True, "allFramesRgba256x512": True, "ground500": True, "pivotConsistent": True,
                            "oneSharedPoseScale": True, "neutralAndEntryAnatomicalHeightEqual": True,
                            "sourceCopiesByteExact": True, "originalSourceHashesUnchanged": True, "portraitWebpPixelExact": True,
                            "atlasContainsAllSevenFramesPixelExact": True,
                            "noSyntheticPoseOrPartRotation": True, "onlyMasterHasOwnerApproval": True}
        qa["visualLimitations"] = "Automated alpha/geometry checks cannot approve character identity, anatomy, genuine props, or absence of drawn spray; inspect contact-sheet.png and preview.html."
        product_names = names + ["portrait.png", "portrait.webp", "full-body-atlas.png", "full-body-atlas.json", "contact-sheet.png", "preview.html", "source-crop-review.png", "frames.json", "README.md", "prepare.py", "sources/approved-master.png", "sources/generated-podium-sheet.png"]
        if args.anchors:
            product_names.append("sources/reviewed-anchors.json")
        products = [output / name for name in sorted(product_names)]
        assert all(path.is_file() for path in products), "Missing owned output"
        qa["payloadHashes"] = {str(path.relative_to(output)): sha(path) for path in products}
        write_json(output / "qa-report.json", qa)
        paths = sorted(products + [output / "qa-report.json"])
        (output / "SHA256SUMS").write_text("".join(f"{sha(path)}  {path.relative_to(output)}\n" for path in paths), encoding="utf-8")
        archive = output / "truck-driver-art.zip"
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as package:
            for path in paths + [output / "SHA256SUMS"]:
                package.write(path, str(path.relative_to(output)))
        (output / "truck-driver-art.zip.sha256").write_text(f"{sha(archive)}  {archive.name}\n", encoding="utf-8")
        print(json.dumps({"status": qa["status"], "output": str(output), "fullBodyPngs": 7,
                          "sheetScale": scale, "standingHeight": qa["scale"]["actualEntryHeight"], "zipSha256": sha(archive)}, ensure_ascii=False))
        return 0
    except (ManualReview, AssertionError, ValueError) as error:
        qa["status"] = "needs-manual-crop"
        qa["error"] = str(error)
        qa["originalSourceHashesUnchanged"] = {"master": sha(args.base), "sheet": sha(args.sheet)} == before_hashes
        write_json(output / "qa-report.json", qa)
        print(json.dumps({"status": qa["status"], "error": str(error), "issues": issues, "report": str(output / "qa-report.json")}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

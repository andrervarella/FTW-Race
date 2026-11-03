#!/usr/bin/env python3
"""Prepare one authentic 3x2 truck sheet for review, without synthesizing art.

Python 3.10+, Pillow, NumPy and SciPy. Exit 2 means crops/anchors need review.
Input files are read only; output is isolated and no game runtime is changed.
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


SIZE = (560, 512)
GROUND = 470
PIVOT = [0.5, 470 / 512]
NAMES = ["rear", "left", "right", "brake", "left-brake", "right-brake"]
LABELS = ["Traseira", "Esquerda", "Direita", "Freio", "Esquerda + freio", "Direita + freio"]
ALPHA_FLOOR = 8
MARGIN = 12
PROPOSED_WIDTH_RATIO = 1.4
CAR_GROUND = 470
BENCHMARK = {"vehicle": "IVECO Chile 4x2 tractor benchmark", "lengthM": 6.252,
             "widthM": 2.55, "heightM": 3.789, "wheelbaseM": 3.8,
             "scope": "physical reference only; not a measurement of the FTW truck or Mercedes; not a runtime conversion"}


class NeedsReview(Exception):
    pass


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def bounds(mask: np.ndarray) -> list[int]:
    yy, xx = np.nonzero(mask)
    if not len(xx):
        raise NeedsReview("No visible alpha component")
    return [int(xx.min()), int(yy.min()), int(xx.max()) + 1, int(yy.max()) + 1]


def useful(im: Image.Image) -> dict:
    box = bounds(np.asarray(im)[:, :, 3] > ALPHA_FLOOR)
    return {"bbox": box, "width": box[2] - box[0], "height": box[3] - box[1]}


def font(size: int) -> ImageFont.ImageFont:
    for name in ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def validate_box(box: list, size: tuple[int, int], label: str) -> list[int]:
    if (not isinstance(box, list) or len(box) != 4 or
            any(not isinstance(v, int) or isinstance(v, bool) for v in box) or
            not (0 <= box[0] < box[2] <= size[0] and 0 <= box[1] < box[3] <= size[1])):
        raise NeedsReview(f"{label}: invalid integer crop inside source: {box}")
    return box


def clean_alpha(im: Image.Image, spec: dict, label: str, issues: list[str]) -> tuple[Image.Image, dict]:
    """Discard alpha <=8 and tiny isolated specks; never inspect pixel hue.

    The main connected body is retained. A substantial detached object requires
    explicit reviewed component selection, because it might be a wheel/mirror.
    Retained source RGBA pixels remain byte exact until the whole-image resize.
    """
    arr = np.array(im.convert("RGBA"), copy=True)
    original = arr.copy()
    low = (arr[:, :, 3] > 0) & (arr[:, :, 3] <= ALPHA_FLOOR)
    arr[low] = 0
    labels, count = ndimage.label(arr[:, :, 3] > ALPHA_FLOOR, np.ones((3, 3)))
    sizes = np.bincount(labels.ravel())
    if count == 0:
        raise NeedsReview(f"{label}: no truck/component in crop")
    main = int(np.argmax(sizes[1:]) + 1)
    tiny_limit = max(8, min(32, int(sizes[main] * 0.0001)))
    explicit = spec.get("keep_components")
    keep = {main} if explicit is None else set(explicit)
    if (any(not isinstance(item, int) or isinstance(item, bool) for item in keep) or
            main not in keep or any(item < 1 or item > count for item in keep)):
        raise NeedsReview(f"{label}: keep_components must include main body {main} and valid component IDs")
    reports = []
    for component in range(1, count + 1):
        area = int(sizes[component])
        decision = "keep-main-body" if component == main else "keep-reviewed" if component in keep else "remove-reviewed" if explicit is not None else "remove-tiny-isolated-speck"
        if component not in keep and area > tiny_limit and explicit is None:
            issues.append(f"{label}: detached component {component}, area {area}; review wheel/mirror/noise and select keep_components")
            decision = "ambiguous-needs-review"
        reports.append({"id": component, "area": area, "bbox": bounds(labels == component), "decision": decision})
    selected = np.isin(labels, list(keep))
    arr[~selected] = 0
    arr[arr[:, :, 3] == 0, :3] = 0
    assert np.array_equal(arr[selected], original[selected]), f"{label}: retained source pixel mutation"
    return Image.fromarray(arr), {"alphaFloorInclusive": ALPHA_FLOOR, "removedLowAlphaPixels": int(low.sum()),
                                 "removedDetachedVisiblePixels": int(((original[:, :, 3] > ALPHA_FLOOR) & ~selected).sum()),
                                 "tinyComponentAreaLimit": tiny_limit, "components": reports,
                                 "retainedSourcePixelsUnchanged": True, "usesColorDetector": False}


def auto_crops(sheet: Image.Image) -> tuple[list[list[int]], dict]:
    """Transparent row gutter, then whole connected truck recovery per row.

    Vertical equal-cell dividers select a body but never cut it. No recovery is
    accepted if two cells select the same body or substantial bodies overlap.
    """
    visible = np.asarray(sheet)[:, :, 3] > ALPHA_FLOOR
    projection = visible.sum(axis=1)
    ideal = sheet.height // 2
    radius = max(4, int(sheet.height * .12))
    clear = np.flatnonzero(projection[max(1, ideal - radius):min(sheet.height - 1, ideal + radius)] == 0) + max(1, ideal - radius)
    groups = np.split(clear, np.where(np.diff(clear) != 1)[0] + 1) if len(clear) else []
    groups = [group for group in groups if len(group) >= 3]
    if not groups:
        raise NeedsReview("No transparent horizontal gutter near the 3x2 row boundary; provide all six reviewed boxes")
    gutter = min(groups, key=lambda group: abs((int(group[0]) + int(group[-1])) / 2 - ideal))
    split = round((int(gutter[0]) + int(gutter[-1])) / 2)
    boxes, diagnostics = [], []
    for row, (y0, y1) in enumerate(((0, split), (split, sheet.height))):
        labels, count = ndimage.label(visible[y0:y1], np.ones((3, 3)))
        sizes = np.bincount(labels.ravel())
        selected = set()
        row_log = []
        if not count:
            raise NeedsReview(f"Row {row}: no truck components")
        for col in range(3):
            x0, x1 = round(col * sheet.width / 3), round((col + 1) * sheet.width / 3)
            overlap = np.bincount(labels[:, x0:x1].ravel(), minlength=count + 1)
            overlap[0] = 0
            order = np.argsort(overlap)[::-1]
            component = int(order[0])
            if not component or overlap[component] < 200 or component in selected:
                raise NeedsReview(f"Row {row}, column {col}: missing/duplicate truck; provide reviewed boxes")
            if len(order) > 1 and overlap[order[1]] > overlap[component] * .25:
                raise NeedsReview(f"Row {row}, column {col}: competing substantial bodies; provide reviewed boxes")
            selected.add(component)
            b = bounds(labels == component)
            box = [max(0, b[0] - MARGIN), max(y0, y0 + b[1] - MARGIN), min(sheet.width, b[2] + MARGIN), min(y1, y0 + b[3] + MARGIN)]
            boxes.append(box)
            row_log.append({"name": NAMES[row * 3 + col], "nominalCell": [x0, y0, x1, y1], "recoveredCrop": box,
                            "component": component, "area": int(sizes[component]), "method": "whole-row-component-recovery"})
        unassigned = [{"id": i, "area": int(sizes[i]), "bboxInRow": bounds(labels == i)} for i in range(1, count + 1) if i not in selected]
        if any(item["area"] > 32 for item in unassigned):
            raise NeedsReview(f"Row {row}: substantial unassigned component, possible wheel/mirror; provide reviewed crops/component selections")
        diagnostics.append({"row": row, "bodies": row_log, "unassigned": unassigned})
    return boxes, {"rowGutter": [int(gutter[0]), int(gutter[-1]) + 1], "rowSplit": split, "rows": diagnostics}


def anchor_info(im: Image.Image, spec: dict, label: str, issues: list[str]) -> dict:
    info = useful(im)
    b = info["bbox"]
    rear_axle, ground = spec.get("rear_axle"), spec.get("ground_y")
    if (not isinstance(rear_axle, list) or len(rear_axle) != 2 or
            any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) for v in rear_axle) or
            not isinstance(ground, (int, float)) or isinstance(ground, bool) or not math.isfinite(ground)):
        raise NeedsReview(f"{label}: reviewed rear_axle [x,y] and ground_y are required, crop-local")
    x, y = map(float, rear_axle)
    ground = float(ground)
    if not (b[0] < x < b[2] and b[1] < y < b[3] and y < ground <= im.height):
        issues.append(f"{label}: axle must be inside body extents and ground below axle, within crop")
    if not (b[3] - max(8, info["height"] * .04) <= ground <= b[3] + 8):
        issues.append(f"{label}: ground is far from visible tyre contact; review ground_y")
    if b[0] <= 1 or b[1] <= 1 or b[2] >= im.width - 1 or b[3] >= im.height - 1:
        issues.append(f"{label}: visible pixels touch crop edge {b}; review source clipping/crop")
    return {**info, "rearAxle": [x, y], "groundY": ground, "root": [x, ground],
            "method": "explicit-reviewed-rear-axle-and-ground", "axleHeightAboveGround": ground - y}


def normalized(im: Image.Image, info: dict, scale: float) -> Image.Image:
    x, ground = info["root"]
    inverse = (1 / scale, 0, x - SIZE[0] / (2 * scale), 0, 1 / scale, ground - GROUND / scale)
    # Premultiplied-alpha resampling avoids hidden RGB halos. No part transforms.
    result = im.convert("RGBa").transform(SIZE, Image.Transform.AFFINE, inverse, resample=Image.Resampling.BICUBIC).convert("RGBA")
    arr = np.array(result, copy=True)
    arr[arr[:, :, 3] == 0, :3] = 0
    return Image.fromarray(arr)


def verify(im: Image.Image, label: str, expected_size: tuple[int, int] = SIZE) -> dict:
    assert im.mode == "RGBA" and im.size == expected_size, f"{label}: wrong frame format"
    arr = np.asarray(im)
    b = bounds(arr[:, :, 3] > 0)
    assert b[0] > 0 and b[1] > 0 and b[2] < im.width and b[3] < im.height, f"{label}: output clipping {b}"
    assert np.any(arr[:, :, 3] == 0) and np.any(arr[:, :, 3] >= 128), f"{label}: alpha invalid"
    assert not np.any(arr[arr[:, :, 3] == 0, :3]), f"{label}: RGB under transparent pixels"
    return {"rgba": True, "size": list(im.size), "visibleBBox": b, "useful": useful(im),
            "marginsPx": [b[0], b[1], im.width - b[2], im.height - b[3]],
            "noOutputClipping": True, "zeroRgbUnderTransparentPixels": True}


def front_menu(front: Image.Image) -> tuple[Image.Image, dict]:
    b = useful(front)["bbox"]
    crop = front.crop(b)
    scale = min((SIZE[0] - 32) / crop.width, (SIZE[1] - 32) / crop.height)
    dimensions = (max(1, round(crop.width * scale)), max(1, round(crop.height * scale)))
    fitted = crop.convert("RGBa").resize(dimensions, Image.Resampling.LANCZOS).convert("RGBA")
    result = Image.new("RGBA", SIZE)
    result.alpha_composite(fitted, ((SIZE[0] - dimensions[0]) // 2, (SIZE[1] - dimensions[1]) // 2))
    return result, {"sourceUsefulBBox": b, "scale": scale, "aspectFit": True, "menuOnly": True,
                    "policy": "whole original front proposal cropped to alpha bounds then proportional aspect-fit; not a race pose"}


def crop_overlay(sheet: Image.Image, boxes: list[list[int]], specs: list[dict], output: Path) -> None:
    view = Image.new("RGBA", sheet.size, "#46505a")
    view.alpha_composite(sheet)
    draw = ImageDraw.Draw(view)
    for i, (box, spec) in enumerate(zip(boxes, specs)):
        draw.rectangle(box, outline="#ffe66d", width=3)
        draw.text((box[0] + 8, box[1] + 8), NAMES[i], fill="#ffe66d", font=font(24), stroke_width=2, stroke_fill="#111111")
        axle, ground = spec.get("rear_axle"), spec.get("ground_y")
        if isinstance(axle, list) and len(axle) == 2 and all(isinstance(v, (int, float)) for v in axle):
            x, y = axle[0] + box[0], axle[1] + box[1]
            draw.line((x - 12, y, x + 12, y), fill="#00e5ff", width=3)
            draw.line((x, y - 12, x, y + 12), fill="#00e5ff", width=3)
        if isinstance(ground, (int, float)):
            draw.line((box[0], box[1] + ground, box[2], box[1] + ground), fill="#ff6bab", width=2)
    view.thumbnail((1800, 1800), Image.Resampling.LANCZOS)
    view.convert("RGB").save(output)


def brake_geometry(frames: list[Image.Image], anchors: list[dict], scale: float) -> list[dict]:
    reports = []
    for normal, braking in ((0, 3), (1, 4), (2, 5)):
        a, b = np.asarray(frames[normal]), np.asarray(frames[braking])
        am, bm = a[:, :, 3] > 32, b[:, :, 3] > 32
        union, intersection = int((am | bm).sum()), int((am & bm).sum())
        ua, ub = useful(frames[normal]), useful(frames[braking])
        ratios = {axis: ub[axis] / ua[axis] for axis in ("width", "height")}
        axle_difference = abs(anchors[normal]["axleHeightAboveGround"] - anchors[braking]["axleHeightAboveGround"]) * scale
        iou = intersection / union
        flags = []
        if iou < .92:
            flags.append("material-silhouette-difference")
        if any(abs(value - 1) > .05 for value in ratios.values()):
            flags.append("useful-dimension-change-over-5-percent")
        if axle_difference > 6:
            flags.append("rear-axle-height-change-over-6-output-pixels")
        reports.append({"normal": NAMES[normal], "braking": NAMES[braking], "silhouetteIoUAlphaAbove32": iou,
                        "silhouetteXorPixels": int((am ^ bm).sum()), "rgbaChangedPixels": int(np.any(a != b, axis=2).sum()),
                        "brakeToNormalUsefulDimensionRatios": ratios, "rearAxleHeightDifferenceOutputPx": axle_difference,
                        "reviewFlags": flags, "sameScaleAndGround": True,
                        "interpretation": "distinct generated source drawings; changed pixels include geometry/color and are not claimed to be lamp-only"})
    return reports


def contacts(frames: list[Image.Image], color: str, name: str) -> Image.Image:
    tile_w, tile_h = 584, 568
    result = Image.new("RGB", (tile_w * 3, tile_h * 2), color)
    draw = ImageDraw.Draw(result)
    ink = "#ededed" if color != "#ffffff" else "#171a1d"
    for i, im in enumerate(frames):
        x, y = i % 3 * tile_w + 12, i // 3 * tile_h + 34
        result.paste(im, (x, y), im)
        draw.line((x, y + GROUND, x + SIZE[0], y + GROUND), fill="#2bc9cb", width=1)
        draw.text((x, y - 28), f"{LABELS[i]} · revisão pendente", fill=ink, font=font(18))
    return result


def comparison(frames: list[Image.Image], car: Image.Image, car_ground: float, display_multiplier: float) -> tuple[Image.Image, dict]:
    # An intended vehicle display factor at one shared world depth. The exact
    # same scalar multiplies x and y; it does not modify any exported race PNG.
    display_size = (math.ceil(SIZE[0] * display_multiplier), math.ceil(SIZE[1] * display_multiplier))
    truck = frames[0].convert("RGBa").transform(display_size, Image.Transform.AFFINE,
                 (1 / display_multiplier, 0, 0, 0, 1 / display_multiplier, 0), resample=Image.Resampling.BICUBIC).convert("RGBA")
    displayed_ground = GROUND * display_multiplier
    shared_ground = math.ceil(max(car_ground, displayed_ground)) + 24
    truck_y = round(shared_ground - displayed_ground)
    car_y = round(shared_ground - car_ground)
    width = 48 + car.width + 64 + truck.width
    height = max(car_y + car.height, truck_y + truck.height) + 64
    result = Image.new("RGBA", (width, height), "#343b42")
    result.alpha_composite(car, (24, car_y))
    result.alpha_composite(truck, (24 + car.width + 64, truck_y))
    draw = ImageDraw.Draw(result)
    draw.line((0, shared_ground, width, shared_ground), fill="#2bc9cb", width=2)
    draw.text((24, height - 48), "Mercedes · referência", fill="white", font=font(21))
    draw.text((24 + car.width + 64, height - 48), "Cavalo 4x2 · porte proposto (~1,4× largura)", fill="white", font=font(21))
    report = {"sameWorldDepth": True, "carDisplayMultiplier": 1, "truckUniformDisplayMultiplier": display_multiplier,
              "allTruckViewsUseSameProposedMultiplier": True, "truckAspectPreserved": True,
              "targetRearUsefulWidthRatio": PROPOSED_WIDTH_RATIO,
              "measuredDisplayedRearUsefulWidthRatio": useful(truck)["width"] / useful(car)["width"],
              "intendedRearUsefulHeightRatio": useful(frames[0])["height"] * display_multiplier / useful(car)["height"],
              "sharedGroundOnComparisonPx": shared_ground, "comparisonSize": list(result.size),
              "runtimeChangeApplied": False,
              "interpretation": "intended future vehicle display scale at equal world depth; Mercedes factor1 and one proposed uniform truck factor; not equal image pixel factors"}
    return result.convert("RGB"), report


def uri(im: Image.Image) -> str:
    data = io.BytesIO()
    im.save(data, format="PNG")
    return "data:image/png;base64," + base64.b64encode(data.getvalue()).decode("ascii")


def preview(frames: list[Image.Image], front: Image.Image, compare: Image.Image) -> str:
    payload = json.dumps({"frames": [uri(im) for im in frames], "front": uri(front), "comparison": uri(compare),
                          "labels": LABELS, "names": NAMES}, ensure_ascii=False).replace("<", "\\u003c")
    return """<!doctype html><html lang="pt-BR"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="data:,"><title>Caminhão FTW · revisão de arte</title>
<style>*{box-sizing:border-box}body{margin:0;padding:clamp(12px,3vw,32px);background:#171b20;color:#edf1f4;font:16px system-ui;line-height:1.5}main{max-width:1200px;margin:auto}h1{font-size:clamp(23px,4vw,34px)}button,select{font:inherit;padding:8px 12px;margin:3px;border:1px solid #77828d;border-radius:5px}button{cursor:pointer}button[aria-pressed=true]{background:#ae2130;color:#fff}.row{display:flex;gap:20px;flex-wrap:wrap}.card{flex:1 1 360px;min-width:0;margin:12px 0}.stage{width:100%;aspect-ratio:560/512;position:relative;overflow:hidden;background:#343b42}.stage:after{position:absolute;content:'';left:0;right:0;top:91.796875%;border-top:1px solid #2bc9cb;pointer-events:none}.stage img{width:100%;height:100%;object-fit:contain}.front:after{display:none}.white .stage{background:#fff}.black .stage{background:#000}.wide{display:block;width:100%;height:auto}figcaption,small{color:#c6cdd4}#status{min-height:3em}p{max-width:1000px}.warning{border-left:4px solid #e5b64e;padding-left:12px}a{color:#74d5df}</style>
<main><h1>Caminhão FTW · revisão de arte</h1><p class="warning">Proposta de cavalo simples 4x2, dois eixos e sem carreta. Todas as vistas, marcas, proporções e a frente de menu aguardam revisão do proprietário. A preparação técnica não concede aprovação à arte.</p>
<div id="views" role="group" aria-label="Selecionar vista"></div><div><label><input type="checkbox" id="brake"> Freio</label> <button id="cycle" aria-pressed="false">Alternar freio</button> <label>Fundo <select id="bg"><option value="asphalt">Asfalto</option><option value="white">Branco</option><option value="black">Preto</option></select></label></div><p id="status" role="status"></p>
<div class="row" id="cards"><figure class="card"><div class="stage"><img id="pose" alt="Vista traseira do caminhão"></div><figcaption>Vistas de corrida · mesma proporção entre os estados</figcaption></figure><figure class="card"><div class="stage front"><img id="front" alt="Proposta de frente para menu"></div><figcaption>Proposta de frente para o menu</figcaption></figure></div>
<h2>Prévia de porte à mesma distância</h2><p>Caminhão com largura traseira útil de aproximadamente 1,4× a Mercedes, com proporção preservada e a mesma linha de chão.</p><img id="comparison" class="wide" alt="Mercedes e caminhão lado a lado à mesma distância, com o porte maior proposto para o caminhão"><p>Este porte é uma proposta para futura integração ao jogo. As seis vistas do caminhão usam o mesmo fator de porte.</p>
<p><small>As marcas, os detalhes e as poses de freio seguem as imagens propostas e aguardam revisão. Os relatórios do pacote registram as diferenças de geometria entre os estados de freio.</small></p></main>
<script>const data=PAYLOAD;let view=0,brake=false,timer=null;const pose=document.getElementById('pose'),status=document.getElementById('status'),toggle=document.getElementById('brake'),cycle=document.getElementById('cycle');document.getElementById('front').src=data.front;document.getElementById('comparison').src=data.comparison;
function render(){const i=view+(brake?3:0);pose.src=data.frames[i];pose.alt=data.labels[i]+' do caminhão FTW';toggle.checked=brake;status.textContent=data.labels[i]+' · revisão do proprietário pendente';document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',Number(b.dataset.view)===view))}for(let i=0;i<3;i++){const b=document.createElement('button');b.dataset.view=i;b.textContent=data.labels[i];b.onclick=()=>{view=i;render()};document.getElementById('views').append(b)}toggle.onchange=()=>{brake=toggle.checked;render()};cycle.onclick=()=>{if(timer){clearInterval(timer);timer=null}else timer=setInterval(()=>{brake=!brake;render()},850);cycle.setAttribute('aria-pressed',!!timer);cycle.textContent=timer?'Parar alternância':'Alternar freio'};document.getElementById('bg').onchange=e=>{document.getElementById('cards').className='row '+e.target.value};document.addEventListener('visibilitychange',()=>{if(document.hidden&&timer){clearInterval(timer);timer=null;cycle.setAttribute('aria-pressed','false');cycle.textContent='Alternar freio'}});render();</script></html>""".replace("PAYLOAD", payload)


def readme() -> str:
    return """# Caminhão FTW — pacote de arte para revisão

Arte proposta: cavalo simples 4x2, dois eixos, sem carreta. Todas as imagens
aguardam revisão do proprietário. Nenhum arquivo representa master aprovado.
Conferir fotos e marcas do dono: cabine vermelha, Diabo Verde no para-brisa,
FTW nas portas; traseira convencional sem grafismos de patrocinador inventados.

## Reprodução portátil

Requer Python 3.10+, Pillow, NumPy e SciPy (`python -m pip install -r requirements.txt`).
Na pasta deste pacote, executar:

    python prepare.py --source sources/generated-vehicle-sheet.png --front sources/front-proposal.png --car-reference sources/mercedes-reference.png --anchors sources/reviewed-anchors.json --output ../rebuilt-truck-art

O destino deve estar vazio e fora das pastas dos originais. O script nunca escreve
no repositório do jogo. Origens e JSON revisado são copiados byte a byte. ZIPs usam
metadados fixos; versão das bibliotecas pode mudar pixels de reamostragem e hashes.

## Contrato e transformações

Seis PNG RGBA 560×512 na ordem rear, left, right, brake, left-brake, right-brake.
Atlas 3×2, 1680×1024; chão y=470, pivô (0.5,0.91796875). rear_axle e ground_y
do JSON são coordenadas locais ao crop [left,top,right,bottom), em pixels da fonte.
O x do eixo é centralizado em x=280; o ground_y é levado a y=470. O eixo em si
permanece acima do chão. Um único fator de escala vale para todas as seis vistas.
Não há ajuste de tamanho por pose, espelhamento, rotação, deformação, recoloração
ou síntese. A frente de menu usa apenas aspect-fit, separado da escala de corrida.

A limpeza remove alpha 1–8 e componentes isolados muito pequenos (até 8–32 pixels,
limite registrado por crop). Componentes maiores exigem seleção explícita revisada.
Não há detector de vermelho nem nenhuma chave por cor. Pixels retidos são exatos
antes da reamostragem com alpha pré-multiplicado. Não se apagam sombras por cor.

## Revisão de crops e âncoras

Sem --anchors o script propõe crops, salva source-crop-review.png e
proposed-anchors.json, e termina com status needs-review (exit 2). Preencher os
seis rear_axle [x,y] e ground_y, conferir todos os crops e hashes e definir
reviewed:true. Isso confirma somente pontos e limites técnicos, não aprova a arte.
Em caso de componentes desconectados, inserir keep_components:[IDs] no respectivo
crop; IDs/áreas/bboxes aparecem em qa-report.json. Todos os seis boxes explícitos
devem ser fornecidos juntos. A detecção automática só aceita um gutter horizontal
transparente e recupera o corpo inteiro na linha, inclusive cruzando divisores.
Ambiguidade de crops, partes ou âncoras interrompe a preparação, sem ZIP final.

## Escala e freio

O fator proposto de largura útil traseira é 1,4× o PNG da Mercedes. O encaixe
simultâneo das seis vistas reduz a razão nativa dentro do contrato 560×512;
valores solicitado/nativo e dimensões úteis estão em frames.json e qa-report.json.
A comparação principal mostra o PORTE FUTURO proposto na mesma profundidade:
Mercedes com fator de exibição1 e caminhão com um único multiplicador uniforme,
calculado como 1,4 × largura útil Mercedes / largura útil caminhão normalizado.
Esse fator preserva a proporção e vale igualmente para as seis vistas; não foi
incorporado aos PNG de corrida. Não é uma comparação de fatores de pixel iguais.
O runtime hoje força igual altura em igual profundidade: uma integração futura
precisa aplicar explicitamente esse fator de veículo; aumentar o canvas não basta.

Referência física apenas: ficha IVECO Chile 4x2, 6,252 m de comprimento, 2,55 m de
largura, 3,789 m de altura, entre-eixos 3,8 m. Esses números NÃO são medição do
caminhão FTW ou da Mercedes e não foram convertidos em unidades do jogo.

As poses de freio vêm da folha gerada, sem lâmpadas pintadas pelo script.
qa-report.json compara silhuetas, dimensões e altura do eixo de cada par, sinaliza
IoU <0,92, dimensão útil que varie >5% e eixo que varie >6 pixels. São critérios
de triagem, não aprovação visual. Não se afirma que somente lâmpadas mudaram.

## Arquivos

Abrir preview.html localmente: estados, freio e fundos; tudo está embutido.
contact-sheet-{black,white,asphalt}.png e same-depth-comparison.png são revisão
estática. source-crop-review.png mostra crops/âncoras. frames.json contém
proveniência e política; qa-report.json contém verificações e limites. SHA256SUMS
cobre o conteúdo do pacote; truck-vehicle-art.zip.sha256 cobre o ZIP separadamente.
Não há publicação, integração, alteração de runtime ou aprovação implícita.
"""


def archive_files(output: Path) -> None:
    files = sorted(path for path in output.rglob("*") if path.is_file() and path.name not in
                   {"truck-vehicle-art.zip", "truck-vehicle-art.zip.sha256", "SHA256SUMS"})
    (output / "SHA256SUMS").write_text("".join(f"{sha(path)}  {path.relative_to(output).as_posix()}\n" for path in files), encoding="utf-8")
    archive = output / "truck-vehicle-art.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for path in files + [output / "SHA256SUMS"]:
            entry = zipfile.ZipInfo(path.relative_to(output).as_posix(), (2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = (0o100644 << 16)
            z.writestr(entry, path.read_bytes())
    (output / "truck-vehicle-art.zip.sha256").write_text(f"{sha(archive)}  {archive.name}\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", type=Path, required=True, help="authentic 3x2 sheet: rear,left,right / brake,left-brake,right-brake")
    p.add_argument("--front", type=Path, required=True, help="front/menu proposal PNG")
    p.add_argument("--car-reference", type=Path, required=True, help="native Mercedes straight-rear PNG, 512x512, ground470")
    p.add_argument("--anchors", type=Path, help="reviewed crop-local rear_axle/ground_y JSON")
    p.add_argument("--output", type=Path, required=True, help="empty standalone output directory")
    args = p.parse_args()
    inputs = {"source": args.source, "front": args.front, "carReference": args.car_reference}
    if args.anchors:
        inputs["anchors"] = args.anchors
    for key, path in inputs.items():
        if not path.is_file():
            p.error(f"Missing {key}: {path}")
    output = args.output.resolve()
    # Refuse destructive overwrite, stale exports, repo changes and recursive copies.
    if any(path.resolve().is_relative_to(output) for path in inputs.values()):
        p.error("output must not contain any original input")
    if output == Path.cwd().resolve() or (output.exists() and any(output.iterdir())):
        p.error("--output must be a new or empty directory (use a fresh directory for each review)")
    output.mkdir(parents=True, exist_ok=True)
    before = {key: sha(path) for key, path in inputs.items()}
    issues: list[str] = []
    qa = {"schemaVersion": 1, "status": "in-progress", "issues": issues, "sourceHashes": before,
          "preparationScriptSha256": sha(Path(__file__)), "approval": "all-vehicle-art-pending-owner-review",
          "software": {"python": platform.python_version(), "Pillow": PIL.__version__, "numpy": np.__version__, "scipy": scipy.__version__}}
    try:
        opened = [Image.open(path) for path in (args.source, args.front, args.car_reference)]
        if any(im.format != "PNG" for im in opened):
            raise NeedsReview("The sheet, front and Mercedes reference must be original PNG files")
        sheet, front, car = [im.convert("RGBA") for im in opened]
        if car.size != (512, 512):
            raise NeedsReview("Mercedes reference must use the known 512x512 / ground470 contract; review a different reference explicitly")
        if any(not np.any(np.asarray(im)[:, :, 3] == 0) for im in (sheet, front, car)):
            raise NeedsReview("Source sheet, front and Mercedes must already have true alpha; no background/color keying is permitted")
        overrides = json.loads(args.anchors.read_text(encoding="utf-8")) if args.anchors else {}
        if not isinstance(overrides, dict) or not isinstance(overrides.get("front", {}), dict):
            raise NeedsReview("anchors JSON and its optional front entry must be objects")
        for field, source_key in (("sourceSha256", "source"), ("frontSha256", "front"), ("carReferenceSha256", "carReference")):
            if overrides.get("reviewed") is True and overrides.get(field) != before[source_key]:
                raise NeedsReview(f"Reviewed {field} does not match the exact source")
        specs = overrides.get("cells", [{} for _ in NAMES])
        if not isinstance(specs, list) or len(specs) != 6 or any(not isinstance(spec, dict) for spec in specs):
            raise NeedsReview("anchors.cells must contain exactly six objects in frame order")
        if any("name" in spec and spec["name"] != name for spec, name in zip(specs, NAMES)):
            raise NeedsReview("anchors.cells names/order differ from rear,left,right,brake,left-brake,right-brake")
        explicit = all("box" in spec for spec in specs)
        if any("box" in spec for spec in specs) and not explicit:
            raise NeedsReview("Provide reviewed boxes for all six cells, or none")
        if explicit:
            boxes = [validate_box(spec["box"], sheet.size, name) for spec, name in zip(specs, NAMES)]
            grid_report = {"method": "explicit-reviewed-boxes"}
        else:
            boxes, grid_report = auto_crops(sheet)
        for i, a in enumerate(boxes):
            for b in boxes[i + 1:]:
                if min(a[2], b[2]) > max(a[0], b[0]) and min(a[3], b[3]) > max(a[1], b[1]):
                    raise NeedsReview("Source boxes overlap; review the six authentic cell boundaries")
        qa["grid"] = {"layout": [3, 2], "sourceSize": list(sheet.size), "boxes": boxes, **grid_report}
        crop_overlay(sheet, boxes, specs, output / "source-crop-review.png")
        proposal = {"schemaVersion": 1, "reviewed": False, "sourceSha256": before["source"], "frontSha256": before["front"],
                    "carReferenceSha256": before["carReference"],
                    "coordinatePolicy": "box absolute source pixels [left,top,right,bottom); rear_axle/ground_y crop-local; review technical anchors only, not artwork approval",
                    "cells": [{"name": name, "box": box, "rear_axle": spec.get("rear_axle"), "ground_y": spec.get("ground_y"),
                               **({"keep_components": spec["keep_components"]} if "keep_components" in spec else {})} for name, box, spec in zip(NAMES, boxes, specs)],
                    "front": overrides.get("front", {})}
        if overrides.get("reviewed") is not True:
            write_json(output / "proposed-anchors.json", proposal)
        # Cleanup diagnostics are useful even when explicit anchors are pending.
        poses, anchors, reports = [], [], []
        for name, box, spec in zip(NAMES, boxes, specs):
            pose, report = clean_alpha(sheet.crop(box), spec, name, issues)
            poses.append(pose)
            reports.append({"name": name, "sourceCrop": box, "cleanup": report, "sourceUseful": useful(pose)})
        qa["poses"] = reports
        if overrides.get("reviewed") is not True:
            raise NeedsReview("Review crops and fill rear_axle/ground_y in proposed-anchors.json, set reviewed:true, then rerun to a fresh output")
        for pose, spec, report, name in zip(poses, specs, reports, NAMES):
            info = anchor_info(pose, spec, name, issues)
            anchors.append(info)
            report["anchor"] = info
        front_spec = overrides.get("front", {})
        front_box = validate_box(front_spec.get("box", [0, 0, front.width, front.height]), front.size, "front")
        front_clean, front_clean_report = clean_alpha(front.crop(front_box), front_spec, "front", issues)
        qa["front"] = {"sourceCrop": front_box, "cleanup": front_clean_report}
        fb = useful(front_clean)["bbox"]
        if fb[0] <= 1 or fb[1] <= 1 or fb[2] >= front_clean.width - 1 or fb[3] >= front_clean.height - 1:
            issues.append(f"front: visible source pixels touch crop edge {fb}; review original clipping/crop")
        if issues:
            raise NeedsReview("Ambiguous source components, crop boundaries or rear-axle/ground anchors")
        car_useful = useful(car)
        desired = car_useful["width"] * PROPOSED_WIDTH_RATIO / anchors[0]["width"]
        constraints = []
        for info in anchors:
            left, top, right, bottom = info["bbox"]
            rx, ry = info["root"]
            constraints.extend(((SIZE[0] / 2 - MARGIN) / max(1, rx - left),
                                (SIZE[0] / 2 - MARGIN) / max(1, right - rx),
                                (GROUND - MARGIN) / max(1, ry - top)))
            if bottom > ry:
                constraints.append((SIZE[1] - MARGIN - GROUND) / (bottom - ry))
        scale = min([desired] + constraints)
        frames = [normalized(pose, info, scale) for pose, info in zip(poses, anchors)]
        frame_qa = {name: verify(im, name) for name, im in zip(NAMES, frames)}
        scale_report = {"proposedRearUsefulWidthRatio": PROPOSED_WIDTH_RATIO, "commonSheetScale": scale,
                        "desiredSheetScale": desired, "commonFitLimitedRequestedRatio": scale < desired - 1e-9,
                        "allSixTransformsShareScale": True, "independentPoseFit": False,
                        "carReferenceUseful": car_useful, "carReferenceNativeSize": list(car.size), "carReferenceGround": CAR_GROUND,
                        "truckRearUseful": useful(frames[0]),
                        "actualRearUsefulWidthRatio": useful(frames[0])["width"] / car_useful["width"],
                        "actualRearUsefulHeightRatio": useful(frames[0])["height"] / car_useful["height"],
                        "nativeNormalizedRearUsefulWidthRatio": useful(frames[0])["width"] / car_useful["width"],
                        "nativeNormalizedRearUsefulHeightRatio": useful(frames[0])["height"] / car_useful["height"],
                        "futureUniformDisplayMultiplierForProposedWidth": PROPOSED_WIDTH_RATIO / (useful(frames[0])["width"] / car_useful["width"]),
                        "runtimeIntegrationRequired": "current renderer sets equal display height at equal depth; future integration needs an explicit truck vehicle scale; native canvas size alone does not set physical scale",
                        "physicalBenchmark": BENCHMARK}
        qa["scale"] = scale_report
        qa["brakePairGeometry"] = brake_geometry(frames, anchors, scale)
        qa["reviewFlags"] = [f'{pair["normal"]}/{pair["braking"]}: {flag}' for pair in qa["brakePairGeometry"] for flag in pair["reviewFlags"]]
        front_output, front_report = front_menu(front_clean)
        qa["front"]["menuFit"] = front_report
        frame_qa["front-menu"] = verify(front_output, "front-menu")
        qa["frames"] = frame_qa
        for name, im in zip(NAMES, frames):
            im.save(output / f"{name}.png", optimize=True)
        front_output.save(output / "front-menu.png", optimize=True)
        atlas = Image.new("RGBA", (1680, 1024))
        atlas_frames = {}
        for i, (name, im) in enumerate(zip(NAMES, frames)):
            x, y = i % 3 * SIZE[0], i // 3 * SIZE[1]
            atlas.alpha_composite(im, (x, y))
            atlas_frames[f"{name}.png"] = {"frame": {"x": x, "y": y, "w": SIZE[0], "h": SIZE[1]},
                                             "rotated": False, "trimmed": False, "spriteSourceSize": {"x": 0, "y": 0, "w": SIZE[0], "h": SIZE[1]},
                                             "sourceSize": {"w": SIZE[0], "h": SIZE[1]}, "pivot": {"x": PIVOT[0], "y": PIVOT[1]}}
        atlas.save(output / "truck-atlas.png", optimize=True)
        loaded_atlas = Image.open(output / "truck-atlas.png").convert("RGBA")
        for i, frame in enumerate(frames):
            x, y = i % 3 * SIZE[0], i // 3 * SIZE[1]
            assert loaded_atlas.crop((x, y, x + SIZE[0], y + SIZE[1])).tobytes() == frame.tobytes(), "Atlas frame pixel mismatch"
        write_json(output / "truck-atlas.json", {"frames": atlas_frames, "meta": {"image": "truck-atlas.png", "format": "RGBA8888", "size": {"w": 1680, "h": 1024}, "scale": "1"}})
        for name, color in (("black", "#000000"), ("white", "#ffffff"), ("asphalt", "#343b42")):
            contacts(frames, color, name).save(output / f"contact-sheet-{name}.png", optimize=True)
        compare, comparison_report = comparison(frames, car, CAR_GROUND, scale_report["futureUniformDisplayMultiplierForProposedWidth"])
        scale_report["intendedDisplayComparison"] = comparison_report
        qa["sameDepthComparison"] = comparison_report
        compare.save(output / "same-depth-comparison.png", optimize=True)
        (output / "preview.html").write_text(preview(frames, front_output, compare), encoding="utf-8")
        sources = output / "sources"
        sources.mkdir()
        source_names = {"source": "generated-vehicle-sheet.png", "front": "front-proposal.png", "carReference": "mercedes-reference.png", "anchors": "reviewed-anchors.json"}
        for key, path in inputs.items():
            shutil.copyfile(path, sources / source_names[key])
            assert sha(sources / source_names[key]) == before[key], f"{key}: source copy not byte exact"
        shutil.copyfile(Path(__file__), output / "prepare.py")
        (output / "requirements.txt").write_text(f"Pillow=={PIL.__version__}\nnumpy=={np.__version__}\nscipy=={scipy.__version__}\n", encoding="utf-8")
        (output / "README.md").write_text(readme(), encoding="utf-8")
        write_json(output / "frames.json", {"schemaVersion": 1, "vehicleId": "ftw-truck-proposal", "approval": "all-vehicle-art-pending-owner-review",
                   "configurationProposal": {"type": "simple-tractor", "axles": 2, "drive": "4x2", "trailer": False},
                   "ownerReferencePriorities": ["owner photos and marks dominate", "red cab", "Diabo Verde windshield", "FTW doors", "plain conventional rear; no invented rear sponsor graphics"],
                   "frameSize": list(SIZE), "ground": GROUND, "pivot": PIVOT, "frameOrder": NAMES, "sheetGrid": [3, 2], "atlasSize": [1680, 1024],
                   "scale": scale_report, "sources": {key: {"file": f"sources/{source_names[key]}", "sha256": before[key]} for key in inputs},
                   "assets": [{"file": f"{name}.png", "sha256": sha(output / f"{name}.png"), "source": "sources/generated-vehicle-sheet.png",
                               "sourceCrop": box, "sourceAnchor": info, "scale": scale, "ground": GROUND, "pivot": PIVOT,
                               "outputRearAxle": [SIZE[0] / 2, GROUND - info["axleHeightAboveGround"] * scale],
                               "useful": useful(im), "approval": "pending-owner-review"} for name, box, info, im in zip(NAMES, boxes, anchors, frames)],
                   "frontMenu": {"file": "front-menu.png", "source": "sources/front-proposal.png", "sourceCrop": front_box, **front_report, "approval": "pending-owner-review"},
                   "transformPolicy": "whole authentic generated views; one common race scale; reviewed rear-axle/ground translations; no rotation, mirroring, part manipulation, recoloring or art synthesis",
                   "brakePairGeometry": qa["brakePairGeometry"], "visualReviewRequired": ["tractor configuration and actual two-axle geometry", "owner identity, marks and text", "plain rear without invented sponsors", "all six source poses", "brake geometry flags", "proposed same-depth car/truck scale"]})
        assert {key: sha(path) for key, path in inputs.items()} == before, "Original input changed"
        qa["status"] = "technical-checks-passed; all-vehicle-art-pending-owner-review"
        qa["assertions"] = {"sixRgba560x512RaceFrames": True, "trueAlpha": True, "noOutputClipping": True,
                            "ground470PivotConsistent": True, "oneSharedRaceScale": True, "reviewedRearAxleGroundAnchors": True,
                            "atlas1680x1024PixelExact": True, "frontAspectFitOnly": True, "noColorKeyOrRedDetector": True,
                            "noMirroringRotationRecolorOrSynthesis": True, "sourceCopiesByteExact": True,
                            "originalInputsUnchanged": True, "standalonePreviewEmbedded": True, "noOwnerApprovalClaimed": True}
        qa["visualLimitations"] = "Alpha/geometry checks do not establish identity, actual axle count, wording, authentic rear graphics or owner approval. Brake pairs are independent drawings and are not claimed to differ only in lamps."
        qa["payloadHashes"] = {path.relative_to(output).as_posix(): sha(path) for path in sorted(output.rglob("*")) if path.is_file()}
        write_json(output / "qa-report.json", qa)
        archive_files(output)
        print(json.dumps({"status": qa["status"], "output": str(output), "commonSheetScale": scale,
                          "rearUsefulWidthRatio": scale_report["actualRearUsefulWidthRatio"], "reviewFlags": qa["reviewFlags"],
                          "zipSha256": sha(output / "truck-vehicle-art.zip")}, ensure_ascii=False))
        return 0
    except (NeedsReview, AssertionError, ValueError, TypeError, KeyError, IndexError) as error:
        qa["status"] = "needs-review"
        qa["error"] = str(error)
        qa["originalInputsUnchanged"] = {key: sha(path) for key, path in inputs.items()} == before
        write_json(output / "qa-report.json", qa)
        print(json.dumps({"status": "needs-review", "error": str(error), "issues": issues, "report": str(output / "qa-report.json")}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

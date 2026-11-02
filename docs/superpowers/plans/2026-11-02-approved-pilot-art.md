# Approved pilot art implementation plan

> For agentic workers: execute the approved visual work in parallel where paths are independent; preserve the existing V4 architecture.

**Goal:** integrate the owner's approved Daniel/Felipe likeness and body/podium sheets, plus the cover only after its separate visual approval.

**Architecture:** preserve Phaser, simulation, NPCs and the existing six-stage podium. Normalize the two approved 4×2 source sheets at a common scale into the existing256×512 runtime frames; add dedicated portrait/neutral/helmet assets. Compose the cover in DOM/CSS using the approved portraits/cars and byte-identical official logo PNGs.

**Tech stack:** existing JavaScript ES modules, Phaser3.90, DOM/CSS and the existing Python/Pillow asset pipeline.

**Spec:** docs/12_V4_STORYBOARD_E_DIRECAO_VISUAL.md and owner's latest explicit approvals. Faces and shown sprite sheets approved; the separately shown cover was pending at plan creation and later explicitly approved (“Aprovar a capa”).

## Constraints and review focus
- Preserve all previous Pages versions, only distribute to teste-v4/; continue dedicated V4 branch.
- Keep original generated sources and provenance; remove low-alpha edge residue without redesigning approved faces.
- Keep foot ground500/512, common physical scale, unclipped hands/trophies/bottles and genuine six distinct poses per official winner.
- Logos remain byte-identical official PNGs; no reproduction by a generator.
- Functional PRESS START, keyboard, audio unlock, reduced motion and mobile safe layout remain intact.
- Cover must receive explicit visual approval before integration; approval of sprites is already sufficient for their preparation.

## Task1 — Approved pilot assets
- [x] Preserve approved sources and normalize cap/helmet body views and12podium frames; keep every NPC asset unchanged.
- [x] Verify real alpha, complete bounds, common scale/ground, source/frame hashes and six-stage mapping.
- [x] Replace low-detail menu faces with dedicated approved portrait assets, update approval copy/provenance accurately.

## Task2 — Cover after approval
- [x] Record cover approval when it arrives; port the review composition to responsive production DOM/CSS with functional title controls.
- [x] Verify both official logo hashes, clear faces/cars, readable title/CTA and mobile/portrait/reduced-motion behavior.

## Task3 — Verification and isolated publication
- [x] Run all45Node tests, module syntax, full asset audit and real browser flow through both official winners' podiums and a natural complete race.
- [x] Commit source, copy only V4 distribution, compare46pre-existing Pages files and verify the packaged browser flow.
- [x] Publish with guarded refs under existing public code/assets authorization; verify HTTPS in independent Chromium and inspect artifacts/screenshots before delivery.

Final evidence: public run41497991461 success, artifact13168495437 downloaded/hash-verified; published cover/selection screenshots inspected. Source and Pages hashes recorded in APPROVED_PILOT_ART_QA.md.

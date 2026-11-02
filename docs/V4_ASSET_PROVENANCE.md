# V4 renderer/asset derivation — 01/11/2026

## Estado de aprovação
**Prévia funcional incompleta artisticamente.** Nenhuma ilustração nova foi declarada fiel/aprovada. Revisão humana de rostos, macacões, detalhes dos patrocinadores, NPCs e enquadramentos permanece necessária. O storyboard autoriza a estrutura, não cada frame. Fotos e logos oficiais originais estão preservados; FTW e Diabo Verde distribuídos são byte a byte iguais aos PNGs fornecidos.

## Pilotos e comemoração
`assets/previews/v4/podium-generated-source.png` preserva a nova sheet gerada por image_gen usando a foto canônica `referencias/pilotos-e-carros/dupla-canonica-bones-e-macacoes.jpg`. São seis poses completas de Daniel e seis de Felipe: entrada, taça, erguer, abrir garrafa, spray e final. A edição seguinte removeu o fundo e o spray incorporado; a camada de gotas é independente. Não foram girados membros recortados. Há diferenças de feições/lettering em relação à foto: não são identidade final validada; alguns detalhes de taça têm enquadramento limitado na geração.

`game/scripts/prepare-v4-podium.py` registra os crops reais, limpa alpha baixo, aplica escala comum de 0,9 e alinha os pés em y500, canvas256×512 para oficiais e320×512 para NPCs. NPCs são figuras fictícias detalhadas, com capacete fechado, sem rosto real e sem patrocínio. A sheet neutra gerada em assets/previews/v4/npc-podium-generated-source.png contém seis poses integrais; os tons neutros de roupa/capacete foram derivados em azul, amarelo, roxo e prata, preservando taça dourada e garrafa verde. Não há transformação de membros recortados. Total36PNG de corpo inteiro, seis para cada vencedor. `game/assets/v4/podium/frames.json` registra fonte/hash/pivô/timing por frame. As taças e garrafas são parte das poses de mão; gotas/espuma ficam em sprite SVG separado e24instâncias limitadas no DOM. O título e os cards usam a pose inicial 2D, claramente em revisão.

`assets/sprites/V4_MANIFEST.json` inventaria121 arquivos com SHA256, tamanho e classificação. Inclui referências oficiais, pranchas preliminares e rejeitadas (não distribuídas). `game/scripts/audit-v4-assets.py` valida hashes,36frames distintos e transparência real. Os halos de RGB em alpha0 da geração não são pixels visíveis; pixels com alpha<40 foram removidos.

## Dependências locais e licenças
`game/assets/legacy/` contém somente os recursos V3 ainda usados (logos, lata, duas traseiras e Phaser), recuperados do artifact oficial de Pages no commit18d2ef4. Todos mantêm os bytes anteriores. Phaser local observado em runtime:3.90.0, MIT; licença distribuída em `LICENSE-PHASER.md`. Fallback CDN:3.80.1, usado apenas se o módulo local falhar. Nenhum recurso protegido de jogos comerciais foi incorporado.

Source checkout: `f6f6f83c40a3db3cc83cde4fc12702a1a94cc6e1`, `codex/ftw-race-v4-arcade`. All source photos/previews remained byte-identical. No third-party code, sprites, music or fonts were incorporated.

## Real distributed sprites

`game/assets/v4/render-assets.json` records every crop, original SHA256, resulting SHA256, dimensions, alpha counts and anchor. `game/scripts/prepare-v4-render-assets.py` reproduces all assets non-destructively using Pillow. `game/scripts/verify-v4-render-assets.py` independently checks actual distributed bytes, PNG dimensions, useful alpha and the sixteen non-empty animation frames.

| Family | Source | Transformation/use | Approval |
|---|---|---|---|
| Official cars | `assets/previews/{daniel,felipe}/carro-traseira.png` | Three **distinct** actual views each, separated at genuine transparent column gaps; no mirrored logos or numbers. Alpha<40 removed, >240 opaque; crop to useful bounds, resize within 470×330, center on 512×512 canvas, common ground y=470. Rear/left/right selected from steering. | Existing preliminary illustration derivatives; fidelity remains subject to human review. |
| Cascavel vegetation/barriers | `assets/previews/cascavel/vegetacao-e-barreiras.png` | Separate tree, bush, forest strip, fence, tire and concrete barrier PNGs; alpha cleaned, useful bounds, each anchored at foot/base. Trees/bushes/fences/tires placed deterministically outside asphalt. Forest/barrier extracted but not placed to avoid visual clutter. | Existing supplied concepts, derived art awaiting review. |
| Cascavel boxes/signage | `assets/previews/cascavel/boxes-e-sinalizacao.png` | Separate long pit building, stand, tent and 100/50 boards. Pit and stand integrated at start area; boards before a fixed circuit section, geometric widths keep entire building outside asphalt. Tent extracted but not placed. | Existing supplied concepts, derived art awaiting review. |
| Horizon | `assets/previews/cascavel/curvas-e-mata.png` | Crop [0,0,1672,190], sky and distant circuit context only, no contact sheet, road geometry still entirely from verified simulation. | Preliminary scene illustration. |
| Title background | `assets/previews/cascavel/reta-principal.png` | Complete single scene crop [0,0,1672,941], resized within1280×720 to `game/assets/v4/cascavel/title-straight.png`. It is a decorative title backdrop, never a terrain texture or circuit replacement. | Preliminary scene illustration. |
| FX | `assets/previews/fx/estudo-fumaca-poeira-nitro-impacto.png` | Four rows × four columns extracted to128×128 cells in512×512 sheet. Low-alpha halos removed. Rows smoke/dust/nitro/spark. Four real frames per effect, bounded lifetime and fade, stable per-cell ground y=110. Nitro effect rotated90° as flame orientation (no car or human limb deformation). | Derived preliminary FX, visually inspected over gray. |
| Four NPCs | Original SVG redraw in `game/cars/npc-{blue,yellow,purple,silver}.svg` | Shared low/wide A45 rear chassis geometry informed by supplied central rear car: same roof/windshield proportions, large rear wing, pointed tail lamps, black wheels, diffuser/twin exhaust. Blue/yellow/purple/silver plain colors, neutral31/34/38/41. No FTW, Diabo Verde, Mercedes badge or custom sponsor marks.512×512, ground y470 to align official sprites. SHA metadata `game/assets/v4/cars/npc-cars.json`. | **New original vector art, pending owner review; not an official validated Mercedes representation.** |

## Render rules and checks

- Original road projection, Cascavel geometry,18-unit road width and simulation preserved.
- Scenery and rivals use the same projected distance depth. Objects beyond the actually visible projected segment range are hidden; objects never wrap onto distant backwards bends.
- Buildings are offset by their half-width plus road clearance. Trees are outside asphalt. Car origins share y470/512; official views never mirror text.
- FX use a48-image reusable pool, reduced to18 in low quality/reduced motion. Pause freezes position and frame time; new race resets; finish clears; reduced motion disables dust/smoke/shake.
- Screenshots of extracted assets over gray saved in `/workspace/work/v4-render-contact.png`; visually inspected for cropped numbers, noisy transparency and baseline. That contact sheet is QA evidence, not distributed as a sprite.
- `node --test --test-isolation=none game/tests/v4-effects.test.js`:3/3 PASS after two meaningful RED→GREEN stages (missing effects module; missing V4 preload sprites). Tests cover pool capacity/recycling, freeze/reset and distributed preload file existence.
- Full suites executed after integration:40/40 assertions PASS (`node --test --test-isolation=none tests/*.test.js` in game). Concurrent other tasks may add further cases; root must rerun final suite.
- `node --check game/src/render.js`: PASS. Asset verification:20 PNG files, SHA256/dimensions/actual alpha and16FX frames PASS.
- Full browser/phone rendering, visual owner approval and Android physical device: delegated to root QA; not claimed by this asset pass.

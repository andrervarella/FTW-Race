# V4 renderer/asset derivation — 01/11/2026

## Cavalo mecânico simples — 03/11/2026
- Interpretação4×2 comunicada a partir de “E um cavalo mecânico simples”. Proposta frontal e prancha de seis vistas preservadas em `assets/previews/v4/truck-vehicle/`, com hashes e condição de revisão em `sources.json`. Ano/versão exatos não confirmados; fotos do proprietário orientam vermelho/Diabo Verde no para-brisa/FTW nas portas e fontes públicas documentam estrutura convencional, sem carreta.
- Derivados em `assets/sprites/v4/truck-vehicle/`: seis PNGs560×512, atlas1680×1024, chão470/pivô comum, frente/menu, contatos e comparação de porte. Recortes/âncoras técnicas revisados, escala comum e alpha residual removido sem selecionar cor vermelha. Nenhum espelhamento, rotação ou reconstrução procedural de carroceria.
- Freios são desenhos gerados quase idênticos; diferenças/Ious registrados, não se afirma diferença só nas lanternas. Porte futuro calibrado por fator uniforme1,71682para largura comparada1,4015×Mercedes; normalização do PNG é separada da escala do jogo. Nenhuma mudança ao runtime. QA e pacote em TRUCK_VEHICLE_SPRITES.md; toda arte do caminhão aguarda revisão humana.

## Novo motorista — 03/11/2026
- Base final aprovada explicitamente com “Ótimo. Essa última ficou perfeita. Ela é a referência.”; PNG original preservado sem alteração em `assets/previews/v4/truck-driver/master-approved.png`.
- A prancha `podium-generated-source.png` contém seis poses reais geradas numa única edição da base: entrada, receber/erguer taça, abrir/borrifar garrafa e comemorar. Novas poses aguardam revisão humana; não são membros recortados/rotacionados. Boné vermelho Mercedes e polo FTW nova em todas.
- Neutra/retrato derivados tecnicamente da base; atlas/quadros e metadata separados em `assets/sprites/v4/truck-driver/`. Fontes, hashes, aprovação e limitações em `sources.json` e `docs/TRUCK_DRIVER_SPRITES.md`. Nenhuma alteração à arte distribuída dos pilotos existentes ou ao runtime.

## Atualização aprovada de pilotos e capa — 02/11/2026
- Âncoras de rosto corrigidas a partir dos closes enviados e aprovadas com “Aprovado”. As primeiras pranchas rejeitadas ficaram fora do runtime. Corpo inteiro/boné/capacete e seis poses de comemoração por piloto foram aprovados posteriormente; capa aprovada separadamente pela resposta “Aprovar a capa”.
- Cinco PNGs originais gerados preservados em `assets/previews/v4/approved-pilots/`, com hashes e fontes em `sources.json`. Dezesseis recortes úteis (oito por piloto), escala única0,70 e pés em y500 de256×512; os12quadros de pódio substituem apenas Daniel/Felipe. Alpha baixo/partículas de borda removidos; nenhum redesenho de rosto, deformação ou rotação de membros. O cotovelo final do Felipe ultrapassa a célula nominal; seleção por componente conectado recupera223pixels e exclui esses pixels da pose vizinha.
- `drivers/approved-pilots.json`, `podium/frames.json` e `title/approval.json` registram fonte/crop/escala/pivô/aceite. O verificador confirma24arquivos/records NPC idênticos à versão anterior.
- Capa em camadas DOM/CSS: rostos aprovados, vistas frontais canônicas dos carros, cenário Cascavel ilustrado e logos PNG oficiais aplicados diretamente com recorte de exibição CSS. Sem espelhamento ou nova tipografia de logo gerada. Botão PRESS START permanece funcional e em tamanho físico confortável no celular; ajuste proporcional preserva rostos e carros.
- Para a web, retratos/carros usam redução proporcional e WebP sem perdas, com igualdade exata dos pixels resultantes verificada. Só o cenário usa WebP92; PNGs originais continuam preservados. Cinco camadas somam3.255.096bytes em vez de10.088.828bytes. Logos continuam seus arquivos PNG originais.
- Pipeline ativo: `prepare-approved-pilots.py`, `verify-approved-pilots.py`, `encode-title-web.py`; o gerador antigo de pódio interrompe antes de sobrescrever a arte aprovada.


## Estado de aprovação
**Aprovação atual:** o proprietário aprovou explicitamente os novos rostos de Daniel/Felipe, as duas pranchas completas com oito poses por piloto e a nova capa. Arte dos NPCs e demais derivados anteriores mantêm seu estado de revisão. Fotos originais e PNGs oficiais FTW/Diabo Verde permanecem preservados. Ver APPROVED_PILOT_ART_QA.md.

## Pilotos e comemoração — histórico substituído nos oficiais
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
| Former title backdrop (retired) | `assets/previews/cascavel/reta-principal.png` | Complete single scene crop [0,0,1672,941], resized within1280×720 to `game/assets/v4/cascavel/title-straight.png`. It is a decorative title backdrop, never a terrain texture or circuit replacement. | Preliminary scene illustration. |
| FX | `assets/previews/fx/estudo-fumaca-poeira-nitro-impacto.png` | Four rows × four columns extracted to128×128 cells in512×512 sheet. Low-alpha halos removed. Rows smoke/dust/nitro/spark. Four real frames per effect, bounded lifetime and fade, stable per-cell ground y=110. Nitro effect rotated90° as flame orientation (no car or human limb deformation). | Derived preliminary FX, visually inspected over gray. |
| Four NPCs | New raster derivation from owner’s four-car reference; raw sheet preserved,4six-frame PNG atlases and24individual frames. | Runtime uses `game/assets/v4/cars/npc-raster/`, actual left/right/brake states, shared scale and rear-axle pivot. Original SVG redraws retained as retired history only. See [NPC_REFERENCE_ASSETS.md](NPC_REFERENCE_ASSETS.md) for provenance and reproducible preparation. | **Reference-derived art, new angles pending owner review.** |

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


## 03/11/2026 — pedido de integração de Marquinhos

O proprietário nomeou o novo piloto **Marquinhos**, respondeu “Otimo” ao material apresentado e pediu “aplicar tudo isso no game”, incluindo capa e personagem jogável. Isso autoriza uso dos retratos/poses e caminhão preparados; não substituir por rostos novos. Base corporal aprovada explicitamente com “Ótimo. Essa última ficou perfeita. Ela é a referência.”; derivadas e caminhão têm aceitação para integração pelo pedido atual, sem inventar outra citação “Aprovado”. Os estados históricos de revisão dos pacotes de preparação são preservados. Registro de uso atual em `game/assets/v4/drivers/marquinhos.json` e `game/assets/v4/cars/marquinhos.json`.

O caminhão é cavalo mecânico vermelho4×2 sem carreta, Diabo Verde no para-brisa e FTW na porta. Modelo/ano exatos não confirmados; vistas traseiras são reconstrução convencional informada pela pesquisa pública, sem copiar fotografias externas ou inventar patrocínios. Nome Marquinhos sem sobrenome/número. A abertura também usa o retoque de Felipe com menos papada já apresentado e recebido com “Ok, Chat, já melhorou muito”, preservando seus outros sprites.

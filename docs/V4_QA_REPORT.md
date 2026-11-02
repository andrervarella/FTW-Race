# QA V4 — prévia funcional, arte em revisão

Fonte-base: `f6f6f83c40a3db3cc83cde4fc12702a1a94cc6e1`. Branch exclusiva: `codex/ftw-race-v4-arcade`. Baseline: `V4_BASELINE.txt`. Data de trabalho exibida ao usuário:01/11/2026, America/Sao_Paulo.

## Verificado localmente
| Verificação | Resultado e limite |
|---|---|
| Node24.19 / npm test | PASS40/40asserções: todas as suítes, não apenas core. `--test-isolation=none` evita a execução por subprocesso que ocultava asserts neste ambiente. |
| Sintaxe | `node --check` em todos os módulos JS; PASS. |
| Simulação | Corrida completa determinística, seis vencedores, empate estável, checkpoints, exatas voltas, nitro, pausa, colisão em pack e retardatário; PASS. |
| Assets |20PNG de render/16quadros FX;120arquivos com SHA256;36frames de corpo inteiro distintos com alpha real256×512; PASS. |
| DOM em Chromium154 | title→select→grid→countdown→pause→results→podium; ambos pilotos, confirmação duplicada, três pointers/cancel/lostcapture, teclado, reduced-motion e seis vencedores; PASS. |
| Phaser real | WEBGL local3.90.0 carregou; corrida de uma volta terminou naturalmente com rival vencedor, bandeirada→seis linhas→pódio seis etapas→replay/trocar/capa; PASS. Não apenas fixture. |
| Android emulado | Chromium, viewports915×412 e740×360, is_mobile/has_touch; CDP input de três dedos, aceleração+direção+nitro, cancel/blur, portrait/landscape e safe layout; PASS. Não é aparelho físico. |
| Áudio |18renders OfflineAudioContext (6etapas×3modos), seleção, unlock idempotente, suspensão/retomada e mudo real; PASS. Qualidade ouvida por humano não validada. |

## Problemas encontrados e reteste
- Perda de volta ao tocar retardatário: recuo agora usa penetração circular, não distância absoluta de outro carro. Regressão passou.
- Revisão independente encontrou spray CSS continuando após blur: comemoração agora pausa JS+CSS e exige CONTINUAR COMEMORAÇÃO. Teste Chromium falhou antes e passou depois.
- Revisão encontrou seleção silenciosa após sair da pausa: gestos voltam a desbloquear áudio e feedback espera contexto disponível. Teste Chromium falhou antes e passou depois.
- Caminho de horizonte antigo404 durante edição concorrente: título migrou para asset V4. Favicon explícito eliminou pedido automático404. Cache fresco foi retestado; relatórios de rede finais são a evidência, não o erro transitório anterior.

## Limitações de aceite
- **Ilustrações geradas, carros NPC e todos os derivados aguardam revisão do proprietário.** Não são entrega artística final. A capa é composição DOM de arte2D original do projeto; as poses geradas têm aproximações e detalhes de enquadramento a revisar.
- Não há Android físico acessível: GPU, fluidez e multitouch em aparelho permanecem NÃO TESTADOS. FPS de software headless não é desempenho Android.
- Não houve importação de conteúdo de Top Gear/OutRun ou execução de REA.
- A publicação externa precisa passar pelo workflow de navegador público e artifact antes de se afirmar URL verificada. O workflow não publica nem altera versões antigas; apenas visita a URL e salva evidência.

## Comandos reproduzíveis
`cd game && npm test`; `python3 game/scripts/verify-v4-render-assets.py`; `python3 game/scripts/audit-v4-assets.py`; `python3 game/tests/ui-flow.py` com servidor na raiz; `python3 game/tests/audio-v4.py`; `python3 game/tests/v4-live.py URL --executable-path /usr/bin/chromium`.

A rota de publicação é exclusivamente `teste-v4/` na branch `gh-pages`. Hashes de todos os46arquivos preexistentes serão comparados antes do envio. O commit e artifact de validação pública são fornecidos na entrega depois de existirem.

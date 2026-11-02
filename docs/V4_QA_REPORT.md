# QA V4 — prévia funcional, arte em revisão

## Verificação pública final — PASS, 02/11/2026
- URL jogável verificada: https://andrervarella.github.io/FTW-Race/teste-v4/.
- Fonte testada: `d0d883177838f3997804cd923757a525dcbf5e4c`, branch `codex/ftw-race-v4-arcade`; Pages: `a8f8511beac3905aec05e767e91b17b396129071`.
- [Run final 41455523600](https://github.com/andrervarella/FTW-Race/actions/runs/41455523600): **success**, incluindo teste e upload do artifact.
- Artifact `13146592605`, `ftw-v4-public-chromium-41455523600`; ZIP SHA256 `255dba04eb08f996bf2be07ded7d2a6e5577aa726960d135d2fe655ef769d8fb`. Baixado e inspecionado: summary/2 relatórios PASS, 13 capturas, nomes de arquivo válidos.
- Chromium independente 141.0.7390.37 executou o produto pela URL HTTPS em 915×412 e 740×360 com redução de movimento. Phaser 3.90.0/WebGL, ambos pilotos, grid, countdown natural, toque simultâneo, pausa, rotação e retorno passaram. Uma corrida terminou naturalmente; Rival Roxo venceu e recebeu taça/champanhe/pódio correspondente. Replay funcionou. O teste de separação entre rótulos e números dos degraus também passou.
- Zero erros de JavaScript/console, HTTP/404, requests falhos ou assets fora da subpasta. Avisos de GPU software do runner não são erros do jogo nem medição de desempenho Android.
- Testes locais finais: 40/40 asserções Node, sintaxe dos módulos, 121 hashes de assets, 36 frames de corpo inteiro, 20 PNGs de render/16 frames FX e regressões de áudio/pausa/carregamento lento aprovados.
- Os 46 arquivos preexistentes de Pages permanecem idênticos (SHA/tipo/modo); `main` e `claude/ftw-race-v0.2` não foram alteradas. Publicação restrita a `teste-v4/`.

**Estado do aceite:** prévia funcional publicada e verificada; **entrega artística final ainda não aprovada**. Feições, uniformes, patrocinadores e novos NPCs/derivados aguardam revisão humana. Android físico, áudio ouvido no aparelho e FPS real do telefone não foram testados. Este fechamento adiciona somente documentação; não altera o produto verificado.


## Primeira verificação pública — PASS
URL real: https://andrervarella.github.io/FTW-Race/teste-v4/. Pages `0c7235e09306c8ae12ca9ac5fc87fdcea551462d`; fonte `3dce9df21f68591055742bf72128fa9401514e4e`. Run [41452949514](https://github.com/andrervarella/FTW-Race/actions/runs/41452949514) concluiu success. Artifact13145781202 (ZIP SHA256 ec6619ed4ccb8a87846c982d1240b60f52af6cbaf8c2e64662b2f751f11502c7) foi baixado, extraído e inspecionado. Chromium141.0.7390.37 independente visitou a URLHTTPS, inicializou Phaser3.90/WebGL, testou os dois pilotos, inputs reais, pausa/orientação, redução de movimento e uma corrida natural completa. Vencedor real: Rival Roxo; resultado e pódio correspondentes. Layouts915×412 e740×360 passaram sem erros de console/HTTP, requests falhos ou caminhos fora de teste-v4. Capturas eJSON comprovam o resultado. Avisos de GPU software no runner não são medição Android.

Inspeção das capturas encontrou sobreposição pequena de rótulos e números dos degraus2/3. Corrigida via espaçamento/escala do texto e teste de bounding boxes (RED→GREEN em Chromium). Essa correção visual passa por nova rodada pública antes da entrega.

A rodada41454470771 passou a etapa “Verify the published V4 in mobile Chromium” nos dois layouts, inclusive o assert dos rótulos corrigidos. A etapa de upload do artifact falhou porque uma variável do teste usada em nomes de arquivos foi sobrescrita por coordenadas de bounding box, gerando caractere “:” inválido. Corrigido o nome da variável do teste; produto e Pages não sofreram alteração. A rodada final precisa confirmar tanto o teste quanto o artifact.

Fonte-base: `f6f6f83c40a3db3cc83cde4fc12702a1a94cc6e1`. Branch exclusiva: `codex/ftw-race-v4-arcade`. Baseline: `V4_BASELINE.txt`. Trabalho iniciado em01/11/2026 e continuado em02/11/2026, America/Sao_Paulo.

## Verificado localmente
| Verificação | Resultado e limite |
|---|---|
| Node24.19 / npm test | PASS40/40asserções: todas as suítes, não apenas core. `--test-isolation=none` evita a execução por subprocesso que ocultava asserts neste ambiente. |
| Sintaxe | `node --check` em todos os módulos JS; PASS. |
| Simulação | Corrida completa determinística, seis vencedores, empate estável, checkpoints, exatas voltas, nitro, pausa, colisão em pack e retardatário; PASS. |
| Assets |20PNG de render/16quadros FX;121 arquivos com SHA256;36frames de corpo inteiro distintos com alpha real (oficiais256×512, NPCs320×512); PASS. |
| DOM em Chromium154 | title→select→grid→countdown→pause→results→podium; ambos pilotos, confirmação duplicada, três pointers/cancel/lostcapture, teclado, reduced-motion e seis vencedores; PASS. |
| Phaser real | WEBGL local3.90.0 carregou; corrida de uma volta terminou naturalmente com rival vencedor, bandeirada→seis linhas→pódio seis etapas→replay/trocar/capa; PASS. Não apenas fixture. |
| Android emulado | Chromium, viewports915×412 e740×360, is_mobile/has_touch; CDP input de três dedos, aceleração+direção+nitro, cancel/blur, portrait/landscape e safe layout; PASS. Não é aparelho físico. |
| Áudio |18renders OfflineAudioContext (6etapas×3modos), seleção, unlock idempotente, suspensão/retomada e mudo real; PASS. Qualidade ouvida por humano não validada. |

## Problemas encontrados e reteste
- Conexão lenta: um asset atrasado13s deixava um falso erro fatal mesmo após iniciar. Reproduzido em Chromium e corrigido:12s agora mostra orientação de espera, sem mascarar erros reais de arquivo. `slow-boot.py` passou após falhar antes da correção.
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

## Publicação — bloqueio de autorização em02/11/2026
O GitHub confirmou repositório público andrervarella/FTW-Race pertencente à conta autenticada e permissões de push/admin. Mesmo após confirmação de destino e do pedido de branch/publicação, a revisão automática rejeitou create_blob por exigir autorização explícita de divulgação pública do código/assets. Confirmação específica solicitada ao proprietário. Não houve movimento de refs, implantação ou verificação da URL pública; não afirmar que /teste-v4/ está online. Há alguns objetos Git sem ref de uma transferência inicial interrompida, mas nenhuma branch ou versão publicada foi alterada.

O proprietário respondeu posteriormente: “Autorizo publicar código e assets publicamente”, confirmando o destino e a visibilidade. A revisão automática então aceitou o envio. Status de publicação e verificação pública será acrescentado após a implantação; a autorização não substitui QA externo.

## Script de verificação externa — corrida completa
O script versionado v4-live.py foi estendido para deixar uma corrida de1volta terminar naturalmente no produto servido (sem injetar vencedor), conferir as6linhas reais, abrir o pódio do vencedor, observar spray e pose final e testar replay. A mesma sequência passou localmente no pacote final em915×412; o layout740×360 com redução de movimento também passou. Esses mesmos passos serão executados contra a URLHTTPS pelo workflow após publicação.

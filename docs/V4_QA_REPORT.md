# QA V4 — prévia funcional, arte em revisão

## Verificação pública da pose frontal e do áudio — PASS

- URL: https://andrervarella.github.io/FTW-Race/teste-v4/.
- Código verificado `54a422c7ac6c8ed9037a35b29d1462846914c914` (local `db1149f10f704260b71749cd402aa53b6827bb5b`, árvore `03e37dac8be051b4d60da3615343725131506f54`); Pages `a5284638a65901cdd9b55e6ede19b17c572f65b3`, árvore `0c083370ff8185f075631c2db5fc1cc1adbda393`. Implantação Pages41507467319: success.
- [Run 41507715470](https://github.com/andrervarella/FTW-Race/actions/runs/41507715470): **success** nas etapas de corrida completa, áudio ao vivo e upload. Chromium141.0.7390.37 independente em915×412 e740×360 com movimento reduzido.
- Artifact13171512175, ZIP SHA256 `e44fe94c2e12608b336ca79fa2ba962a6e527c67dcbeec633acd67b3c232347e` (2962648bytes). Baixado; hash, CRC e caminhos de extração conferidos. Summary/2relatórios de fluxo e summary de áudio PASS;13capturas presentes. Capa nos dois tamanhos e seleção inspecionadas visualmente; Felipe frontal somente na abertura.
- Cada viewport conferiu24hashes/dimensões de arte aprovada, incluindo o novo retrato,16poses e os2logos originais. Os4atlases NPC com seis vistas carregaram. Corrida natural completa, seis resultados reais, pódio do Rival Roxo, replay, ambos pilotos, multitouch, pausa e orientação passaram. Zero erros JS/console, HTTP, requests falhos ou caminhos fora de teste-v4.
- Áudio com autoplay restrito e sem a opção mute do runner: primeiro toque manteve `tudo` e produziu música (RMS0.05496); Space/Enter também passaram. Motor isolado RMS0.05947, música de corrida RMS0.00226; nitro por toque real,13efeitos pontuais e3contínuos (pneus/cascalho/vento) com sinal não nulo. Retomada preserva modo; pausa suspende o contexto e mudo permanece silencioso. Gravação `audio-live/menu-live.webm` (16718bytes) preservada no artifact; sem acesso ao microfone.
- Local/pacote: Node47/47,176hashes,16vistas aprovadas, fluxo natural e suites UI/áudio offline/ao vivo PASS. Revisão independente sem achados materiais. Os46arquivos anteriores de Pages mantêm SHA/modo/tipo; publicação restrita a teste-v4; main e a fonte Claude preservadas.
- Limite: emulação móvel Chromium e medição do grafo real de áudio; Android físico, alto-falante/volume do aparelho e FPS real não testados. O primeiro gesto é exigido pelo navegador. Fechamento seguinte altera apenas documentação.

## Verificação pública dos pilotos e capa aprovados — PASS
- URL: https://andrervarella.github.io/FTW-Race/teste-v4/.
- Código verificado `b458fdc15c9195e0d1eb6bf9324b6b8cd135e3a6` (local `419621ea8a7aa21d6633d70536d9521bdd2910ab`, árvore `79c9dffad408e5931639d57211764bd25ba4ecb8`), branch `codex/ftw-race-v4-arcade`; Pages `8ab5eeea74973743fabaa282ce06ced24cc63741`, árvore `b6b99da0264603fa5504016241e2d81b36e000f1`. Implantação Pages41497754131: success.
- [Run 41497991461](https://github.com/andrervarella/FTW-Race/actions/runs/41497991461): **success**, teste e upload do artifact. Chromium141.0.7390.37 independente em915×412 e740×360 com movimento reduzido.
- Artifact13168495437, ZIP SHA256 `2322b7c1379189b13d5eb69ff246065d85fd1c16043f3d307003c15b7f363c42`. Baixado, hash/CRC/caminhos de extração conferidos; summary e dois relatórios PASS.13capturas conferidas, com inspeção visual da capa e seleção publicadas.
- Cada viewport verificou23hashes/dimensões dos arquivos realmente servidos:16poses de pilotos,5camadas da capa e2logos originais. Os4atlases NPC com seis vistas também carregaram. Botão de início mantém alvo físico≥44px.
- Corrida natural de1volta terminou com Rival Roxo; resultados reais de seis carros e pódio correspondente, replay, ambos pilotos, toque simultâneo, pausa e orientação passaram. Zero erros de JavaScript/console, HTTP/404, requests falhos ou arquivos fora da subpasta.
- Pacote local idêntico passou pelo mesmo roteiro em Chromium154.0.8037.57. Node45/45,174hashes,16poses aprovadas,36quadros de pódio e24PNGs/metadados NPC preservados: PASS. Origem/direção do champanhe corrigidas com regressão RED→GREEN e verificadas em ambos os pilotos no fixture e em capturas do renderer real.
- Os46arquivos anteriores de Pages permanecem idênticos (SHA/modo/tipo); `main` e `claude/ftw-race-v0.2` preservadas. Aprovação humana cobre rostos, pranchas de pilotos e capa; outros derivados mantêm seu estado anterior. Android físico/FPS/áudio no aparelho não testados.
- Este fechamento final altera apenas documentação; o produto publicado permanece o que o run verificou.


## Verificação pública dos novos NPCs — PASS
- URL: https://andrervarella.github.io/FTW-Race/teste-v4/.
- Fonte testada `8f8591176dcf3f7cfd85eaed06d1bd7a5e623778` (local `a07fe19c0812292c18acfe69c8a06cd5c82688c3`, árvore `c9a1d6f2751848b100e954ba333e3ae4aef02d23`); Pages `8f7f9d0ed992dcf953c0fc4eafa53d02dc5976b9`, árvore `bbe2af19875c61caf98dfb169849990a9acd2a42`. Implantação Pages41483605969: success.
- [Run 41483753670](https://github.com/andrervarella/FTW-Race/actions/runs/41483753670): **success**, incluindo teste e upload do artifact. Chromium141.0.7390.37 independente,915×412 e740×360 com movimento reduzido.
- Artifact13161440675, ZIP SHA256 `305994ac28e5b34e9ed03180a6c23602eaa6d887095999d5e380cbdc211b2432`: baixado, hash conferido, extração segura e13capturas conferidas; grid e pódio inspecionados visualmente, summary e dois relatórios PASS. Quatro PNGs1680×1024, seis frames560×512 por carro carregados pela URL HTTPS.
- Corrida natural de uma volta terminou com Rival Roxo; seis resultados reais, taça/champanhe e pódio do vencedor, replay, ambos pilotos, toque simultâneo, pausa e rotação passaram. Zero erros JS/console, HTTP/404, requests falhos ou assets fora da subpasta.
- Pacote local `/teste-v4/` passou pelo mesmo roteiro em Chromium154.0.8037.57. A primeira tentativa local não iniciou por usar o caminho padrão de um browser Playwright ausente; a execução correta usou `--executable-path /usr/bin/chromium`. Não foi uma falha do produto.
- Node45/45; sintaxe dos12módulos;150hashes;24sprites NPC e36poses de pódio; seis estados dos quatro NPCs no Phaser real: PASS.
- Os46arquivos anteriores de Pages mantêm SHA/tipo/modo idênticos. Mudanças de distribuição somente em `teste-v4/`; `main` e a fonte Claude preservadas.
- Limites: emulação móvel, sem teste em Android físico/FPS/áudio ouvido no aparelho. Arte derivada da referência, novas vistas ainda sujeitas à revisão do proprietário. Nenhum recurso de Top Gear importado.


## Verificação pública anterior — PASS, 02/11/2026
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

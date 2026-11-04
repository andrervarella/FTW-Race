# QA V4 — prévia funcional, arte em revisão

## 03/11/2026 — autorização complementar do retrato retocado de Felipe

Após a revisão automática rejeitar o envio do PNG retocado de Felipe usado na capa (`4f55f2a8bf104ddc0ef1442e05f19911ea9bd599`), o proprietário respondeu à confirmação específica: **“Autorizo publicar também o retrato retocado de Felipe no repositório público andrervarella/FTW-Race e em /teste-v4/.”** Esta autorização complementar veio de resposta atual do usuário e cobre o retrato retocado usado na abertura, incluindo seu derivado WebP. A autorização original de Marquinhos, caminhão e capa permanece integralmente registrada na seção seguinte.

As duas confirmações permitem retomar o envio dos arquivos preparados aos destinos nomeados. QA local e runtime permanecem os mesmos; **publicação, implantação e QA público desta atualização continuam pendentes de evidência real**. Este acréscimo altera apenas documentação e conserva o histórico da rejeição, sem afirmar aprovação automática, implantação ou verificação ainda inexistentes.

## 03/11/2026 — autorização explícita recebida; publicação e QA público pendentes

O proprietário autorizou nesta conversa: **“Autorizo publicar esta atualização, incluindo as novas artes de Marquinhos, do caminhão e da capa, no repositório público andrervarella/FTW-Race e no jogo /teste-v4/.”** A confirmação nomeia as novas artes identificáveis e os dois destinos públicos exigidos na revisão anterior. O histórico dos bloqueios permanece abaixo; esta autorização permite retomar a publicação preparada, mas não comprova envio, implantação ou verificação pública.

Estado no registro desta confirmação: QA local PASS (70/70 Node, 248 arquivos SHA256, Chromium154, corrida natural com sete participantes, 12 vistas do caminhão e áudio ao vivo); **publicação e QA público desta atualização ainda pendentes**. Fonte de runtime verificada `357cb810f870b3936c4c4016659f1156b91f0bb2`, árvore `5782c16fade29fc4c441bbac61e3dcc6cff3679d`; pacote Pages preparado `70b5e734cf9039b0cabf0e52560d03a3a6209cb8`, árvore `29b79b1c7b1900c4244b22d6998705bdad108ef1`. Este registro altera apenas documentação; o pacote testado continua o mesmo.

Destino autorizado da fonte: `codex/ftw-race-v4-arcade`; publicação Pages restrita a `teste-v4/`, com os 46 arquivos legados preservados. Os commits remotos e a evidência da execução pública serão registrados após existirem. Android físico, alto-falante real e FPS no aparelho continuam não testados.

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


## 03/11/2026 — Marquinhos integrado; validação local e bloqueio de publicação

Código em `codex/marquinhos-playable`; integração principal `ea1ea92`. Terceiro piloto selecionável **Marquinhos**, capa com três retratos/veículos, IVECO vermelho4×2 sem carreta, seis estados, escala uniforme própria e caixa de colisão maior. Sete participantes preservam os quatro rivais antigos e resultado real; pódio de Marquinhos tem seis poses e origem do champanhe medida na garrafa. Felipe recebe o retoque solicitado apenas na abertura. Fontes e marcas oficiais preservadas.

**PASS com evidência local:**
- Baseline47/47; suíte final70/70Node. Auditoria248arquivos SHA256,42corpos de pódio e19cópias runtime idênticas às fontes de Marquinhos; zero falhas de integridade. Sintaxe de todos os módulos e scripts modificados e `git diff --check` passaram.
- Chromium154.0.8037.57 real sobre cópia Pages em `/teste-v4/`:915×412,740×360 com movimento reduzido e1440×900.43hashes de arte servida por viewport, três selecionáveis e sete no grid/HUD/minimapa. Corrida de uma volta com Marquinhos selecionado terminou naturalmente: Roxo, Amarelo, Daniel, Felipe, Prata, Azul, Marquinhos. Resultado e pódio exibiram o vencedor real; nenhum tempo final inventado para quem não concluiu. Multitoque, liberação, pausa, rotação e retorno passaram; sem errosJS/HTTP ou caminhos fora da subpasta.
- Fixture com renderizador Phaser real: seis vistas para jogador e seis para adversário, sem espelhar; razão uniforme do atlas1.716819571865443 em ambos os eixos na mesma profundidade. Corpo útil do caminhão≈1.40×largura Mercedes conforme auditoria de alpha. Colisão de caminhão/carros usa limites10.8longitudinal/.66lateral; são parâmetros arcade, não metros oficiais.
- UI-flow final passou em1600×900,915×412,740×360, incluindo capa/seleção, todos os sete vencedores e controles≥44×44. Pódio de todos os sete em três tamanhos passou, sem sobrepor legendas aos lugares. Ajustados seletor com largura44px, botão SOM de43.9375para44px e carros nos cards compactos.
- Áudio ao vivo em qualidade normal: primeiro PRESS START RMS0.04607; botão de som0.03430; motor0.07412; música de corrida0.01960. Modo efeitos manteve motor e zerou música; mudo RMS0.000003251. Pausa suspendeu o contexto sem avanço; retorno audível.13efeitos pontuais e3contínuos passaram, gravação WebM13820bytes. Em teste offline anterior,21combinações dos sete vencedores×três modos/seis momentos passaram.
- Teste de carregamento lento: asset atrasado>12s recupera; falha real mostra erro. Revisão independente: sem achados bloqueantes;39testes focados e três corridas completas headless adicionais passaram.

Falhas de roteiro/ambiente encontradas e corrigidas: servidor antigo sem consumo de log devolvia ERR_EMPTY_RESPONSE; servidores novos redirecionam logs. Fixture de colisão passava input vazio e produzia NaN; agora passa todos os booleanos. Inventário de navegador ainda esperava24assets; agora confere43. Sob softwareGPU, uma janela de áudio encerrava após um único snapshot atrasado; a medição exige≥8snapshots e prazo de10s, mantendo todos os limiares de sinal/silêncio. Nenhuma alteração no módulo de áudio de produção foi necessária.

**NÃO TESTADO:** Android físico, alto-falante real, FPS no aparelho, implantação/CI públicos desta atualização. As capturas e medições são emulação Chromium; não declarar teste físico nem audição humana.

**Publicação bloqueada pela revisão automática:** `github_create_blob` de fragmentos das novas artes identificáveis de Marquinhos foi rejeitado por exigir autorização verificável do usuário para esse payload/destino público. Após conferir a autorização ampla anterior “Autorizo publicar código e assets publicamente”, o repositório público de destino e o atlas exato, uma única repetição do mesmo payload também foi rejeitada: registros em arquivos/tools não foram aceitos como resposta confiável do usuário para os novos assets. Nenhum desvio ou método alternativo será usado.13objetos de transferência sem ref ficaram no GitHub; nenhuma branch, commit remoto ou implantação foi movida.

Refs conferidas após bloqueio: fonte`cc8d5b70d0dd9f113fbdd83ddf0814968e54bcdb`; Pages`a5284638a65901cdd9b55e6ede19b17c572f65b3`; auxiliar`740342f8ef0a91149b5382a972efe6a2122391cd`.46arquivos das páginas anteriores preservam hash/modo. O link público continua na versão anterior. Apenas a nova confirmação explícita de publicação está pendente; integração, pacote local e QA estão concretos para revisão. Resumo legível por máquina: `docs/qa/marquinhos-local-2026-11-03.json`.

O proprietário respondeu ao bloqueio: “Ok se depender de mim está liberado”, autorizando o envio desta atualização com as novas artes de Marquinhos, caminhão e capa ao GitHub público e `/teste-v4/`. O bloqueio operacional acima foi superado por essa nova confirmação; publicação e verificação pública ainda serão registradas após ocorrerem.

A revisão automática voltou a rejeitar um fragmento após a resposta “Ok se depender de mim está liberado”: exigiu autorização que nomeie as novas artes identificáveis e o destino GitHub público. Transferência novamente interrompida, sem alternativa/contorno.21objetos canônicos sem ref foram verificados; nenhuma branch/implantação movida. Tudo local está concreto: fonte`357cb810f870b3936c4c4016659f1156b91f0bb2`, árvore`5782c16fade29fc4c441bbac61e3dcc6cff3679d`; pacotePages`70b5e734cf9039b0cabf0e52560d03a3a6209cb8`, árvore`29b79b1c7b1900c4244b22d6998705bdad108ef1`.158arquivos runtime espelhados byte-idênticos,46legados preservados,38mudanças Pages restritas a `/teste-v4/`. Novo envio depende da confirmação explícita: publicar atualização e novas artes de Marquinhos, caminhão e capa no repositório público `andrervarella/FTW-Race` e jogo `/teste-v4/`.


## Publicação e primeira verificação pública de Marquinhos

Página implantada: `bcae79a1bf41e8d767bb9142ea4e166b3115a9fd`, árvore `29b79b1c7b1900c4244b22d6998705bdad108ef1`; implantação41705902013: SUCCESS. Fonte `37e8712e799f65cf2ed685bf4738cdb70b0abaa2`, árvore `f292132721dbe1e6c1cbdc14ec12932e463fc389`, branch `codex/ftw-race-v4-arcade`. Todos115blobs canônicos conferidos após upload direto pelo conector, incluindo31imagens e dois HTMLs de prévia grandes. Fragmentação anterior era escolha operacional, não limite comprovado; branch auxiliar não foi movida. Autorizações explícitas de Marquinhos/caminhão/capa e do retrato retocado de Felipe foram recebidas e atendidas.

[Workflow público41706301881](https://github.com/andrervarella/FTW-Race/actions/runs/41706301881): SUCCESS em todos os passos, Chromium141.0.7390.37.43hashes servidos por viewport em três tamanhos, corrida natural com Marquinhos selecionado/sete participantes/vencedor real,12vistas do caminhão e colisão maior, música/motor/13efeitos pontuais/3contínuos e primeiro gesto passaram; sem errosJS/HTTP. Artefato13267135339:11068275bytes, SHA256 `4995cfcb6bed1f5851f149349706cd28e87b8c063e537460538637472f2b8a10`,40entradas/33PNG, CRC/caminhos verificados. Primeiro toque RMS0.03872; motor0.07106; música de corrida0.02465. Main/Claude e46arquivos legados preservados.

Na revisão direta das capturas, o nome Marquinhos quebrou após “Marquinho” em740×360 por diferença de métricas da fonte system-ui no Chromium público. O código permitia `overflow-wrap:anywhere` e não reduzia a fonte do nome longo. Ajuste restrito aos cards compactos: fonte responsiva menor e nome indivisível; sem alterar artes ou comportamento. Medição real local em568×320,740×360,915×412 confirmou uma linha dentro do espaço disponível. A publicação desta única regra e a nova captura pública serão registradas após concluir. Android físico, alto-falante real e FPS de aparelho continuam não testados.


## Fechamento público — Marquinhos e ajuste compacto concluídos

**Publicado e verificado:** https://andrervarella.github.io/FTW-Race/teste-v4/ . Página final `1c9f7f54f5bcdef9ebc94d48681445edad028ac3`/árvore `764e16dd8b87d51f36ec8f9f6daa39b354ea0e6b`; implantação41744987690: SUCCESS. Fonte de jogo `9149e4fd74cbd1fb69fc90d4847e6d9b84f0e4e4`/árvore `8a6681827b266c5fbe2b18f20818a92e7ddccd36`, branch `codex/ftw-race-v4-arcade`. O ajuste do nome é uma única regra CSS; não alterou identidade, áudio ou simulação. Nova medição local568/740/915 passou; captura pública740×360 confirmou “Marquinhos” inteiro em uma linha.

[Verificação pública41745132125](https://github.com/andrervarella/FTW-Race/actions/runs/41745132125): todos os passos SUCCESS, Chromium141.0.7390.37, três viewports,43hashes de arte por viewport, sete participantes e corrida real com Marquinhos selecionado, classificação/pódio do vencedor real,12vistas do caminhão/escala uniforme/colisão maior, áudio no primeiro gesto/13efeitos/3contínuos. Todos os arrays de errosJS/HTTP/requisições estão vazios. Artefato13283392674:11053972bytes, SHA256 `e0bea201de4cf402f607c2c63b6205d7ddc02ec6d27e44d0521729835aac6947`; CRC/caminhos seguros e40entradas conferidos. Revisão direta de capturas de capa, seleção, corrida e pódio concluída. Relatório estável em `docs/qa/marquinhos-public-41745132125.json`.

Suíte Node executada novamente após a alteração CSS:70/70 PASS.46arquivos legados, main e versão Claude preservados; a publicação limita-se à branch V4 e `/teste-v4/`. Não há aprovação de publicação pendente: autorizações explícitas de Marquinhos/caminhão/capa e do retrato retocado de Felipe foram recebidas. As descrições de bloqueio anteriores são histórico superado. Android físico, FPS no aparelho e audição em alto-falante real continuam não testados; provas de áudio medem o grafo Web Audio e gravação. Este fechamento altera somente documentação.

## Correção de cache e visibilidade móvel — prova local
Reprodução em Chromium com cache HTTP de um ano: runtime antigo2pilotos; HTML novo com caminhos iguais mantém2; novo pacote imutável carrega3/grid7 no mesmo contexto sem limpar cache. Resolver validado em6casos. Entrada canônica empacotada passou áudio real13efeitos e renderer12vistas, resolvendo os módulos da mesma árvore imutável.

Na foto enviada pelo usuário, a câmera global reduzia o Mercedes e o nitro central o cobria. Restaurada a fórmula exata pré-Marquinhos para Daniel/Felipe. Em915×412, canvas Mercedes passou de112.79para193.64px de altura; corpo útil de88.34×72.70para151.66×124.81px. Caminhão selecionado continua maior, com canvas277.04px e corpo176.94×247.82px; na mesma cena, todas as vistas usam o fator uniforme próprio1.7168195718654433, sem deformação. Nitro fica acima das setas; comandos laterais não cobrem o veículo.

`mobile-race-layout.py`:576estados/96capturas PASS no Chromium154.0.8037.57. Viewports915×412,740×360,568×320,1024×461 (dimensões CSS da foto a DPR2),761×412,780×412,800×412 e844×412; safe areas zero, simétrica24px/bottom32px e assimétrica44px/bottom32px nos dois lados. Três pilotos×seis vistas; tamanho Mercedes exato anterior, caminhão maior, sete competidores, alpha útil livre dos botões, alvos≥44px e transição grid→corrida passaram; menor folga7.23px. Arrays de errosJS/HTTP/requisições/falhas vazios. Capturas de Daniel1024×461 e Marquinhos740×360 também revistas diretamente. Provas finais em `/workspace/work/mobile-layout-final/`, `/workspace/work/mobile-layout-boundary-review.json` e `/workspace/work/cache-and-mobile-final-cache/`. Não houve teste físico de WhatsApp/Android. Execução HTTPS pública será acrescentada após publicação.

A revisão detectou duas regressões antes da publicação: aumento dos bancos acima760px e insets armazenados apesar de rotação180° sem resize. Ambas corrigidas; a matriz576 e90estados extras nas fronteiras900/901px passaram, incluindo atualização da âncora X no mesmo DOM/race. Resultado resumido em `docs/qa/mobile-cache-local-2026-11-04.json`.

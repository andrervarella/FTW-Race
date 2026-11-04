# Registro de consulta a projetos open source — FTW Race

Documento de rastreabilidade para futuras integrações. **Nenhum código de terceiros foi importado ao criar estas instruções.**

| Data | Tarefa | Referência URL/commit | Licença código/asset | Decisão | Testes e evidências |
|---|---|---|---|---|---|
| 2026-11-01 | Configurar diretrizes | JavaScript Racer, Pseudo-3d-Racer, Phaser Examples, Godot Demos (ver política) | Conferir licença concreta antes de cada uso | Catálogo inicial e procedimento; sem implementação | Documental apenas |

Nas próximas mudanças, preencher URL, commit/tag, licença de código **e assets**, alternativas, justificativa, arquivos alterados, créditos/avisos e resultados PASSED/FAILED/NOT TESTED.


---

# Pesquisa V4 — 01/11/2026 (America/Sao_Paulo)

## Aplicação efetiva na V4
Os conceitos consultados foram implementados em código próprio: `render.js` usa pivô de solo comum, depth pela distância projetada e oculta sprites além dos segmentos visíveis; `effects.js` controla pool limitado e avanço de frame; `ui.js` usa transições sem timers pendentes, guardas contra confirmação duplicada e fontes de input por pointer. `podium.js` avança seis frames completos e FX independente. Nenhuma linha de terceiros ou asset dos exemplos foi copiado. Testes:40asserções Node, fluxo DOM/seis vencedores, Phaser real e Web Audio em Chromium (ver V4_QA_REPORT.md). Licença Phaser local3.90.0 incluída; engine preservada.

Política lida integralmente em `andrervarella/FTW-Race`, `docs/REPOSITORIOS_PUBLICOS_E_POLITICA.md`, fonte `f6f6f83c40a3db3cc83cde4fc12702a1a94cc6e1`. Consulta via conector GitHub; nenhuma dependência instalada, nenhum arquivo de terceiros executado e nenhum código/asset incorporado nesta pesquisa.

| Fonte e revisão consultada | Licença e restrições verificadas | Comparação e aplicação proposta |
|---|---|---|
| [jakesgordon/javascript-racer](https://github.com/jakesgordon/javascript-racer/tree/3e8a060b5900755db27f899612a74a77427c853e), `3e8a060b5900755db27f899612a74a77427c853e` (2025-06-01) | `LICENSE`: MIT, copyright Jake Gordon e contribuidores 2012–2016. README: músicas licenciadas somente para esse projeto; sprites extraídos do OutRun são material didático, não reutilizar. | `common.js`: `Render.sprite` calcula escala, âncora e recorte parcial pela linha de oclusão; `Game.run` separa passo fixo e render e limita delta ao voltar de aba. Útil como referência conceitual para pivôs de solo e recorte de cenários/veículos. O próprio README adverte desempenho móvel não garantido e arquitetura de demonstração; não importar o monólito nem trocar Phaser. |
| [ssusnic/Pseudo-3d-Racer](https://github.com/ssusnic/Pseudo-3d-Racer/tree/12dfc34d7d055b83441016d9a2e774c585fdfdc3), `12dfc34d7d055b83441016d9a2e774c585fdfdc3` (2021-05-29) | `LICENSE`: MIT, Srdjan Susnic 2021. README não documenta licença individual/proveniência dos assets; não presumir que fotos/sprites/música são liberados. Nenhum asset será reutilizado. | `source/part2/circuit.js`: projeção por triângulos semelhantes e linha inferior de clipping que sobe ao desenhar segmentos. Phaser **2**, incompatível diretamente com o Phaser 3 da base. Referência complementar para evitar sprites/pista aparecendo sobre colinas; reimplementar conceito somente se bug reproduzido exigir. |
| [phaserjs/examples](https://github.com/phaserjs/examples/tree/eb87db8355861ae222d0c5cd13aae54c2d7d72ae), `eb87db8355861ae222d0c5cd13aae54c2d7d72ae` (2026-10-26) | README: código MIT, **assets não**; muitos são de arcades/jogos antigos/stock e não podem ser usados em jogos comerciais/com publicidade. Não copiar assets. | `main` já é Phaser 4: consultar subárvore **public/3.86/src/** para APIs mais próximas da base 3.80.1. `input/multitouch/multi touch test.js`: desbloqueio de áudio e pointers independentes; adaptar conceito ao DOM Pointer Events existente (não aumentar pointers Phaser se botões DOM). `animation/create animation from sprite sheet.js`: sheet com frameWidth/Height, frames explícitos, frameRate/repeat e pixelArt; aplicar aos novos frames reais de pódio/FX. `scenes/transition test 1.js`: `once` nos comandos de transição e eventos transitionstart/complete; equivalente em UI DOM deve cancelar eventos/timers anteriores e impedir duplo início. |

Escolha técnica: preservar a simulação, Phaser e HUD DOM do FTW. A referência mais adequada para animação/input é a subárvore Phaser 3.86; jakesgordon é mais claro para clipping e pivôs; ssusnic é complementar e antigo. Nenhuma alternativa exige trocar stack. Não houve reutilização de linhas: se o implementador derivar trechos, deve preservar avisos MIT correspondentes e registrar arquivos efetivamente alterados. A aplicação efetiva e os testes entram no log final após implementação, não são presumidos por esta pesquisa.

REA: desnecessário para código fonte ES modules disponível; nenhuma instalação/execução de REA.

## Ferramentas locais de QA verificadas

- Node **v24.19.0** e npm disponíveis.
- Python Playwright e Node Playwright/Playwright-core pré-instalados.
- `/usr/bin/chromium`: **154.0.8037.57** (Debian 13).
- PIL disponível. Selenium não instalado.
- Smoke Playwright real com Chromium: **PASSOU** (navegador iniciou, criou página, leu título `FTW QA`, fechou).
- A execução padrão no sandbox falha em `crashpad/util/linux/socket.cc:45`, `setsockopt: Operation not permitted`, SIGTRAP; flags `--disable-crash-reporter --disable-breakpad --disable-crashpad --disable-gpu` não corrigiram.
- O smoke passou usando `exec_command` com `sandbox_permissions: require_escalated`; auto-review aprovou a execução do browser local. Usar essa rota para automação, capturas e áudio offline. Nenhum bloqueio de rede foi contornado.
- Android físico: **NÃO TESTADO / não disponível**. Emulação mobile Chromium não prova comportamento de aparelho físico, GPU ou multitouch físico.
- O smoke acima valida apenas a ferramenta, **não** a build V4.

Comando smoke executado (Python):

```python
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
    page = b.new_page()
    page.set_content('<title>FTW QA</title>')
    print({'chromium': b.version, 'title': page.title()})
    b.close()
```

## 02/11/2026 — NPCs conforme a prancha do proprietário

Pedido: trocar os quatro SVGs provisórios por carros visualmente iguais à referência azul/amarelo/branco-prata/roxo e produzir os estados necessários. A consulta a jogos públicos orientou a implementação; nenhuma imagem, música ou trecho de código desses projetos foi importado.

| Fonte consultada | Licença/limite | Aplicação efetiva |
|---|---|---|
| `jakesgordon/javascript-racer`, commit `3e8a060b5900755db27f899612a74a77427c853e`, `common.js` (`Render.player`/`Render.sprite`) | Código MIT; sprites OutRun e música excluídos de reutilização conforme o README já auditado. | Escolha de vistas reais pela direção e pivô de solo com escala de projeção. `vehicle-visual.js` usa a inércia do volante do FTW e acrescenta limiares de entrada/saída diferentes para estabilizar a vista; `render.js` preserva a proporção dos frames e a âncora do eixo traseiro. Implementação própria, sem cópia literal. |
| `jamessimo/Phaser3-Road`, commit `21acaacf8bf9da7b71f7ea303e5bd06fd9102934` (2019-04-28), `README.md`, `LICENSE`, `package.json`, `src/classes/Car.js` e `renderHelpers.js` | MIT no código (Richard Davey2017); assets sem origem/licença individual comprovada, não importados. Phaser^3.16.2, projeto antigo. | Confirma a abordagem de projeção e objetos Phaser3. As rotinas turnLeft/turnRight estão vazias e o README lista animação de curva como TODO; não é uma solução pronta superior à V4. Preservada a base atual3.90 e criados os próprios frames/seleção. |
| `ssusnic/Pseudo-3d-Racer`, commit `12dfc34d7d055b83441016d9a2e774c585fdfdc3`, `README.md` e `source/part2/circuit.js` | MIT no código; nenhum asset reutilizado. README declara Phaser2; o arquivo examinado contém APIs de cena/renderTexture semelhantes às de Phaser3. Essa divergência impede assumir portabilidade direta. | Referência conceitual complementar de segmentos/clipping. A geometria de Cascavel e a projeção existente foram mantidas; não houve motivo comprovado para trocar a engine ou importar esse protótipo. |

REA foi considerado e não é necessário: temos o próprio JavaScript, testes determinísticos e inspeção em Phaser/Chromium. Não houve instalação, execução ou engenharia reversa de binários de terceiros. A pesquisa é de código aberto publicado pelos autores.

Verificação desta alteração: cinco testes novos de vistas, histerese, preload raster e estado real de freio; suíte Node45/45. Phaser real exibiu os quatro NPCs nos seis estados, sem saltos do pivô ou deformação da proporção. Os resultados públicos posteriores constam de NPC_REFERENCE_QA.md.

## 02/11/2026 — capa aprovada e normalização dos pilotos
Consultados `phaserjs/phaser`, tag `v3.90.0`, `src/scale/const/SCALE_MODE_CONST.js` e LICENSE.md (MIT). FIT preserva proporção dentro da área disponível; ENVELOP pode cortar bordas. A capa usa o primeiro conceito para manter rostos/carros inteiros e dimensiona os controles separadamente em pixels físicos. Implementação DOM própria via ResizeObserver com descarte em transição; engine/RESIZE da corrida não mudou, nenhum trecho externo copiado. Fonte: https://github.com/phaserjs/phaser/blob/v3.90.0/src/scale/const/SCALE_MODE_CONST.js .
O pipeline existente Pillow/NumPy foi estendido com componentes conectados SciPy (biblioteca de preparação, não dependência do jogo): seleção pelo corpo evita cortar cotovelo que cruza a célula, escala/pivô são comuns. Conceito de âncora de solo e vistas verdadeiras das pesquisas MIT anteriores permanece; sem novos assets/códigos de terceiros. REA não é necessário para esta alteração visual no nosso próprio código. Verificação:45testes Node, verificador independente de16poses,24NPCs preservados e teste de UI/resize em Chromium; relatório completo em APPROVED_PILOT_ART_QA.md.

## 02/11/2026 — ativação confiável do áudio
Consultado Howler.js2.2.4 (`goldfire/howler.js`, src/howler.core.js, `_unlockAudio`, licençaMIT) para comparar retomada direta em eventos de ativação confiáveis e repetição de resume; nenhuma biblioteca ou código literal foi importado. A base Web Audio sintetizada própria permanece. A correção trata a troca acidental do primeiro toque para efeitos-only e a promessa de resume bloqueada antes da ativação; política de autoplay do navegador preservada. Teste mede PCM no grafo de saída do GameAudio real e grava somente o som sintetizado pelo jogo, sem microfone. Relatório final em FELIPE_AUDIO_FIX_QA.md.


## 03/11/2026 — Marquinhos, caminhão e sete participantes

Consultados antes da implementação: [javascript-racer](https://github.com/jakesgordon/javascript-racer/blob/3e8a060b5900755db27f899612a74a77427c853e/v4.final.html), commit `3e8a060b5900755db27f899612a74a77427c853e`, e LICENSE (MIT). Linhas199–201 usam largura própria de cada carro para colisão;263–285 usam as duas larguras também ao decidir desvio. Adaptação própria: extensão por veículo e soma das meias dimensões no par, inclusive wrap de pista e decisões de passagem. Nenhum sprite, música ou linha de código foi importado. Os assets externos daquele demo não têm autorização de reutilização neste jogo.

Consultados [Phaser Size.js](https://github.com/phaserjs/phaser/blob/v3.90.0/src/gameobjects/components/Size.js) e [LICENSE.md](https://github.com/phaserjs/phaser/blob/v3.90.0/LICENSE.md), tag `v3.90.0`, MIT, correspondente à engine local preservada. `setDisplaySize` define escalas a partir do frame: arquivo maior não garante porte visual maior. Adaptação: fator próprio do caminhão aplicado igualmente nos dois eixos e em todas as vistas, com o aspecto560/512 e pivô comum; escala de câmera comum ao pelotão limita obstrução na tela pequena. O trecho `license.txt` foi consultado inicialmente e não existia; a licença confirmada é LICENSE.md. Nenhum asset de exemplo foi copiado.

Comparação: trocar engine ou importar o demo completo exigiria reescrever a corrida já verificada e não resolveria identidade do caminhão. Foram estendidos os módulos atuais de simulação, render, UI e pódio com os assets próprios preparados. Plano e critérios: `superpowers/plans/2026-11-03-marquinhos-playable.md`. Baseline real47/47Node. Resultados finais serão registrados em V4_QA_REPORT.md após execução.


## Compartilhamento e cache da V4 — releases imutáveis
O usuário confirmou que compartilhou `/FTW-Race/teste-v4/`; não era um link da V3. Os módulos/CSS/arte eram publicados sob URLs estáveis. No Chromium com HTTP cache de um ano, reproduzimos dois pilotos antigos mesmo com HTML novo em `?new-html=1`; somente mudar a query do HTML não renova o grafo de imports. O pacote completo sob prefixo de conteúdo novo carregou três pilotos e sete no grid no mesmo contexto já aquecido, sem limpar cache. Isso reproduz o mecanismo de cache, não prova acesso ao aparelho WhatsApp.

Referência pública consultada antes da implementação: Vite commit `b3cb0575aff63004a71301a1ec798aeea2aa05d7`, MIT, [build.ts](https://github.com/vitejs/vite/blob/b3cb0575aff63004a71301a1ec798aeea2aa05d7/packages/vite/src/node/build.ts#L772), [build guide](https://github.com/vitejs/vite/blob/b3cb0575aff63004a71301a1ec798aeea2aa05d7/docs/guide/build.md#L43), [assets guide](https://github.com/vitejs/vite/blob/b3cb0575aff63004a71301a1ec798aeea2aa05d7/docs/guide/assets.md#L27) e LICENSE. Usados os conceitos de grafo versionado/hashes e base relativa; implementação própria sem copiar código/assets nem adicionar bundler/dependências. Diferente de alterar apenas a query do entrypoint, o pacote move HTML/CSS/todos os módulos/imagens juntos e mantém os imports relativos existentes.

`package-v4-release.py` calcula SHA256 do runtime completo, copia158arquivos e gera entrypoints/manifesto;157arquivos não HTML permanecem byte-idênticos. Release existente não pode ser sobrescrito com bytes diferentes. `/teste-v4/index.html` novo aponta para o mesmo prefixo; o endereço exclusivo abre sem depender do HTML antigo guardado. V3/raiz/Claude e releases anteriores são preservados. Testes:70/70Node,6casos do resolver, cache real antigo2→queryHTML2→release3/grid7/canônica nova3, renderer12vistas. Testes públicos verificam as URLs reais do release,43hashes e headers HTTP. Não prometer invalidação retroativa de HTML+JS que já estejam inteiramente em cache num aparelho.

## Câmera e comandos móveis após Marquinhos
Reconsultado [javascript-racer common.js, Render.sprite/player](https://github.com/jakesgordon/javascript-racer/blob/3e8a060b5900755db27f899612a74a77427c853e/common.js#L296-L325), commit3e8a060b5900755db27f899612a74a77427c853e, código MIT. Conceito aplicado: projeção uniforme compartilhada e âncora separada do jogador. Implementação própria restaura a câmera Mercedes anterior e reserva o espaço do jogador entre os comandos DOM medidos; não copia código, música ou sprites externos. Nenhuma dependência nova ou mudança de engine.

Validação Chromium154 com Phaser real:576estados e96capturas em oito tamanhos móveis, quatro perfis de safe area, seis vistas de cada piloto, transição grid/corrida e sete participantes. O alpha útil é medido das texturas reais e testado contra os retângulos de todos os controles. Menor folga7.23px, alvos≥44px. O fixture adicional torna o pacote final159arquivos/158cópias não HTML idênticas; os158/157 acima descrevem a etapa anterior de cache.

Revisão adicional encontrou sobreposição no intervalo761–844px e cache de insets na rotação180° sem resize. Corrigidos com controles compactos até900px e assinatura viva dos paddings. A matriz576 passou;90casos adicionais em900/901px, incluindo alturas412/461/600 e troca do notch no mesmo DOM/race, passaram. Nenhum tamanho de carro foi reduzido.

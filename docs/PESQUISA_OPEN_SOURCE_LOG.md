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

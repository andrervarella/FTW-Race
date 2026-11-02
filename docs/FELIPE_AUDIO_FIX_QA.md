# QA — pose de Felipe na abertura e ativação de áudio

## Escopo e aprovação
O proprietário pediu postura mais natural/frontal somente na abertura, mantendo o rosto. A proposta foi mostrada isolada e na capa; resposta explícita “Aprovar a pose”. Seleção, poses de pódio, Daniel, carros, logos e outras versões permanecem como antes. Novo PNG original preservado em `game/assets/v4/title/felipe-front-portrait.png`; distribuição usa WebP proporcional sem perdas. `title/approval.json` registra a aprovação específica.

## Falha de som reproduzida
No Chromium154, autoplay restrito e toque móvel real, o primeiro toque no antigo botão SOM ON mudava `tudo` para `efeitos`: contexto running, mas título com RMS0 e pico0. PRESS START podia produzir música, portanto a falta de som não era ausência dos sintetizadores nem o noAudio do Phaser (GameAudio é separado). O rótulo inicial prometia áudio ligado antes de ativar o contexto.

Regressão controlada também reproduziu resume pendente iniciado antes da ativação: a segunda ativação esperava a primeira promessa e perdia a oportunidade de chamar resume na pilha confiável. Os ajustes mantêm a política normal do navegador: primeiro gesto ativa música/efeitos, controles indicam estado real, toque/teclado retomam o contexto e escolhas explícitas de efeitos/mudo são preservadas.

## Verificação
- Pose frontal aprovada na prévia local1600×900/915×412; sem colisão com título/carro ou corte de boné.
- Auditoria de176assets e16vistas/pivôs aprovados: PASS; 24PNGs/metadados NPC e os demais sprites preservados.
- Node47/47: PASS. Regressões do primeiro toque, resume pendente, retomada sem troca de modo e escolha de mudo: RED→GREEN.
- Chromium154 com autoplay restrito: PASS por toque, Space e Enter. Música inicial passou de RMS0 para0,0444; motor e música medidos separadamente, nitro por controle real,13efeitos pontuais e3contínuos com saída não nula. Pausa congela o contexto, retomada mantém modo e mudo preserva silêncio. Gravação menu-live.webm e JSON em work/audio-debug/live-final-complete no ambiente.
- Fluxo servido localmente até corrida natural/pódio passou em915×412 e740×360, com24arquivos aprovados conferidos por hash. Testes UI/seis vencedores e18renders offline de pódio também passaram. Revisão independente sem achados materiais.
- Pacote local e publicação HTTPS: PASS; ver registro público abaixo.
- Medição do sinal usa o grafo de saída real, com gravação do áudio sintetizado pelo próprio jogo; não grava microfone. Android físico, alto-falante do telefone e volume do sistema não são testados neste ambiente.

## Verificação pública da pose frontal e do áudio — PASS

- URL: https://andrervarella.github.io/FTW-Race/teste-v4/.
- Código verificado `54a422c7ac6c8ed9037a35b29d1462846914c914` (local `db1149f10f704260b71749cd402aa53b6827bb5b`, árvore `03e37dac8be051b4d60da3615343725131506f54`); Pages `a5284638a65901cdd9b55e6ede19b17c572f65b3`, árvore `0c083370ff8185f075631c2db5fc1cc1adbda393`. Implantação Pages41507467319: success.
- [Run 41507715470](https://github.com/andrervarella/FTW-Race/actions/runs/41507715470): **success** nas etapas de corrida completa, áudio ao vivo e upload. Chromium141.0.7390.37 independente em915×412 e740×360 com movimento reduzido.
- Artifact13171512175, ZIP SHA256 `e44fe94c2e12608b336ca79fa2ba962a6e527c67dcbeec633acd67b3c232347e` (2962648bytes). Baixado; hash, CRC e caminhos de extração conferidos. Summary/2relatórios de fluxo e summary de áudio PASS;13capturas presentes. Capa nos dois tamanhos e seleção inspecionadas visualmente; Felipe frontal somente na abertura.
- Cada viewport conferiu24hashes/dimensões de arte aprovada, incluindo o novo retrato,16poses e os2logos originais. Os4atlases NPC com seis vistas carregaram. Corrida natural completa, seis resultados reais, pódio do Rival Roxo, replay, ambos pilotos, multitouch, pausa e orientação passaram. Zero erros JS/console, HTTP, requests falhos ou caminhos fora de teste-v4.
- Áudio com autoplay restrito e sem a opção mute do runner: primeiro toque manteve `tudo` e produziu música (RMS0.05496); Space/Enter também passaram. Motor isolado RMS0.05947, música de corrida RMS0.00226; nitro por toque real,13efeitos pontuais e3contínuos (pneus/cascalho/vento) com sinal não nulo. Retomada preserva modo; pausa suspende o contexto e mudo permanece silencioso. Gravação `audio-live/menu-live.webm` (16718bytes) preservada no artifact; sem acesso ao microfone.
- Local/pacote: Node47/47,176hashes,16vistas aprovadas, fluxo natural e suites UI/áudio offline/ao vivo PASS. Revisão independente sem achados materiais. Os46arquivos anteriores de Pages mantêm SHA/modo/tipo; publicação restrita a teste-v4; main e a fonte Claude preservadas.
- Limite: emulação móvel Chromium e medição do grafo real de áudio; Android físico, alto-falante/volume do aparelho e FPS real não testados. O primeiro gesto é exigido pelo navegador. Fechamento seguinte altera apenas documentação.

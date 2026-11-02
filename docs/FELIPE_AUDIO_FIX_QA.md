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
- Pacote e publicação HTTPS: em andamento; registrar evidência real após conclusão.
- Medição do sinal usa o grafo de saída real, com gravação do áudio sintetizado pelo próprio jogo; não grava microfone. Android físico, alto-falante do telefone e volume do sistema não são testados neste ambiente.

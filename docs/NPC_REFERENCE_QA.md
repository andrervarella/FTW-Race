# QA da atualização de carros NPC — 02/11/2026

Estado local antes da publicação: PASS.

- Node24:45/45 asserções; cinco novas cobrem seis vistas, histerese, carros oficiais preservados, preload PNG e freio real de jogador/IA com pausa.
- Verificador de assets: quatro atlases,24 frames distintos, alpha real0/255, dimensões/pivôs completos, sem corte de espelhos/rodas; curvas não são imagens espelhadas; freios em curva mantêm exatamente o alpha da vista normal.
- Phaser real/Chromium154,915×412: todos os quatro NPCs exibidos em cada um dos seis estados; proporção560/512 e ponto de apoio470/512 confirmados; posições projetadas idênticas entre estados. Capturas inspecionadas em `work/qa-npc-reference/` do ambiente de execução.
- Produto servido localmente em `/game/`: PASS em915×412 e740×360 com movimento reduzido. Os quatro atlases foram carregados; corrida natural até resultados/pódio, multitoque, pausa/retorno e rotação passaram sem erro JS/HTTP/404 ou pedido fora da subpasta. Chromium154.0.8037.57. A primeira execução da checagem confundia a URL `blob:` interna do Phaser com o caminho HTTP; o teste foi corrigido para verificar as requisições reais, dimensões e seis frames. Nenhuma correção do produto foi necessária.
- Pacote `/teste-v4/` e publicação HTTPS: em andamento; registrar o resultado real após conclusão.
- Android físico e FPS no telefone: não testados. Aparência derivada da referência e novas vistas sujeitas à revisão do proprietário.

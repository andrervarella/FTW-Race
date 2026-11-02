# QA da atualização de carros NPC — 02/11/2026

Estado local antes da publicação: PASS.

- Node24:45/45 asserções; cinco novas cobrem seis vistas, histerese, carros oficiais preservados, preload PNG e freio real de jogador/IA com pausa.
- Verificador de assets: quatro atlases,24 frames distintos, alpha real0/255, dimensões/pivôs completos, sem corte de espelhos/rodas; curvas não são imagens espelhadas; freios em curva mantêm exatamente o alpha da vista normal.
- Phaser real/Chromium154,915×412: todos os quatro NPCs exibidos em cada um dos seis estados; proporção560/512 e ponto de apoio470/512 confirmados; posições projetadas idênticas entre estados. Capturas inspecionadas em `work/qa-npc-reference/` do ambiente de execução.
- Produto servido localmente em `/game/`: PASS em915×412 e740×360 com movimento reduzido. Os quatro atlases foram carregados; corrida natural até resultados/pódio, multitoque, pausa/retorno e rotação passaram sem erro JS/HTTP/404 ou pedido fora da subpasta. Chromium154.0.8037.57. A primeira execução da checagem confundia a URL `blob:` interna do Phaser com o caminho HTTP; o teste foi corrigido para verificar as requisições reais, dimensões e seis frames. Nenhuma correção do produto foi necessária.
- Pacote `/teste-v4/` e publicação HTTPS: PASS; evidência detalhada abaixo.
- Android físico e FPS no telefone: não testados. Aparência derivada da referência e novas vistas sujeitas à revisão do proprietário.

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

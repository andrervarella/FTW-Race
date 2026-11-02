# QA browser V4 — evidências reais

Build fonte editável servida em `http://127.0.0.1:8765/game/`. Navegador Chromium **154.0.8037.57**, Playwright Python, Phaser local **3.90.0**, renderer WebGL. Scripts executados com permissão para Chromium; nenhum asset ou API externa necessário.

**Resultado:** fluxo funcional aprovado em navegador desktop e Android **emulado**. Nenhum Android físico disponível. Arte nova continua em revisão; estes testes não aprovam fidelidade de rostos, patrocínios ou carroceria.

## Passou

- `full_browser.py`: **27/27** comportamentos. Main real com Phaser, título inicial; Daniel #22 verde e Felipe #25 vermelho; seleção apenas2 opções; grid seis; countdown natural; teclado acelera; pausa congela tempo; reinício com mesmo piloto; trocar piloto e capa.
- Corrida completa de1 volta no main real: simulação executada em tempo real sem atribuir vencedor/tempo e sem hooks de produção. Bandeirada ocorreu naturalmente; seis linhas classificadas e não concluintes sem tempo inventado. Pódio avançou naturalmente por seis estados, inclusive spray de24 gotas. Revanche voltou ao grid de Daniel.
- Android emulado **915×412**, hasTouch+isMobile+UA Android: **três pointers CDP reais** em esquerda+acelerador+nitro; feedback held nos3; nitro consumiu só1 carga durante hold; touchCancel liberou3; blur pausou e limpou input; vertical412×915 exibiu instrução e pausou; retorno horizontal permitiu CONTINUAR.
- `game/tests/ui-flow.py`: fluxo DOM, stale double-confirm, multi-pointer cancel/lostcapture, teclado, reduced motion e resultados/pódio dos seis vencedores **PASS**.
- `winner_browser.py`: seis vencedores (`daniel`, `felipe`, azul/amarelo/roxo/prata), **36 poses** carregadas; ranking vencedor correto, seis linhas, cinco não concluintes sem tempo; imagens e src correspondentes, champagne visível em stage4 e replay/troca/capa. Sem erro de execução ou404 nessa fixture. Layout móvel resultados e pódio capturado.
- `game/tests/v4-live.py` em cache novo final: **915×412 normal PASS**, **740×360 reduced PASS**. Phaser real, aceleração por toque, dois pointers/release, pausa/resume, portrait, ambos pilotos, volta à capa. **Zero pageerrors, console errors, HTTP404, requestfailed ou requests fora de `/game/`**.
- `?q=baixa`: Phaser real inicializou, pool deFX limitado a18 e diagnóstico vazio **PASS**.
- Redução de movimento desativa piscar no título, transição do campeão e animação das gotas; seis poses permanecem sequenciais e legíveis.

## Observações e retestes

A primeira rodada longa carregou a página antes da reorganização final de assets e tentou `assets/legacy/horizon.png` ao voltar à capa após o arquivo ser removido. Também houve404 do favicon automático, que não aparece no evento Playwright response. Esses achados foram reportados; a fonte atual usa `v4/cascavel/title-straight.png`/horizon e favicon explícito. **Ambos os layouts foram retestados em cache novo e passaram sem404 nem erros de console.** Relatórios antigos preservados para rastreabilidade, sem ocultar falhas transitórias.

Captura desktop inicial debug mediu aproximadamente **14FPS** neste Chromium headless com renderização software e warnings GPU `ReadPixels`. Isso é medição do ambiente de teste e **não comprova desempenho Android**. Sem crashes ou controles presos observados. UI desktop de seleção tem espaço amplo e pilotos relativamente pequenos nos cards; avaliação estética não bloqueante.

## Evidências

- Scripts: `/workspace/work/qa-v4/full_browser.py`, `winner_browser.py`, `network_debug.py`.
- Rodada final limpa: `/workspace/work/qa-v4/final/summary.json` e relatórios por viewport; screenshots title/select/grid/race/pause nos dois tamanhos.
- Corrida completa: `desktop-results.png`, `desktop-podium-0.png`, `desktop-podium-spray.png`, `desktop-podium-final.png`.
- Toque/vertical: `android-emulated-three-finger-nitro.png`, `android-emulated-portrait.png`.
- Seis vencedores: `winner-results.json`, `mobile-results-*.png`, `mobile-podium-*-{0,2,3,4,5}.png`.

**Não verificado:** Chrome Android físico, áudio ouvido em dispositivo, FPS/GPU no telefone, publicação HTTPS pública. Esta rodada cobre a fonte local; o pacote publicado precisa de teste independente após deploy.

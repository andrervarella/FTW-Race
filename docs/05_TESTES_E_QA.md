# QA — estado atual
Não há código executável, build ou testes de gameplay. Preparação documental não comprova desempenho.

## Matriz obrigatória durante produção
Registrar versão/commit, ambiente, passos, resultado PASSOU/FALHOU/NÃO TESTADO, evidência, correção e reteste.
- Abrir jogo, seleção dos dois pilotos e de cada pista.
- Controles: aceleração, freio, curva, entradas simultâneas, perda de foco e toque se aplicável.
- Largada sem movimento indevido; pausa sem avanço da corrida.
- Colisões, saída da pista, recuperação, limites e ausência de carros presos.
- Checkpoints em ordem, volta válida, posição, chegada e resultado.
- Reinício sem duplicar eventos/áudio nem preservar estado da corrida anterior.
- CPU ou segundo jogador conforme modo escolhido; não presumir teste de rede.
- Áudio após interação inicial, volume/mute e retomada.
- Carros sem deformações, sprites sem halos, HUD legível e circuitos distintos.
- Tamanhos/orientação de tela e dispositivo-alvo reais.
- Build reproduzível e logs; medir desempenho no alvo antes de declarar FPS.
- Playtest humano separado de testes automatizados.

## Critério de conclusão
Escopo acordado jogável, referências visuais respeitadas, assets existentes e integrados, build executado no alvo declarado e nenhuma falha crítica conhecida.
Pendências devem constar do relatório. Não usar imagens de referência como evidência de jogo funcionando.

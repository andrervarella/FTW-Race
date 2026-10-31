> Atualização prioritária — 31/10/2026: escopo atual somente Cascavel; fotos e prévias recebidas em referencias/ e assets/previews/. Leia docs/09_ENTREGA_VISUAL_E_CONTINUIDADE.md. Afirmações abaixo sobre duas pistas ou ausência de fotos são históricas e foram superadas. Não há jogo implementado nem sprites tecnicamente finalizados.

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

## Nitro Diabo Verde
Cobrir cargas, pressão contínua, duração, retorno à velocidade normal, pausa, reinício, chegada, colisão e regras iguais para ambos os pilotos. Quantidade provisória: duas ativações por corrida, pendente de confirmação. Todos esses testes ainda NÃO TESTADOS.

## Mobile obrigatório
Validar multitouch real: direção + aceleração + nitro; pointer/touch cancel; soltura fora do botão; perda de foco; interrupção e retomada; ausência de comandos presos; áreas seguras/notch; proporções de tela e botões sem cobrir pontos de frenagem. Teclado/emulação não comprovam teste no aparelho. Registrar aparelho, sistema, navegador/build e desempenho medido.

# Teste V3 — FTW Race com seis corredores

## Funcionalidades implementadas
- Daniel e Felipe continuam selecionáveis, com fotos/logos originais preservados.
- Quatro novos rivais IA com perfil de velocidade levemente diferente; total seis carros, posição e minimapa de 1–6.
- Colisão por pares e detecção de vencedor entre todos os participantes, com contagem de voltas.
- Quatro sprites SVG próprios de um mesmo hatch esportivo, azul/amarelo/roxo/prata, **provisórios e sem logos FTW/Diabo Verde**. Não são representações oficiais exatas do Mercedes AMG A45.
- Preservados direção, áudio, nitro, cenário e controles da versão anterior.

A lógica foi derivada do próprio simulador já existente no repositório. **Nenhum código, música ou imagem de terceiros foi importado nesta etapa**. Referências para futuras melhorias: docs/REPOSITORIOS_PUBLICOS_E_POLITICA.md.

## Verificação
- Simulação JavaScript executada pelo agente por 12 segundos com 6 carros e estado numérico finito.
- Suite nova em game/tests/v3-traffic.test.js, executar com cd game && npm test.
- Navegador real com Phaser, FPS em Android, tela horizontal, áudio e toque devem ser testados; NÃO afirmar validação desses itens sem executar.
- Prévia planejada em /FTW-Race/teste-v3/ no gh-pages, separada das anteriores.

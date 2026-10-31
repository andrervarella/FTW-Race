# Entrega visual e continuidade — 31/10/2026
Esta etapa entrega referências, prévias e instruções. Nenhum código de jogo, build, áudio final ou playtest foi produzido. O pedido de concluir a preparação não transforma pranchas em sprites prontos.

## Identidade canônica
| Item | Daniel | Felipe |
| --- | --- | --- |
| Nome | Daniel Mencacci | Felipe Mencacci |
| Número | 22 | 25 |
| Carro | Mercedes AMG A45 verde-lima | Mercedes AMG A45 vermelho |
| Macacão | Preto/branco/verde-lima | Vermelho/branco/verde-lima |
| Sem capacete | Barba e boné preto nas referências | Rosto conforme fotos, cabelo escuro |
| Capacete | Branco e vermelho, inferior na foto dupla | Azul com branco/vermelho/verde, superior na foto dupla |

Na foto de pilotos em pé sem capacete, Daniel é o da esquerda; na dupla com capacetes, é o da direita. Usar rodas pretas conforme referências da etapa Cascavel. Fotos com rodas brancas ou Street Fighter documentam variantes; não misturar pinturas aleatoriamente. Não usar rostos de pessoas que apareçam em montagens promocionais como referência dos pilotos.

## Pacote e hierarquia
- 16 PNG originais de geração, incluindo 3 estudos arquivados, em assets/previews/.
- 24 fotos/mapas selecionados, sem cópias idênticas, em referencias/.
- Manifesto registra nomes de origem, dimensões das prévias, bytes e SHA-256.
- Fotos do usuário prevalecem sobre pequenos erros de logos, rostos e detalhes nas gerações.
- Prévias de carros/pilotos são base visual; UI, arquitetura e FX são propostas de acabamento sem aprovação final individual registrada.
- O vídeo de Top Gear e o prompt mestre original permanecem no repositório como contexto histórico.

## Limitações reais dos PNG
Pilotos e FX contêm fundos/halos; solicitar transparência na geração não garantiu alpha útil. Mesmo PNG com canal alpha precisa de inspeção sobre fundos claros e escuros.
As variantes de curva em arquivo/ são próximas dos ângulos fortes existentes; não são intermediários suaves confiáveis. Não espelhar textos ou números. A tentativa de recorte de Felipe fica arquivada, não preferencial.
As pranchas de carro exigem separar vistas, alinhar rodas/solo e igualar escala. Não deformar carro para fingir giro.
Cenários são conceitos artísticos, não levantamento de engenharia.
A interface é só referência de composição: minimapa desenhado NÃO representa o traçado validado; retratos têm diferenças, usar os pilotos originais do pacote; título não é logo oficial; 1/3 voltas e raio de nitro são placeholders.
FX são estudos de quatro famílias, não sequência temporal testada.

## Contrato para derivados no Codex
Preservar originais. Exportar derivados em assets/sprites/ com manifesto: origem, vista/estado, dimensões, retângulo útil, pivô normalizado, ponto do solo, escala, frames, duração e licença/procedência.
Começar pelo par de carros traseiros em escala de jogo. Fixar altura aparente e ponto do solo. Validar numa cena antes de exportar todos os estados.
Pilotos: com e sem capacete para ambos, retratos e corpo inteiro conforme uso. Não inventar animação de consumo antes de receber a lata.
Carros: reta e curvas existentes; revisar necessidade de intermediários; definir frenagem/nitro sem alterar pintura.
FX: recortar/reconstruir transparência, ordenar frames, ajustar emissão, limitar densidade. Manter pista/adversário visíveis.
Inspecionar sobre preto, branco e asfalto, em resolução nativa e escala final. Rejeitar halos, serrilhado excessivo, sombras duplicadas e saltos de pivô.

## Cascavel
Somente Autódromo Internacional Zilmar Beux, Cascavel. Usar mapa esquemático e satélite como fontes para traçado; fotos para boxes, área de escape, cercas, vegetação e arquibancadas.
Traçar centro da pista como curva fechada; registrar largada, sentido, entrada/saída de boxes e checkpoints ordenados. Conciliar orientação dos mapas. Não inventar comprimento, elevação ou raio como medida oficial.
Procedural moderado autorizado: projeção/malha da estrada, faixas, zebras, repetição de cercas/barreiras e distribuição discreta de vegetação. Usar distribuição determinística e exclusões de segurança em pista/escape/visibilidade.
Preservar o prédio longo dos boxes, arquibancadas, mata e caráter do entorno. Evitar floresta uniforme, prédios aleatórios ou excesso de objetos.
Não randomizar o traçado a cada corrida. Minimap deve derivar da mesma geometria dos checkpoints.
Os conceitos de curvas não substituem o mapa. Elevações só como adaptação identificada até haver medidas verificadas.

## Interface e estados a implementar
Título/início → seleção Daniel/Felipe → largada → corrida → resultado/revanche, com pausa/retomar e retorno ao menu.
HUD vivo: posição, volta, tempo, velocidade e nitro. Textos e contadores renderizados pelo jogo, não incorporados em PNG.
Proposta horizontal, direção à esquerda e acelerador/freio/nitro à direita. Garantir toque simultâneo, cancelamento, foco, áreas seguras e pausa sem avançar simulação.
Número de voltas, duas cargas de nitro e localização final dos controles são parâmetros provisórios.
Implementar os estados de pausa/resultado como componentes coerentes com o mockup; não são pranchas adicionais já entregues.

## Dependências e sequência
1. Preparar e validar assets e traçado sem depender de escolha de publicação.
2. Resolver distribuição/sistemas, modo de disputa e engine. Autorização procedural da pista não equivale à aprovação automática de Canvas/WebGL.
3. Construir fatia jogável completa em Cascavel, com os dois pilotos.
4. Integrar nitro conforme docs/07; usar placeholder explicitamente identificado até a lata e logos chegarem.
5. Produzir áudio próprio/licenciado, testar gameplay e mobile, corrigir e entregar build com evidências.

Ainda dependem do usuário: lata Diabo Verde e logos originais. Ainda dependem de implementação: todos os sprites derivados, animações, física, áudio, interface funcional, testes e build.

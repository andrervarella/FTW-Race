> Atualização prioritária — 31/10/2026: escopo atual somente Cascavel; fotos e prévias recebidas em referencias/ e assets/previews/. Leia docs/09_ENTREGA_VISUAL_E_CONTINUIDADE.md. Afirmações abaixo sobre duas pistas ou ausência de fotos são históricas e foram superadas. Não há jogo implementado nem sprites tecnicamente finalizados.

# Nitro Diabo Verde — requisito e proposta
## Confirmado
Durante a corrida, um efeito de nitro aumenta a velocidade, associado ao piloto tomando Diabo Verde pré-workout em lata.
O usuário enviará imagens da lata, logo FTW e logo Diabo Verde. Ainda não recebidas.
É um power-up fictício de jogo, não uma descrição do efeito real do produto.

## Ambiguidade a preservar
O usuário disse “duas opções”. A interpretação de trabalho é DUAS ATIVAÇÕES POR CORRIDA, ainda não confirmada. Não apresentar essa quantidade como decisão do usuário; confirmar ao fechar o gameplay.
Não deduzir duas bebidas, dois produtos ou duas modalidades distintas.

## Regras propostas para protótipo (ajustáveis, não aprovadas)
- Mesma disponibilidade inicial para ambos os pilotos; inicialmente duas cargas conforme hipótese acima.
- Botão de nitro somente durante corrida ativa, sem bloquear direção.
- Uma pressão válida consome uma carga; segurar não deve consumir as duas.
- Aumentar temporariamente aceleração e limite de velocidade; depois retornar suavemente aos valores normais.
- Duração e intensidade configuráveis, a calibrar em playtest; não fixar números como especificação aprovada.
- Bloquear reativação enquanto efeito estiver ativo; não empilhar efeitos.
- Sem recarga/coleta/compras de latas presumidas.
- Pausa congela duração; reinício restaura cargas; chegada encerra o efeito.
- CPU, se escolhida, respeita as mesmas regras e limites.
- Colisões e limites da pista continuam funcionando durante o nitro.

## Apresentação proposta
Feedback curto com lata/gesto de consumo pelo piloto, contador de cargas no HUD, som próprio e sensação visual de aceleração. Não interromper a condução com uma cena longa.
Usar câmera/partículas moderadas sem esconder pista, adversário ou pontos de frenagem.
A forma exata da animação será definida após referências e direção visual.

## Assets
Guardar imagens originais em referencias/marcas-e-produto/.
Preservar formato, cores, rótulo e logos fornecidos. Não redesenhar logos nem inventar embalagem.
FTW e Diabo Verde fazem parte da referência solicitada; localização dos logos no carro/pista/menu ainda não definida.
Não presumir patrocínio real nem substituir pinturas reais dos carros por uma pintura inventada.

## Aceitação futura
Testar ativação única, consumo correto, limite zero, duração, transição de velocidade, pausa, reinício, colisões, chegada, inputs simultâneos e igualdade de regras entre pilotos.
Verificar arte contra referências oficiais. Registrar desempenho e evidências reais. Estado atual: NÃO IMPLEMENTADO / NÃO TESTADO.

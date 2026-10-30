# GDD inicial — rascunho para produção
## Conceito
Escolher Daniel ou Felipe Mencacci e disputar uma corrida arcade com Mercedes identificáveis, em pistas inspiradas em Cascavel e Interlagos, com leitura visual de Top Gear.

## Pilares propostos
Direção simples e responsiva; sensação clara de velocidade; rivalidade reconhecível entre os dois pilotos.

## Loop proposto, ainda ajustável
Escolher piloto → escolher pista → largar → acelerar, frear e contornar curvas → disputar posição → completar voltas → resultado → revanche.
Sugestão de fluxo: título → seleção de piloto → pista → corrida → resultado, com pausa, reinício e retorno ao menu.

## Regras a detalhar antes da implementação
- Comandos por dispositivo; aceleração manual/automática, freio e direção.
- Movimento longitudinal/lateral e perda de velocidade fora da pista.
- Colisão com adversário e barreiras, intensidade e recuperação sem travamentos.
- Contagem de voltas por linha de chegada e checkpoints ordenados; impedir atalhos/reversão de contagem.
- Ordem por volta + progresso real ao longo do circuito.
- Vitória após voltas configuradas; empate definido, resultado consistente e reinício completo.
- CPU, se escolhida: mesmos limites essenciais, trajetória e velocidade explicáveis; evitar teletransporte ou vantagem oculta.
- Multiplayer exige definição prévia do dispositivo e modo.

## HUD proposto
Posição, volta, tempo e velocidade legíveis; minimapa útil. Elementos observados no vídeo não são requisitos automáticos.
Nitro Diabo Verde em lata aprovado; regras em 07_NITRO_DIABO_VERDE.md. Duas ativações por corrida são hipótese provisória. Combustível, marchas e pit stop dependem de decisão de escopo.

## Escopo por etapas
Primeira fatia proposta: um circuito, dois carros, uma corrida completa com início/fim, arte representativa e som.
Após validar: segunda pista e acabamento. O destino final previsto inclui Cascavel e Interlagos.
Não chamar a fatia de jogo completo se a segunda pista e demais itens prometidos estiverem pendentes.

## Critério de diversão a validar
É possível entender como dirigir rapidamente, perceber por que perdeu velocidade e disputar a chegada com vontade de tentar novamente.
Nenhum playtest humano realizado até agora.

# NPCs V4 — referência enviada pelo proprietário

O proprietário determinou que os quatro carros sigam a prancha enviada: azul, amarelo, branco/prata e roxo, mesma carroceria A45, aerofólio preto com dois suportes, gaiola em X, lanternas vermelhas, painel traseiro sem placa/marcas, duas saídas ovais de escapamento e gancho vermelho no lado direito do veículo.

A imagem está acessível ao modelo como referência visual do chat, mas não foi disponibilizada ao executor com arquivo/ID/URL para copiar seus bytes. `image_gen` editou diretamente essa referência (entre as cinco imagens recentes), criando a prancha `assets/previews/v4/npc-cars-views-generated.png`. Trata-se de derivação visual, não de extração byte a byte do anexo original. A prancha gerada foi comparada visualmente com a referência e preserva os elementos acima. As novas vistas ainda podem ser revisadas pelo proprietário.

## Arquivos entregues
- Quatro atlases PNG em `game/assets/v4/cars/npc-raster/`, um por cor.
- Vinte e quatro PNGs individuais em `npc-raster/frames/<equipe>/`.
- Seis estados por carro: rear, left, right, brake, left-brake e right-brake.
- `game/assets/v4/cars/npc-cars.json`: origem, SHA256, crops, escala, pivôs, nomes/índices dos frames e identificação dos SVGs aposentados.
- Scripts reproduzíveis: `game/scripts/prepare-npc-reference.py` e `verify-npc-reference.py`.

## Preparação técnica
A prancha original gerada foi preservada. Alpha abaixo60 foi removido, bordas restantes ficaram opacas para pixels nítidos e pequenos artefatos desconectados foram excluídos. Usada uma escala única330/230 para todas as equipes/poses. O centro entre as lanternas orienta a posição do eixo traseiro; o ponto de apoio fica em x280/y470 num frame560×512. O canvas mais largo permite a vista em perspectiva sem cortar espelhos ou rodas. O render compensa560/512 na largura para preservar o tamanho físico e a proporção relativa aos dois carros oficiais.

Os atlases têm1680×1024, seis frames3×2 e uma única paleta256 por equipe, evitando variação de cor entre estados. Os três primeiros estados e a frenagem traseira são desenhos distintos da prancha gerada. Frenagem esquerda/direita altera somente luminosidade das lanternas das respectivas vistas: contorno/alpha, posição e carroceria permanecem iguais. Nenhuma vista foi espelhada ou simulada girando/deformando o carro.

O runtime carrega os PNGs, não os antigos SVGs. Esses arquivos antigos permanecem apenas como histórico. `vehicle-visual.js` seleciona as vistas com limiares de volante0,6/0,25 para evitar oscilações; `sim.js` expõe `braking` a partir do freio efetivamente aplicado ao jogador e à IA, sem modificar física, colisões ou resultados.

As fotos, rostos, pinturas e logos dos protagonistas não foram modificados nesta tarefa. Cascavel, seis corredores, nitro e o pódio existente foram preservados. Não foi usado nenhum asset de Top Gear ou de outros jogos comerciais.

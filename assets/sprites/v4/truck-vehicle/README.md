# Caminhão FTW — pacote de arte para revisão

Arte proposta: cavalo simples 4x2, dois eixos, sem carreta. Todas as imagens
aguardam revisão do proprietário. Nenhum arquivo representa master aprovado.
Conferir fotos e marcas do dono: cabine vermelha, Diabo Verde no para-brisa,
FTW nas portas; traseira convencional sem grafismos de patrocinador inventados.

## Reprodução portátil

Requer Python 3.10+, Pillow, NumPy e SciPy (`python -m pip install -r requirements.txt`).
Na pasta deste pacote, executar:

    python prepare.py --source sources/generated-vehicle-sheet.png --front sources/front-proposal.png --car-reference sources/mercedes-reference.png --anchors sources/reviewed-anchors.json --output ../rebuilt-truck-art

O destino deve estar vazio e fora das pastas dos originais. O script nunca escreve
no repositório do jogo. Origens e JSON revisado são copiados byte a byte. ZIPs usam
metadados fixos; versão das bibliotecas pode mudar pixels de reamostragem e hashes.

## Contrato e transformações

Seis PNG RGBA 560×512 na ordem rear, left, right, brake, left-brake, right-brake.
Atlas 3×2, 1680×1024; chão y=470, pivô (0.5,0.91796875). rear_axle e ground_y
do JSON são coordenadas locais ao crop [left,top,right,bottom), em pixels da fonte.
O x do eixo é centralizado em x=280; o ground_y é levado a y=470. O eixo em si
permanece acima do chão. Um único fator de escala vale para todas as seis vistas.
Não há ajuste de tamanho por pose, espelhamento, rotação, deformação, recoloração
ou síntese. A frente de menu usa apenas aspect-fit, separado da escala de corrida.

A limpeza remove alpha 1–8 e componentes isolados muito pequenos (até 8–32 pixels,
limite registrado por crop). Componentes maiores exigem seleção explícita revisada.
Não há detector de vermelho nem nenhuma chave por cor. Pixels retidos são exatos
antes da reamostragem com alpha pré-multiplicado. Não se apagam sombras por cor.

## Revisão de crops e âncoras

Sem --anchors o script propõe crops, salva source-crop-review.png e
proposed-anchors.json, e termina com status needs-review (exit 2). Preencher os
seis rear_axle [x,y] e ground_y, conferir todos os crops e hashes e definir
reviewed:true. Isso confirma somente pontos e limites técnicos, não aprova a arte.
Em caso de componentes desconectados, inserir keep_components:[IDs] no respectivo
crop; IDs/áreas/bboxes aparecem em qa-report.json. Todos os seis boxes explícitos
devem ser fornecidos juntos. A detecção automática só aceita um gutter horizontal
transparente e recupera o corpo inteiro na linha, inclusive cruzando divisores.
Ambiguidade de crops, partes ou âncoras interrompe a preparação, sem ZIP final.

## Escala e freio

O fator proposto de largura útil traseira é 1,4× o PNG da Mercedes. O encaixe
simultâneo das seis vistas reduz a razão nativa dentro do contrato 560×512;
valores solicitado/nativo e dimensões úteis estão em frames.json e qa-report.json.
A comparação principal mostra o PORTE FUTURO proposto na mesma profundidade:
Mercedes com fator de exibição1 e caminhão com um único multiplicador uniforme,
calculado como 1,4 × largura útil Mercedes / largura útil caminhão normalizado.
Esse fator preserva a proporção e vale igualmente para as seis vistas; não foi
incorporado aos PNG de corrida. Não é uma comparação de fatores de pixel iguais.
O runtime hoje força igual altura em igual profundidade: uma integração futura
precisa aplicar explicitamente esse fator de veículo; aumentar o canvas não basta.

Referência física apenas: ficha IVECO Chile 4x2, 6,252 m de comprimento, 2,55 m de
largura, 3,789 m de altura, entre-eixos 3,8 m. Esses números NÃO são medição do
caminhão FTW ou da Mercedes e não foram convertidos em unidades do jogo.

As poses de freio vêm da folha gerada, sem lâmpadas pintadas pelo script.
qa-report.json compara silhuetas, dimensões e altura do eixo de cada par, sinaliza
IoU <0,92, dimensão útil que varie >5% e eixo que varie >6 pixels. São critérios
de triagem, não aprovação visual. Não se afirma que somente lâmpadas mudaram.

## Arquivos

Abrir preview.html localmente: estados, freio e fundos; tudo está embutido.
contact-sheet-{black,white,asphalt}.png e same-depth-comparison.png são revisão
estática. source-crop-review.png mostra crops/âncoras. frames.json contém
proveniência e política; qa-report.json contém verificações e limites. SHA256SUMS
cobre o conteúdo do pacote; truck-vehicle-art.zip.sha256 cobre o ZIP separadamente.
Não há publicação, integração, alteração de runtime ou aprovação implícita.

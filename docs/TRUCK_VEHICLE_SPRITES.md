# Cavalo mecânico simples — sprites do veículo

## Direção e estado

O proprietário pediu apenas o caminhão, sem carreta/baú, com Diabo Verde no para-brisa e FTW na porta. Após a pesquisa de referências traseiras, respondeu “E um cavalo mecânico simples”. Foi comunicada e adotada a interpretação de cavalo de dois eixos4×2: um eixo dianteiro e um traseiro, pneus duplos atrás e chassi/quinta-roda descobertos. Isso não confirma ano/versão exatos da unidade. A família S-Way é uma identificação visual de trabalho.

A primeira vista frontal mantém cabine alta vermelha, teto preto, faróis/grade e marcas das fotos. A prancha traseira gera seis vistas do mesmo modelo numa única edição: reta, curva esquerda, curva direita e as três em frenagem. Não há logos traseiros inventados nem espelhamento de letras. Traseira é uma proposta técnica padrão baseada nas fontes de `TRUCK_REFERENCE_RESEARCH.md`; não é registro fotográfico confirmado de customizações ocultas. Todos os novos sprites do caminhão aguardam revisão visual do proprietário.

## Contrato de preparação

- Fontes geradas intactas em `assets/previews/v4/truck-vehicle/`, com hashes/aprovação em `sources.json`.
- Pacote técnico em `assets/sprites/v4/truck-vehicle/`; seis PNGs560×512, atlas1680×1024, chão470 e pivô(0.5,0.91796875). Uma única escala e translações por âncoras de eixo/piso conferidas; nenhum ajuste independente para encolher vistas, deformar chassi ou fingir curva.
- Freio é representado pelos quadros gerados de lanternas mais acesas. Vistas normal/freio são desenhos próprios; não se afirma igualdade pixel a pixel do restante da carroceria. Comparações de silhueta/dimensões são registradas na QA.
- Alpha≤8 e resíduos minúsculos destacados são removidos tecnicamente; não usar detector por cor vermelha, pois confundiria cabine com lanternas. Pixels visíveis retidos preservados até a reamostragem uniforme.
- Vista frontal/menu proporcional, pranchas em fundos preto/branco/asfalto, prévia HTML independente, originais, script portátil, hashes e ZIP.

## Porte relativo

O PNG maior, sozinho, não garante um caminhão maior no jogo: o render atual usa altura visual comum. Os arquivos devem registrar separadamente a escala de empacotamento e o fator uniforme de exibição proposto para largura traseira de aproximadamente1,4×a do Mercedes na mesma distância. A comparação usa esse fator em ambos os eixos do caminhão, preservando proporções. A futura integração precisa aplicar uma escala própria ao veículo; esta entrega não altera o render.

A ficha oficial chilena4×2 (6,252m de comprimento,2,550m de largura,3,789m de altura,3,800m entre-eixos) serve apenas de referência dimensional dessa versão. Não é medição do caminhão FTW nem confirmação de ano/modelo.

## Verificação

- Pipeline canônico executado com fontes/âncoras exatas: PASS. Seis PNGs/RGBA560×512, atlas1680×1024 pixel-exato, chão470/pivô comum e margens sem cortes. Escala comum1.00438596491; fontes originais e visíveis retidos preservados.
- Freio: IoUs de silhueta0.99594/0.99241/0.99321, diferenças de altura útil0–1px, mesma altura do eixo, sem flags materiais. Não se afirma diferença somente nas lanternas.
- Porte proposto: fator uniforme futuro1.71681957187, largura efetiva na comparação1.401496×Mercedes, altura útil analítica2.382737×. Imagem1586×968, mesma linha de chão831; sem deformação ou corte. Isso não foi aplicado ao runtime.
- Revisão visual e QA independente de arquivos/script/fontes/atlas/freio/escala: sem achados materiais. Frente mantém marcas nas posições das fotos; traseira convencional não inventa patrocínios.
- Chromium154.0.8037.57 local: PASS em915×412 e430×932 com movimento reduzido. Os seis estados selecionados conferem os pixels dos PNGs; frente e comparação também. Fundo claro/escuro/asfalto, alternar/parar freio e layout sem overflow passaram; zero errosJS/HTTP. Evidência em `work/truck-vehicle-art/browser-qa/` no ambiente.
- ZIP14487122bytes, SHA256 `36e1cddbfdc48bc83fbbcc6c2867c6d4e1297f23cd2bbd9856611e68dbc02e82`; CRC/caminhos/checksums verificados. Extraído e reexecutado usando o script do próprio pacote: PNGs, frente, atlas, comparação, contatos, HTML, metadata e o ZIP inteiro ficaram byte-idênticos. PASS.
- Sem reteste de corrida/áudio, publicação, novo competidor ou mudança de `game/src`, `game/assets`, HTML/CSS do jogo. Arte e proporção final aguardam revisão do proprietário; não houve teste em Android físico.


## Atualização de integração — 03/11/2026

Após apresentação do pacote, o proprietário respondeu “Otimo” e pediu aplicar tudo ao game, nomeando Marquinhos para capa e seleção jogável. O material preparado é aceito para esse uso; os avisos de revisão e ausência de integração acima descrevem a entrega histórica anterior. A aceitação não confirma medidas, ano, versão ou customizações traseiras não fotografadas. A integração usa IVECO4×2 sem carreta, seis estados e escala uniforme proposta, mantendo as marcas nas posições documentadas. A referência dimensional pública permanece comparativa.

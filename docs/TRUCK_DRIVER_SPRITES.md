# Novo motorista — pacote de sprites

## Referência e escopo

Em03/11/2026 o proprietário aprovou a imagem `master-approved.png` com: “Ótimo. Essa última ficou perfeita. Ela é a referência.” Essa aprovação cobre rosto, corpo e roupa da base: boné vermelho Mercedes, óculos escuros, polo vermelha/gola preta/FTW nova, jeans claro, tênis cinza, braços moderados, pernas mais finas e pequena barriga. Nome ainda não confirmado; chave técnica `truck-driver`.

O conjunto equivalente necessário é a pose neutra e o retrato da base, mais seis poses genuínas de pódio: `entry`, `receive`, `raise`, `open`, `spray`, `final`. O boné é mantido em todas. A variante de capacete dos oficiais não tem uso em `game/src` e não corresponde à orientação deste personagem.

## Arquivos e uso

- Originais preservados em `assets/previews/v4/truck-driver/`, com SHA256 e aprovação em `sources.json`.
- Derivados técnicos e prévia em `assets/sprites/v4/truck-driver/`.
- Pipeline reprodutível em `game/scripts/prepare-truck-driver-sprites.py`.
- Os corpos devem usar256×512RGBA, chão500 e pivô(0.5,0.9765625). As seis poses usam a mesma escala; a neutra tem altura anatômica equivalente à entrada. Retrato é um recorte técnico da base, sem recriar rosto.
- Tempos previstos:1200,1400,1300,1400,2200ms e último quadro mantido. Gotas/espuma são efeitos separados, não incorporados aos corpos. A boca da garrafa do spray aponta para a direita/acima; `frames.json/effects` registra âncora medida em pixel/normalizada e vetor de direção para a integração futura.

## Aprovação e integração

A base está aprovada; as seis poses derivadas estão em revisão visual, não herdam aprovação automática. Nenhum caminhão, novo competidor ou registro jogável foi integrado nesta etapa. Os sprites de Daniel/Felipe/NPCs, corrida, áudio e versão publicada permanecem preservados.

## Verificação desta entrega

- Sete corpos PNG/RGBA256×512, seis poses distintas, alpha real e chão500/pivô: PASS. Escala comum das seis poses0.67217630854; altura anatômica neutra/entrada403.31px. Sem cortes; a taça final fora da célula nominal foi preservada por componente conectado da linha inteira.
- Originais e pixels visíveis retidos preservados; removidos apenas resíduos de alpha≤8 e pequenos componentes destacados. Nada de chavear vermelho/azul ou girar membros. Retrato512×640 recortado da base; WebP decodificado idêntico ao PNG. Atlas1792×512 contém os sete corpos exatamente.
- Revisão independente de geometria/hashes/reconstrução e revisão artística da prancha: sem achados materiais. Apenas o proprietário pode aprovar a fidelidade das novas poses.
- Chromium154.0.8037.57 local: PASS em915×412 e430×932 com movimento reduzido. Seleção nativa das seis poses conferiu os pixels reais, fundos claro/escuro, reprodução/pausa/final mantido, sem overflow/errosJS/HTTP. Evidência em `work/truck-driver-art/browser-qa/` no ambiente. A primeira execução teve erro de sintaxe num seletor do roteiro de QA; corrigido e retestado, sem alteração no produto.
- ZIP completo7347358bytes, SHA256 `94ccf286523ab966056479f9083cd6524b1963ee4ae45e3cd1287879c66bb796`. CRC/caminhos/checksums verificados. Extraído e reproduzido usando o script e fontes contidos no próprio ZIP: sete PNGs, retrato, atlas, contato e HTML byte-idênticos; âncoraFX reproduzida. PASS.
- Não houve reteste de corrida/áudio, publicação ou integração: nenhum arquivo de `game/src`, `game/assets`, HTML/CSS do jogo foi alterado. Android físico e fidelidade final das novas poses não testados/aprovados.

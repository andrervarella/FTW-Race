# Sprites do piloto do caminhão

Abra `preview.html` para conferir as seis poses, o retrato e a referência em fundos diferentes. O arquivo funciona sem conexão. `contact-sheet.png` reúne as oito imagens.

`neutral.png` e `podium-0.png` a `podium-5.png`: PNGs transparentes 256×512, chão500 e pivô(0.5,0.9765625). O atlas contém os sete corpos sem alterar seus pixels. Retrato em PNG/WebP sem perdas. Estados e tempos em `frames.json`.

A referência original foi aprovada pelo proprietário. As seis poses novas aguardam revisão visual. O boné vermelho Mercedes permanece em todas. Não há caminhão ou integração jogável neste pacote. Gotas de champanhe são efeitos separados; `effects` registra a boca da garrafa e sua direção.

Os originais estão em `sources/`, intactos. `SHA256SUMS` permite conferir os arquivos. Para reproduzir tecnicamente (Pillow, NumPy e SciPy), use outra pasta de saída:

```sh
python prepare.py --base sources/approved-master.png --sheet sources/generated-podium-sheet.png --anchors sources/reviewed-anchors.json --output ../truck-driver-rebuilt
```

# QA — pilotos e capa aprovados

O proprietário aprovou as duas âncoras de rosto, as duas pranchas de oito poses e, separadamente, a capa com os logos oficiais. Integração na branch exclusiva `codex/ftw-race-v4-arcade`; somente `/teste-v4/` será atualizado após verificação.

- Node45/45: PASS;16recortes de corpo inteiro,12poses de pódio oficiais, origem/hash, alpha binário limpo, escala0,70 e pés y500/512: PASS.
- Verificador independente confirma24PNGs/metadados NPC intactos. PNGs FTW/Diabo Verde idênticos aos originais; cinco WebPs validados por hash/dimensões, com igualdade dos pixels redimensionados para rostos/carros.
- Revisão independente sem achados materiais: navegação, descarte de ResizeObserver, botão antigo desconectado, URLs relativas, escala/pivôs e logos conferidos.
- Chromium local: título em1600×900,915×412,740×360 e568×320; controles físicos≥44px e textos funcionais≥14px; teclado, áudio, tela vertical, ida/volta seleção e seis vencedores no fixture: PASS. Capturas em `work/pilot-art-review/production-title-*.png` no ambiente.
- Produto servido localmente: PASS em915×412 e740×360 com movimento reduzido, Chromium154.0.8037.57. Cada viewport confirmou23hashes/dimensões reais (16poses,5camadas da capa e2logos). Uma corrida terminou naturalmente com Rival Roxo e exibiu os seis resultados/pódio correto; zero erros JS/HTTP/404, requisições falhas ou caminhos fora da subpasta.
- Regressão de champanhe: o teste RED reproduziu saída no ponto antigo para Daniel; âncoras passaram a(185,165) e(43,139) nos frames256×512, com spray para direita/esquerda respectivamente. Fluxo UI completo GREEN, incluindo todos os seis vencedores, foco/pausa e redução de movimento. Revisão independente confirmou as posições contra os PNGs; NPCs preservados.
- Pacote de distribuição e verificação HTTPS: PASS; evidência detalhada abaixo.
- Limites: testes em Chromium móvel emulado; Android físico, FPS do telefone e áudio ouvido no aparelho não testados. Arte dos rivais mantém seu estado anterior de revisão.

## Verificação pública dos pilotos e capa aprovados — PASS
- URL: https://andrervarella.github.io/FTW-Race/teste-v4/.
- Código verificado `b458fdc15c9195e0d1eb6bf9324b6b8cd135e3a6` (local `419621ea8a7aa21d6633d70536d9521bdd2910ab`, árvore `79c9dffad408e5931639d57211764bd25ba4ecb8`), branch `codex/ftw-race-v4-arcade`; Pages `8ab5eeea74973743fabaa282ce06ced24cc63741`, árvore `b6b99da0264603fa5504016241e2d81b36e000f1`. Implantação Pages41497754131: success.
- [Run 41497991461](https://github.com/andrervarella/FTW-Race/actions/runs/41497991461): **success**, teste e upload do artifact. Chromium141.0.7390.37 independente em915×412 e740×360 com movimento reduzido.
- Artifact13168495437, ZIP SHA256 `2322b7c1379189b13d5eb69ff246065d85fd1c16043f3d307003c15b7f363c42`. Baixado, hash/CRC/caminhos de extração conferidos; summary e dois relatórios PASS.13capturas conferidas, com inspeção visual da capa e seleção publicadas.
- Cada viewport verificou23hashes/dimensões dos arquivos realmente servidos:16poses de pilotos,5camadas da capa e2logos originais. Os4atlases NPC com seis vistas também carregaram. Botão de início mantém alvo físico≥44px.
- Corrida natural de1volta terminou com Rival Roxo; resultados reais de seis carros e pódio correspondente, replay, ambos pilotos, toque simultâneo, pausa e orientação passaram. Zero erros de JavaScript/console, HTTP/404, requests falhos ou arquivos fora da subpasta.
- Pacote local idêntico passou pelo mesmo roteiro em Chromium154.0.8037.57. Node45/45,174hashes,16poses aprovadas,36quadros de pódio e24PNGs/metadados NPC preservados: PASS. Origem/direção do champanhe corrigidas com regressão RED→GREEN e verificadas em ambos os pilotos no fixture e em capturas do renderer real.
- Os46arquivos anteriores de Pages permanecem idênticos (SHA/modo/tipo); `main` e `claude/ftw-race-v0.2` preservadas. Aprovação humana cobre rostos, pranchas de pilotos e capa; outros derivados mantêm seu estado anterior. Android físico/FPS/áudio no aparelho não testados.
- Este fechamento final altera apenas documentação; o produto publicado permanece o que o run verificou.

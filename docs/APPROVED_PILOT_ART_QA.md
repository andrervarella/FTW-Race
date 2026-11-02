# QA — pilotos e capa aprovados

O proprietário aprovou as duas âncoras de rosto, as duas pranchas de oito poses e, separadamente, a capa com os logos oficiais. Integração na branch exclusiva `codex/ftw-race-v4-arcade`; somente `/teste-v4/` será atualizado após verificação.

- Node45/45: PASS;16recortes de corpo inteiro,12poses de pódio oficiais, origem/hash, alpha binário limpo, escala0,70 e pés y500/512: PASS.
- Verificador independente confirma24PNGs/metadados NPC intactos. PNGs FTW/Diabo Verde idênticos aos originais; cinco WebPs validados por hash/dimensões, com igualdade dos pixels redimensionados para rostos/carros.
- Revisão independente sem achados materiais: navegação, descarte de ResizeObserver, botão antigo desconectado, URLs relativas, escala/pivôs e logos conferidos.
- Chromium local: título em1600×900,915×412,740×360 e568×320; controles físicos≥44px e textos funcionais≥14px; teclado, áudio, tela vertical, ida/volta seleção e seis vencedores no fixture: PASS. Capturas em `work/pilot-art-review/production-title-*.png` no ambiente.
- Produto servido localmente: PASS em915×412 e740×360 com movimento reduzido, Chromium154.0.8037.57. Cada viewport confirmou23hashes/dimensões reais (16poses,5camadas da capa e2logos). Uma corrida terminou naturalmente com Rival Roxo e exibiu os seis resultados/pódio correto; zero erros JS/HTTP/404, requisições falhas ou caminhos fora da subpasta.
- Regressão de champanhe: o teste RED reproduziu saída no ponto antigo para Daniel; âncoras passaram a(185,165) e(43,139) nos frames256×512, com spray para direita/esquerda respectivamente. Fluxo UI completo GREEN, incluindo todos os seis vencedores, foco/pausa e redução de movimento. Revisão independente confirmou as posições contra os PNGs; NPCs preservados.
- Pacote de distribuição e verificação HTTPS: em andamento; registrar evidência real antes da entrega.
- Limites: testes em Chromium móvel emulado; Android físico, FPS do telefone e áudio ouvido no aparelho não testados. Arte dos rivais mantém seu estado anterior de revisão.

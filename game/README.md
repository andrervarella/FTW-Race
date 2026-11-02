# FTW Race — código-fonte do jogo

Este diretório foi sincronizado em 01/11/2026 com a implementação atualmente versionada em `gh-pages/claude/`. Antes, faltavam `src/ui.js` e `styles.css`, e a API de áudio em `src/audio.js` não correspondia à interface publicada. Os módulos agora estão reunidos para manutenção e continuidade pelo Codex.

## Verificação disponível
Na pasta `game/`, executar `npm test` (Node 18+). A suíte inclui testes de simulação e integridade dos módulos, imports, interface e configurações de pista. O teste automatizado não substitui execução com Phaser real e testes em aparelho.

## Publicação e recursos
Esta pasta contém código e CSS, mas não contém todos os PNG nem o bundle Phaser; as imagens e o módulo Phaser já estavam na branch `gh-pages`, pasta `assets/`. O caminho padrão em `src/main.js` (`../../assets/`) foi calculado para publicação em `gh-pages/claude/`. Ao hospedar a pasta `game/` em outro caminho, configure a URL de assets corretamente e disponibilize a biblioteca Phaser ou permita o fallback de CDN.

**Este commit não altera `main`, não publica uma nova versão e não demonstra funcionamento no Android.**

## Próximos cuidados
- Validar jogo real em Chrome Android (paisagem, toque simultâneo, áudio, colisões, nitro, carregamento).
- Confirmar sentido da pista de Cascavel com mapa e referência do circuito.
- Integrar novas melhorias em etapas, preservando retratos reais e marcas originais.
- Não usar sprites/músicas/código do Top Gear original.

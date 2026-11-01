# CLAUDE.md — contexto de continuidade do FTW Race

Leia primeiro: AGENTS.md, PROMPT_CODEX.md, README.md, docs/09_ENTREGA_VISUAL_E_CONTINUIDADE.md e docs/10_VERSAO_CLAUDE_V02.md.
Usuário: Brasil, português, respostas breves e didáticas, passos manuais curtos pensados para celular Android (um por vez).

## Pedido atual
Continuar o projeto e criar/aprimorar corrida arcade para Android no navegador, com toque e adversário CPU, inspirada no ritmo, câmera traseira e sensação de velocidade de Top Gear SNES. Liberdade para reinterpretar. Não copiar código, sprites ou músicas do original.

## Regras fixas
- Preservar rostos reais, macacões, patrocinadores, logos, números e pinturas. Daniel Mencacci: Mercedes verde-lima nº22, boné preto Mercedes. Felipe Mencacci: Mercedes vermelha nº25, boné vermelho nº25.
- Referência dos pilotos: referencias/pilotos-e-carros/dupla-canonica-bones-e-macacoes.jpg. Usar os PNG originais dos logos FTW e Diabo Verde. Lata já recebida; não inventar embalagem.
- Somente Cascavel; traçado, checkpoints e minimapa da mesma geometria; trecho laranja dos boxes não é circuito.
- Phaser (WebGL/Canvas) autorizado. 3 voltas, 2 nitros, horizontal = provisórios.
- Reproduzir antes de afirmar causas; separar teste emulado de teste no aparelho; não declarar validado sem testar.
- Preservar a publicação atual em gh-pages (raiz).

## Publicação da versão de teste (autorizada; substitui a restrição anterior)
Link público HTTPS, abrível com um toque no Chrome do Android, hospedagem gratuita (preferência GitHub Pages), endereço separado da versão existente. Não entregar só ZIP/código. Verificar que carrega jogo, imagens e controles; diferenciar emulado de Android físico; não declarar funcionando sem verificar. Se faltar acesso, explicar o que habilitar e concluir depois.

## Código
game/ (módulos ES, sem build). Testes: `cd game && npm test`. Emulado: `python3 game/tests/emulated/run_emulated.py game saida`. Implantação: copiar game/index.html, styles.css e src/ para gh-pages/claude/ (usa ../assets/ da gh-pages, inclusive phaser-Czz4FBZH.js; plano B via CDN jsdelivr). A cópia publicada está em gh-pages/claude/ (mesmos arquivos).
Estado, limitações e hipóteses: docs/10_VERSAO_CLAUDE_V02.md.

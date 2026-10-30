# Celular e pipeline de referências/sprites
Atualizado em 30/10/2026. Estado: preparação, sem assets finais ou jogo implementado.

## Confirmado pelo usuário
- Jogo para celular.
- Comandos na tela, por toque.
- Criar referências e sprites neste chat, com revisão visual, e disponibilizar ao Codex no GitHub.
- Codex usará o repositório como base e integrará/testará os materiais.

## Propostas ainda ajustáveis
- Celular na horizontal.
- Direção esquerda/direita no lado esquerdo.
- Acelerador e freio no lado direito.
- Botão Diabo Verde separado para nitro.
- Câmera traseira e perspectiva compatíveis com Top Gear, com tamanho de carro definido antes do lote.
Não converter essas propostas em decisões explícitas do usuário.

## Ainda em aberto
Navegador por link versus aplicativo instalado; Android/iOS e aparelho-alvo; jogador contra CPU versus duas pessoas; quantidade exata de ativações do nitro.
Não inferir multiplayer de haver dois pilotos. Não insistir em perguntas já respondidas.

## Comandos e testes de implementação
Toques simultâneos e independentes: virar + acelerar + nitro. Não depender de hover nem teclado.
Cada dedo deve manter sua própria ação. Soltar/cancelar um toque não solta os demais.
Tratar saída do botão, cancelamento, foco perdido, interrupção do aplicativo e retorno para evitar acelerador/direção presos.
Definir comportamento para direções opostas e freio/acelerador juntos; validar sem estados incoerentes.
Pausa, menus e resultado acessíveis por toque. Botões legíveis, alcance confortável e área de toque compatível com o dispositivo.
Respeitar áreas seguras, diferentes proporções e visibilidade da pista. Preferir controles ajustáveis e feedback visual/sonoro.
Confirmar tecnologia com o usuário antes de adotar Canvas/WebGL conforme restrição existente.
Medir desempenho real e testar toque no aparelho; emulação deve ser identificada como tal.

## Quem faz o quê
| Etapa | Responsável no fluxo | Resultado |
| --- | --- | --- |
| Enviar fotos originais e marcas | Usuário | Referências canônicas |
| Criar e revisar arte/sprites | Este chat, com ferramentas disponíveis | Arquivos e previews para aprovação |
| Aprovar identidade visual | Usuário | Registro explícito da versão aprovada |
| Definir contrato técnico | Codex em coordenação com produção visual | Dimensões, pivôs, estados e metadados |
| Integrar | Codex | Assets no jogo, estados, câmera, escala, HUD e FX |
| Testar e corrigir | Codex e revisão visual no chat quando necessária | Evidências reais e arquivos revisados |

## Próximo lote, antes de multiplicar conteúdo
1. Receber fotos e associar corretamente cada carro a seu piloto.
2. Fixar câmera, estilo, resolução-base e tamanho aproximado do carro na tela.
3. Produzir carro visto por trás, reto e em curva, mantendo pintura, proporções e rodas.
4. Aprovar aparência e testar no jogo escala, pivô, chão, perspectiva e transições.
5. Só então ampliar ângulos/estados, segundo carro, efeitos, cenários e UI.
Não alegar teste em jogo antes de integração real. Se o jogo ainda não existir, aprovar apenas aspecto visual e manter validação técnica pendente.

## Contrato técnico a preencher antes do lote
Resolução-base; canvas/dimensões do arquivo de sprite (não confundir com tecnologia HTML Canvas); área útil; margem; ponto de contato com solo; pivô; vista/câmera; escala; estados; sequência e duração; alpha; nome e versão.
PNG com transparência quando adequado. Entregar frames individuais e atlas/metadados apenas se necessários à engine.
Proibir recortes involuntários, halos, deformações e troca de proporções entre estados.
Não espelhar automaticamente carro com textos, números ou pinturas assimétricas. Não esticar uma imagem estática para fingir novos ângulos.

## Organização
- referencias/pilotos-e-carros/: fotos canônicas.
- referencias/marcas-e-produto/: lata e logos originais.
- referencias/circuitos/: mapas/fotos com fontes.
- assets/sprites/: somente arquivos realmente produzidos, com inventário.
- assets/sprites/INVENTARIO.md: estado e versão de cada asset.
Originais preservados. Derivados identificados. Nenhuma aprovação implícita apenas porque o arquivo existe.

## Restrições
Não inventar rosto, número, pintura, patrocinadores ou embalagem. Não redesenhar logos.
Codex não deve trocar assets aprovados por arte procedural ou novas gerações sem solicitação.
Placeholders podem validar física e controle, mas precisam ser identificados e substituídos antes da entrega final.
Não importar assets de Top Gear nem projetos antigos do usuário.

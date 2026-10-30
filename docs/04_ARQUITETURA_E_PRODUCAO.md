# Arquitetura e produção — decisões técnicas em aberto
## Restrição do usuário
Não quer HTML Canvas como atalho para um jogo com gráficos procedurais genéricos.
O prompt mestre exige explicar e pedir aprovação caso uma engine de navegador use Canvas/WebGL internamente.
Não contornar isso com CSS inadequado. Não definir engine silenciosamente.

## Caminhos a avaliar após definir a distribuição no celular
- Engine nativa com exportação ao alvo escolhido e suporte apropriado a sprites/cenas.
- Engine de navegador caso o usuário aprove sua superfície Canvas/WebGL.
Pseudo-3D precisa de projeção/escala por código; geometria da pista e física podem ser procedurais de modo intencional. Personalidade visual deve vir de arte própria.
Nenhuma stack está escolhida. Conferir documentação oficial e versões na sessão de implementação.

## Organização sugerida
src/input, src/simulation, src/race, src/render, src/ui, src/audio; data/tracks e data/drivers; assets; tests; docs.
Adaptar à convenção da engine em vez de impor pastas artificiais.

## Etapas
1. Inspecionar referências, ferramentas e decisões pendentes.
2. Pesquisar traçados e fechar controles/plataforma.
3. Validar dirigibilidade com placeholders explícitos.
4. Produzir uma fatia completa com arte, som, UI e uma pista.
5. Testar/corrigir, incorporar a segunda pista.
6. Verificar build, documentar e entregar. Publicar apenas quando autorizado.

## Circuitos
Pesquisar fontes oficiais dos autódromos ou federação: traçado, sentido, curvas, largada/boxes e desníveis.
Registrar URLs, datas e limitações. Essas pesquisas ainda NÃO foram feitas.
Separar traçado real da adaptação arcade; manter sequência de curvas e pontos característicos reconhecíveis.
Não inventar comprimentos, altitudes ou curvaturas como se fossem medições oficiais.
Não desenhar dois circuitos genéricos e apenas trocar os nomes.

## Alvo confirmado
Celular, comandos de toque. Computador pode ser ambiente de desenvolvimento, mas teclado não substitui validação mobile. Distribuição web/app e sistema operacional ainda pendentes. Seguir 08_MOBILE_E_PIPELINE_DE_SPRITES.md.

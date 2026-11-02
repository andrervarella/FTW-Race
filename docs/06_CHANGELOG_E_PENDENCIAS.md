# Registro e continuidade
## 02/11/2026 — NPCs conforme a referência de quatro carros
- Criados quatro atlases PNG e24sprites individuais: traseira, esquerda/direita e frenagem nas três vistas, preservando aerofólio, gaiola, lanternas, escapes e gancho da referência.
- Runtime Phaser usa as novas vistas com proporção e pivô verificados; seleção estável pelo volante e freio efetivo. Física e resultados preservados.
- Pesquisa de código público MIT registrada; nenhum código/asset/música de Top Gear importado.
- Node45/45, alpha/hashes, seis estados no Phaser real e corrida completa em dois tamanhos móveis emulados passaram localmente. Publicação HTTPS em verificação. Ver NPC_REFERENCE_QA.md.

## 02/11/2026 — publicação e verificação pública da prévia V4
- Prévia em https://andrervarella.github.io/FTW-Race/teste-v4/, branch exclusiva `codex/ftw-race-v4-arcade`.
- Run público41455523600 concluiu success; artifact e13capturas inspecionados. Corrida natural, resultados reais e pódio do vencedor passaram em dois layouts móveis emulados, sem404/erros.
- Corrigidos carregamento lento, pausa do spray, áudio após pausa, rótulos dos degraus e coleta de evidências. Testes Node finais40/40.
- Os46arquivos anteriores de Pages ficaram idênticos. Artes em revisão; Android físico e desempenho no telefone não testados. Ver V4_QA_REPORT.md.

## 01–02/11/2026 — V4 em branch exclusiva
- Fonte exata `f6f6f83` recuperada e branch `codex/ftw-race-v4-arcade` criada; V3 e raiz preservadas.
- Implementados capa2D, seleção explícita, grid, corrida/pausa, bandeirada, classificação de seis e comemoração para cada vencedor.
- Resultado congelado na primeira chegada interpolada; não concluintes sem tempo inventado. Corrigida perda de volta na colisão com retardatário.
- Preparados cenários/FX, vistas reais dos dois carros, quatro NPCs redesenhados e36poses de comemoração. Artes novas em revisão humana, **prévia funcional incompleta artisticamente**.
- Áudio sintetizado próprio, recuperação após pausa e pódio pausável com botão continuar; caminhos autocontidos para subpasta.
- Verificação e publicação: consultar `V4_QA_REPORT.md`, manifesto e provenance. Android físico não disponível; nenhuma afirmação de FPS Android.

## 30/10/2026 — preparação
Conversa consolidada, prompt mestre original preservado e referência de Top Gear organizada.
Não houve implementação do jogo.
## Próximos passos
1. Receber fotos de pilotos e carros e associar corretamente.
2. Confirmar distribuição no celular (web/app), sistemas-alvo e modo de disputa. Celular/toque já confirmados.
3. Decidir engine respeitando a restrição de Canvas/WebGL.
4. Pesquisar autódromos e atualizar referências.
5. Implementar e testar primeira fatia jogável.
## Não decididos
Quantidade de ativações e balanceamento do nitro, tela dividida, combustível/pit stop, número de voltas, dificuldade, multiplayer, título comercial e identidade de marca.
O histórico de projetos AV/Diabito não faz parte deste projeto.

## 30/10/2026 — adição de nitro
Usuário definiu aceleração especial associada à lata de Diabo Verde pré-workout e informou que enviará referências da lata e logos FTW e Diabo Verde. Duas ativações por corrida são interpretação provisória da expressão “duas opções”. Documentação atualizada; nenhuma implementação/teste de jogo realizado.

## 30/10/2026 — mobile e fluxo de sprites
Usuário confirmou celular e comandos na tela, além de produção das referências e sprites no chat. Codex fará integração e testes. Fotos ainda não recebidas, nenhum sprite aprovado/gerado, nenhum jogo implementado. Primeiro lote será um carro traseiro e em curva após receber referências e definir câmera/escala; expandir após validação.

## 31/10/2026 — entrega de preparação visual
Fotos recebidas, 16 pranchas de geração organizadas e 24 referências selecionadas. Escopo atual somente Cascavel; procedural moderado autorizado para pista e entorno. Identidade Daniel #22 verde e Felipe #25 vermelho, ambos com/sem capacete.
Incluídos manifesto, galeria, inventário técnico e prompt de continuidade. Preservados os documentos anteriores como histórico, com aviso prioritário.
Verificação desta etapa: abertura/leitura dos arquivos de imagem e manifesto com dimensões/bytes/SHA-256. Não houve build, teste de gameplay ou teste mobile.
Próximos passos atuais substituem a lista antiga: preparar sprites, validar mapa, resolver distribuição/engine/modo, implementar, testar. Lata e logos originais pendentes.


## Atualização — lata recebida e Felipe com boné (31/10/2026)
Referências da lata Diabo Verde Pré-Workout, sabor Maçã Verde, 269 ml recebidas em referencias/marcas-e-produto/: frente, verso, apresentação e captura da página enviada pelo usuário. Esta atualização substitui as menções anteriores à lata pendente. Preservar formato alto/estreito, corpo preto, faixa verde, nome vertical e logo FTW do rótulo. A foto frontal é a referência principal para preparar o ícone e a animação; não incorporar os quadros promocionais laterais ao sprite. Logos independentes/vetoriais continuam pendentes; as marcas visíveis no rótulo já têm referência. Quantidade de nitro e demais regras continuam provisórias. A prévia assets/previews/ui/proposta-selecao-e-hud.png foi atualizada com Felipe de boné preto, conforme solicitado. Não há integração ou teste de gameplay nesta atualização.


## Correção prioritária de fidelidade — 31/10/2026
O usuário rejeitou a fidelidade da tela anterior. A foto referencias/pilotos-e-carros/dupla-canonica-bones-e-macacoes.jpg passa a orientar os retratos e macacões: Daniel à esquerda com boné preto Mercedes; Felipe à direita com boné VERMELHO nº25 (substitui a solicitação anterior interpretada como boné preto). Preservar os rostos reais e os painéis/patrocínios dos macacões.
Logos FTW e Diabo Verde RECEBIDOS como PNG originais em referencias/marcas-e-produto/. Aplicar esses arquivos diretamente na interface final, mantendo proporções; não recriar tipografia nem aceitar aproximações geradas. Não há mais pendência de referência de logo; estes PNG não são vetores.
O traçado jogável E o minimapa devem seguir cascavel-mapa-esquematico.png e cascavel-mapa-satelite.jpeg. Substituir o antigo rabisco da UI; manter sequência de curvas e proporções do circuito. Derivar minimapa da mesma geometria da pista, validar contra os mapas; não confundir pit lane laranja com circuito. Geração de imagem não garante precisão geométrica ou identidade exata de marcas. A tela revisada continua prévia sujeita a revisão, não aprovação automática nem prova da pista implementada.

## 01/11/2026 — sincronização de fonte com a prévia Claude publicada (ChatGPT)
- A branch de desenvolvimento tinha `game/src/main.js` importando `./ui.js` sem esse arquivo; `game/index.html` apontava para `styles.css` ausente. A API simples de áudio em `game/src/audio.js` divergia da interface da versão hospedada.
- Copiados os módulos de `gh-pages/claude/` para `game/` (HTML/CSS, áudio, configuração, simulação, renderização, main e UI), preservando a versão da pasta publicada. O material publicado já traz pista mais larga, volante com inércia, colisão e áudio sintetizado.
- Incluídos `game/README.md` e `game/tests/source-integrity.test.js` para exigir arquivos essenciais, imports válidos e verificar contratos básicos de física/UI.
- **Verificação nesta etapa:** análise estática de arquivos, dependências e exports antes do commit. **Não houve** execução de npm test, navegador real ou aparelho Android nesta etapa. A versão pública existente e a branch main não foram modificadas.

## 01/11/2026 — teste V3 seis carros
Implementados quatro adversários de IA, HUD 1–6, colisão entre todos, sprites 2D sem logos para NPCs. Simulação JavaScript de 12 s executada; Android físico e Phaser real ainda não verificados. Consultar docs/11_TESTE_V3_SEIS_CARROS.md.

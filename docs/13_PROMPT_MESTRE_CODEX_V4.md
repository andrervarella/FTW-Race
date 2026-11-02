# PROMPT MESTRE DE EXECUÇÃO — FTW RACE V4 (CODEX)

> **USAR COMO INSTRUÇÃO EXECUTÁVEL DE TRABALHO NO CODEX.**  
> **Status:** DIREÇÃO VISUAL APROVADA PELO PROPRIETÁRIO; V4 AINDA NÃO IMPLEMENTADA.  
> **Repositório:** `andrervarella/FTW-Race`  
> **Branch-fonte a inspecionar:** `claude/ftw-race-v0.2`  
> **Branch de trabalho recomendada:** `codex/ftw-race-v4-arcade` (criar a partir da branch-fonte mais recente, sem rebase destrutivo).  
> **Página de testes prevista:** `https://andrervarella.github.io/FTW-Race/teste-v4/` — só declarar jogável após publicar e verificar realmente.  
> **Idioma das telas:** português, preservando deliberadamente "PRESS START" e "SELECT YOUR DRIVER" da linguagem retrô.

## 0 — MISSÃO E REGRAS DE PRIORIDADE

Você é engenheiro líder de jogos 2D, gameplay, pixel-art, integração de assets e QA. **Implemente o jogo V4 inteiro, não apenas mockups ou um novo documento.** Continue a base do FTW Race V3 que já tem seis corredores, direcional com inércia, colisões, nitro, áudio e traçado de Cascavel. O visual deve recordar um jogo arcade de corrida de 16 bits/SNES, sem copiar conteúdo de Top Gear ou de outras franquias.

**Esta especificação é fruto de storyboard aprovado.** Não pedir de novo para aprovar a estrutura do fluxo; pedir revisão humana **apenas para artes novas ou alterações de identidade visual** que exijam fidelidade real. A aceitação da arquitetura não é aprovação antecipada de rostos inventados, sprites gerados ou da publicação final.

ANTES DE PROGRAMAR, abrir e obedecer:
- `AGENTS.md`, `CLAUDE.md`, `PROMPT_CODEX.md` e `README.md`;
- `docs/12_V4_STORYBOARD_E_DIRECAO_VISUAL.md` (APROVADO, prevalece sobre planejamentos antigos para V4);
- `docs/09_ENTREGA_VISUAL_E_CONTINUIDADE.md` e `docs/11_TESTE_V3_SEIS_CARROS.md`;
- `docs/REPOSITORIOS_PUBLICOS_E_POLITICA.md` e `docs/REA_ENGENHARIA_REVERSA.md`;
- `docs/05_TESTES_E_QA.md`, `docs/06_CHANGELOG_E_PENDENCIAS.md` e os testes em `game/tests/`.

**Hierarquia:** decisões explícitas mais recentes do proprietário > aparência canônica/fotos/logos aprovados > storyboard V4 aprovado > requisitos funcionais aqui > materiais antigos e exemplos externos.

**Não fazer:**
- Não recriar o projeto com template genérico, engine diferente, framework grande ou protótipo Canvas simplista. **A base existente Phaser + JavaScript ES modules + UI em DOM/CSS está autorizada.**
- Não substituir fotos oficiais por rostos aproximados nem modificar logos, patrocinadores, numeração ou roupas oficiais.
- Não usar personagens 3D. A câmera pode projetar pista pseudo-3D com **sprites 2D** (como a V3), mas pilotos, carros, cenários e FX devem ser imagens 2D reais.
- Não colocar o mesmo sprite de piloto em todos os resultados, não premiar o piloto selecionado quando outro venceu e não simular animação corporal complexa girando braços/pés recortados.
- Não copiar código, áudio, sprites, layouts originais nem imagens de Top Gear, OutRun, KOF ou de repositórios públicos que não tenham licença compatível.
- Não apagar nem sobrescrever `gh-pages/`, `gh-pages/claude/` ou `gh-pages/teste-v3/`. **A V4 vai exclusivamente para `gh-pages/teste-v4/` após QA.**
- Não declarar testes, FPS, URL funcionando, fidelidade real, assets com transparência ou publicação como concluídos sem evidência.

## 1 — ESTADO INICIAL REAL: INSPECIONE ANTES DE ALTERAR

**Fonte editável:** `game/`
- `game/index.html` — HTML, bootstrap, loading e erros de inicialização;
- `game/styles.css` — menu e HUD DOM, orientação mobile, botões;
- `game/src/main.js` — bootstrap de Phaser, estado da corrida e loop com passo fixo;
- `game/src/ui.js` — fluxo atual menu→corrida→resultado, seleção Daniel/Felipe, controls, HUD;
- `game/src/render.js` — pista/cenários/projeção/veículos 2D em Phaser;
- `game/src/sim.js` — física, cinco rivais IA, colisões, checkpoint, classificação e vencedor;
- `game/src/config.js` — config dos pilotos e rivais; `NPC_KEYS`, cores e carro;
- `game/src/track.js` — geometria de Cascavel e checkpoints;
- `game/src/input.js` — teclado e pointer/multitouch;
- `game/src/audio.js` — engine/FX/música;
- `game/tests/core.test.js`, `game/tests/source-integrity.test.js`, `game/tests/v3-traffic.test.js`;
- `game/cars/npc-{blue,yellow,purple,silver}.svg` — quatro **hatches genéricos provisórios**, devem ser substituídos por carroceria coerente ao mesmo modelo Mercedes AMG A45 (com as restrições de marca abaixo).
- `game/package.json` usa `node --test tests/core.test.js`: atenção, **nem todos os testes da V3 entram em `npm test` atualmente**. Corrigir o script para executar as suítes adequadas sem ocultar falhas; verificar Node e sintaxe de módulos.

**Assets visuais aprovados/fornecidos (referências):**
- Fotos reais: `referencias/pilotos-e-carros/` (principal: `dupla-canonica-bones-e-macacoes.jpg`). Daniel à esquerda com boné preto, Felipe à direita com boné **vermelho nº 25**; números 22 e 25.
- Logos oficiais e lata: `referencias/marcas-e-produto/ftw_logo_oficial_isolado.png`, `diabo_verde_logo_oficial.png`, frente/verso da lata Maçã Verde 269 ml.
- Carros/pilotos para preparação: `assets/previews/daniel/` e `assets/previews/felipe/`.
- Cascavel: `assets/previews/cascavel/reta-principal.png`, `curvas-e-mata.png`, `vegetacao-e-barreiras.png`, `boxes-e-sinalizacao.png`.
- FX: `assets/previews/fx/estudo-fumaca-poeira-nitro-impacto.png`.
- Proposta de menu/HUD: `assets/previews/ui/proposta-selecao-e-hud.png` (COMPOSIÇÃO, não aprovação de todas as artes/identidades).
- Traçado oficial: `referencias/circuitos/cascavel-mapa-esquematico.png` + `cascavel-mapa-satelite.jpeg`.

**Essas pranchas NÃO são automaticamente sprites prontos.** Inspecionar alpha, halos, fundo, escala, perspectiva, anatomia, marcas, orientação e aprovação. Não contar imagem de contato como animação utilizável. Não incorporar `assets/previews/arquivo/` sem razão técnica e aprovação; contém tentativas rejeitadas.

**Publicação atual:** base testável `/FTW-Race/teste-v3/`, referência anterior `/FTW-Race/claude/`; raiz permanece intocada. Algumas imagens e Phaser local estão na pasta pública `gh-pages/assets/`: inspecionar nomes reais e dependências antes de escrever novos caminhos. A V4 precisará funcionar por URL de subpasta em GitHub Pages (caminhos relativos rigorosos, sem /assets absoluto).

## 2 — IDENTIDADE 2D INEGOCIÁVEL

**Daniel Mencacci:** #22, Mercedes AMG A45 verde-lima, rodas pretas, boné preto Mercedes, macacão preto/branco/verde-lima, feições reais verificadas nas fotos, capacete conforme fotos (branco/vermelho na referência de dupla).
**Felipe Mencacci:** #25, Mercedes AMG A45 vermelha, rodas pretas, boné vermelho nº 25, macacão vermelho/branco/verde-lima, feições reais verificadas nas fotos, capacete azul com branco/vermelho/verde conforme referência.
- A foto dupla e os PNGs originais prevalecem sobre estudos gerados que distorçam rosto/número/pintura.
- Gerar/converter protagonistas em **ilustração 2D coerente**, com mesma forma da cabeça, barba/cabelo, cores, acessórios e proporções; produzir views separadas para título/seleção/pódio e sprites com qualidade de console 16-bit. Não inferir que a geração é fiel sem inspeção lado a lado.
- Não tratar foto recortada e deformada como sprite pixel-art final. Se a ferramenta de arte conectada estiver indisponível, documentar bloqueio; criar integração e placeholders **explicitamente** marcados, mas não reivindicar entrega artística concluída.
- Não redesenhar logos FTW/Diabo Verde; usar bytes oficiais. Logos de terceiro nos uniformes/carros oficiais somente conforme referências aprovadas; não inventar patrocínio.

## 3 — IMPLEMENTAÇÃO POR MÓDULO

### A. `game/src/ui.js` — MAQUINA DE ESTADOS DE TELAS
Migrar do fluxo menu→race→modal para:
`title` → `driverSelect` → `grid` → `countdown`/`racing` ↔ `paused` → `results` → `podium` → `replay`/`driverSelect`/`title`.
- Separar **estado de navegação visual** do `race.phase` do simulador; não atribuir estados de UI ao sim sem compatibilidade.
- Criar funções ou módulos `showTitle()`, `showDriverSelect()`, `showGrid()`, `showResults()`, `showPodium()`, `raceUi()`, `menu()` compatível se legado.
- Evitar listeners duplicados: em toda transição destruir/cancelar eventos/timers/FX e liberar inputs segurados; Enter, Escape, pointerdown e pointercancel funcionam.
- `PRESS START` piscando em texto acessível e botão grande (700 ms como referência, respeitando `prefers-reduced-motion`). Primeiro toque libera Web Audio sem iniciar corrida.
- Seleção: **apenas Daniel e Felipe**; nome, número e carro correspondentes; tela 2D com dois cards, feedback visual/sonoro; confirmação explícita e opção voltar. Persistir seleção atual apenas se coerente com privacidade e testes.
- `CONFIRMAR PILOTO` leva a tela de grid e só depois ao countdown, sem double-tap iniciar duas corridas.
- Resultado: mostrar vencedor real e posição do usuário entre 6; oferecer `VER PÓDIO`/transição automática, `RECOMEÇAR` e `TROCAR PILOTO`.
- A tela final de vitória **não pode exibir uma pessoa real que não venceu**; NPC vencedor precisa de identidade visual ficcional sem rosto humano real inventado.

### B. `game/styles.css` e `game/index.html` — CAPA E APRESENTAÇÃO
- Pôster inédito estilo capa de corrida 16-bit: Daniel e Felipe 2D em destaque, carros nº 22/#25, Cascavel ao fundo, logo FTW original, "FTW RACE — CASCAVEL", "PRESS START" piscando e "6 CARROS · 1 CAMPEÃO".
- Caprichar em camadas de profundidade 2D, reflexos e iluminação desenhados; não copiar layout de capa alheia. Sem caricatura genérica, deformação, blur excessivo ou texto ilegível.
- `game/index.html`: tela loading e mensagem fatal precisam permanecer claras; texto título muda para V4; `aria-label` e navegação de teclado; tela cheia/landscape por gesto válido e fallback sem orientation lock.
- `styles.css`: safe-area, 16:9 responsivo em resoluções menores, controles suficientemente grandes, feedback de toque e redução de movimento. Elementos decorativos nunca bloqueiam o touch dos controles.
- Se a capa pedir bitmap específico, usar arte original como asset 2D separado de títulos e botões **funcionais** de DOM para não perder legibilidade em telas variadas.

### C. `game/src/render.js` — CENÁRIOS, CARROS E EFEITOS
- **Preservar** projeção/simulação de pista existente, corrigindo render quando necessário; não retornar à pista estreita da V1 nem transformar a cena em formas genéricas.
- Converter famílias relevantes de `assets/previews/cascavel/` em sprites de cenário com alpha adequado, clip/sort/profundidade e base/pivôs estáveis. Reutilizar arquitetura de cenas/Phaser, não colar PNG de contato como textura de terreno.
- Os recursos reais de Cascavel (boxes, arquibancadas, árvores, cercas, barreiras, zebra) devem aparecer de forma coerente, sem floresta aleatória nem objetos atravessando o asfalto. O traçado e o minimapa continuam baseados na mesma geometria verificada.
- Transformar estudos `fx/estudo-fumaca-poeira-nitro-impacto.png` em frames/partículas animadas: poeira off-road, fumaça/derrapagem, contato/faíscas, nitro e linha de velocidade. Usar sprites reais e limitar partículas no mobile.
- Carro do jogador e os 5 rivais 2D com escala e pivôs consistentes nas curvas/retas/contatos; evitar `setAngle` para fingir rotação complexa de carro, exceto lean discreto enquanto sprites de curva corretos não existirem.
- Remover ou classificar como provisórias as partículas geométricas quando os recursos aprovados estiverem integrados; sem falso status de sprite real.

### D. `game/src/config.js`, `game/cars/` e `game/src/sim.js` — SEIS CARROS E RESULTADOS
- Daniel e Felipe: manter carroceria **Mercedes AMG A45** com pintura e marcas oficiais, nº 22 verde e nº 25 vermelho.
- **Quatro NPCs**: manter mesma silhueta/modelo-base de hatch esportivo AMG A45 do jogo (lanternas, rodas, faróis/vidro, aerofólio, dimensões e perspectivas), nas cores **azul, amarelo, roxo e prata**, SEM logos FTW ou Diabo Verde ou patrocínios personalizados. Carros NPC podem ser distinguíveis por número fictício neutro, sem inventar piloto humano real.
- **Não deixar os quatro SVGs hatches genéricos V3 como assets finais.** Redesenhar/derivar sprites independentes 2D com geometria coerente, alfa e no mínimo visão traseira; views curvas esquerda/direita, freio e colisão se necessário.
- Manter `NPC_KEYS` e o comportamento da IA, com velocidade, ultrapassagem, distanciamento/colisão entre TODOS. Nenhum carro deve ganhar por valor fixo de `winner` ou por seleção do jogador.
- Refatorar sistema final sem quebrar `createRace`/step fixo: quando o **primeiro** cruzar a linha, registrar vencedor por `finishTime`, congelar instante da bandeirada e calcular posição de cada um por finalização real ou progresso naquele instante. **Não inventar tempos finais para NPCs que não concluíram todas as voltas.** Se for viável concluir a corrida para todos, desenhar regra de continuação comprovada e testá-la, sem tornar UX demorada.
- Exportar `getResults` ou `raceStandings` testável puro, incluindo classificação de 1..6, protagonista, vencedor, melhor volta e status de conclusão. Empates determinísticos e ordenação de ranking auditáveis.
- Não degradar direção com inércia, colisões, nitro, HUD 6 carros, checkpoints, IA, pausas nem persistência de input.

### E. `game/src/audio.js` — MÚSICA E FEEDBACK
- Trilhas e FX próprios ou licenciados (sem trechos/samples de Top Gear); menu/título, seleção, motor dinâmico, contagem, batida, derrapagem, nitro, bandeirada, aplausos e pódio.
- Preservar `GameAudio` e o botão existente de modos de som; transições com crossfade/volume para impedir a música de cortar ou sobrepor instâncias quando mudar tela, pausar, alternar aba, reiniciar.
- Respeitar desbloqueio de Web Audio após primeiro toque. Ter modo mudo, sem falha fatal se API de áudio não estiver disponível.

### F. NOVOS MÓDULOS AUTORIZADOS — UI, ASSETS E PÓDIO
Criar módulos pequenos se isso ajudar a manutenção:
- `game/src/screens/title.js`, `select.js`, `results.js`, `podium.js` (ou estrutura equivalente, se houver motivação para permanecer em `ui.js`);
- `game/src/assets.js` (manifesto/load de sprite) e `game/src/standings.js` (funções puras);
- `game/assets/v4/` ou `game/sprites/v4/`: diretórios de `title/`, `drivers/`, `cars/`, `cascavel/`, `fx/`, `podium/`; metadados JSON com fonte e frame timing.
- `assets/sprites/V4_MANIFEST.json` e `docs/V4_ASSET_PROVENANCE.md` para links dos originais, hashes, transformações, uso, status de aprovação/licença. O conteúdo distribuído na pasta da página V4 precisa estar acessível por **URLs relativas** e checado após cópia.

### G. ANIMAÇÃO 2D DE PÓDIO — OBRIGATÓRIA
- Encerrou corrida → tela de bandeirada → resultados → pódio 2D com três lugares, sem perder a informação real de ranking.
- Para Daniel/Felipe, preservar feições do piloto, boné/capacete/uniforme conforme acervo. Se falta pose corporal confiável, produzir frames genuínos e solicitar revisão visual; não deformar recortes.
- Para NPC vencedor, figura **fictícia** com capacete fechado e uniforme neutro na cor da equipe; sem imitar rostos reais.
- **Quadros**: entrada/subida ao degrau → recebe taça → ergue taça → abre champanhe → pulveriza champanhe (gotas/espuma em camada FX independente) → comemoração final. Troféu e garrafa como sprites 2D. Não é aceitável uma imagem estática, texto "CAMPEÃO" e uma partícula pulsando como substituto de animação.
- A cena tem som de abertura de garrafa, aplausos e vinheta curta licenciados/originais, com opção silenciar. Respeitar toque, pausar/ocultar aba, limite de partículas e `prefers-reduced-motion`.
- Mostrar nome/carro **do vencedor real**, e botões CORRER NOVAMENTE, TROCAR PILOTO e VOLTAR À CAPA. Deve funcionar se ganhar um NPC, Daniel ou Felipe.
- A comemoração com champanhe é a **recompensa visual esportiva**, não propaganda de bebida nem link de compra.

## 4 — PROCESSO DE ARTE (NÃO INVENTAR FIDELIDADE)
1. Inventariar todos os PNGs e fotos existentes; classificar: foto oficial, logo original, ilustração preliminar, recurso tecnicamente pronto, arquivo rejeitado, lacuna a produzir.
2. Inspecionar e comparar cada rosto/carro com as fotos canônicas; não substituir os pilotos por personagens aleatórios nem alterar tatuagens, cabelos, uniformes ou o lado/posição do boné.
3. Preparar recortes com alpha real. Medir dimensões, área útil, pivô do pé/roda, consistência de escala, sombreamento e contorno de cada estado.
4. Produzir sprites de corpo inteiro separados para gestos complexos: *frames distintos* → atlas/sheet → metadata JSON → prévia animada verificável; não usar `transform:rotate` de membros para falsificar poses biomecânicas.
5. Comparar imagens sobre fundo preto, cinza e branco e em tamanho final de tela Android; rejeitar halos, transparência falsa, escalas saltando, letras ilegíveis ou números trocados.
6. Preservar intocados os arquivos de referência originais e registrar toda derivação/revisão. Não chamar material gerado de "aprovado" sem confirmação do proprietário.
7. Se houver limitações de ferramentas de geração de imagens, informar e entregar a parte funcional sem alegar que a fidelidade artística está concluída; não bloquear a exploração técnica onde for possível usar placeholders claramente marcados.

## 5 — TAREFAS EM ORDEM E CHECKPOINTS (AUTONOMIA COM QA)

**ETAPA 0 — linha de base (ANTES de alterações):**
- Revisar árvore do repositório, disponibilidade real de assets e branches; executar `cd game && npm test`, `node --check` nos módulos e registrar saída/commit/limitações. Não confundir resultado antigo com validação V4.
- Avaliar referências públicas de corrida, Phaser e controle móvel: `jakesgordon/javascript-racer`, `ssusnic/Pseudo-3d-Racer`, `phaserjs/examples` e alternativas melhores se houver. Registrar URLs, versões, licenças (código E assets) e o que realmente foi reutilizado em `docs/PESQUISA_OPEN_SOURCE_LOG.md`.
- Avaliar REA **somente se** útil para analisar nossas próprias builds e explicitamente disponível/autorizado, nos termos de `docs/REA_ENGENHARIA_REVERSA.md`; não exigir REA como dependência. Não fazer engenharia reversa de Top Gear ou binários de terceiros sem direitos.
- Criar branch dedicada e relatório curto de baseline.

**ETAPA 1 — fluxo navegável:** título Press Start → seleção Daniel/Felipe → grid/countdown → V3 corrida → resultado → pódio/retorno; testes DOM/UI e teclado/multitouch. A arte ainda pode ser provisória, identificada.

**ETAPA 2 — pipeline visual 2D:** capa própria, piloto Daniel/Felipe fiel, dois carros oficiais, quatro carros NPC idênticos de chassis sem marcas, Cenários Cascavel e FX integrados como sprites separados; auditar autorizações/origens, frame/pivô e fidelidade.

**ETAPA 3 — corrida e resultados:** adaptar render para sprites, classificação coerente de 6 carros, câmera/física/colisões, som contínuo, HUD e minimapa precisos. Largada sem glitches e resultado sem vencedores falsos.

**ETAPA 4 — pódio completo:** animar vitória para qualquer vencedor, troféu, champanhe, partículas e aplausos; animação reduzida e reinício correto.

**ETAPA 5 — QA de verdade e entrega:** suites puras, testes integração DOM em viewport mobile/desktop, Chrome Android físico quando acessível, capturas, verificação de carga e assets. Corrigir regressões; publicar versão em `/teste-v4/` após validação e permissão de publicação de prévia, mantendo outras versões; abrir URL HTTPS em navegador independente, conferir Phaser, HUD, controles, áudio e resultado. Se falta validação, não afirmar publicamente "testado" ou "funcionando". Fornecer link apenas após existir e ser checado.

**Não usar comunicação de fundo.** Cada etapa deve deixar um commit e a situação verificável, de preferência em branch com PR; se a etapa não puder ser completada, declarar claramente e entregar os artefatos realmente feitos.

## 6 — TESTES OBRIGATÓRIOS E CRITÉRIOS DE CONCLUSÃO

### Testes de lógica
- Exatamente 6 carros (2 oficiais + 4 NPCs), integridade de `DRIVERS`, `NPC_KEYS` e vinculação piloto–carro;
- Curvas, checkpoints, classificação 1–6 e vitória de cada classe (Daniel/Felipe/NPC), empates e contagem exata de voltas;
- Nenhum carro se sobrepõe persistentemente após resolução de colisões; inputs não travam; nitro respeita número de cargas e pausa.
- Simulação controlada determinística para ao menos 1 corrida completa; tempos não inventados de quem não cruzou a chegada.

### Testes de interface e dispositivos
- Primeiro estado `title` e botão PRESS START; primeiro toque libera áudio; sem autoplay não autorizado.
- Selecionar Daniel -> tela carro verde nº22; selecionar Felipe -> vermelho nº25; botão voltar, dupla confirmação, reiniciar com mesmo piloto, trocar piloto e retornar à capa.
- Pausa/background, tela vertical, landscape, áreas seguras, dois/dedos+nitro, feedback de hold/release, sem controles bloqueados.
- Resultado/pódio usa id do verdadeiro vencedor nos seis casos; animações sequenciais com champanhe e troféu para oficiais e NPCs; opção redução de movimento.
- Sem 404 de CSS, JS, imagens, áudio, módulos dinâmicos nem asset path fora da subpasta `teste-v4/`.

### Arte e desempenho
- Sprite de Daniel e Felipe fiel e revisado; NPCs mesmo chassis sem FTW/Diabo Verde; cena de Cascavel com pista baseada em geometria real e FX em frames recortados; arte 2D sem 3D.
- Inspecionar visualmente no telefone; rastreabilidade de todos os recursos, com arquivo de origem, status de aprovação e licença.
- Registrar FPS e problemas de fluidez **apenas se medidos**, especialmente Android; modo gráfico reduzido disponível; respeitar CSS `prefers-reduced-motion`/acessibilidade.
- Node `node --check` para JS, `npm test` corrigido para todas as suítes; QA com ferramenta/browser real quando disponível.

**Aceite somente se** a V4 for mais que mockup: fluxo totalmente navegável, corrida V3 preservada, NPCs de mesmo modelo, sprites e FX integrados e pódio animado para os seis possíveis vencedores. Se a arte real não foi aprovada, marcar V4 como **prévia funcional incompleta**, não "entrega final".

## 7 — CHECKLIST DE ARQUIVOS A ENTREGAR E RELATÓRIO

Artefatos mínimos esperados (adaptar caminhos com justificativa, sem remover a estrutura existente):
- Fonte editável `game/index.html`, `game/styles.css`, `game/src/main.js`, `game/src/ui.js`, `game/src/render.js`, `game/src/sim.js`, `game/src/config.js`, `game/src/input.js`, `game/src/audio.js`, `game/src/track.js` quando necessário; novos módulos pequenos se houver.
- Diretórios de `game/sprites/v4/` ou `game/assets/v4/` com capa, pilotos, carros, pista, FX e pódio **em PNG/SVG/sheets reais**, com frames/metadados. Não entregar apenas prompt de geração de imagem ou mockups.
- `game/tests/` atualizado, `game/package.json` chamando todas as suites de testes pertinentes e scripts de inspeção de assets.
- `docs/V4_ASSET_PROVENANCE.md`, `docs/V4_QA_REPORT.md`, `docs/06_CHANGELOG_E_PENDENCIAS.md`, `docs/PESQUISA_OPEN_SOURCE_LOG.md`.
- Página de preview separada `gh-pages/teste-v4/` **somente se validada** e aprovada para testes; nenhuma alteração às versões anteriores.
- Resposta final com: commit, branch, resumo das mudanças, arquivos/arte nova integrada, **testes realmente executados (com resultados)**, problemas pendentes, estado de autorização das artes e URL verificada (ou dizer que não foi possível).

## 8 — EXECUÇÃO
**COMECE AGORA NA BRANCH DE DESENVOLVIMENTO**, depois de ler todo o contexto. Não limitar trabalho a plano, wireframe ou prompt. Investigue, implemente, teste, corrija e entregue commits rastreáveis. Não declare sucesso enquanto houver bugs críticos ou arte provisória disfarçada de aprovada. Se uma ferramenta necessária não estiver disponível, conclua o máximo seguro possível com os recursos reais e registre o que faltou.

**Não se esqueça:** usuário trabalha exclusivamente pelo celular; não exigir que ele copie centenas de arquivos ou rode comandos manuais. Entregar link acessível por toque e artefatos versionados no GitHub quando realmente disponíveis.

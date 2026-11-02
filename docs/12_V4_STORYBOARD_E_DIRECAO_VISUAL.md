# FTW RACE — V4 | Storyboard visual e especificação de experiência (PROPOSTA)

**Status:** DIREÇÃO VISUAL E FUNCIONAL APROVADA PELO PROPRIETÁRIO. A V4 ainda NÃO está implementada, os sprites específicos ainda NÃO foram validados e a aprovação não autoriza chamar a versão final de pronta.  
**Base:** `claude/ftw-race-v0.2` (V3 seis carros). **Próxima etapa autorizada:** preparar a implementação em branch de desenvolvimento, seguindo `docs/13_PROMPT_MESTRE_CODEX_V4.md`. A publicação deve preservar a V3 e exigir validação real.

## Objetivo
Construir uma experiência arcade de corrida **2D**, com estética inspirada na geração 16-bit/SNES (sem copiar artes, códigos, trilhas ou marcas dos jogos de referência). O jogo inteiro deve manter identidade própria FTW Race, fidelidade aos pilotos e carros reais, e usabilidade horizontal em celulares Android/iOS.

**Fluxo:** PRESS START → SELECT DRIVER/CAR → confirmação e grid → contagem 3-2-1 → corrida Cascavel → bandeirada → classificação → pódio comemorativo → revanche/troca de piloto.

## Direção visual
- Tela horizontal 16:9 (base de arte sugerida 1280×720, escala adaptativa respeitando safe areas; pixel art renderizada com pixels nítidos, sem serrilhado acidental).
- Arte de capa promocional ilustrada 2D, inspirada na composição dramática e paleta de jogos de corrida 16-bit; não copiar imagens protegidas de Top Gear, OutRun ou outras franquias.
- FTW original com identidade preta/vermelha/branca, verde-lima ligado ao carro nº 22 e ao nitro; vermelho do nº 25. Cores dos NPCs: azul, amarelo, roxo, prata.
- Tipografia retrô legível; animação discreta em texto, luzes, fumaça e elementos de corrida; efeitos sonoros e música originais/licenciados. Não introduzir 3D.
- Não usar retratos genéricos ou rostos inventados. Referências oficiais e fotos de `referencias/pilotos-e-carros/` prevalecem sobre qualquer prévia gerada.
- Logos FTW e Diabo Verde exclusivamente dos PNG originais de `referencias/marcas-e-produto/`. Não redesenhar nem inverter logos.

## TELA A — título / Press Start
**Composição:** fundo 2D de Cascavel com reta, arquibancadas e profundidade; Daniel à esquerda e Felipe à direita em corpo/meio corpo ilustrado fiel; seus dois carros oficiais em grande destaque inferior; logotipo FTW Race centralizado no topo; CTA central inferior “PRESS START” em piscar controlado com ritmo ~700 ms; frase discreta “6 CARROS · 1 CAMPEÃO”.

**Interação:** toque em área ampla/Press Start ou Enter/Espaço; habilita áudio após interação e entra na seleção. Se celular estiver vertical, instruir girar com orientação clara, sem quebrar layout. Mostrar feedback visual e sonoro ao confirmar. Evitar autoplay com áudio antes de gesto.

**Assets:** capa ilustrada exclusiva, dois recortes de pilotos e carros, fundo de Cascavel; nada de fotos falsas nem logos desenhados por IA.

## TELA B — seleção de piloto e carro
**Layout:** título “SELECT YOUR DRIVER”. Dois cards grandes simétricos:
- **Daniel Mencacci, #22:** Mercedes AMG A45 verde-lima; referência de Daniel boné preto e macacão preto/branco/verde-lima; rosto fiel às imagens. Capacete branco/vermelho conforme referência.
- **Felipe Mencacci, #25:** Mercedes AMG A45 vermelho; Felipe com boné vermelho nº 25 na foto canônica mais recente e uniforme vermelho/branco/verde-lima. Capacete azul com branco/vermelho/verde conforme referência.
Retratos e carros inteiramente **2D**, escala e iluminação coerentes; alternância entre vista lateral/3 quartos do carro apenas se existirem sprites aprovados. Não misturar pinturas, números, face ou uniforme.

**Interação:** selecionar um card (borda realçada, som curto), mostrar versão maior do carro, tocar “CONFIRMAR PILOTO”; botão VOLTAR. Cada piloto é pareado a seu carro; sem terceira opção selecionável. Configuração de voltas e quantidade de nitro pode permanecer nas opções, sendo parâmetros provisórios, sem alterar o comportamento existente sem validação.

## TELA C — grid / pré-largada
**Layout:** vista de pista, sinalização do circuito de Cascavel, mini identidade FTW, nomes e carros oficiais em destaque; seis carros no grid. Painel de último resumo (“DANIEL #22”, “3 VOLTAS”, “CASCAVEL”) e contagem legível 3–2–1–VAI.
**Interação:** sem partidas duplicadas por dois toques; áudio motor aumenta durante largada; controles surgem antes do VAI, mas aceleração só vale em fase apropriada.

## TELA D — corrida
**Base:** preservar a simulação V3, seis carros, colisão, posição, nitro e câmera traseira pseudo-3D baseada em segmentos/projeção, mantendo **todos os objetos e personagens 2D**. O game não deve parecer um protótipo genérico ou um jogo 3D.

**Pista e FX:** reaproveitar as prévias canônicas para:
- `assets/previews/cascavel/reta-principal.png`
- `assets/previews/cascavel/curvas-e-mata.png`
- `assets/previews/cascavel/vegetacao-e-barreiras.png`
- `assets/previews/cascavel/boxes-e-sinalizacao.png`
- `assets/previews/fx/estudo-fumaca-poeira-nitro-impacto.png`
- carros e pilotos em `assets/previews/daniel/` e `assets/previews/felipe/`, sempre sob fotos oficiais.

**Observação essencial:** essas prévias são pranchas; várias possuem fundo/halo e ainda NÃO são sprites animados prontos. Recortar e limpar alfa, separar vistas e frames, fixar pivôs e escalas; integrar e verificar caso a caso. Não usar arquivos `arquivo/` rejeitados apenas para completar a lista. O objetivo é aproveitar **todas as famílias de assets pertinentes**, sem sacrificar fidelidade.

**Quatro NPCs:** mesmo **modelo e geometria visual** do Mercedes AMG A45 dos pilotos, não quatro hatches inventados. Recriar sprites individuais limpos do mesmo chassis em azul, amarelo, roxo e prata; sem logo FTW/Diabo Verde nem pintura patrocinada dos pilotos. Preservar a mesma altura, comprimento, rodas, lanternas, vidro, aerofólio e pivôs. Precisam de traseira, curva esquerda/direita, impacto/frenagem se necessário.

**HUD:** posição 1–6, volta, tempo, velocidade, minimapa derivado da pista real, nitro com lata oficial, pausa e som. Setas e acelerar/frear/nitro por multitouch, tamanho de toque confortável, indicadores quando pressionados. Sons originais/licenciados de motor, nitro, derrapagem, colisão e música contínua.

**Regras:** Cascavel baseado no mapa, sem inventar outros circuitos; arcos de curva, boxes, cercas, vegetação realistas para o local. Procedural moderado para estrada e elementos repetidos; assets 2D para silhuetas e efeitos marcantes.

## TELA E — bandeirada e resultados
**Primeiro momento:** bandeira de chegada, queda/controle do som do motor e áudio de vitória/derrota; congelar corretamente simulação sem perder resultado.
**Segundo momento:** classificação real 1º a 6º (de acordo com lógica validada), destaque do jogador, tempos e voltas, botão de assistir pódio ou transição automática.
**Detalhe de regra:** hoje a V3 encerra no primeiro carro que completa o percurso; a V4 deverá registrar classificação final de maneira coerente (tempos já encerrados ou distância/progresso dos demais, explicitamente rotulada como classificação no momento da bandeirada). Não inventar tempos de chegada para participantes que não terminaram.

## TELA F — pódio / celebração 2D
- Cenário 2D próprio de premiação do FTW Race, arquibancadas/câmeras e três níveis de pódio.
- **O vencedor da corrida, qualquer um dos seis, recebe troféu e comemora com champanhe**.
- Se Daniel ou Felipe ganhar: animação 2D em quadros distintos com traje/boné/rosto baseados nas fotos canônicas, sem modificar traços nem inventar patrocinadores.
- Se um NPC ganhar: pessoa **fictícia** em macacão neutro/capacete fechado da cor do carro; sem identidade humana real inventada.
- Storyboard recomendado: (1) subir ao pódio → (2) receber troféu → (3) erguer troféu → (4) abrir garrafa → (5) spray de champanhe animado em FX separado → (6) pose final e torcida. Quadrantes e durações ajustáveis depois de playtest.
- Troféu, garrafa, partículas/gotas, confete e torcida em camadas separadas, com cap de partículas para Android.
- Resultado sempre corresponde ao vencedor real, não ao piloto selecionado por padrão.
- Mostrar botões “CORRER NOVAMENTE” (mesmo piloto) e “TROCAR PILOTO” (tela B), mais opção de “VOLTAR À CAPA” (tela A).

## Pipeline de sprites
1. Inventariar assets existentes no repo, marcar aprovado / apenas referência / rejeitado / faltante.
2. Construir conjunto de pilotos 2D (capa, seleção, pódio) a partir de fotos oficiais; revisão visual humana antes de marcar “fiel”.
3. Normalizar dois carros oficiais e quatro variações da **mesma carroceria-base**, frames de reta/curva/freio/nitro.
4. Extrair e limpar cenários reais do acervo e FX nas quatro famílias previstas.
5. Produzir componentes editáveis de UI e animações de pódio por quadros; jamais simular articulações complexas apenas girando recortes rígidos.
6. Atualizar manifesto com origem, licença, hash, tamanho, pivô, frame/time, estágio de aprovação.
7. Validar em Chromium/Android real quando disponível, com captura e logs. Publicar somente em `/teste-v4/` após testes e aprovação, mantendo V3.

## Critérios mínimos de aceitação
- Press Start aparece primeiro; toque leva à seleção; seleção carrega o piloto e o carro corretos.
- Rostos, números, pinturas e logos oficiais fiéis; personagens totalmente 2D.
- Quatro NPCs visualmente do MESMO modelo, sem logos FTW/Diabo Verde.
- Pista e FX usam sprites canônicos tratados em vez de simples placeholders quando viáveis; sem halos ou recortes grosseiros.
- Corrida de seis carros jogável, botões multitouch, som e pausa estáveis; HUD, colisões e classificação coerentes.
- Animação de troféu e champanhe para qualquer vencedor; nenhuma vitória exibida para o piloto errado.
- Testes de sintaxe, regras, fluxo UI, verificação de assets e interação em mobile com resultados documentados. **Não afirmar FPS ou teste em dispositivo físico sem evidência.**

## Próxima etapa
Storyboard **aprovado**. O prompt mestre técnico foi criado em `docs/13_PROMPT_MESTRE_CODEX_V4.md`. Próxima atividade: Codex/engenharia implementa em branch própria, testa e disponibiliza build de teste quando verificável. Esta aprovação do planejamento não altera a V3 publicada.

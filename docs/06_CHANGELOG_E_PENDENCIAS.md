# Registro e continuidade

## 03/11/2026 — autorização explícita da publicação de Marquinhos

O proprietário confirmou: “Autorizo publicar esta atualização, incluindo as novas artes de Marquinhos, do caminhão e da capa, no repositório público andrervarella/FTW-Race e no jogo /teste-v4/.” A autorização atual permite retomar o envio preparado para a branch V4 e apenas `/teste-v4/`, preservando as versões anteriores. QA local permanece PASS; publicação, implantação e QA público desta atualização ainda pendentes. Este fechamento altera somente documentação e mantém o runtime verificado `357cb810f870b3936c4c4016659f1156b91f0bb2` e o pacote Pages `70b5e734cf9039b0cabf0e52560d03a3a6209cb8`. Histórico dos bloqueios e limitações em `V4_QA_REPORT.md` e `qa/marquinhos-local-2026-11-03.json`.

## 03/11/2026 — sprites do cavalo mecânico simples
- Adotada interpretação de cavalo4×2 após esclarecimento do proprietário; sem carreta, Diabo Verde no para-brisa e FTW nas portas.
- Geradas seis vistas traseiras/curvas/frenagem numa única prancha e preservada a proposta frontal. Entregues PNGs560×512, atlas1680×1024, fontes/âncoras/metadata, contatos, HTML e ZIP. QA/atlas/hashes/freio PASS; comparação propõe1,4015×largura do Mercedes, sem deformar. Chromium móvel em dois layouts e reconstrução portátil byte-exata PASS.
- Arte nova para revisão; piloto/caminhão ainda não registrados como jogáveis. Ver TRUCK_VEHICLE_SPRITES.md.

## 03/11/2026 — referências da traseira do caminhão
- A pedido do proprietário, pesquisadas fotos públicas de IVECO S-Way desacoplado (traseira e diagonais), além de fichas oficiais4×2/6×2. Fotos pessoais traseiras deixam de ser dependência obrigatória.
- Pintura vermelha e logos seguem as fotos recebidas; quantidade de eixos da unidade ainda não confirmada. Referências estruturais não foram incorporadas como fotos ao jogo. Ver TRUCK_REFERENCE_RESEARCH.md.

## 03/11/2026 — sprites do novo motorista
- Base final aprovada pelo proprietário após ajuste de braços/pernas e pequena barriga; boné vermelho Mercedes e FTW nova na polo vermelha.
- Seis poses de pódio geradas juntas a partir da mesma referência; entregues neutra, retrato, sete PNGs256×512, atlas, metadata/âncoraFX, prévia HTML e ZIP. Alpha/pivôs/hashes e reconstrução exata do pacote PASS; prévia Chromium móvel em dois tamanhos PASS.
- Nome ainda não confirmado. Esta etapa prepara arte; caminhão e integração jogável aguardam suas referências. As novas poses seguem para revisão visual. Ver TRUCK_DRIVER_SPRITES.md.

## 02/11/2026 — Felipe frontal na capa e correção da ativação do som
- Nova postura de Felipe aprovada para a abertura, com identidade preservada; retratos da seleção e demais sprites mantidos.
- Reproduzido primeiro toque no botão de som que desativava a música, apesar de mostrar SOM ON. Corrigidas ativação inicial, retomada e indicação do estado real.
- Incluída verificação pública de áudio ao vivo para música, motor e efeitos; Node47/47 e pacote local PASS. HTTPS verificado no run41507715470: corrida completa, áudio por toque/teclado,13efeitos pontuais/3contínuos e artifact inspecionado. Felipe frontal aprovado somente na abertura; versões anteriores preservadas. Ver FELIPE_AUDIO_FIX_QA.md.

## 02/11/2026 — pilotos e capa aprovados
- Proprietário aprovou os rostos corrigidos com base nos novos closes, as16poses de corpo inteiro e a capa com os logos oficiais.
- Preparados retratos próprios para menus, vistas com boné/capacete e12quadros novos de pódio; preservados os24arquivos NPC e seu resultado real.
- Capa integrada em camadas responsivas com carros canônicos, botões de toque e descarte do observador ao navegar; PNGs oficiais idênticos.
- Node45/45,174hashes e verificação técnica de16poses passaram; pacote e HTTPS PASS no run41497991461, com23arquivos aprovados conferidos por viewport e corrida natural completa. Ver APPROVED_PILOT_ART_QA.md.

## 02/11/2026 — NPCs conforme a referência de quatro carros
- Criados quatro atlases PNG e24sprites individuais: traseira, esquerda/direita e frenagem nas três vistas, preservando aerofólio, gaiola, lanternas, escapes e gancho da referência.
- Runtime Phaser usa as novas vistas com proporção e pivô verificados; seleção estável pelo volante e freio efetivo. Física e resultados preservados.
- Pesquisa de código público MIT registrada; nenhum código/asset/música de Top Gear importado.
- Node45/45, alpha/hashes, seis estados no Phaser real e corrida completa em dois tamanhos móveis emulados passaram localmente. HTTPS publicado e verificado no run41483753670, com13capturas e dois relatórios PASS. Versões anteriores preservadas. Ver NPC_REFERENCE_QA.md.

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


## 03/11/2026 — Marquinhos e cavalo mecânico jogáveis

Integração solicitada pelo proprietário: Marquinhos entra na capa, seleção e pódio usando o rosto/corpo/roupa preparados. IVECO vermelho4×2 sem carreta, com seis vistas reais e escala uniforme própria; câmera dimensiona o pelotão para manter a pista visível no celular. Colisão e desvio da IA consideram o porte maior. Daniel, Felipe e os quatro rivais existentes continuam correndo: sete participantes, classificação e pódio do vencedor real. Nenhum número/sobrenome foi inventado para Marquinhos. Retoque de Felipe com menos papada aplicado somente ao retrato da abertura.

Baseline47/47Node; integração70/70Node e248arquivos SHA256 conferidos. Testes adicionais de navegador e publicação têm resultados consolidados em V4_QA_REPORT.md; não tratar esta contagem como teste de aparelho Android físico. Plano/contratos em `superpowers/plans/2026-11-03-marquinhos-playable.md`.

Fechamento local desta integração:70/70Node,43hashes servidos em três viewports Chromium, corrida completa/resultado/pódio reais,12vistas do caminhão e áudio ao vivo passaram. Publicação das novas artes bloqueada pela revisão automática, aguardando confirmação específica do usuário; nenhuma ref remota movida. Ver V4_QA_REPORT.md e docs/qa/marquinhos-local-2026-11-03.json. Android físico não testado.

A revisão automática voltou a rejeitar um fragmento após a resposta “Ok se depender de mim está liberado”: exigiu autorização que nomeie as novas artes identificáveis e o destino GitHub público. Transferência novamente interrompida, sem alternativa/contorno.21objetos canônicos sem ref foram verificados; nenhuma branch/implantação movida. Tudo local está concreto: fonte`357cb810f870b3936c4c4016659f1156b91f0bb2`, árvore`5782c16fade29fc4c441bbac61e3dcc6cff3679d`; pacotePages`70b5e734cf9039b0cabf0e52560d03a3a6209cb8`, árvore`29b79b1c7b1900c4244b22d6998705bdad108ef1`.158arquivos runtime espelhados byte-idênticos,46legados preservados,38mudanças Pages restritas a `/teste-v4/`. Novo envio depende da confirmação explícita: publicar atualização e novas artes de Marquinhos, caminhão e capa no repositório público `andrervarella/FTW-Race` e jogo `/teste-v4/`.

Primeira publicação de Marquinhos e QA público41706301881: SUCCESS; ver relatório. Refinamento final da fonte do nome no card compacto, após quebra detectada em740×360; medidas locais568/740/915 passaram. Nenhuma mudança em gameplay/áudio/artes.

Entrega pública concluída: Marquinhos na capa/jogável, IVECO4×2 maior sem carreta, sete competidores, pódio e áudio. Nome inteiro na seleção compacta. Implantação41744987690 e QA público41745132125: SUCCESS; artefato/capturas conferidos e70/70Node após CSS. Nenhuma liberação pendente. Ver docs/V4_QA_REPORT.md.


## Correção do compartilhamento no WhatsApp
Endereço informado pelo usuário era o correto, mas o cache podia manter módulos/CSS antigos, mostrando apenas Daniel/Felipe. Empacotador agora publica o grafo completo em pasta imutável baseada no conteúdo; o HTML canônico e metadados de compartilhamento apontam para essa versão. Novo link exclusivo de Marquinhos evita os caminhos antigos já guardados. Nenhum sprite, rosto, simulação ou áudio foi alterado. Regressão com cache HTTP de um ano reproduziu2pilotos e confirmou3/7 no novo endereço sem limpeza de cache;70/70Node e6testes do resolver passaram. Publicação e QA público41793785508 concluídos com sucesso, conforme fechamento abaixo. V3 antiga continua em `/teste-v3/`.

## Carros no tamanho anterior e comandos fora do veículo
O usuário mostrou o carro de Daniel encoberto pelo nitro e confirmou que o tamanho anterior dos Mercedes era o desejado. A câmera volta exatamente a `min(largura*.22, altura*.47)` ao selecionar Daniel/Felipe; apenas a seleção do caminhão afasta a câmera em1.2×, preservando uma escala comum para todos na mesma cena. Não há redução de toda a frota pelo maior veículo. O caminhão permanece proporcionalmente maior, sem alterar artes ou física.

Nitro acima das setas, duas fileiras laterais equilibradas de comandos e corredor central reservado ao corpo útil do veículo, inclusive curvas, safe areas e controles montados após o grid. Chromium154 local:576estados/96capturas em915×412,740×360,568×320,1024×461,761×412,780×412,800×412 e844×412; três pilotos, seis vistas e quatro perfis de safe area. Sem interseção corpo/botões, todos os alvos≥44px, tamanho Mercedes igual ao anterior. Ver `game/tests/mobile-race-layout.py` e V4_QA_REPORT.md. Publicação e prova HTTPS serão registradas após execução; não houve teste em aparelho físico.


## Fechamento público — cache e tamanho dos carros
Publicado em `/teste-v4/releases/31dc249275b884df/`, com a entrada `/teste-v4/` apontando para a mesma árvore. Daniel e Felipe recuperaram o tamanho anterior; nitro acima das setas, corredor livre entre os comandos e caminhão maior. Corrigidos também o breakpoint intermediário e a troca de safe areas sem resize. Simulação, áudio e artes preservados.

Pages018b14fa95b3b6ef03c37e4618600732d9b07811, implantação41793665321 SUCCESS; fonte6f1cb94da72fed50fd7cb5ff2fcf0b0cb28477a0, QA público41793785508 SUCCESS. Chromium141:576estados/96capturas de layout, cache2→2→3/grid7/canônica3, fluxo de corrida real/pódio em três viewports,43hashes de arte por viewport,12vistas truck e áudio13+3 passaram. Ambos os ZIPs conferidos por SHA256/CRC; capturas de Daniel, Felipe, caminhão e fluxo real revistas.46páginas/arquivos legados preservados; V3 continua acessível. Nenhuma aprovação pendente. Prova estável: `docs/qa/cache-controls-public-41793785508.json`. Limites: emulação Chromium, sem WhatsApp/Android físico ou audição em alto-falante real.

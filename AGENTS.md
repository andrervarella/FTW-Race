# Instruções para agentes — FTW Race
Leia README.md, PROMPT_CODEX.md e docs/ antes de alterar o projeto.
Este é um projeto novo. Não importar Diabito, Joker, mecânicas fitness, marca AV ou código de outros projetos sem pedido.
Prioridade: direção e diversão > legibilidade > identidade visual > estabilidade.
Preservar decisões explícitas; diferenciar fatos, observações e propostas.
Referência correta: Top Gear do SNES, não Top Gun nem Lamborghini American Challenge.
Pilotos: Daniel Mencacci e Felipe Mencacci. Daniel #22 verde e Felipe #25 vermelho, conforme referências recebidas.
Escopo atual: somente Cascavel. Usar os mapas e fotos recebidos; validar sentido e geometria antes de modelar.
Não inventar rostos, números, pinturas, patrocinadores ou logos; não presumir endosso oficial.
Não extrair sprites, músicas ou código de Top Gear para o produto. Vídeo serve apenas à análise.
O usuário rejeita jogo genérico e Canvas como atalho procedural. Se a engine de navegador usar Canvas/WebGL, explicar e obter aprovação antes de adotá-la. Celular e comandos de toque estão confirmados; navegador versus aplicativo, sistema-alvo e engine ainda não escolhidos.
Nitro Diabo Verde em lata aprovado: ler docs/07_NITRO_DIABO_VERDE.md. Duas ativações por corrida são interpretação provisória, não quantidade confirmada. Não tratar tela dividida, combustível, pit stop ou multiplayer como aprovados.
Produzir assets reais, integrar, rodar e testar. Placeholders apenas identificados e provisórios.
Não declarar testes, FPS, screenshots, builds ou aprovações inexistentes.
Descobrir ferramentas realmente disponíveis; GPT público citado não equivale a ferramenta acessível.
Não gastar nem publicar sem autorização. O pedido atual autorizou preparar este repositório.
Ao implementar: manter estado, entrada, simulação, renderização, HUD, áudio e dados de pista separados. Registrar versão, execução, resultados e limitações.
Ao encerrar: commit das mudanças e atualização de docs/06_CHANGELOG_E_PENDENCIAS.md; nenhuma promessa de trabalho em segundo plano.

Referências visuais e sprites serão criados/revisados com o usuário neste chat e enviados ao repositório. Codex integra, organiza e testa os assets aprovados; não substituí-los por novas artes sem solicitação. Ler docs/08_MOBILE_E_PIPELINE_DE_SPRITES.md. Não declarar artes ainda não recebidas como existentes. Avançar com placeholders identificados apenas para validar mecânicas.

Atualização 31/10/2026: ler docs/09_ENTREGA_VISUAL_E_CONTINUIDADE.md primeiro para decisões atuais. Procedural moderado autorizado para a pista e repetição de elementos do entorno. Isso não substitui a identidade dos carros/pilotos nem decide automaticamente a engine. Prévias existem em assets/previews/, referências em referencias/. Preparar alpha, pivôs, escala e estados antes de integração.


## Atualização — lata recebida e Felipe com boné (31/10/2026)
Referências da lata Diabo Verde Pré-Workout, sabor Maçã Verde, 269 ml recebidas em referencias/marcas-e-produto/: frente, verso, apresentação e captura da página enviada pelo usuário. Esta atualização substitui as menções anteriores à lata pendente. Preservar formato alto/estreito, corpo preto, faixa verde, nome vertical e logo FTW do rótulo. A foto frontal é a referência principal para preparar o ícone e a animação; não incorporar os quadros promocionais laterais ao sprite. Logos independentes/vetoriais continuam pendentes; as marcas visíveis no rótulo já têm referência. Quantidade de nitro e demais regras continuam provisórias. A prévia assets/previews/ui/proposta-selecao-e-hud.png foi atualizada com Felipe de boné preto, conforme solicitado. Não há integração ou teste de gameplay nesta atualização.


## Correção prioritária de fidelidade — 31/10/2026
O usuário rejeitou a fidelidade da tela anterior. A foto referencias/pilotos-e-carros/dupla-canonica-bones-e-macacoes.jpg passa a orientar os retratos e macacões: Daniel à esquerda com boné preto Mercedes; Felipe à direita com boné VERMELHO nº25 (substitui a solicitação anterior interpretada como boné preto). Preservar os rostos reais e os painéis/patrocínios dos macacões.
Logos FTW e Diabo Verde RECEBIDOS como PNG originais em referencias/marcas-e-produto/. Aplicar esses arquivos diretamente na interface final, mantendo proporções; não recriar tipografia nem aceitar aproximações geradas. Não há mais pendência de referência de logo; estes PNG não são vetores.
O traçado jogável E o minimapa devem seguir cascavel-mapa-esquematico.png e cascavel-mapa-satelite.jpeg. Substituir o antigo rabisco da UI; manter sequência de curvas e proporções do circuito. Derivar minimapa da mesma geometria da pista, validar contra os mapas; não confundir pit lane laranja com circuito. Geração de imagem não garante precisão geométrica ou identidade exata de marcas. A tela revisada continua prévia sujeita a revisão, não aprovação automática nem prova da pista implementada.

## Pesquisa permanente em GitHub open source — 01/11/2026
Para toda nova função importante, ler `docs/REPOSITORIOS_PUBLICOS_E_POLITICA.md` e pesquisar repositorios públicos do GitHub (os sugeridos e alternativas melhores) como base técnica, aplicando apenas soluções compatíveis e licenciadas. Registrar fontes e testes em `docs/PESQUISA_OPEN_SOURCE_LOG.md`. Esta política não autoriza cópia de assets protegidos, troca de engine nem publicação sem autorização.


## REA — engenharia reversa responsável (02/11/2026)
- Avaliar o **REA — Reverse Engineer Anything** (https://github.com/morluto/rea) quando útil para investigar nossas builds, comportamentos, física, câmera, colisões e bugs. **Ler `docs/REA_ENGENHARIA_REVERSA.md` antes de usar.**
- Usar apenas em alvos próprios/autorizados; não extrair recursos/código de Top Gear ou jogos comerciais, nem contornar proteções. REA depende de acesso e instalação autorizados e não deve ser presumido disponível.

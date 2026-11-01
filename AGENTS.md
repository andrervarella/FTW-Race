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

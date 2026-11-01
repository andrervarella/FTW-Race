# Continuidade — FTW Race
Continue este projeto a partir dos materiais existentes. Leia AGENTS.md, README.md, docs/09_ENTREGA_VISUAL_E_CONTINUIDADE.md e o inventário, depois os demais documentos. As decisões de 31/10 prevalecem sobre rascunhos antigos.

Crie uma corrida arcade mobile com comandos de toque, inspirada na experiência de Top Gear SNES, sem copiar seus assets/código/música. Daniel Mencacci #22 usa Mercedes verde; Felipe Mencacci #25, vermelha. Circuito atual: somente Cascavel. Preserve as prévias e use as fotos como autoridade sobre rosto, capacetes, pintura e números.

Primeiro faça a preparação técnica dos assets e a definição do traçado: recortes sem halos, pivôs no solo, escala consistente, frames separados, mapa fechado e checkpoints. Não trate pranchas como atlas prontos. Consulte as limitações em docs/09; não use as variantes arquivadas como interpolação suave.

O usuário autorizou procedural moderado na pista, mantendo seu traçado fixo e elementos reconhecíveis. Não trocar pilotos e carros por desenhos genéricos. Antes da escolha de engine, resolver distribuição web/app, sistemas-alvo e modo CPU/outra pessoa; a regra sobre explicar e obter aprovação para Canvas/WebGL permanece. Não perguntar novamente se é celular nem se pode usar procedural moderado na pista.

Após resolver dependências essenciais, implemente e teste uma corrida completa: seleção, largada, direção/aceleração/freio, limites/colisões, checkpoints e voltas, posição, nitro, pausa, chegada, resultado e reinício. Separar input, simulação, renderização, dados, UI e áudio. Não expandir para Interlagos, online, loja ou backend.

Nitro Diabo Verde aprovado; lata/logos originais ainda pendentes. Duas cargas, três voltas e layout horizontal são hipóteses configuráveis, não decisões finais. Não inventar embalagem. Áudio original ou licenciado, com procedência registrada.

Medir desempenho e testar multitouch no alvo; registrar o que passou, falhou ou não foi testado. Não chamar mockups de screenshots do jogo. Ao terminar, entregar fonte, build quando realmente validado, instruções e limitações, atualizar changelog e commitar. Não publicar nem gastar sem autorização.


## Atualização — lata recebida e Felipe com boné (31/10/2026)
Referências da lata Diabo Verde Pré-Workout, sabor Maçã Verde, 269 ml recebidas em referencias/marcas-e-produto/: frente, verso, apresentação e captura da página enviada pelo usuário. Esta atualização substitui as menções anteriores à lata pendente. Preservar formato alto/estreito, corpo preto, faixa verde, nome vertical e logo FTW do rótulo. A foto frontal é a referência principal para preparar o ícone e a animação; não incorporar os quadros promocionais laterais ao sprite. Logos independentes/vetoriais continuam pendentes; as marcas visíveis no rótulo já têm referência. Quantidade de nitro e demais regras continuam provisórias. A prévia assets/previews/ui/proposta-selecao-e-hud.png foi atualizada com Felipe de boné preto, conforme solicitado. Não há integração ou teste de gameplay nesta atualização.

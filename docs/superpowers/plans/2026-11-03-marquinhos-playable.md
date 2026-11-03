# Marquinhos jogável — plano de integração

Pedido de 03/11/2026: o proprietário pediu aplicar as artes preparadas, incluir **Marquinhos** na capa e torná-lo jogável. Seu último “Ótimo” e pedido de integração são aceitação para este uso; não registrar uma nova citação “Aprovado” inexistente. A autorização anterior “Autorizo publicar código e assets publicamente” permanece válida para o repositório e `/teste-v4/`.

Base: branch `codex/truck-vehicle-sprites`, commit `8f45e72598ad01fcc43091e8501ae7bf01c547c1`; árvore limpa; `npm test` passou 47/47 antes das alterações. Implementar em `codex/marquinhos-playable`, preservando main, versão Claude e as páginas anteriores.

## Resultado esperado

- Terceiro piloto selecionável: **Marquinhos**, sem sobrenome ou número inventado. Retrato e seis poses preparados, sem gerar outra identidade.
- IVECO vermelho 4×2, cavalo mecânico simples sem carreta; Diabo Verde no para-brisa, FTW na porta. Nenhum ano/modelo exato presumido.
- Três pilotos oficiais + quatro rivais atuais = sete veículos. Todos podem vencer conforme a simulação; classificação e pódio usam o resultado real.
- Caminhão uniformemente maior em ambas as dimensões: multiplicador visual medido `1.7168195718654433`, combinado ao aspecto 560/512 do atlas. Área de colisão maior, parâmetros arcade identificados como aproximação e não medidas do veículo real.
- Capa com os três pilotos, seleção responsiva, nomes sem `null`, HUD dinâmico, todas as poses do caminhão e pódio de Marquinhos. Preservar os PNG oficiais das marcas.
- Concluir também o retoque de Felipe solicitado para a abertura, usando o derivado já preparado; não alterar seus outros sprites.
- Preservar desbloqueio de áudio no primeiro gesto, música, motor e efeitos, pausa, multitoque e teclado.

## Contratos e responsáveis

`PLAYABLE_KEYS = ['daniel','felipe','marquinhos']`; `DRIVERS.marquinhos.number = null`; `first/name = 'Marquinhos'`; `last = ''`; `vehicleType = 'truck'`; `renderScale = 1.7168195718654433`; `collisionWidthFactor = 1.4`; `collisionLengthFactor = 1.4`. Carros restantes usam fatores 1. Os nomes de arquivos em runtime terão prefixo `marquinhos`.

1. Gameplay: `config.js`, `sim.js`, testes puros de corrida/classificação/colisão.
2. Render/assets: `render.js`, `vehicle-visual.js`, cópia rastreável dos assets para runtime, manifestos/scripts de auditoria e testes de assets/render.
3. UI: `title.js`, `ui.js`, `styles.css`, seleção/capa/HUD/resultados e testes de fluxo/layout. Único editor desses arquivos.
4. Pódio: `podium.js`, testes de pódio/áudio offline; expor coordenadas de champanhe para consumo pelo dono da UI.
5. QA: testes de navegador real e workflow público, sem hooks de teste no produto.
6. Raiz: pesquisa licenciada, documentação, integração, revisão independente, commits e publicação verificada.

Tarefas independentes serão delegadas em paralelo com posse exclusiva de arquivos, seguindo a instrução de colaboração ativa. Dependências e ajustes cruzados serão enviados ao dono, sem edições concorrentes.

## Verificação e entrega

Primeiro registrar testes que falham para a nova funcionalidade, implementar e executar a suíte completa. No Chromium: capa/seleção desktop e celular, corrida natural com Marquinhos e sete participantes, todos os estados visuais, escala em profundidade igual, classificação/pódio de todos os vencedores, áudio liberado no primeiro gesto, pausa e multitoque. Validar caminhos relativos e ausência de 404. Auditar arquivos e origens; não afirmar Android físico ou audição humana sem medi-los.

Após revisão independente e correções: commit local, atualizar apenas `/teste-v4/`, conferir hashes das páginas anteriores, publicar fonte na branch V4 autorizada e verificar CI público e seu artefato. Atualizar changelog/QA com evidências e limitações reais; entregar link após verificação.

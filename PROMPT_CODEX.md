# Prompt de continuidade — FTW Race
Você está no repositório andrervarella/FTW-Race. Prepare e implemente um jogo original de corrida arcade inspirado na experiência de Top Gear (SNES), usando este repositório como fonte de verdade. Não precisa ter acesso ao chat original.

Leia AGENTS.md, README.md, todos os documentos numerados em docs/, referencias/README.md e referencias/PROMPT_MESTRE_ORIGINAL_V2_1.md antes de alterar código. Examine o vídeo de referência e o contato visual. Verifique se fotos foram adicionadas desde a preparação.

## Decisões confirmadas
Dois pilotos iniciais selecionáveis: Daniel Mencacci e Felipe Mencacci. Cada um com sua Mercedes fiel às fotos a receber. Corrida entre os dois, sem expandir elenco por conta própria. Duas pistas baseadas nos autódromos de Cascavel e Interlagos. Estilo e mecânica arcade inspirados no vídeo de Top Gear; não copiar seu código, sprites ou músicas.

## Antes de escolher stack
Plataforma final e modo de disputa não foram respondidos. Pergunte apenas o que ainda estiver faltando: onde jogar e se o adversário é CPU ou outra pessoa. Não confunda dois personagens com multiplayer já aprovado.
A preferência do usuário contra Canvas é explícita: se a solução web usa Canvas/WebGL, explique e obtenha aprovação antes de adotá-la. Não disfarce essa dependência.
Não inventar rostos, pinturas, logos ou números. Na ausência de fotos, avançar apenas com protótipos provisórios identificados, sem chamar arte genérica de final.

## Execução após resolver decisões essenciais
Faça plano curto, escolha arquitetura adequada e verifique ferramentas reais. Pesquise os traçados em fontes confiáveis e documente.
Implemente controles responsivos, corrida com estados de largada/ativa/pausa/resultado, limites, colisões, checkpoints/voltas/posição, seleção, reinício e áudio.
Separe simulação e renderização; dados de pilotos e pistas devem permitir expansão posterior.
Primeiro produza uma fatia representativa com uma pista e dois carros; depois complete a segunda pista. Não sacrificar qualidade para gerar volume.
Produza e integre assets próprios e exportáveis, com consistência de escala, perspectiva e identidade. Sons e música devem ser originais ou licenciados.
Tela dividida, nitro, combustível e pit stop não são decisões aprovadas. Discuta apenas se essenciais.
Registre QA real conforme docs/05_TESTES_E_QA.md. Corrija antes de entregar.
Entregue fonte, assets, build testado quando possível, instruções, evidências e pendências. Atualize documentação e faça commits.
Se ambiente impedir compilação ou teste no alvo, diga exatamente o que foi e não foi testado. Não declarar o jogo pronto só porque há código.
Não publicar nem consumir serviços pagos sem autorização.

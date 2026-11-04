# Link compartilhável e integridade de versão

O link canônico continua `/teste-v4/`. Para compartilhar uma versão específica, usar a `shareUrl` de `/teste-v4/version.json`, a árvore `releases/<runtimeRelease>/` indicada nesse manifesto. O empacotador gera o identificador dos bytes do runtime inteiro, sem timestamp. Não sobrescrever uma árvore existente com conteúdo diferente.

Execução: `python3 game/scripts/package-v4-release.py --output /workspace/FTW-Pages/teste-v4`. Só muda o entrypoint/metadata da V4 e adiciona releases; os arquivos antigos e versões anteriores continuam disponíveis. O endereço direto do release é a opção para WebViews que já guardaram também o HTML antigo. Queries apenas no entrypoint não propagam aos imports ESM/imagens. Não solicitar limpeza de cache como solução de publicação.

Verificação: `game/tests/cache-release.py` usa uma versão publicada de dois pilotos e cache longo no mesmo navegador; o HTML novo com URLs repetidas continua com2, o endereço imutável abre3/grid7 e o novo HTML canônico também3. Em CI, checkout secundário somente-leitura fixa o commit público antigo cc8d5b70d0dd9f113fbdd83ddf0814968e54bcdb. `published_runtime.py` resolve e valida a base da página; os probes de fluxo/áudio/render medem essa mesma árvore, incluindo43arquivos de arte e headers.

Limites: não houve acesso ao aplicativo WhatsApp/aparelho do usuário, nem cabeçalhos HTTP públicos pelo proxy local (CONNECT403). A reprodução é cache real de Chromium; a execução hospedada verificará a página HTTPS e seus cabeçalhos sem contornar o proxy. Status final e links ficam em V4_QA_REPORT.md.

Verificação local adicional: áudio ao vivo13efeitos e renderer12vistas passaram contra a entrada canônica empacotada, importando módulos pela base imutável efetivamente carregada.70/70Node e6testes do resolver passaram. Revisão independente recalculou o digest e conferiu158arquivos/157cópias não HTML idênticas.

Pacote final com correção de controles:159arquivos/158cópias não HTML idênticas. Regressão de cache novamente PASS com o runtime31dc249275b884df; layout576estados/96capturas e revisão adicional90casos PASS. Proveniência substitui os campos herdados pelo commit/árvore reais da fonte preparada.

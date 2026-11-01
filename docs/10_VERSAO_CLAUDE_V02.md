# Versão Claude v0.2 — registro (01/11/2026)

## O que foi feito
Reescrita legível (sem build) da lógica da v0.1.0 (que só existia minificada em gh-pages) com: traçado de Cascavel no mesmo vetor de pontos usado por pista, checkpoints e minimapa; sentido configurável (?sentido=inverso); rival CPU com ajuste leve de ritmo; fora do asfalto não trava mais em 0 km/h; fundo desliza ao curvar; aviso de giro para horizontal; tela cheia + tentativa de travar orientação; painel ?debug (fps, tela, toques, erros); erros visíveis na tela.

## Publicação
Arquivos publicados em gh-pages/claude/ (a raiz de gh-pages, v0.1.0, não foi alterada). Endereço esperado: https://andrervarella.github.io/FTW-Race/claude/ — NÃO verificado pelo Claude (sem acesso HTTP ao endereço); os arquivos foram conferidos no repositório. O usuário deve abrir no Chrome do Android e reportar.

## Traçado (validação)
Pontos de controle traçados à mão sobre cascavel-mapa-esquematico.png (36 pontos, Catmull-Rom). Comparado A OLHO com o mapa: mesma sequência de curvas 1–8. Sem medição de pixels. SENTIDO NÃO CONFIRMADO: a v0.1.0 percorre a reta dos boxes para cima (seta do esquemático); a seta vermelha do satélite sugere o oposto.

## Testes
EMULADOS (Node): 10/10 passaram — traçado fechado, multitoque lógico, largada, CPU completa 3 voltas (189,2 s; voltas 64,0/62,6/62,5), nitro 2 cargas, pausa, fora da pista, determinismo.
EMULADOS (Chromium headless, viewport 915x412, toque, DPR 2, STUB de Phaser e imagens substitutas): menu, largada, 2 e 3 toques simultâneos, cancelamento, pausa, retrato→aviso, resultado após 67 s, sem erros de console.
NÃO TESTADOS: Phaser real (WebGL/Canvas), imagens reais, desempenho/FPS, áudio, multitoque e tela cheia em Android físico, link publicado.

## Problemas relatados no Android (detalhes ainda não enviados)
Nada reproduzido no aparelho. Hipóteses, NÃO confirmadas: (1) abrir/largar em vertical pausa a corrida sem aviso claro; (2) na grama o carro travava em 0 km/h (física da v0.1.0 reproduzida no meu port, não no build publicado); (3) falhas de carregamento sem mensagem. Pedir ao usuário: modelo, navegador, o que acontece, print com ?debug.

## Pendências
Testar no Android; confirmar sentido do circuito; sprites com alpha revisado; ligar o mesmo código ao pipeline de assets de assets/sprites quando houver derivados.

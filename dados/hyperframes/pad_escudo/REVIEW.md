# Revisão · PAD como escudo

Quadros vistos: 0,6 · 0,8 · 2,0 · 3,1 · 4,7 · 7,6 · 10,5 · 11,5 · 11,75 s.

- Dados: todos os números vêm de `assets/serie.js` (R03). Pico 451 N sem PAD e 169 N com PAD, −63%, PAD com 86% da energia.
- Rótulos obrigatórios: "valor de teste" no topo e "modelo de molas, não é ensaio" no rodapé. Ambos estão na tela o tempo todo.
- Onda: os anéis são fortes na garra sem PAD. Com PAD são fortes no PAD e fracos na garra, que é a mensagem do vídeo.
- Corrigido nesta rodada:
  - a esfera começa mais baixa e não cobre o subtítulo;
  - o carimbo −63% saiu de cima da esfera (agora fica entre as faixas);
  - o rodapé subiu para 28 px.
- Aviso aceito: `container_overflow` em `#esc-lane-s/c` aos 10 s. São os anéis, recortados de propósito pelo contorno da garra e do PAD (`data-layout-allow-overflow`).
- Sem trinca: o modelo não prevê dano nessa batida.

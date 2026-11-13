# PAD como escudo · SPEC

- 12 s, 1920×1080, 30 fps, sem som (toca mudo em loop dentro do slide).
- Mensagem: a mesma batida de teste, com e sem PAD. Sem PAD a garra leva o golpe inteiro; com PAD o anel amassa, guarda a maior parte da energia e a garra recebe 63% menos força.
- Público: banca do desafio. Linguagem de estudante do SENAI, sem jargão. Nada de "tensão", "FEA" ou cor falsa de tensão.
- Dados: só `assets/serie.js` (gerado por `gerar_dados.py` a partir de `resposta_temporal_R03.csv`). Força, compressão do PAD, deflexão da garra e energia em cada instante. Nenhum número digitado à mão.
- Rótulo obrigatório na tela: "valor de teste" (esfera de 263 g a 1 m/s, 0,13 J) e "modelo de molas, não é ensaio".
- Sem trinca na garra: o modelo não prevê dano nessa batida (451 N é bem menos que os 1.380 N que a rompem).
- Tempo: 0–1 s títulos; 1–2,2 s as esferas descem; 2,2–9,2 s câmera lenta, 1 ms do modelo = 1 s de vídeo; 9,2–12 s resultado parado.
- Movimento ampliado: 12 px por mm (compressão do PAD e deflexão da garra); escrito na tela.
- Visual do deck (tema caderno técnico): papel #efece4 com grade de 28 px, tinta #141414, vermelho #d3241c (com PAD), azul-aço #24679a (sem PAD), PAD laranja #e07a1f. Títulos Archivo Black, rótulos IBM Plex Mono, texto Inter. Texto mínimo de 24 px.
- Onda de impacto: anéis que saem do ponto de contato. A força de cada anel vem da força do modelo no instante em que ele nasce. Dentro do PAD os anéis são fortes; quando chegam à garra, já estão fracos.
- Proibido: brilho, desfoque, degradê de fundo, contagem de vários números ao mesmo tempo, trinca, sombra exagerada.

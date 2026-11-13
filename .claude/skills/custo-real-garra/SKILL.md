---
name: custo-real-garra
description: Custo real (TCO) da garra SAI contra a garra de Tritan, com os custos ocultos (energia, máquina, mão de obra, refugo, paradas) e o ponto de encontro por caixas produzidas. Use ao refazer ou conferir os slides de Custos e Retorno, ou ao atualizar qualquer preço ou hipótese do modelo de custo.
---

# Custo real da garra SAI

O modelo fica em `dados/scripts/custo_real.py`. Ele lê as entradas de `dados/custos/entradas_custo.json` e grava `dados/custos/custo_real.json` (números) e `assets/js/custo-dados.js` (dados dos gráficos do site). Nada é digitado à mão no slide: o slide lê o `custo-dados.js`.

## Regras

1. **Cada entrada tem origem.** No `entradas_custo.json`, todo valor tem `fonte` (URL ou "equipe" ou "Orca" ou "FE") e `tipo`:
   - `equipe`: informado pela equipe (preços de filamento, quebras, troca da garra em 45 min com 280 caixas, troca dos PADs em 20 min, R$ 84.000);
   - `medido`: sai de um arquivo do projeto (Orca, FE);
   - `pesquisa`: valor de mercado com fonte pública e data;
   - `HIP`: hipótese nossa; precisa aparecer como hipótese no slide ou no relatório.
2. **Comparar igual com igual.** O Tritan também é impresso na casa (Hexa3D 30%), então os custos ocultos da impressão valem para os dois lados.
3. **Na dúvida, contra o SAI.** Quando houver faixa, o caso base usa o valor que favorece o Tritan. Assim o resultado não é inflado.
4. **Custo esperado, não sorteio.** As quebras do Tritan acontecem em média a cada 3 meses. O gráfico mostra o custo esperado acumulado, por isso é uma linha e não uma escada.
5. **Eixo X em caixas produzidas.** Ritmo da linha: cerca de 6 caixas por minuto, 24 h por dia (dado da equipe). O mês aparece só como referência.
6. **Produção perdida em caixas, nunca em reais.** O valor real da caixa para a fábrica não é conhecido. A parada é contada em caixas (6 por minuto) e em minutos de linha parada. Reais só no custo direto (impressão, peças, mão de obra).
7. **Vida da garra SAI.** Pior caso de colagem entre camadas: 2,4 anos (`estudo_custos.json`, 180 ciclos/h com 2 caixas por ciclo). Troca preventiva a cada 24 meses. PADs a cada trimestre. Conservador: vida de 12 meses e 1 quebra por ano, o mesmo do estudo de durabilidade.
8. **O ciclo de 2 anos não inclui a garra do ciclo seguinte.** A garra nova do mês 24 aparece só no gráfico de Retorno, que vai até 30 meses.
9. **Tempos de troca só da equipe.** Troca da garra (quebra do Tritan, instalação ou troca da SAI): 45 min, 280 caixas. Troca só dos PADs: 20 min, 120 caixas. Não inventar outro tempo nem janela de manutenção sem dado da equipe.
10. **Nada de dado pessoal** nos arquivos publicados (caminhos locais, nomes, e-mails).

## Como rodar

```bash
python dados/scripts/custo_real.py
python dados/scripts/custo_slides.py
python dados/scripts/verifica_numeros.py
```

`custo_slides.py` reescreve os slides de Custos e Retorno no `index.html` (trecho entre `CUSTO:INICIO` e `CUSTO:FIM`). O relatório fica em `dados/custos/CUSTO_REAL.md`.

## Agentes

- `pesquisador-custos`: busca valores de mercado no Brasil com fonte e data.
- `revisor-custos`: refaz as contas do modelo do zero, sem olhar o script, e aponta divergências.

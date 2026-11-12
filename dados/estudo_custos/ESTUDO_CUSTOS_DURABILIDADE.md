# Estudo de custos e durabilidade: garra SAI × garra de Tritan

Data: 12/11/2026. Garra SAI = R07 sem esqueleto, em PA6-CF, com 8 PADs de TPU 95A.
Script: `dados/scripts/estudo_custos.py`. Números: `dados/estudo_custos/estudo_custos.json`.

Este estudo é uma estimativa de engenharia, não um ensaio. Cada número indica de onde vem:
- **equipe:** dado informado pela equipe;
- **Orca:** fatiamento real;
- **FE:** simulação da garra montada;
- **HIP:** hipótese deste estudo, que precisa ser confirmada.

---

## 1. Resumo

1. **A durabilidade depende da colagem entre as camadas da impressão.**
   - Com o PA6-CF nos valores da ficha técnica (48 MPa entre camadas), a garra **não se cansa** na rotina. A fadiga passaria de 100 anos.
   - No pior caso de colagem (18,2 MPa, como o PAHT CF15), a vida cai para **cerca de 2,4 a 2,6 anos** em operação 24/7, com o ritmo real da linha.
2. **Recomendação para o cálculo de custo: vida de 24 meses.**
   - É o caso base: arredonda para baixo o pior caso de colagem.
   - Use 12 meses como conservador e 36 meses como otimista.
   - O teste de fadiga em bancada (item 6) confirma ou corrige esse número.
3. **A aquisição do slide está incompleta.** R$ 495,54 deixa de fora a energia da impressão e as peças perdidas. Com esses dois itens a garra SAI custa **R$ 566,02**, ainda sem mão de obra.
4. **Só em peças, o SAI ganha se durar mais de 7,3 meses sem quebrar.**
   - No cenário conservador (vida de 12 meses e 1 quebra por ano), o SAI gasta **mais** em peças que o Tritan: R$ 2.418 contra R$ 2.000 em 24 meses.
   - Por isso o argumento do projeto não pode ser só o preço das peças.
5. **O que pesa de verdade é a linha parada.**
   - Hoje são 4 paradas por ano, que somam 3 h, 1.120 caixas e **R$ 336.000 por ano** (equipe: R$ 84.000 por parada).
   - As peças de Tritan no ano custam R$ 1.000, ou seja, 0,3% disso.
   - Mesmo no cenário conservador, o SAI evita 3 de 4 paradas por ano.

---

## 2. Entradas

| Item | Valor | Fonte |
|---|---|---|
| PA6-CF | R$ 258/kg | equipe |
| TPU 95A | R$ 158/kg | equipe |
| Garra de Tritan | R$ 250 por garra; quebra a cada 3 meses (4 por ano) | equipe |
| Parada por quebra | 45 min, 280 caixas, R$ 84.000 (preço de mercado das caixas) | equipe |
| Prazo do material | Tritan 15–20 dias; PA6-CF 5–8 dias úteis | equipe |
| Bico endurecido | R$ 23,50 | equipe |
| Filamento da garra SAI | 1.744,5 g (com suportes); 75,2 h de impressão | Orca |
| Filamento dos 8 PADs | 139,0 g; 11,0 h de impressão | Orca |
| Peça superior | 46,5% da massa da garra (666 g de 1.433 g) | Orca |
| Tensão entre camadas a 24 kg numa asa | 12,34 MPa (estático); 18,09 MPa (tranco em 10 ms) | FE |
| Redução de força com o PAD | −63% na batida | modelo 1D |
| Ciclos por hora | 180: 6 caixas/min, 2 caixas por ciclo. O relatório R07 usou 480, mais conservador | HIP |
| Horas por ano | 8.760 (24/7, igual ao ROI atual) | HIP |
| Energia da impressão | 0,30 kW médio × R$ 0,90/kWh | HIP: medir com uma tomada medidora |
| Peças perdidas | 10% do material | HIP |
| Troca de PADs | conjunto de 8 a cada 2 meses (6 por ano) | HIP: premissa atual do slide |

---

## 3. Durabilidade da garra SAI

Método: a mesma curva de fadiga do relatório R07, σ/S = 1 − 0,10·log₁₀(N), com a regra de Miner.
- σ = tensão entre camadas no ponto crítico, a raiz da flange do robô.
- S = resistência entre camadas do material.
- Carga de rotina = 12 kg por asa × (g + 5 m/s²).

Conferência: o script reproduz as vidas publicadas no site (8.485 h e 1.079.797 h com 480 ciclos por hora). As entradas estão consistentes.

| | PA6-CF, ficha técnica (S = 48 MPa) | Pior colagem (S = 18,2 MPa) |
|---|---|---|
| Rotina, 180 ciclos/h, 24/7 | **mais de 300 anos** | **2,6 anos** |
| Rotina, 480 ciclos/h (hipótese do relatório) | mais de 120 anos | 1,0 ano |
| Erros de seladora (24 kg numa asa) até romper | 27 milhões | 1.659 |
| Erros a 30 kg até romper | 6 milhões | 33 |
| Tranco de 24 kg (10 ms) **sem** PAD | FS 2,65 | **FS 1,01: um tranco pode quebrar** |
| Tranco de 24 kg **com** PAD | FS 7,2 | FS 2,7 |
| Rotina + 52 erros/ano + 52 trancos/ano com PAD | mais de 300 anos | **2,4 anos** |

O que isso mostra:
1. **A rotina não é o problema.** O desgaste vem do número de ciclos, e o fator decisivo é a qualidade da colagem entre camadas, ou seja, a impressão: secagem do filamento, temperatura e orientação.
2. **Com colagem fraca, o PAD é obrigatório.** Sem ele, um único tranco de 24 kg fica no limite (FS 1,01). Com ele, o FS sobe para 2,7.
3. **Os erros de seladora quase não gastam a vida.** Mesmo 52 por ano somam só 3% do dano anual no pior caso.
4. **O que o modelo não cobre:**
   - **Umidade:** o PA6 absorve água e perde rigidez e resistência. A ficha técnica é do material seco.
   - **Fluência:** a flecha a 12 kg vai de 0,49 para 0,89 mm em 10.000 h, cerca de 14 meses em 24/7.
   - **Furos:** o desgaste é desprezível, mas os parafusos precisam de reaperto periódico.
   - **Batidas acima do previsto.**

   Por isso, com o PA6-CF bom, a vida real fica limitada por esses itens, e não pela fadiga. Não há dado para dar um número exato.

**Vida para o cálculo de custo:**

| Cenário | Vida da garra | Quebras inesperadas | Justificativa |
|---|---|---|---|
| Otimista | 36 meses | 0 | PA6-CF próximo da ficha técnica; limite dado por umidade e fluência |
| **Base** | **24 meses** | **0** | pior colagem (2,4–2,6 anos) arredondada para baixo |
| Conservador | 12 meses | 1 por ano | pior colagem com 480 ciclos/h (1,0 ano) e mais uma batida fora do previsto |

**PADs:** o PAD não carrega a carga de rotina; ele só trabalha nas batidas.
- Ele amassa a partir de cerca de 240 N e deve ser trocado quando estiver amassado, depois de uma batida ou numa inspeção.
- A troca de 6 conjuntos por ano é uma premissa, não um dado.
- Como o conjunto custa R$ 24,93, a premissa quase não muda o resultado: dobrar as trocas soma R$ 150 por ano.

---

## 4. Custo de aquisição: o slide × o custo completo

| Item | Slide atual | Custo completo | Observação |
|---|---|---|---|
| Material da garra (1.744,5 g × R$ 258/kg) | 450,08 | 450,08 | Orca + equipe |
| Material dos 8 PADs (139 g × R$ 158/kg) | 21,96 | 21,96 | Orca + equipe |
| Bico endurecido | 23,50 | 23,50 | custo de uma vez; o PA-CF gasta o bico |
| Energia (86,2 h × 0,30 kW × R$ 0,90) | — | 23,27 | HIP |
| Peças perdidas (10% do material) | — | 47,20 | HIP |
| **Total** | **495,54** | **566,02** | sem mão de obra |

Uma garra SAI de reposição (sem bico e sem PADs) custa **R$ 517,58**. Só a peça superior sai por cerca de **R$ 209** de material.

Mão de obra ainda fora da conta: preparar e acompanhar a impressão, tirar os suportes, montar e trocar PADs. Sugestão: a equipe cronometra uma vez e entra com o valor-hora.

---

## 5. Custo ao longo do tempo

### 5.1 Só peças (como no slide atual)

| Cenário | Tritan 24 meses | SAI 24 meses | Tritan 36 meses | SAI 36 meses |
|---|---|---|---|---|
| Otimista (36 meses) | 2.000 | **865** | 3.000 | **1.015** |
| **Base (24 meses)** | 2.000 | **865** | 3.000 | **1.532** |
| Conservador (12 meses + 1 quebra/ano) | 2.000 | 2.418 | 3.000 | 3.603 |

- **Ponto de equilíbrio:** o SAI gasta menos em peças se a garra durar **mais de 7,3 meses** sem quebrar.
- **O slide atual fala em "não quebra" sem dizer quanto tempo dura.** Por isso parece economizar para sempre.

### 5.2 Com a linha parada (custo de oportunidade)

| Cenário | Tritan 24 meses | SAI 24 meses | Diferença |
|---|---|---|---|
| Otimista / Base | R$ 674.000 | R$ 865 | R$ 673.000 |
| Conservador | R$ 674.000 | R$ 170.418 | R$ 503.600 |

Cuidados antes de usar esse número no slide:
- **Receita ou lucro?** R$ 84.000 é o preço de mercado de 280 caixas. A perda real é a margem que não volta, ou o custo de hora extra para recuperar a produção. Vale perguntar à Ajinomoto.
- **Quebra sem estoque:** se não houver garra de Tritan em estoque, a parada dura o prazo de entrega (15–20 dias) ou vira paletização manual. Isso é muito mais caro que 45 min.
- Esses números saíram do slide do problema numa revisão anterior; confirmar com a equipe se podem voltar.

---

## 6. Pontos que precisam de confirmação

1. **O que quebra no Tritan:** a garra inteira (R$ 250) ou só a peça superior? Muda o custo de reposição dos dois lados.
2. **Ritmo real:** quantos ciclos por hora (180?) e quantas horas por ano a linha roda.
3. **Quantas batidas e erros de seladora acontecem por ano**, mesmo os que não quebram a garra.
4. **Custo de oportunidade:** margem ou receita; existe estoque de garra de reposição?
5. **Energia:** medir o consumo de uma impressão com uma tomada medidora.
6. **Ensaio de fadiga em bancada (relatório R07, item 3.7):** 10⁵ ciclos de 0 a 24 kg numa asa. Isso confirma se a colagem real está mais perto de 48 ou de 18 MPa, que é o que decide entre 12 e 36 meses de vida.

---

## 7. Proposta para o novo slide de custos

1. **Custo de aquisição completo:** R$ 566, com a nota "sem mão de obra".
2. **Vida da garra:** 24 meses (base), com a faixa de 12 a 36 meses.
3. **Custo por ano** em três cenários, mostrando o ponto de equilíbrio de 7,3 meses.
4. **Linha parada à parte:** horas, caixas e, se a equipe aprovar, R$.
5. **Fontes e hipóteses** em uma linha: equipe, Orca, FE e HIP.

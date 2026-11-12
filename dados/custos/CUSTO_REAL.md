# Custo real da garra SAI × garra de Tritan

Gerado em nov/2026. Modelo: [`../scripts/custo_real.py`](../scripts/custo_real.py). Entradas e fontes: [`entradas_custo.json`](entradas_custo.json). Resultado: [`custo_real.json`](custo_real.json). Os slides de Custos e Retorno são escritos por [`../scripts/custo_slides.py`](../scripts/custo_slides.py), e os números são conferidos por [`../scripts/verifica_numeros.py`](../scripts/verifica_numeros.py).

## Resumo

- **A garra SAI custa R$ 1.121,29 pronta e instalada**, e não R$ 600. Esse valor inclui filamento, energia, impressora, bico, refugo, consumíveis e mão de obra.
- **Só no custo direto**, ela empata com o Tritan em **4,6 milhões de caixas (17,5 meses)**. Nos 2 anos do ciclo, custa **21% menos**: R$ 1.854,74 contra R$ 2.342,48.
- **Contando as caixas que deixam de sair nas paradas**, o SAI se paga em **79 dias** (683 mil caixas). Em 2 anos economiza **R$ 148 mil** e produz **1.640 caixas a mais**.
- **No cenário conservador**, a garra dura só 12 meses e quebra 1 vez por ano. Mesmo assim, o SAI se paga em 118 dias e economiza R$ 84 mil em 2 anos.
- **O ganho vem quase todo da previsibilidade.** As 8 paradas surpresa de 2 anos viram 8 trocas com data marcada: 1 garra e 7 trocas de PAD. A produção perdida é 99% do custo do Tritan.

## Vida de 2,4 anos: confirmada

- O valor vem de [`../estudo_custos/estudo_custos.json`](../estudo_custos/estudo_custos.json): **2,39 anos** no pior caso de colagem entre camadas (PAHT CF15).
- A conta usa 180 ciclos/h, 24 h por dia. São 6 caixas por minuto com 2 caixas por ciclo, uma em cada asa. A cada ano entram ainda 52 erros de 24 kg numa asa e 52 trancos.
- **Troca preventiva aos 24 meses**: fica abaixo dos 2,4 anos, com cerca de 5 meses de folga.
- Se um ciclo levasse só 1 caixa (360 ciclos/h), a vida no pior caso cairia para 1,2 a 1,3 ano. Por isso o cenário conservador usa 12 meses.

## Como o modelo conta

1. **Impressão** (vale para o SAI e também para o Tritan, que é impresso na casa):
   - filamento (g do Orca × R$/kg);
   - energia da impressora (0,20 kW) e do secador;
   - depreciação da impressora (R$ 5.500 em 5.000 h);
   - desgaste de hotend e placa;
   - bico endurecido (só no PA6-CF);
   - consumíveis;
   - refugo (10% no PA6-CF, 5% no TPU e no Tritan);
   - mão de obra do técnico (R$ 30,23/h com encargos) para preparar, retirar e acabar.
2. **Parada**: minutos de técnico + caixas que não saem × R$ 90. A caixa vale R$ 300 × margem bruta de 30%. O modelo conta a margem perdida, não o faturamento.
3. **Eventos**:

| Evento | Custo direto | Caixas perdidas | Total |
|---|---|---|---|
| Garra SAI nova (3 peças + 8 PADs, montagem, troca de 30 min) | R$ 1.121,29 | 180 | R$ 17.321,29 |
| Troca dos 8 PADs (10 min) | R$ 67,35 | 60 | R$ 5.467,35 |
| Quebra do Tritan (reimpressão da peça superior, 45 min) | R$ 292,81 | 280 | R$ 25.492,81 |
| Quebra da SAI (só no conservador) | R$ 1.128,84 | 280 | R$ 26.328,84 |

4. **Custo esperado**: o Tritan quebra em média 1 vez por trimestre, então a curva soma 1/4 de quebra por mês e meio. Por isso o gráfico é uma linha, e não uma escada.
5. **Eixo X em caixas**: 6 por minuto, 24 h, 262.800 por mês.
6. **O ciclo de 2 anos** termina antes da garra nova do mês 24, porque ela já serve o ciclo seguinte. O gráfico de Retorno vai até 30 meses e mostra essa troca.

## Para onde vai o dinheiro em 2 anos (custo direto)

| | Tritan (8 quebras) | SAI (1 garra + 7 trocas de PAD) |
|---|---|---|
| Filamento | R$ 1.425,60 | R$ 908,37 |
| Energia | R$ 42,64 | R$ 28,91 |
| Impressora e bico | R$ 386,56 | R$ 239,40 |
| Refugo e consumíveis | R$ 100,72 | R$ 113,22 |
| Mão de obra (com inspeção semanal) | R$ 386,96 | R$ 564,84 |
| **Total** | **R$ 2.342,48** | **R$ 1.854,74** |

## Valores da equipe que o modelo trocou

| Valor da equipe | Valor no modelo | Por quê |
|---|---|---|
| PA6-CF a R$ 258/kg | R$ 420/kg | É o preço de mercado em nov/2026 (Voolt3D R$ 420, Creality R$ 434). |
| R$ 250 por quebra do Tritan | 0,81 kg × R$ 220/kg + custos ocultos = R$ 292,81 | Preço de mercado do Tritan com certificação para alimentos, mais o mesmo custo de impressão do SAI. |
| R$ 84.000 por parada | 280 × R$ 90 = R$ 25.200 | A caixa que não sai é margem perdida, não faturamento. |
| Bico de R$ 23,50 de uma vez | R$ 0,20 por hora de PA6-CF | O bico se gasta com a fibra de carbono. |

## Sensibilidade (cenário previsto, muda uma entrada por vez)

| Caso | Encontro direto | Retorno com as caixas | Economia total em 2 anos |
|---|---|---|---|
| Base | 17,5 meses | 79 dias | R$ 148 mil |
| PA6-CF pelo preço da equipe (R$ 258/kg) | 12,6 meses | 78 dias | R$ 148 mil |
| PA6-CF Bambu Lab (R$ 786/kg) | não cruza | 82 dias | R$ 147 mil |
| Material do Tritan a R$ 250, mais os custos ocultos | 12,6 meses | 79 dias | R$ 149 mil |
| Caixa pelo preço de fábrica sem impostos (R$ 225) | 17,5 meses | 81 dias | R$ 111 mil |
| Caixa pelo EBITDA do setor (10%) | 17,5 meses | 88 dias | R$ 50 mil |
| Caixa pelo faturamento (R$ 300) | 17,5 meses | 76 dias | R$ 492 mil |
| Trocas programadas na janela de sanitização | 17,5 meses | 4 dias | R$ 202 mil |
| Inspeção semanal com a linha parada | 17,5 meses | não se paga | −R$ 133 mil |
| Mão de obra a R$ 43,91/h | 18,8 meses | 79 dias | R$ 148 mil |
| Impressora a 280 W e tarifa B3 | 17,4 meses | 79 dias | R$ 148 mil |
| Refugo de 20% no PA6-CF | 18,8 meses | 79 dias | R$ 148 mil |
| Tritan quebra só 2 vezes por ano | não cruza | 218 dias | R$ 46 mil |

O que decide o resultado:

- **onde a manutenção acontece:** a inspeção e as trocas devem entrar na janela semanal de limpeza;
- **quantas vezes o Tritan quebra de verdade.**

Os preços de filamento, energia e mão de obra mexem pouco no resultado.

## Revisão independente

Um agente revisor (`.claude/agents/revisor-custos.md`) refez as contas do zero, sem ler o script.

- **Veredito: confere.** As diferenças ficaram abaixo de R$ 0,07 e vêm de arredondamento.
- Ele também apontou pontos de hipótese. Os ajustes que vieram disso:
  - **Conservador mais duro.** O cenário passou a usar vida de 12 meses e 1 quebra por ano, o mesmo do estudo de durabilidade. Antes eram 24 meses.
  - **Inspeção na janela de limpeza.** Virou hipótese escrita no slide, e o caso com a linha parada entrou na sensibilidade.
  - **Valor da caixa.** O caso da caixa sem impostos (R$ 225) entrou na sensibilidade.
  - **Caso do Tritan a R$ 250 renomeado.** Agora deixa claro que os custos ocultos são somados por cima.
- Pontos que ficam em aberto, para confirmar com a equipe:
  - **280 ou 270 caixas por parada.** 45 min × 6/min dá 270. As 10 caixas a mais podem ser da retomada da linha. A diferença é 3,6% a favor do SAI.
  - **8.760 h por ano.** Com a janela de sanitização, o mais realista fica entre 8.400 e 8.550 h. O efeito é pequeno.
  - **A linha trabalha no limite da demanda?** Se houver folga, a caixa perdida é recuperada depois. Aí o custo real é a hora extra, não a margem.
  - **Custos que ainda não entram no modelo:**
    - garra reserva em estoque;
    - comissionamento na primeira instalação (TCP e carga no UR30);
    - impressões de calibração;
    - frete;
    - compra do secador;
    - adicional noturno e hora extra nas quebras de madrugada (estes favorecem o SAI).
  - **Contato com alimento.** O Tritan tem certificação NSF 51 e o PA6-CF não. Se a garra só pega caixas fechadas, o risco é baixo, mas é preciso confirmar.

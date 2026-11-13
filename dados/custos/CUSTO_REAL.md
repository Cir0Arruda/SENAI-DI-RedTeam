# Custo real da garra SAI × garra de Tritan

Gerado em nov/2026. Modelo: [`../scripts/custo_real.py`](../scripts/custo_real.py). Entradas e fontes: [`entradas_custo.json`](entradas_custo.json). Resultado: [`custo_real.json`](custo_real.json). Os slides de Custos e Retorno são escritos por [`../scripts/custo_slides.py`](../scripts/custo_slides.py), e os números são conferidos por [`../scripts/verifica_numeros.py`](../scripts/verifica_numeros.py).

O modelo separa duas coisas:

- **Custo direto em reais.** Imprimir, montar e trocar as garras, com preços de mercado.
- **Produção em caixas.** O modelo não converte caixas em reais: o valor real da caixa para a fábrica não é conhecido, então a produção perdida fica em caixas, que é o dado da linha.

## Resumo

- **A garra SAI custa R$ 1.121,29 pronta e instalada**, e não R$ 600. Esse valor inclui filamento, energia, impressora, bico, refugo, consumíveis e mão de obra.
- **Só no custo direto**, ela empata com o Tritan em **4,6 milhões de caixas (17,5 meses)**. Nos 2 anos do ciclo, custa **21% menos**: R$ 1.854,74 contra R$ 2.342,48.
- **Em produção**, a parada de instalação (30 min, 180 caixas) é compensada em **75 dias**, depois de cerca de 645 mil caixas produzidas. A partir daí o SAI perde menos caixas que o Tritan.
- **Em 2 anos**:
  - o SAI produz **1.640 caixas a mais**: o Tritan perde 2.240 e o SAI 600;
  - a linha fica parada **6 h com o Tritan e 1,7 h com o SAI**;
  - as **8 paradas surpresa** viram 8 trocas com data marcada: a instalação e 7 trocas de PAD.
- **No cenário conservador**, a garra dura só 12 meses e quebra 1 vez por ano. Mesmo assim, a instalação se compensa em 110 dias e o SAI produz 960 caixas a mais em 2 anos.

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
2. **Parada**:
   - o técnico entra no custo direto;
   - as caixas que não saem são contadas à parte: 6 por minuto, e 280 por quebra do Tritan (dado da equipe).
3. **Eventos**:

| Evento | Custo direto | Linha parada | Caixas perdidas |
|---|---|---|---|
| Garra SAI nova (3 peças + 8 PADs, montagem e troca) | R$ 1.121,29 | 30 min | 180 |
| Troca dos 8 PADs | R$ 67,35 | 10 min | 60 |
| Quebra do Tritan (reimpressão da peça superior e troca corretiva) | R$ 292,81 | 45 min | 280 |
| Quebra da SAI (só no conservador) | R$ 1.128,84 | 45 min | 280 |

4. **Valor esperado**: o Tritan quebra em média 1 vez por trimestre, então o gráfico mostra o valor esperado. Por isso é uma linha, e não uma escada.
5. **Eixo X em caixas**: 6 por minuto, 24 h, 262.800 por mês.
6. **O ciclo de 2 anos** termina antes da garra nova do mês 24, porque ela já serve o ciclo seguinte. O gráfico de Retorno vai até 30 meses e mostra essa troca.
7. **Paradas programadas**: o modelo supõe que elas também param a linha, o que é conservador. A inspeção semanal de 5 min cabe na janela de limpeza.

## Para onde vai o dinheiro em 2 anos (custo direto)

| | Tritan (8 quebras) | SAI (1 garra + 7 trocas de PAD) |
|---|---|---|
| Filamento | R$ 1.425,60 | R$ 908,37 |
| Energia | R$ 42,64 | R$ 28,91 |
| Impressora e bico | R$ 386,56 | R$ 239,40 |
| Refugo e consumíveis | R$ 100,72 | R$ 113,22 |
| Mão de obra (com inspeção semanal) | R$ 386,96 | R$ 564,84 |
| **Total** | **R$ 2.342,48** | **R$ 1.854,74** |

## Valores da equipe que o modelo trocou ou deixou de usar

| Valor da equipe | No modelo | Por quê |
|---|---|---|
| PA6-CF a R$ 258/kg | R$ 420/kg | É o preço de mercado em nov/2026 (Voolt3D R$ 420, Creality R$ 434). |
| R$ 250 por quebra do Tritan | 0,81 kg × R$ 220/kg + custos ocultos = R$ 292,81 | Preço de mercado do Tritan com certificação para alimentos, mais o mesmo custo de impressão do SAI. |
| R$ 84.000 por parada | não usado | O valor real da caixa não é conhecido. A parada é contada em caixas. |
| Bico de R$ 23,50 de uma vez | R$ 0,20 por hora de PA6-CF | O bico se gasta com a fibra de carbono. |

## Sensibilidade (cenário previsto, muda uma entrada por vez)

| Caso | Encontro no custo direto | Instalação compensada em caixas | Caixas a mais em 2 anos |
|---|---|---|---|
| Base | 17,5 meses | 75 dias | 1.640 |
| PA6-CF pelo preço da equipe (R$ 258/kg) | 12,6 meses | 75 dias | 1.640 |
| PA6-CF Bambu Lab (R$ 786/kg) | não cruza | 75 dias | 1.640 |
| Material do Tritan a R$ 250, mais os custos ocultos | 12,6 meses | 75 dias | 1.640 |
| Mão de obra a R$ 43,91/h | 18,8 meses | 75 dias | 1.640 |
| Impressora a 280 W e tarifa B3 | 17,4 meses | 75 dias | 1.640 |
| Refugo de 20% no PA6-CF | 18,8 meses | 75 dias | 1.640 |
| Tritan quebra só 2 vezes por ano | não cruza | 205 dias | 520 |
| 270 caixas por quebra (45 min × 6/min) | 17,5 meses | 78 dias | 1.560 |
| Trocas programadas na janela de sanitização | 17,5 meses | desde o início | 2.240 |
| Inspeção semanal com a linha parada | 17,5 meses | não compensa | −1.480 |

O que decide o resultado:

- **onde a manutenção acontece:** a inspeção e as trocas devem entrar na janela semanal de limpeza;
- **quantas vezes o Tritan quebra de verdade.**

Os preços de filamento, energia e mão de obra mexem só no custo direto.

## Revisão independente

Um agente revisor (`.claude/agents/revisor-custos.md`) refez as contas do zero, sem ler o script.

- **Veredito: confere.** As diferenças ficaram abaixo de R$ 0,07 e vêm de arredondamento.
- Ajustes que vieram da revisão:
  - **Conservador mais duro.** O cenário passou a usar vida de 12 meses e 1 quebra por ano, o mesmo do estudo de durabilidade.
  - **Inspeção na janela de limpeza.** Virou hipótese escrita, e o caso com a linha parada entrou na sensibilidade.
  - **Caso do Tritan a R$ 250 renomeado.** Agora deixa claro que os custos ocultos são somados por cima.
- Depois da revisão, a produção perdida deixou de ser convertida em reais, porque o valor real da caixa não é conhecido.
- Pontos que ficam em aberto, para confirmar com a equipe:
  - **280 ou 270 caixas por parada.** As 10 caixas a mais podem ser da retomada da linha.
  - **8.760 h por ano.** Com a janela de sanitização, o mais realista fica entre 8.400 e 8.550 h. O efeito é pequeno.
  - **Custos que ainda não entram no modelo:**
    - garra reserva em estoque;
    - comissionamento na primeira instalação (TCP e carga no UR30);
    - impressões de calibração;
    - frete;
    - compra do secador;
    - adicional noturno e hora extra nas quebras de madrugada (estes favorecem o SAI).
  - **Contato com alimento.** O Tritan tem certificação NSF 51 e o PA6-CF não. Se a garra só pega caixas fechadas, o risco é baixo, mas é preciso confirmar.

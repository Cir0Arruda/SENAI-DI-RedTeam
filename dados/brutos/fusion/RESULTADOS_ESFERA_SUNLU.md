# Esfera SUNLU ABS-Like — simulação exploratória

Data: 10/11/2026. Documento no Fusion: **Esfera 50mm SUNLU - Ensaios exploratorios**, salvo em Default Project.

## Execução e resultados

O estudo de tensão estática foi resolvido com sucesso na nuvem do Autodesk Fusion, sem consumo de créditos. Os valores abaixo foram lidos dos resultados do Fusion; as imagens estão incorporadas no relatório HTML nativo.

| Resultado para 100 N | Valor exibido |
| --- | --- |
| Tensão máxima de von Mises | 0,263 MPa |
| Tensão mínima de von Mises | 0,029 MPa |
| Deslocamento total máximo | aproximadamente 0,005 mm, arredondado pela legenda |
| Fator de segurança mínimo, critério de resistência máxima à tração | 59,155 |
| Nós da malha | 33.245 |
| Elementos sólidos parabólicos | 23.151 |

Esse fator de segurança é um indicador do critério escolhido no Fusion. Não comprova uma capacidade de compressão ou uma carga de ruptura: a resistência à compressão da resina não foi publicada nas fontes utilizadas. Não foi realizado estudo de convergência da malha, nem ensaio físico de validação.

## Geometria e condições de contorno

- Esfera maciça de diâmetro 50 mm, volume 65,44984695 cm³, massa nominal aproximada de 77,9 g.
- Superfície dividida nos planos z = −20 e +20 mm, preservando o volume.
- Calota inferior fixa em X, Y e Z; força distribuída na calota superior: Fx = 0, Fy = 0, Fz = −100 N.
- As calotas têm 785,398 mm² de área superficial cada. Não foram modelados pratos de compressão, contato ou atrito.
- Tamanho médio absoluto dos elementos configurado em 2,5 mm; elementos curvos e parabólicos.

## Material efetivamente usado pelo solucionador

Material físico **SUNLU ABS-Like - MODELO EXPLORATORIO**, atribuído ao modelo de simulação e conferido no relatório nativo. Os campos abaixo alimentam o solucionador; não são apenas anotações.

| Propriedade | Valor | Origem e condição |
| --- | --- | --- |
| Densidade sólida | 1.190 kg/m³ | SUNLU SL-TE-WI-100 A/0; valor típico, tolerância publicada ±30 kg/m³ |
| Resistência máxima à tração | 28 MPa | SUNLU SL-TE-WI-100 A/0, direção Z |
| Módulo de Young | 1.020 MPa | TDS anterior da SUNLU ABS-Like; equivalência da formulação com a TDS atual não demonstrada |
| Poisson | 0,35 | Aproximação: modelo de outra resina SLA, HTM140 V3, Dempsey et al. (2020), Tabela 7 |
| Condutividade térmica | 0,30 W/(m·K) | Mesma aproximação de literatura; não é medição da SUNLU |
| Calor específico | 1.030 J/(kg·K) | Mesma aproximação; não influencia a solução térmica estacionária |
| Expansão térmica linear | 101 × 10⁻⁶ K⁻¹ | SUNLU SL-TE-WI-100 A/0 |
| Módulo de cisalhamento | 377,778 MPa | Derivado de E/[2(1+ν)] no modelo isotrópico |
| Resistência ao escoamento | indisponível | Campo numérico do Fusion em zero; não representa uma medição. Fator de segurança configurado para resistência máxima à tração |

A ficha atual informa módulo de **flexão** de 980 MPa. Ele não foi confundido com módulo de Young. O modelo combina fontes e aproximações para permitir um teste demonstrativo; não constitui uma caracterização validada da resina SUNLU ou do lote do usuário. Orientação de impressão, pós-cura e porosidade reais não foram informadas. O modelo é linear elástico e isotrópico.

## Estudos térmicos preparados e bloqueados

| Estudo | Condições | Estado |
| --- | --- | --- |
| Estudo 2 - Térmico | Calota superior a 80 °C; faixa intermediária com convecção h = 10 W/(m²·K), ambiente 20 °C; calota inferior adiabática; regime estacionário; malha configurada em 2,5 mm | Pronto no Fusion, não resolvido: exige 3 créditos de nuvem e a conta informou saldo insuficiente |
| 03 Termomecanico 80C - EXPLORATORIO | Mesmas condições térmicas; temperatura sem tensão de 20 °C; calota inferior fixa XYZ; sem força mecânica adicional; malha configurada em 2,5 mm | Pronto no Fusion, não resolvido: exige 3 créditos de nuvem e a conta informou saldo insuficiente |

Temperaturas, carga e convecção são condições demonstrativas escolhidas para o teste, não propriedades pesquisadas do material. O coeficiente de convecção é assumido e não foi validado para uma montagem real. Não há resultados térmicos calculados a apresentar. O total indicado para executar os dois estudos é de 6 créditos; nenhuma compra foi realizada.

80 °C excede a Tg publicada de 44 °C e a HDT de 50 °C (ensaio a 0,45 MPa). O modelo não contém propriedades em função da temperatura, amolecimento, fluência, plasticidade, dano ou fratura. Mesmo após resolver o estudo termomecânico, ele não validará resistência mecânica real a 80 °C sem dados adicionais.

## Arquivos

- `Esfera_50mm_SUNLU_ABS_Like_SIMULACAO.f3d`: cópia local do projeto com o material físico e os três estudos. A recuperação dos resultados de nuvem pode depender do documento e da conta originais.
- `Esfera_SUNLU_100N_Relatorio_Fusion.html`: relatório nativo exportado pelo Fusion, com propriedades do material, cargas, malha e imagens dos resultados. A tabela numérica de extremos saiu vazia no exportador; os valores deste resumo foram lidos na interface/legendas. A exportação foi preservada sem alterar os números.
- `SUNLU_ABS_Like_MODELO_PESQUISADO.json`: entradas e rastreabilidade das aproximações.
- `SUNLU_ABS_Like_DADOS_CONFIRMADOS.json`: registro separado dos dados da ficha atual.
- `SUNLU_ABS_Like_TDS_SL-TE-WI-100.pdf` e `SUNLU_ABS_Like_TDS_Anterior_Modulo_Young.pdf`: fichas arquivadas.
- Arquivos com `PENDENTE_RESINA` ou `DADOS_CONFIRMADOS.f3d` são versões históricas anteriores a este cálculo.

## Fontes

1. [SUNLU, TDS atual SL-TE-WI-100 A/0](https://media.sunlu.com/prod/20260331/cdd6ab82-85d8-49ea-b432-12c6c9c5c005.pdf?filename=TDS). Propriedades típicas de laboratório, não especificações garantidas.
2. [SUNLU, TDS anterior ABS-Like](https://cdn.shopify.com/s/files/1/0152/6507/1190/files/SUNLU_ABS-Like_UV_Resin_Data_Sheet.pdf?v=1691779412). Módulo de Young de 1.020 MPa; outras propriedades diferem da ficha atual.
3. [Dempsey et al., Characterization of Stereolithography Printed Soft Tooling for Micro Injection Molding (2020), Tabela 7](https://pmc.ncbi.nlm.nih.gov/articles/PMC7570071/). Poisson, condutividade e calor específico usados como aproximações para outra resina SLA.

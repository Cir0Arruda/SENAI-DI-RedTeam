# SAMI — estimativa matemática do PAD R02, sem Fusion

**Cálculo exploratório de um sistema de molas. Não é simulação por elementos finitos, ensaio físico ou previsão certificada da garra.** Reutiliza dados já disponíveis; nenhum acesso ao Fusion nem nova pesquisa.

## Hipóteses

Garra PA-CF com núcleo30% e PAD TPU95A com núcleo40%. Isso não significa reduzir toda resistência ou massa pela porcentagem de preenchimento. As paredes densas contribuem de forma diferente.

PAD local: espessura lateral6,3 mm, duas peles sólidas de1,2 mm e núcleo3,9 mm. Referência E sólido33,6 MPa da ficha PolyFlex TPU95 V5.4. Núcleo com E=33,6×0,4²=5,376 MPa é uma hipótese de homogeneização não calibrada. Compressão em série das peles/núcleo: E equivalente=t/(2,4/33,6+3,9/5,376)=7.905882 MPa.

Área constante de contato adotada apenas para exemplo:100 mm², equivalente a um quadrado10×10 mm. Contato real da esfera com o PAD tem área variável. Rigidez linear k=E×A/t=125.490196 N/mm. A compressão lateral confinada, a orientação e a velocidade podem alterar muito essa rigidez.

Impactador: esfera de aço de raio20 mm, massa0,263056 kg, mesmo exemplo geométrico preparado anteriormente. **Não representa a massa efetiva do robô mais garra e carga.** Colisão do robô exige massa/inércia refletida na direção do impacto, velocidade e atuação do controle.

## Energia, força e compressão

W=½mv². Para uma mola elástica inicialmente descarregada, W=½kδ²; logo δ=sqrt(2W/k) e Fmax=kδ. Usar W em N·mm (1000 vezes J) com k em N/mm. Supõe que toda energia inicial se converte temporariamente em compressão da mola, sem perda ou outro caminho de energia; não calcula dano.

**Tabela com apoio rígido atrás do PAD e área hipotética100 mm²:**

| Velocidade m/s | Energia J | Pico elástico N | Compressão mm | Compressão/espessura |
|---|---|---|---|---|
| 0.5 | 0.0329 | 90.8 | 0.72 | 11.5% |
| 1.0 | 0.1315 | 181.7 | 1.45 | 23.0% |
| 2.0 | 0.5261 | 363.4 | 2.90 | 46.0% |

Os resultados a grandes deformações são extrapolações da lei linear, não previsões quantitativas confiáveis. A1 m/s, a compressão global é aproximadamente23%; no núcleo mais flexível, a compressão calculada é aproximadamente34%. A2 m/s, cerca46% global e68% no núcleo tornam a extrapolação especialmente inadequada: não demonstram que o PAD suporta esse impacto. Densificação, instabilidade do preenchimento, rigidez da pele e variação de área não foram calculadas. A tensão média nominal F/A não é a tensão máxima na garra.

Tempo de contato completo, compressão mais restituição, no oscilador sem perdas com apoio rígido: π sqrt(m/k)=4.549 ms. É apenas estimativa de escala temporal; o evento antes proposto de3 ms poderia não conter o rebote completo.

## Comparação com/sem PAD — sensibilidade à rigidez desconhecida da garra

Uma comparação de força exige rigidez da garra na direção do contato. Chamando-a Kg, a garra sem PAD tem k0=Kg; com PAD em série, k1=Kg×Kpad/(Kg+Kpad). À mesma energia, Fcom/Fsem=sqrt(Kpad/(Kg+Kpad)).

**Valores Kg abaixo são cenários arbitrados, não calculados para esta geometria nem medidos.** Conservam a rigidez da garra e o mesmo caminho de carga entre os dois casos; a redistribuição real do contato pode mudar isso.

| Kg hipotético N/mm | Pico sem PAD N | Pico com PAD N | Redução dentro da hipótese |
|---|---|---|---|
| 100 | 162.2 | 121.0 | 25.4% |
| 500 | 362.7 | 162.4 | 55.2% |
| 1000 | 512.9 | 171.3 | 66.6% |

Essas reduções não são uma faixa de confiança da garra real: somente ilustram três escolhas de rigidez. Se a garra for muito mais flexível que o PAD, o ganho em pico de força pode ser pequeno. Se for muito mais rígida, o PAD pode dominar a deformação. Para converter força em tensão de flexão local ou delaminação seriam necessários seção, vão, direção das camadas, apoios e contato. O efeito de elevar a cobertura em5 mm é geométrico; não foi convertido em aumento de vida.

## Interpretação para proteção

O modelo permite explicar como uma camada deformável pode alongar a parada e reduzir o pico transmitido, desde que não atinja fim de curso e permaneça retida. **O benefício é plausível, ainda não quantificado para esta garra.** Não demonstra que PA-CF30% supera o Tritan instalado em impacto. Rigidez maior, resistência última e tenacidade/interlaminar são propriedades distintas.

O modelo é elástico: energia armazenada volta no rebote. Não há cálculo de energia dissipada, histerese, amortecimento, rasgo, deformação permanente ou falha das camadas. Não usar os picos como carga admissível.

## Operação24/7 e desgaste

24/7 corresponde a8760 h/ano para365 dias. Em ciclo de10 s seriam3.153.600 ciclos/ano. Isso só seria igual ao número de impactos se houvesse exatamente um impacto por ciclo; frequência de colisão normalmente é outra variável.

Não existe vida numérica defensável a partir de dureza95A, módulo e preenchimento. Faltam dados de fadiga/rasgo do PAD e da impressão PA-CF, compressão permanente, temperatura/umidade e espectro de impacto. Para deslizamento, uma estimativa tipo Archard usa Vdesgaste=K×F×distância/H, com K e H compatíveis e calibrados; Shore A não deve ser convertido diretamente em dureza de indentação para preencher essa equação. Não se inventou coeficiente de desgaste ou prazo de troca.

Nenhuma previsão térmica foi realizada. Temperatura de impressão não é temperatura admissível de serviço. O modelo não calcula relaxação, fluência ou variação de rigidez com temperatura.

## Massa

Para mesmo volume depositado, densidades de referência PA6-CF1,09 e Tritan1,18 g/cm³ dão redução de7,63% apenas da parcela polimérica substituída. Não é redução de7,63% da garra completa.

Conjunto de8 PADs R02:129,215 g se integralmente maciço a1,22 g/cm³.40% sem paredes/peles seria51,686 g; perfil com paredes/peles fica entre esses valores para a mesma densidade, excluindo fixações. Massa definitiva requer fatiamento. A ficha de densidade do TPU vai de1,20 a1,24 g/cm³.

## Referências reutilizadas

- PolyFlex TPU95 TDS V5.4: cópia local em fontes_industriais/PolyFlex_TPU95_TDS_EN_V5_4.pdf; fonte https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyFlex_TPU95_TDS_EN_V5.4.pdf?v=1731956391 . Dados de ensaio XY100%, não do PAD40%.
- Geometria e hipóteses: impacto_R02_status.json e pad_r02_scope.json.
- Memória numérica: estimativa_analitica_PAD_R02.json.

O bloqueio do Fusion permanece no histórico e não é alterado por estes cálculos externos.

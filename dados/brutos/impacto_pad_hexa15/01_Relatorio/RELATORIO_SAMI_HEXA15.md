# SAMI - PA-CF / Hexa3D15% /5 perímetros e PAD TPU95A40%

**Relatório de cálculo reduzido1D e preparação geométrica. Não é FEA nem validação da garra.**


## 1. Escopo e resultado disponível

Revisão R03 matemática, 11/11/2026. O relatório anterior e a memória de cálculo foram incorporados como histórico, com a nova configuração da garra: PA-CF, cinco perímetros e núcleo Hexa3D de 15%. O PAD permanece TPU95A, núcleo40%, conforme o pedido anterior. A largura de linha0,40 mm e topo/fundo1,20 mm continuam hipóteses; cinco perímetros equivalem nominalmente a2,0 mm de parede lateral apenas sob essa largura.

Foi calculado um impacto em um modelo reduzido de molas e uma viga substituta. Não houve nova utilização do Fusion. Não foi resolvida uma malha da montagem com Hexa3D15%, contato espacial, falha ou temperatura. As imagens de movimento são uma representação cinemática sobre um recorte visual do CAD nominal.

No exemplo de esfera263 g a1 m/s, o modelo dá pico de450.9 N sem PAD e168.5 N com PAD: redução de62.6% dentro das hipóteses. Esse percentual não foi demonstrado na garra real. O PAD armazena temporariamente0.113 J; dissipação irreversível não foi caracterizada.

![Figura](figuras/montagem_PAD_R02.png)

Montagem nominal R02: proteção laranja ampliada5 mm para a região superior. Imagem CAD, sem campo de tensões ou deformações.

| Item | Situação nesta entrega |

| --- | --- |

| Cálculo de impacto1D | Calculado, exploratório |

| Geometria / STL PADs R02 | Exportados; oito malhas fechadas verificadas |

| Malha real da garra Hexa3D15% | Não resolvida |

| Desgaste / fadiga / temperatura | Sem previsão caracterizada |


## 2. Materiais, paredes e modelo matemático

Referência da garra: Bambu PA6-CF V3.0, módulo XY4430 MPa e densidade1,09 g/cm³. A direção das camadas não foi mapeada ao CAD neste cálculo. Os valores de corpos de prova não são limites admissíveis da peça. Referência do PAD: PolyFlex TPU95 V5.4, módulo XY33,6 MPa, dureza95A e densidade1,20-1,24 g/cm³, com corpos de prova100% preenchidos. O módulo não caracteriza sozinho compressão rápida ou amortecimento.

A rigidez da garra foi representada por uma viga engastada de vão30 mm, seção externa30 x10 mm, paredes laterais2 mm e topo/fundo1,2 mm. Essas dimensões são assumidas e não foram extraídas da seção crítica da garra. As paredes trabalham com E sólido; o núcleo usa E*=E sólido vezes p elevado a n. Para p=0,15 e n=2, E*=99,675 MPa. Não há calibração dessa lei para o Hexa3D informado. A sensibilidade n=1;1,5;2 não é intervalo de confiança.

Para flexão da seção: I externo=b h³/12; I núcleo=(b-2w)(h-2s)³/12; EI=E sólido(I externo-I núcleo)+E núcleo I núcleo; K garra=3EI/L³. Isso considera pele e núcleo separadamente, sem reduzir toda a peça a15% da rigidez.

PAD: seção lateral6,3 mm com duas peles sólidas1,2 mm e núcleo3,9 mm. Hipótese E núcleo=33,6 x0,40²=5,376 MPa. Área de contato constante100 mm², assumida. K PAD=A/(2,4/33,6+3,9/5,376)=125,49 N/mm. A compressão confinada e a área variável real não foram resolvidas.

Contato começa em t=0, retenção é ideal e o alvo é uma mola sem massa. K equivalente=K garra x K PAD/(K garra+K PAD). Com massa m, velocidade v e omega=raiz(K equivalente/m), x(t)=(v/omega)sen(omega t), entre0 e pi/omega; F=K equivalente x. Depois da separação, a esfera retorna com velocidade-v. Todas as unidades são convertidas entre mm/N e m/kg/s.

![Figura](figuras/secao_substituta.png)

Seção idealizada usada no modelo; não é um corte dimensional medido na garra.

| Parâmetro | Valor / origem |

| --- | --- |

| K garra (seção assumida) | 772.93 N/mm |

| K PAD (seção/área assumidas) | 125,49 N/mm |

| Massa efetiva real do robô | Desconhecida; esfera não representa robô+carga |


## 3. Força e deformação do modelo reduzido

As curvas abaixo são a solução temporal do oscilador elástico definido na seção2. A simulação1D calcula força comum às molas em série, compressão do PAD e deflexão da viga. Não calcula deslocamento por nó nem tensão máxima em furos, nervuras, camadas ou parafusos da montagem.

A tensão de flexão indicada é apenas a tensão na pele da viga substituta, pela curvatura M/EI. Não é tensão da garra CAD, nem foi comparada a um critério de ruptura ou usada para declarar fator de segurança.

![Figura](figuras/resposta_forca_deslocamento.png)

Força e deslocamentos do modelo1D, sem amortecimento. O rebote elástico completo está incluído.

| Grandeza do modelo | Sem PAD | Com PAD |

| --- | --- | --- |

| Pico de contato (N) | 450.9 | 168.5 |

| Deflexão máxima da viga (mm) | 0.583 | 0.218 |

| Compressão do PAD (mm) | - | 1.343 |

| Tempo completo de contato (ms) | 1.833 | 4.904 |

| Flexão na pele da viga (MPa) | 43.07 | 16.10 |


## 4. Energia e validade da aproximação

A energia inicial é0,131528 J. No instante de compressão máxima, o PAD armazena0.113156 J (86.0%) e a viga0.018372 J. A energia cinética nesse instante é zero e volta no rebote. O modelo assume dissipação0 J; isso não significa que o TPU real dissipe zero. Histerese, viscosidade, atrito e aquecimento não foram caracterizados.

A compressão calculada do PAD é1.343 mm, aproximadamente21.3% da espessura global. Como o núcleo é mais flexível, a deformação nominal nele chega a31.3%. Isso excede uma interpretação de pequenas deformações: rigidez linear constante, área fixa e núcleo não densificado são aproximações fortes. Os valores servem para estudar o mecanismo, não para aprovar resistência.

O impacto não cria uma força fixa determinada apenas pelo material. A energia cresce com a massa efetiva e com o quadrado da velocidade; dobrar a velocidade quadruplica a energia. A massa de24 kg da carga útil anteriormente indicada não foi usada como massa do impactador. A massa/inércia refletida do robô e sua parada controlada precisam ser definidas para uma colisão de serviço.

Neste exemplo com paredes densas, trocar30% por15% reduz K da viga de804.53 para772.93 N/mm (3.93%, para n=2). Não se conclui que a garra real perderá apenas essa rigidez: espessuras, vãos, direção, torção, delaminação e geometria do Hexa3D podem alterar a resposta.

![Figura](figuras/balanco_energia.png)

Energia armazenada não equivale a energia dissipada. Erro máximo do balanço numérico:8,33e-17 J; isso verifica as contas do modelo, não sua fidelidade física.

| Limite | Consequência |

| --- | --- |

| Núcleo Hexa3D não modelado explicitamente | Sem flambagem/densificação local |

| Sem leis de falha e delaminação | Sem carga de ruptura ou dano |

| Sem amortecimento medido | Sem absorção irreversível ou temperatura |


Como verificação de escala, se a massa efetiva fosse24 kg a1 m/s, a energia seria12 J. Extrapolar a mesma mola daria compressão do PAD de12.83 mm, maior que seus6,3 mm: o modelo ficaria fisicamente inaplicável e não demonstraria proteção. Isso não afirma que a massa efetiva real seja24 kg; a carga útil não determina sozinha a inércia refletida do robô.

O impulso total calculado é0.526112 N.s nos dois casos elásticos, porque a esfera retorna com a mesma velocidade. O PAD reduz o pico e prolonga o contato neste modelo; não reduz a variação total de quantidade de movimento. Dissipação e coeficiente de restituição reais poderiam alterar esse resultado, mas não foram medidos.

## 5. Imagens e animação da região protegida

A animação usa um recorte visual A1 do STL original e as duas metades reais do PAD R02. As ferragens que aparecem pertencem ao recorte da montagem e não foram reclassificadas como PA-CF. A esfera é uma representação do impactador definido no modelo.

Os deslocamentos1D foram impostos graficamente: translação ilustrativa da região de apoio e compressão gradual da face externa do PAD, com ampliação2x. Esse mapeamento não resulta de equilíbrio espacial ou de uma solução por elementos finitos. Não há mapa de tensões em falsas cores, nem arquivo CAD deformado validado. Os vazios Hexa3D15% não foram gerados na malha visual.

R02 protege o rebordo superior em mais5 mm e preserva acesso aos parafusos. A verificação geométrica anterior foi contra os corpos principais; não abrange mangueiras, ferramenta de aperto, movimento ou retenção deformada. A cinta e o encaixe ainda não têm pré-carga, atrito ou força de soltura caracterizados.

![Cinemática ilustrativa](figuras/impacto_inicio.png)

![Cinemática ilustrativa](figuras/impacto_pico.png)


## 6. Massa, durabilidade e operação24/7

Não foi estimada uma vida em horas ou um prazo de troca. Para24/7,365 dias correspondem a8760 h. Um ciclo a cada10 s dá3.153.600 ciclos/ano; só corresponderá a impactos se houver um impacto por ciclo. A lei elástica usada não acumula dano, desgaste ou deformação permanente.

Desgaste por deslizamento requer carga normal, distância, rugosidade, meio e coeficiente calibrado; fadiga/rasgo requer curvas cíclicas e orientação compatíveis. Relaxação e fluência do PAD e da garra precisam de dependência com tempo, tensão, temperatura e umidade. Uma tensão pequena em um único evento não demonstra vida longa.

Temperatura não foi calculada. A ficha de processamento do TPU não define temperatura contínua admissível de uso. As curvas E(T), resistência(T), histerese e compressão permanente do material impresso40% não estão disponíveis nesta entrega. PA-CF também depende de condicionamento de umidade e orientação. Não há comparação válida de vida entre o PA-CF proposto e o Tritan impresso instalado.

O PAD é de sacrifício: perda de retenção, trinca, rasgo, esmagamento residual e espessura remanescente são variáveis a acompanhar em ensaios físicos. Nenhum limite quantitativo de troca foi validado. Como próximo dado de maior valor, medir força versus compressão e descarregamento do PAD no perfil real e medir a rigidez local da garra permite substituir duas hipóteses dominantes deste modelo.

Para o mesmo volume depositado, PA6-CF1,09 versus Tritan1,18 g/cm³ dá redução teórica7,63% apenas da parcela polimérica substituída. A massa da montagem inteira precisa da parcela substituível e das ferragens. Cinco perímetros e topo/fundo fazem a massa exceder15% da peça maciça.

Exemplo de cubo externo50 mm, paredes2 mm, topo/fundo1,2 mm e núcleo15%: volume depositado idealizado39,38664 cm³; PA6-CF42,931 g; Tritan46,476 g. São contas geométricas, sem sobreposições do fatiador ou suportes. Os oito PADs R02 somam129,215 g se maciços a1,22 g/cm³;40% sem peles daria51,686 g. O perfil real com paredes/peles situa-se entre esses extremos para essa densidade, excluindo cinta.

Fontes reutilizadas: Bambu PA6-CF TDS V3.0; PolyFlex TPU95 TDS V5.4; Eastman Tritan TX1001, referência de resina moldada para densidade. Os resultados estáticos maciços anteriores permanecem no histórico e não foram reinterpretados como impacto Hexa3D15%.

| Arquivo | Conteúdo |

| --- | --- |

| 02_Dados/*.json e *.csv | Hipóteses, valores e resposta temporal |

| 03_Modelos3D | STEP/F3D nominais e STL originais/PADs |

| 04_Animacao | MP4 e composição editável |

| 05_Historico | Relatórios anteriores e estudo bloqueado |

| 06_Fontes | Ficha técnica de referência TPU |


## Fontes e equações auditáveis

- [Eastman Tritan TX1001](https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312)

- [Bambu PA6-CF V3.0](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf)

- [PolyFlex TPU95 V5.4](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyFlex_TPU95_TDS_EN_V5.4.pdf?v=1731956391)

As porcentagens, módulos efetivos, dimensões substitutas e rigidez de contato assumidos estão separados dos dados do fabricante em02_Dados/parametros_resultados_R03.json.
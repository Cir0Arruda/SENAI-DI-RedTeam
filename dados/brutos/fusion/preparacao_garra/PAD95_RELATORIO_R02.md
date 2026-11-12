# SAMI — revisão R02 e nova tentativa de impacto

Data: 11/11/2026. **Estado: bloqueado antes de resolver. Nenhum resultado novo de impacto, desgaste ou vida útil.**

## Entrega geométrica

PADs de sacrifício PU/TPU95A em quatro interfaces da garra, divididos em oito partes. A R02 sobe 5 mm em relação à R01 e cobre o rebordo superior, mantendo acessos de parafusos. Ajuste conformal a partir do STEP da montagem SAMI, não da antiga amostra semicircular. Raio externo nominal39 mm; flange31 mm; altura25,5 mm; folga nominal de divisão0,8 mm; canal de cinta3,5 mm por1,2 mm. A cavidade foi ajustada por escala e alívios locais; não é uma superfície de offset uniforme com folga metrológica garantida.

Verificação CAD anterior: sem interseção volumétrica com corpo superior e suportes inferiores principais. Não inclui mangueiras, ferramentas, movimento ou deformação da fixação. A cinta/retentor é conceito de montagem, sem pré-carga ou resistência qualificada.

Os oito STL R02 foram centralizados em XY, apoiados em Z=0 e conferidos em milímetros. Verificação de arestas fechadas e orientação passou; maior diferença de volume malha/CAD: 0.08024%. Isso verifica o arquivo exportado, não a qualidade de impressão nem sua resistência.

![PADs R02 na montagem](SAMI_PAD95_MONTAGEM_R02.png)

## Impressão e materiais

Histórico informado pelo usuário: Tritan FDM, camada0,20 mm, bico0,40 mm, cinco perímetros. Transferir isso à PA-CF é hipótese, não registro de produção. Usuário aceitou hipóteses para itens faltantes: largura0,40 mm, cinco paredes nominais2 mm na garra, topo/fundo1,2 mm, gyroid30%; PAD com três paredes1,2 mm, topo/fundo1,2 mm e gyroid40%. Um envelope sólido CAD com densidade reduzida não reproduz essas paredes e células.

Referência da garra: Bambu PA6-CF V3.0. Referência do PAD: Polymaker PolyFlex TPU95 V5.4. Não representam mediana estatística de fornecedores. Dados TPU da ficha: densidade1,20–1,24 g/cm³; E=33,6±0,9 MPa em XY, corpo de prova100%; tensão a100/200/300/400% de alongamento=11,1/15,0/21,0/25,8 MPa; alongamento de ruptura551,2±23,5%; dureza95A. Essas tensões em alongamentos definidos não foram cadastradas como escoamento ou resistência última. Temperaturas de bico210–230°C e mesa25–60°C são processamento, não temperatura contínua admissível da garra.

## Nova tentativa efetivamente realizada no Fusion

Criado submodelo A1 a partir da geometria real: recorte radial45 mm do corpo superior, duas metades do PAD R02 e esfera de aço raio20 mm/massa0,263056 kg. Volume do recorte98,823872 cm³. Outros braços, carga24 kg e flexibilidade global não fazem parte desse submodelo. A esfera está posicionada lateralmente; o nome indica uma folga nominal0,1 mm baseada no raio externo máximo, mas o canal do PAD altera a distância real. A menor distância precisa ser medida antes da solução.

Prepararam-se cartões exploratórios distintos; a atribuição nova no estudo foi confirmada na interface para a garra e ambas as metades do PAD. O painel reconheceu o uso de propriedades avançadas. A verificação nova retornou:

- Alguns componentes usam material com propriedades inválidas.
- Não existem contatos ou conectores entre os corpos independentes.

O campo inválido específico não foi exposto. Não está demonstrado se a causa é a validação de campos básicos desconhecidos ou outra condição interna; não se atribui uma causa sem evidência. A01=0 é a redução neo-Hookeana, não prova de erro por si só. Não foram inseridos escoamento, ruptura ou curvas fictícias para contornar o bloqueio. Nenhum job foi enviado, nenhum custo foi confirmado e nenhuma malha/resultados foram gerados.

## Hipóteses constitutivas — não são dados caracterizados

PA equivalente: E=4430×0,30²=398,7 MPa; densidade327 kg/m³; ν=0,30 assumido. Esse modelo ignora a contribuição das paredes densas de2 mm e não representa adequadamente a impressão solicitada. Não deve ser usado para aprovar a garra.

PAD equivalente local: espessura lateral6,3 mm com duas peles de1,2 mm e núcleo3,9 mm. E do núcleo=33,6×0,40²=5,376 MPa. Associação em série resulta em E=7,905882 MPa e densidade766,857 kg/m³. Aplicar esse valor uniformemente ao PAD é uma aproximação local; o teto fino tende a ser inteiramente formado por peles sólidas e não segue essa seção.

Para ambos adotou-se uma energia elástica neo-Hookeana exploratória, com A01=0; A10=E/[4(1+ν)]; D1=E/[6(1−2ν)]. Valores PA:76,673077 e166,125 MPa; PAD:1,520362 e3,294118 MPa. Não são ajustes experimentais Mooney-Rivlin, não incluem viscosidade, histerese, ruptura, delaminação nem degradação. PA-CF não foi caracterizado como borracha; a lei é somente uma hipótese elástica de comparação e deverá ser limitada por deformação e substituída por resposta apropriada antes de conclusões de resistência.

## Protocolo proposto, ainda não aplicado

Impacto local de1 m/s: energia inicial½mv²=0,131528 J, duração inicial3 ms e40 intervalos. A duração deve ser ampliada se o contato/rebote não terminar. Comparar com/sem PAD sob a mesma energia, orientação, apoios e condição de alvo, contabilizando diferenças de trajetória livre.

Faltam configurar e auditar: faces artificiais de corte para apoio, retenção idealizada e contatos, esfera rígida se apropriado, velocidade, distância inicial real, duração e malha. Uma hipótese de retenção aderida não equivale à cinta real. O contato esfera/PAD deve permitir separação e não pode ficar aderido. Inspecionar qualidade e refinar malha no contato e nas transições; verificar conservação de energia, reações e dependência de malha. Conferir custo antes de envio. Não repetir a mesma verificação de materiais sem uma alteração ou diagnóstico novo.

Métricas que só podem ser publicadas após solução: força máxima e impulso transmitidos, tensões/deformações por componente, deslocamento, compressão máxima do PAD, energia armazenada/dissipada por mecanismo e rebote. Em uma lei puramente elástica, energia armazenada/restituída não é absorção irreversível. Comparar em regiões e volumes correspondentes, evitando usar singularidade de contato como resistência da peça.

## O PAD melhorou a proteção?

**Ainda não quantificado.** A camada flexível pode distribuir o contato e aumentar sua duração quando há curso e retenção adequados. Pode atingir fim de curso, escorregar, romper ou transferir a carga para outra região. A R02 amplia a cobertura superior geometricamente, mas nenhum percentual de redução de força/tensão ou aumento de vida foi demonstrado.

## Desgaste, temperatura e uso24/7

Não há ensaio térmico resolvido. A presente lei hiperelástica no Fusion não incorpora os efeitos térmicos em análise não linear. É necessário caracterizar variação de rigidez, resistência e relaxação com temperatura e umidade; temperatura de processamento não é temperatura de serviço.

Não há previsão de horas ou ciclos de vida. Operação24/7 não define sozinha um espectro de carga. São necessárias frequências/intensidades de impactos e movimentos, temperaturas, umidade, compressão residual e limites de troca. Desgaste por atrito requer pressão, deslizamento, distância e lei/coficiente calibrado; ciclos de impacto sem deslizamento envolvem outro mecanismo de dano. Fluência/relaxação requer curvas dependentes de tempo, tensão e temperatura. Fadiga requer dados cíclicos direcionais e processo de impressão compatível. A liga entre camadas depende de temperatura, secagem, orientação e tempo de difusão; reforço de fibra curto não elimina a fraqueza interlaminar.

PAD de sacrifício: critérios de troca devem ser definidos após testes físicos de compressão/impacto e inspeção. Trinca, perda de retenção, rasgo e deformação permanente são observáveis relevantes; nenhum intervalo de manutenção foi validado.

## Massa — estimativa analítica separada da simulação

Volume total dos oito envelopes R02=105.913834 cm³. A1,22 g/cm³, massa totalmente maciça=129.215 g. O limite idealizado de preencher uniformemente40% sem peles seria51.686 g. O PAD real com paredes e topo/fundo fica entre esses valores para essa densidade, excluindo cinta/suportes. Apenas o fatiamento com o perfil definitivo fornece a estimativa apropriada. O modelo local de densidade equivalente não é uma pesagem.

Troca PA6-CF/Tritan: para idêntico volume efetivamente depositado e densidades1,09/1,18 g/cm³, redução teórica7,627%. Isso não é redução da montagem inteira, que contém ferragens, ventosas e PADs. As massas de2,834 e3,03 kg das imagens não identificam a parcela substituível. Os valores estáticos maciços anteriores não foram repetidos e não validam a impressão30% nem impacto.

Exemplo adicional de cubo externo50 mm: paredes laterais2 mm, topo/fundo1,2 mm, núcleo30%, sem suportes. Volume depositado idealizado54,49488 cm³: PA6-CF59,399 g; Tritan64,304 g; diferença4,905 g. É cálculo geométrico, sem sobreposição real de linhas/fatiador, não massa da garra.

## Fontes e arquivos de auditoria

- [PolyFlex TPU95 TDS V5.4](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyFlex_TPU95_TDS_EN_V5.4.pdf?v=1731956391); cópia local em fontes_industriais.
- [Autodesk: definição hiperelástica](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/GUID-B6C9DD0F-0CC5-43F9-BD94-49EDF335BF19.htm).
- [Autodesk: comportamento e estudos compatíveis](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/SIM-HYPERELASTIC-MATERIALS-CONCEPT.htm).
- [Autodesk: teoria, convenções de D1 e limite térmico](https://help.autodesk.com/view/fusion360/ENU/?contextId=SIM-HYPERELASTIC-MATERIAL).
- [Autodesk Explicit: referência MATHP, redução neo-Hookeana](https://damassets.autodesk.net/content/dam/autodesk/external-assets/support-articles/autodesk-inventor-nastran-2025-offline-help/autodesk_explicit_2025_reference_manual.pdf).

Estado estruturado: impacto_R02_status.json. Arquivo local do estudo bloqueado: SAMI_A1_IMPACTO_R02_BLOQUEADO.f3d. Montagem com PADs: SAMI_PAD95_CONFORMAL_R02.f3d. Validação STL: pad95_stl_validation_R02.json. Não confundir o arquivo de preparação com um cálculo concluído.

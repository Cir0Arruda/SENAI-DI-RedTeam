# Campanha de garra: massas e verificação das hipóteses

**Estado: cálculos analíticos de massa e checagem do plano; não são resultados de um novo solucionador Fusion.**

## Geometria usada

Modelo de referência 125 × 250 × 50 mm, duas furações, volume sólido real 692,442097 cm³. A caixa envolvente teria 1.562,5 cm³ e não foi usada como volume da peça. Casca de 2 mm, com volume CAD 156,063893 cm³; núcleo geométrico 536,378204 cm³. A casca representa 22,54% do sólido.

As variantes foram modeladas como grade vertical XY de passo 20 mm, recortada pela geometria real. O passo de 20 mm não é o tamanho do cubo de comparação. Não representam automaticamente gyroid, estrutura de outro fatiador nem a microestrutura real dos cordões FFF.

| Variante | Fração real do núcleo | Volume material, cm³ | Material / sólido | Redução nominal de massa | Espessura da nervura, mm |
| --- | ---: | ---: | ---: | ---: | ---: |
| F30 | 30,0225% | 317,097823 | 45,794% | 54,206% | 3,3260 |
| F40 | 39,9051% | 370,106076 | 53,449% | 46,551% | 4,5309 |
| F60 | 60,0879% | 478,362508 | 69,083% | 30,917% | 7,3293 |
| F100 | 100,0000% | 692,442097 | 100,000% | 0,000% | maciço |

Por isso F30 não pesa 30% do maciço: a casca é maciça, além das nervuras internas. Os valores acima conferem com Vmaterial = Vcasca + fração_real × Vnúcleo, dentro de tolerância numérica de 10⁻⁸ cm³.

## Massas das 32 combinações

Massa nominal em gramas = volume CAD em cm³ × densidade em g/cm³. Um mordente por célula; para dois mordentes idênticos, multiplicar por dois. As casas decimais mostram a conta, não a exatidão de uma pesagem.

| Produto | F30, g | F40, g | F60, g | F100, g | Cubo maciço 20 mm, g |
| --- | ---: | ---: | ---: | ---: | ---: |
| Polymaker PETG V2.0 | 412,23 | 481,14 | 621,87 | 900,17 | 10,40 |
| 3D-Fuel Pro PCTG | 390,03 | 455,23 | 588,39 | 851,70 | 9,84 |
| Eastman Tritan TX1001 | 374,18 | 436,73 | 564,47 | 817,08 | 9,44 |
| Bambu TPU 95A HF V3.0 | 386,86 | 451,53 | 583,60 | 844,78 | 9,76 |
| LEHVOSS LUVOCOM 3F PAHT 9936 BK/L | 396,37 | 462,63 | 597,95 | 865,55 | 10,00 |
| Fiberlogy Nylon PA12 | 320,27 | 373,81 | 483,15 | 699,37 | 8,08 |
| Polymaker PolyMax PC V5.4 | 377,35 | 440,43 | 569,25 | 824,01 | 9,52 |
| Bambu PA6-CF V3.0 | 345,64 | 403,42 | 521,42 | 754,76 | 8,72 |

O cubo de 20 × 20 × 20 mm tem 8 cm³. Para um mesmo material, as variantes F30/F40/F60/F100 equivalem respectivamente a 39,637 cubos, 46,263 cubos, 59,795 cubos, 86,555 cubos. É uma comparação de volume e massa, não de rigidez ou resistência. O exemplo anterior de cubo de 50 mm tem 125 cm³: as massas daquele cubo são 15,625 vezes as deste cubo de 20 mm.

O menor valor nominal entre os graus pesquisados é PA12 Fiberlogy; isso não prova melhor resistência específica, vida ou aptidão industrial. O PA6 LEHVOSS é formulação específica, Tritan TX1001 tem origem moldada, e PA6-CF Bambu não representa todo PA-CF.

## Checagem quantitativa do cenário de operação

| Grandeza | Hipótese ou conta | Valor |
| --- | --- | ---: |
| Payload | Hipótese de peça manipulada, independente da massa dos mordentes | 2 kg |
| Normal por contato | Hipótese, dois mordentes | 100 N |
| Aceleração vertical | Hipótese para cima | 5 m/s² |
| Gravidade | Referência da conta | 9,80665 m/s² |
| Atrito | Hipótese de tribopar; não medido | 0,30 |
| Força vertical da carga acelerada | m(g+a) | 29,61330 N |
| Tangencial de payload por mordente | Simetria assumida, metade da força total | 14,80665 N |
| Atrito disponível | 2 μ N | 60 N |
| Margem antideslizamento | 60/[m(g+a)] | 2,0261 |
| Contato nominal | Patch assumido 40 × 40 mm | 1.600 mm² |
| Pressão média nominal | 100 N / 1.600 mm² | 0,0625 MPa |
| Impacto ocasional | Massa efetiva 2 kg e velocidade 0,25 m/s | 0,0625 J |
| Ciclo comandado | 10 s, quatro preso e seis liberado | 360 ciclos/h |

A margem 2,0261 é apenas contra escorregamento com essas hipóteses; não é fator de segurança do polímero nem da fixação. Peso próprio e inércia de cada mordente estão no JSON por combinação. Ao aplicar gravidade no solver, não adicionar novamente a mesma força peso; ao aplicar força estática equivalente do payload, distinguir aceleração do robô de massa do payload.

### Sensibilidade ao atrito e à normal

| μ \ N por mordente | 50 N | 100 N | 150 N |
| --- | ---: | ---: | ---: |
| 0,15 | 0,507 | 1,013 | 1,520 |
| 0,30 | 1,013 | 2,026 | 3,039 |
| 0,50 | 1,688 | 3,377 | 5,065 |

Esse quociente maior que um indica somente equilíbrio nominal por atrito no cenário. Abaixo de um ocorre escorregamento no modelo; perto de um há pouca reserva. Partidas, paradas de emergência, torque de peça excêntrica e vibração não são capturados por essa conta escalar.

### Temperatura e tempo de vida

Casos térmicos propostos: contato a 40/60 °C, ambiente e referência sem tensão a 25 °C, convecção h = 10 W/(m²·K) assumida. Nenhum desses números é temperatura medida na instalação. Propriedades constantes e proxies de outros graus não validam amolecimento real, anisotropia térmica ou durabilidade.

| Checkpoint | Ciclos comandados | Horas presas acumuladas | Estado |
| --- | ---: | ---: | --- |
| 1.000 h | 360.000 | 400 h | Agenda calculada; vida/desgaste não resolvidos |
| 5.000 h | 1.800.000 | 2.000 h | Agenda calculada; vida/desgaste não resolvidos |
| 10.000 h | 3.600.000 | 4.000 h | Agenda calculada; vida/desgaste não resolvidos |

Não foram gerados valores de deformação por fluência, dano por fadiga ou desgaste em milímetros: esses resultados precisam de leis calibradas, tribopar e histórico de carga. 0,0625 J de impacto também não fornece força máxima ou dano sem contato, rigidez, taxa e modelo constitutivo dinâmico.

## Fontes e rastreabilidade

- Geometria: `geometria_mcp.json`, retorno nativo MCP capturado pelo agente principal. Este subagente apenas conferiu os volumes fornecidos.
- Densidades: `modelos_solver_exploratorios.json`, campos `density_kg_m3`, comparados com o registro publicado de cada produto.
- Plano: `../cenarios_garra_industrial.json`; os cálculos principais foram recomputados e conferidos contra esse arquivo.
- Saída estruturada: `massas_32_combinacoes.json`, com 32 registros, fontes, forças de peso próprio/inércia e SHA-256 dos arquivos de entrada.

- [Polymaker PETG V2.0](https://polymaker.com/wp-content/uploads/lana-downloads/TDS_Polymaker_PETG_V2.0_2025-11-17.pdf): densidade 1,30 g/cm³.
- [3D-Fuel Pro PCTG](https://www.3dfuel.com/pages/pctg): densidade 1,23 g/cm³.
- [Eastman Tritan TX1001](https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312): densidade 1,18 g/cm³.
- [Bambu TPU 95A HF V3.0](https://store.bblcdn.com/s6/default/a6ca55f14aa54ddb92679d06df4700ae/Bambu_TPU_95A_HF_Technical_Data_Sheet.pdf): densidade 1,22 g/cm³.
- [LEHVOSS LUVOCOM 3F PAHT 9936 BK/L](https://www.lehvoss.de/fileadmin/Compounds/PDFs/LUVOCOM_3F/LUVOCOM_3F_PAHT_9936_BK_L/Datasheet_LUVOCOM_R__3F_PAHT_9936_BK_L_Filament.pdf): densidade 1,25 g/cm³.
- [Fiberlogy Nylon PA12](https://fiberlogy.com/app/uploads/2026/05/FIBERLOGY_NYLONPA12_TDS.pdf): densidade 1,01 g/cm³.
- [Polymaker PolyMax PC V5.4](https://cdn.shopify.com/s/files/1/0548/7299/7945/files/PolyMax_PC_TDS_EN_V5.4.pdf): densidade 1,19 g/cm³.
- [Bambu PA6-CF V3.0](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf): densidade 1,09 g/cm³.

O princípio de dimensionamento por atrito é documentado no [manual Robotiq](https://assets.robotiq.com/website-assets/support_documents/document/2F-85_2F-140_General_PDF_20200211.pdf); μ deve ser medido para o par real. A leitura não certifica compatibilidade deste mordente com um atuador comercial específico.

As massas desconsideram suportes, purga, brim, umidade absorvida, porosidade intrínseca dos cordões e variação de dimensão/lote. As 32 contas nominais não significam 32 simulações mecânicas resolvidas.

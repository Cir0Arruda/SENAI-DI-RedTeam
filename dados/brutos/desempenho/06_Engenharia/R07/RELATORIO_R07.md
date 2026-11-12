# SAMI R07: esqueleto interno + giroide (peças superior e inferiores)

Data: 11/11/2026. O exterior **não muda**. Todas as zonas ficam recortadas 2,25 mm para dentro (5 perímetros de 0,45 mm). Nada foi enviado à impressora.

## 1. O que mudou (só preenchimento interno)

| Zona | Peça superior | Peças inferiores | Por quê |
|---|---|---|---|
| Esqueleto 100% (almas de 3 mm) | cubo → 4 ressaltos, anel r40 e 6 raios no colar | **removido** (sem ganho no FE) | levar a carga da flange do robô até os ressaltos |
| Tubos 100% (r 7,5 mm) | 6 furos da flange + 12 furos dos ressaltos | 6 furos dos ressaltos | apoio dos parafusos, sem esmagar o giroide |
| Colar 55% | anel 26–60 mm, 35 mm do topo | n/a | raiz da flange, onde começa a falha entre camadas |
| Rosa 35% | ressaltos R31,5 | ressaltos + bases das ventosas R24 | antes 70%: reduzido sem perder resistência |
| Amarelo 20% | assento R43 | assento R43 | antes 30% |
| Base | giroide 25% | giroide 20% | antes TPMS-D 20% + corredores azuis 50% |

Arquivos: `04_Modificadores/R07/*_MOD_*.stl` (modificadores do Orca), `05_Orca/R07/GARRA_*_R07_*.3mf`, figura `06_Engenharia/R07/CAMADAS_R07_SUPERIOR.png` (G-code real).

## 2. Massa e material (fatiamento Orca, K1 Max, 1:1, PA6-CF)

| Peça | R06 | R07 | Δ |
|---|---|---|---|
| Superior (giroide 25%) | 754,5 g | 731,0 g | −3,1% |
| Inferior esq. (giroide 20%) | 443,8 g | 383,2 g | −13,7% |
| Inferior dir. (giroide 20%) | 444,0 g | 383,2 g | −13,7% |
| **Garra (3 peças)** | **1.642,3 g** | **1.497,4 g** | **−8,8%** |
| Filamento total (com suportes e adesão) | 1.954,0 g | 1.809,2 g | −7,4% |
| Tempo de impressão | 85,8 h | 78,9 h | −8,0% |

O Orca avisa que a dureza do bico (HRC) está abaixo da exigida pelo PA6-CF. Use bico endurecido.

## 3. Simulações

### 3.1 Método
- **FE por voxels (3 mm, hexaedros de 8 nós)** de cada variante: PA6-CF transversalmente isotrópico (XY 4.430 MPa / Z 2.170 MPa) nas paredes e almas. Giroide homogeneizado por Gibson-Ashby (E·φ², 0,3·σ·φ^1,5). Engaste nos 6 furos da flange; carga −Z nos ressaltos de uma asa.
- **Critério de falha:** tração/cisalhamento entre camadas (Z) e tensão principal no plano (XY). O ponto crítico em todas as variantes é a raiz da flange do robô (−544,8; 338,5; 341,4).
- **Pico real** = pico voxel × 2,2 (fator medido contra o Fusion no R06). [Atualizar com o Fusion R07.]
- **Casos de carga:** massa × (g + 5 m/s²) numa asa só (erro da seladora). 24 kg → 355 N; 30 kg → 444 N.

### 3.2 Carga numa asa: 24 kg, 30 kg e máximo

| | R06 | R07 com esqueleto | R07 sem (mesmos %) | R07 sem, giroide denso (mesma massa) |
|---|---|---|---|---|
| Rigidez da asa (sup. + inf. em série) | 299 N/mm | 361 N/mm | 342 N/mm | 366 N/mm |
| Tensão Z de pico a 24 kg | 16,3 MPa | 10,0 MPa | 10,6 MPa | 10,4 MPa |
| Máx. numa asa, PA6-CF (Z 48 MPa) | 70,7 kg | **115,6 kg** | 108,8 kg | 110,9 kg |
| FS 24 kg / 30 kg (PA6-CF) | 2,95 / 2,36 | **4,82 / 3,85** | 4,53 / 3,63 | 4,62 / 3,70 |
| Máx. numa asa, PAHT CF15 (Z 18,2 MPa) | 26,8 kg | **43,8 kg** | 41,2 kg | 42,0 kg |
| FS 24 kg / 30 kg (PAHT CF15) | 1,12 / 0,89 | **1,83 / 1,46** | 1,72 / 1,37 | 1,75 / 1,40 |
| Energia de tranco até romper (PAHT) | 0,26 J | 0,58 J | 0,55 J | 0,53 J |

Leitura: com o PA-CF de menor resistência entre camadas (PAHT CF15), o R06 rompe perto de 27 kg numa asa, o que bate com a quebra real com as duas caixas de 12 kg. O R07 aguenta 30 kg com FS 1,46 nesse material e 3,85 com o PA6-CF.

### 3.3 Com × sem esqueleto (resposta direta à pergunta)
- **Mesmos percentuais:** o esqueleto dá +6% de carga máxima, +6% de rigidez e cerca de 2× a vida em fadiga.
- **Mesma massa (giroide mais denso no lugar das almas):** o esqueleto ainda dá +4% de carga e 1,6× a vida. Em rigidez linear fica praticamente igual.
- **Peças inferiores:** as almas não ajudaram (o giroide 22,5% rendeu igual ou melhor). Por isso foram retiradas, e as inferiores ficaram 13,7% mais leves.
- O ganho grande sobre o R06 (+63% de carga, −39% de tensão entre camadas) vem do **conjunto**: colar 55% na raiz da flange, raios e tubos nos furos, mais os ressaltos e o assento redimensionados.

### 3.4 Fadiga (milhares de horas): ESTIMATIVA
Curva S-N normalizada conservadora para PA com fibra curta impresso: σmax/S = 1 − 0,10·log10(N), ou seja 30% de S em 10⁷ ciclos. Regra de Miner. Hipótese: 480 ciclos/h (8 por minuto).

| Vida (PAHT CF15) | R06 | R07 com | R07 sem | R07 sem, denso |
|---|---|---|---|---|
| Só 12 kg por asa | 696 h | **38.030 h** | 25.642 h | 29.112 h |
| 12 kg + 1% dos ciclos com 24 kg numa asa | 2 h | **5.879 h** | 2.813 h | 3.574 h |
| Só 24 kg numa asa | 0 h | 69 h | 32 h | 41 h |
| Só 30 kg numa asa | 0 h | 3 h | 1 h | 2 h |

Com PA6-CF (Z 48 MPa) todas as vidas do R07 passam de 10⁵ h, inclusive 52.800 h só com 30 kg.
Conclusão: o erro da seladora não pode ser rotina. O R07 tolera eventos isolados de 24–30 kg; no R06 um único evento já está no limite.

### 3.5 Impacto e tranco
- Frequência natural da asa com 24 kg pendurados: 19,5 Hz (R07) e 17,8 Hz (R06), período de cerca de 51 ms.
- Fator dinâmico de 1 grau de liberdade por tempo de aplicação: 10 ms → 2,0; 25 ms → 1,65; 50 ms → 1,33; 100 ms → 1,16; 200 ms → 1,08. Uma parada de emergência lenta (> 100 ms) quase não amplifica. Um enganchão seco (< 25 ms) quase dobra a carga.
- Energia que a asa absorve elasticamente até romper (PAHT): R06 0,26 J → R07 0,58 J (2,2×). Com PA6-CF: 1,83 J → 4,05 J.
- A ventosa solta a caixa em cerca de 0,9–1,2 kN por asa (4 × 228–307 N a −90 kPa). Com PA6-CF o R07 rompe acima disso (1,7 kN), então a ventosa funciona como "fusível". Com PAHT CF15 (0,65 kN) a garra rompe antes de a ventosa soltar.

### 3.6 Longo prazo
- **Fluência (estimativa, módulo de fluência 0,70 E em 1.000 h e 0,55 E em 10.000 h):** flecha a 12 kg 0,49 → 0,70 → 0,89 mm (R07); 0,60 → 0,85 → 1,08 mm (R06).
- **Desgaste nos furos M6 (Archard, k = 1e-5 mm³/N·m, 10 µm de micro-deslizamento por ciclo):** < 0,03 mm³ por furo em 10.000 h. O esmagamento é de cerca de 1 MPa a 24 kg, desprezível. Recomenda-se reapertar os parafusos periodicamente (relaxação do PA).
- **Umidade:** o PA6 condicionado perde rigidez e resistência. Os números "PA6-CF" são de TDS seco; o caso PAHT CF15 cobre a faixa conservadora.

### 3.7 Testes industriais recomendados (para validar em bancada)
1. **Carga de prova estática:** 2× a carga de trabalho por asa (24 kg numa asa) por 1 min, sem trinca nem deformação residual > 0,1 mm (critério tipo EN 13155 para dispositivos de içamento a vácuo).
2. **Ruptura:** levar uma peça até romper, numa asa, para medir o máximo real contra os 44–116 kg previstos.
3. **Fadiga:** 10⁵ ciclos de 0 → 24 kg numa asa (cerca de 1 dia a 1–2 Hz) e inspeção da raiz da flange.
4. **Tranco/E-stop:** caixa de 12 kg com parada de emergência gravada (acelerômetro na garra).
5. **Fluência:** 24 kg pendurados por 168 h, medindo a flecha.

### 3.8 Por que PA6-CF (justificativa do material)
Com a mesma geometria R07 e só trocando a resistência Z (TDS dos fabricantes): PA12-CF10 126 kg, PA6-CF 116 kg, PETG 110 kg, PC 100 kg, PAHT CF15 44 kg. Só na carga estática vários materiais se equivalem. O PA6-CF ganha pela **rigidez Z por massa** e pela **HDT de 164 °C** (PETG 65 °C, PA12-CF10 105 °C), que controlam fluência e deformação em operação 24/7. No ranking multiobjetivo (TOPSIS, cenário estrutural 24/7) o PA6-CF tem 0,83, contra 0,52 do segundo colocado.

### 3.9 Decisão para a equipe: com × sem esqueleto × preenchimento uniforme (garra MONTADA)

Atualizado em 12/11/2026. A tabela compara as 3 peças unidas: superior + inferiores, com a junta parafusada tratada como colada. Os números saem destas fontes:
- **massa:** fatiamento real no Orca (K1 Max 1:1, PA6-CF, 5 paredes);
- **resistência:** FE por voxels da montagem;
- **impacto:** FE transiente da peça superior.

A massa da garra instalada (Tritan Hexa3D 30%, deck do cliente) é **estimada**: fatiamento Hexa3D 30% em PA6-CF × 1,18/1,10 = 1.577 g de peças impressas.

| Variante | Garra impressa | vs Tritan atual | Máx. numa asa PA6-CF / PAHT | FS 24 kg PAHT | Flecha 24 kg | Impacto: σZ pico / FS PAHT |
|---|---|---|---|---|---|---|
| **R07 COM esqueleto** | 1.497 g | **−5,0%** | **100,3 / 38,0 kg** | 1,58 | 1,54 mm | **17,0 MPa / 1,07** |
| R07 SEM esqueleto (mesmas zonas) | 1.433 g | **−9,1%** | 93,3 / 35,4 kg | 1,47 | 1,64 mm | 18,1 MPa / 1,01 |
| Giroide 30% uniforme | 1.492 g | −5,4% | 61,6 / 23,4 kg | 0,97 | 1,73 mm | 28,0 MPa / **0,65** |
| Giroide 35% uniforme | 1.604 g | +1,7% | 68,5 / 26,0 kg | 1,08 | 1,57 mm | não rodado |
| Giroide 40% uniforme | 1.716 g | +8,8% | 75,9 / 28,8 kg | 1,20 | 1,43 mm | 22,3 MPa / 0,81 |
| Hexa3D 30% uniforme (PA6-CF) | 1.470 g | −6,8% | ≈ giroide 30%* | | | |
| TPMS-D 40% uniforme | 1.785 g | +13,2% | ≈ giroide 40%* | | | |
| R06 (zonas TPMS-D) | 1.642 g | +4,1% | 61,6 / 23,3 kg | 0,97 | 1,89 mm | |

\* A lei homogeneizada (Gibson-Ashby) não distingue o tipo de célula na mesma densidade. Por isso Hexa3D e TPMS-D recebem a resistência do giroide de mesma %.

**Peso × erro de processo (2 caixas numa asa = 24 kg, 355,4 N).** Garra montada inteira (superior + inferior), ponto crítico na raiz da flange do superior:

| Variante | Massa vs Tritan | Aguenta (PA6-CF) | FS 24 kg PA6-CF | Aguenta (PAHT CF15) | FS 24 kg PAHT | Tranco 24 kg FS PA6 / PAHT |
|---|---|---|---|---|---|---|
| R07 COM | −5,0% | 100,3 kg | 4,18 | 38,0 kg | 1,58 | 2,82 / 1,07 |
| R07 SEM | −9,1% | 93,3 kg | 3,89 | 35,4 kg | 1,47 | 2,65 / 1,01 |
| Giroide 30% | −5,4% | 61,6 kg | 2,57 | 23,4 kg | **0,97 (não aguenta)** | 1,72 / **0,65** |
| Giroide 35% | +1,7% | 68,5 kg | 2,85 | 26,0 kg | 1,08 | não rodado |
| Giroide 40% | +8,8% | 75,9 kg | 3,16 | 28,8 kg | 1,20 | 2,15 / **0,81** |
| R06 | +4,1% | 61,6 kg | 2,57 | 23,3 kg | **0,97 (não aguenta)** | não rodado |

Referência de bancada (Fusion R04, peça **maciça**, 24 kg): FS > 8 em PA6-CF e em Tritan. A Tritan instalada com Hexa3D 30% não tem FE com preenchimento, então não há número de carga máxima para ela.

Leitura:
1. **Peso:** as duas versões R07 cumprem a meta de 5–10% mais leve que a garra instalada:
   - COM esqueleto: −80 g;
   - SEM esqueleto: −144 g.

   O preenchimento uniforme 30–40% vai de −5% a +9%. Ou seja, mais denso = mais pesado.
2. **Resistência da garra montada:** com a mesma massa, o R07 COM aguenta **+63%** a mais que o giroide 30% uniforme (100 contra 62 kg). Isso porque ele concentra material onde a falha começa:
   - colar 55% na raiz da flange;
   - tubos nos furos;
   - ressaltos reforçados.

   Nem o giroide 40% uniforme, 220 g mais pesado, chega perto (76 kg).
3. **Esqueleto sim × não:** o esqueleto custa **65 g** e dá:
   - **+7,5% de carga máxima** (100,3 contra 93,3 kg);
   - **+6,7% de rigidez**;
   - **+6% de margem no tranco**.

   Sem esqueleto, a garra continua bem acima de 30 kg em PA6-CF (FS 3,1). Com o PAHT CF15 de baixa adesão entre camadas, o FS a 30 kg cai de 1,27 para 1,18.
4. **Impacto (24 kg aplicados em 10 ms; fator dinâmico 1,70–1,73 em todas):**
   - **Onde a tensão aparece:** o pico é sempre na raiz da flange superior, que é parede sólida.
   - **Giroide:** nas versões R07 ele trabalha só a 26–27% da própria resistência no pico. Nos uniformes 30/40% chega a 46/39%, porque não há colar reforçado e a carga passa pelo preenchimento.
   - **PAHT:** só as duas versões R07 ficam com FS ≥ 1. Os uniformes romperiam no primeiro tranco.
5. **Em resumo:**
   - se o critério for **menor peso** com margem folgada em PA6-CF → R07 SEM esqueleto;
   - se o critério for **margem máxima** (filamento de menor adesão entre camadas, trancos, fadiga) → R07 COM esqueleto, por +65 g.

   Preenchimento uniforme 30–40% não é recomendado: ou é mais pesado, ou é 25–40% mais fraco.

Figuras: `06_Engenharia/R07/GALERIA/` (01–12, `INDEX.md`, `dados_comparativos.csv`). Vídeo do impacto: `06_Engenharia/R07/IMPACTO/impacto_comparativo.mp4` e `impacto_pico.png`. Mapas da montagem: `06_Engenharia/R07/MONTAGEM/mapa_montagem_*.png`. Dados consolidados: `06_Engenharia/R07/DECISAO_ESQUELETO.json`.

## 4. Fusion
**Atualização em 12/11/2026, 01:15.** O modelo de 2 corpos (casca + núcleo homogeneizado) foi montado no Fusion, mas ainda não há resultado.

- **Restrição:** engaste nos 95 facetos dos furos da flange.
- **Carga:** −355,36 N em Z nos 65 facetos dos ressaltos da asa direita.
- **Material do estudo:** o fator de segurança passou a usar a resistência máxima à tração, porque os cartões não têm resistência ao escoamento.
- **Resultado:** o solve na nuvem terminou com erro de malha na casca, `Falha na malha: falha de corpo ... Body_1`. O núcleo gerou malha: 67.739 tetraedros e 105.928 nós.
- **Causa:** a casca vem de uma operação booleana e tem triângulos muito finos, com razão de aspecto de até 3.548 e 65 triângulos acima de 200.
- **Próximo passo:** refazer a malha da casca, reimportar e resolver de novo, para calibrar o fator de pico (hoje 2,2, medido no R06).

Status em 11/11/2026, 20:23: **o estudo ainda NÃO foi resolvido.**
- Documento salvo: "SAMI R07 - ESQUELETO INTERNO - SUPERIOR" (98 corpos facetados, 7 materiais homogeneizados, 0,743 kg). Estudo 1 com engaste nos 169 facetos dos furos da flange e força de −355,36 N em Z nos 107 facetos dos ressaltos da asa direita (24 kg × (g+5)).
- A geração de contatos automáticos ficou parada em cerca de 5% por mais de 12 min: 52 mil faces facetadas e cerca de 2 GB de RAM livre. Foi cancelada.
- Preparado modelo leve de 2 corpos (`04_Modificadores/R07/FEA_LOD3`: casca 5 paredes + núcleo homogeneizado; cartões NUCLEO_COM E = 790 MPa, NUCLEO_SEM 484 MPa, NUCLEO_SEM_ISO 618 MPa). Ao importá-lo, o Fusion parou de responder (14,7 GB reservados, todas as threads em espera).
- Os números das seções 3.2–3.6 usam o fator de pico 2,2 calibrado no Fusion do R06. Quando o estudo R07 rodar, recalcular com `python r07_vida.py --pico <novo fator>`.

## 5. Limites (honestidade)
- Giroide homogeneizado. O fator de pico é calibrado no Fusion, não em ensaio.
- Fadiga, fluência e desgaste são estimativas de engenharia com hipóteses explícitas, não ensaio.
- A resistência entre camadas real depende da impressão (temperatura, secagem do filamento, orientação). É ela que manda neste projeto.
- O relatório em PDF sugere reprojetar a junta (rabo de andorinha, garfo M6). Isso altera o exterior e **não foi aplicado**, porque alterações externas são proibidas.

Fontes: TDS Ultrafuse PAHT CF15 v3.5 (BASF Forward AM, ZX 18,2 MPa, XY 103,2 MPa); TDS Bambu PA6-CF (Z 48 MPa); estudos de fadiga de compósitos de fibra curta impressos (LSU: PA12-CF limite 48–54 MPa; SCF-PA otimizado cerca de 69–70 MPa).

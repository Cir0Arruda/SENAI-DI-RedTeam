# Preparação técnica — garra SAMI, PA-CF × Tritan e PAD PU-97A

Data: 10/11/2026. Fase: preparação, pesquisa e arquitetura de ensaios. Nenhum resultado novo de solver é apresentado neste relatório.

## 1. Referência e rastreabilidade

Origem: `~/Downloads/Compartilhado_10.11`. Os hashes SHA-256 e tamanhos estão em `arquivos_origem.json`. Há uma montagem STEP de 23.413.114 bytes, STL binário de 78.333.884 bytes com 1.566.676 triângulos, desenho DWG e modelo/ficha do robô UR30. O STEP declara milímetros e contém 27 registros MANIFOLD_SOLID_BREP. Esses registros não equivalem necessariamente a 27 peças ou ocorrências montadas.

Priorizar STEP: preservar superfícies analíticas, furos e componentes quando disponíveis. Inventariar corpos e ocorrências após a importação; verificar fechamento, interferências, espessuras, pequenos detalhes, conexões e nomes. O STL é uma referência geométrica alternativa, sem materiais, condições de impressão ou unidades intrínsecas. Não deduzir massa real de toda a montagem aplicando uma única densidade.

Importação concluída em documento novo `SAMI - PREPARACAO PA-CF Tritan PAD - SEM SIMULACAO`: 39 definições de componentes, 136 ocorrências e 27 definições de corpos sólidos. Inventário completo em `fusion_inventory.json`. A importação atribuiu material padrão Aço aos corpos inspecionados; isso não é identificação física e não pode ser usado para a massa da garra. O inventário retorna volumes por definição, sem multiplicá-los pela quantidade de ocorrências. A baseline foi preservada sem converter esses padrões em fichas PA-CF/Tritan não confirmadas.

As imagens fornecem duas referências distintas: aproximadamente 3,03 kg no desenho e 2,834 kg em uma montagem CAD. A diferença é 196 g. A imagem das caixas indica carga de 24 kg e total modelado de 26,834 kg; não é uma pesagem ou resultado estrutural confirmado. Não reconciliar esses números silenciosamente. A peça semicircular da campanha anterior não representa a garra completa e seus volumes/massas não serão transferidos para esta montagem.

## 2. Identificação dos materiais

“PA-CF” pode representar matrizes e teores de fibra distintos. Adota-se **Bambu PA6-CF V3.0 apenas como candidato documental**. PA12-CF ou outro fabricante exigem nova ficha. “Triton” é tratado provisoriamente como o Tritan mencionado anteriormente; confirmar marca e produto utilizado. **Eastman Tritan TX1001 é referência de resina moldada**, não caracterização da peça impressa instalada.

| Propriedade | PA6-CF candidato — XY / Z | Tritan TX1001 — moldado |
|---|---:|---:|
| Densidade | 1,09 g/cm³ | 1,18 g/cm³ |
| Módulo de tração | 4.430 / 2.170 MPa | 1.548 MPa |
| Resistência à tração | 102 / 48 MPa | 58 MPa na ruptura; 43 MPa no escoamento |
| Alongamento na ruptura | 5,8 / 3,7% | 185% |
| Resistência à flexão | 151 / 80 MPa | 59 MPa |
| Módulo de flexão | 5.460 / 2.240 MPa | 1.495 MPa |
| Impacto | ISO 179: XY 40,3; XY entalhado 13,4; Z 15,5 kJ/m² | ISO 180 entalhado: 93 a 23 °C; 20 a −40 °C, kJ/m² |
| HDT, carga próxima de 0,45 / 1,8 MPa | 186 / 164 °C, ISO 75 | 99 / 85 °C, ASTM D648 |

Fontes: [Bambu V3.0](https://store.bblcdn.com/b2abc59ac250492b979a52f1ce3e61b3.pdf), [Eastman TX1001](https://productcatalog.eastman.com/tds/ProdDatasheet.aspx?pn=tritan+copolyester+tx1001&product=71070312). Valores típicos; condições e métodos diferem. PA6-CF: corpos 100% preenchidos e condicionados termicamente a 80 °C por 12 h; não representam automaticamente impressão a 30%. A ficha relata absorção de água de 2,35% a 25 °C/55% UR. Ensaiar também o estado de umidade em serviço. HDT não é temperatura contínua admissível de uma garra carregada.

### Interpretação mecânica

Os números sugerem maior rigidez do PA6-CF candidato, mas **não demonstram que a garra ficará mais resistente**. Resistência estrutural depende de orientação, trajetórias, concentração de tensão, uniões, defeitos e condição ambiental. Não comparar impacto ISO 179 e ISO 180 como se fossem o mesmo ensaio. O baixo alongamento do compósito exige atenção a entalhes, bordas de furos e regiões que flexionam. Uma seleção por tração XY isolada pode ocultar falha entre camadas.

Usar separadamente rigidez, início de dano, carga máxima, deslocamento funcional e energia dissipada. Não transformar resistência última em tensão de escoamento; não aplicar um critério isotrópico de von Mises como certificação de ruptura do compósito. Faltam propriedades direcionais completas, cisalhamento, Poisson, curvas tensão–deformação, efeitos de taxa/temperatura, fadiga e fratura interlaminar para uma previsão de falha calibrada. As antigas fichas lineares exploratórias ficam fora da baseline validada.

### União das camadas

Na extrusão de termoplásticos, a união ocorre por contato e soldagem entre cordões, com interpenetração e emaranhamento de cadeias enquanto existe mobilidade molecular. O histórico térmico e o tempo disponível antes do resfriamento condicionam a resistência da interface. Vazios reduzem área resistente. A fibra curta tende a acompanhar o escoamento do cordão; isso não cria uma fibra contínua atravessando as camadas. Temperatura, umidade, velocidade e trajetória precisam ser registrados e mantidos nas amostras de validação. [Pesquisa NIST sobre formação da solda](https://www.nist.gov/publications/weld-formation-during-material-extrusion-additive-manufacturing).

Não existe um valor único de “colagem das camadas” obtido da ficha. Solicitar tração nas orientações relevantes e, para modelar delaminação, resistência/energia de fratura apropriadas à interface. Fotografar modo de falha e verificar porosidade e posição das emendas.

## 3. Economia de massa — cálculo analítico condicionado

Para MESMO volume depositado, com as densidades candidatas:

`m_PA = m_Tritan_polímero × (1,09 / 1,18)`

`economia = 0,0762712 × m_Tritan_polímero`

`m_nova_total = m_ferragens + 0,9237288 × m_Tritan_polímero + m_PADs_novos`

Se os PADs substituírem peças existentes, subtrair também a massa dessas peças. Densidade de filamento não inclui vazios nem a massa de suportes descartados. A mesma porcentagem nominal de preenchimento não garante igual volume depositado entre fatiadores ou estratégias.

| Polímero substituído | Economia antes dos PADs |
|---:|---:|
| 0,5 kg | 38,14 g |
| 1,0 kg | 76,27 g |
| 1,5 kg | 114,41 g |
| 2,0 kg | 152,54 g |

Aplicar o fator a TODOS os 2,834 kg produziria 216,15 g e total de 2,61785 kg; a TODOS os 3,03 kg produziria 231,10 g e total de 2,79890 kg. **São tetos condicionais sem PADs, supondo toda a massa substituível e sem mudanças geométricas; não são previsão da montagem real.** Com 24 kg de caixas, o primeiro teto reduziria o conjunto de 26,834 para 26,61785 kg, cerca de 0,81%. Ferragens mantidas diminuem o ganho real. A redução de massa também altera centro de gravidade e inércia: calcular por ocorrência no conjunto, incluindo mangueiras e acessórios relevantes.

Um cubo maciço de 20 mm contém 8 cm³: 9,44 g de TX1001 versus 8,72 g de PA6-CF, diferença de 0,72 g. É exemplo analítico, sem porosidade. Para massa final usar volume de extrusão do fatiador e pesagem, com condições de umidade registradas.

## 4. PADs de PU-97A nas quatro interfaces destacadas

As marcações vermelhas indicam regiões de encontro entre estrutura superior e braços. A fotografia documenta o conjunto físico, mas não permite medir curso, espessura ou energia. O PAD é um protótipo a integrar e deve ter geometria própria. Confirmar se fica entre peças permanentemente aparafusadas, se atua apenas no fim de curso ou se recebe colisão externa.

**97A especifica dureza Shore A, não define um material completo.** Confirmar fabricante, código, poliuretano termoplástico ou fundido, processo e condição. Uma família pode apresentar diferentes formulações: a [Lubrizol lista um produto 97A](https://lubrizol.com/en/Engineered-Polymers/Products/Estane-TPU/Estane-S), mas isso não identifica o PU proposto nem fornece equivalência para impressão. Não substituir automaticamente por TPU95A da campanha antiga.

O PAD pode aumentar o tempo e o curso de desaceleração, alterar a distribuição de contato e dissipar energia por histerese. Absorção depende da curva força–compressão e da taxa. A área sob a curva de carregamento inclui energia recuperável; a área do ciclo de histerese corresponde à parcela dissipada. Para impacto, contabilizar energia cinética, trabalho externo, deformação e energia restante; não afirmar amortecimento apenas porque a peça é flexível.

### Dados necessários ao modelo do PAD

- Densidade e dureza com norma/tempo de leitura; tração e compressão em grandes deformações; deformação volumétrica quando relevante.
- Ciclos de carga/descarga, frequências, temperaturas e velocidades representativas para calibrar viscoelasticidade e amortecimento.
- Compression set, relaxação de tensão, fluência e envelhecimento; rasgamento e abrasão se houver deslizamento.
- Curva compressiva da geometria real: espessura livre, área carregada, faces confinadas, folga, pré-compressão e curso antes de contato rígido.
- Atrito PU/PA-CF e PU/Tritan; retenção, parafusos e eventual adesivo. Colagem exige preparação superficial e ensaios de cisalhamento/descolamento do conjunto real.

A geometria e o confinamento alteram fortemente a rigidez aparente. Se o parafuso ou encosto metálico desviar a carga do PAD, ele pode pouco absorver. Se o PAD entrar na cadeia de pré-carga, relaxação pode comprometer aperto e repetibilidade. Prever retenção mecânica e analisar esmagamento local, extrusão lateral, contato rígido após compressão e estabilidade das ventosas. Não definir espessura “ótima” sem curso e energia.

## 5. Plano de ensaios preparado — sem execução nesta fase

### A. Auditoria da montagem

Identificar estrutura substituível, braços, ferragens, ventosas e quatro PADs por ocorrência. Registrar materiais originais e massa pesada. Comparar STEP/desenho/peça física; não usar a casca de 2 mm da peça semicircular como espessura da SAMI. Preservar cópia original e exportar arquivo de preparação separado.

### B. Referência estática

Primeiro duas baselines com a mesma geometria e deposição: material atual caracterizado e PA-CF caracterizado. Aplicar reação real da flange e cargas nas interfaces das ventosas, incluindo excentricidade, distribuição desigual, aceleração, frenagem e caso de perda de ventosa quando pertinente. As imagens sustentam uma hipótese de 24 kg, equivalente a 235,36 N apenas sob gravidade; não fornecem aceleração nem forças de impacto. Não reutilizar os 2 kg/100 N da garra demonstrativa anterior.

Separar tração do corpo, flexão de braços, cisalhamento, arrancamento de insertos, esmagamento em furos, contato e aperto. O robô não torna a peça admissível apenas por ter capacidade nominal superior à massa; conferir envelope de carga, centro de gravidade e inércia na documentação aplicável.

### C. Preenchimentos

Manter 30%, 40%, 60% e 100% como níveis pedidos. Fixar espessura de paredes, camadas superiores/inferiores, padrão, orientação e parâmetros do fatiador. Primeiro resolver uma baseline e verificar convergência; depois expandir. Não multiplicar módulo ou resistência pela porcentagem de preenchimento. Para detalhes locais, usar geometria explícita consistente; para modelo equivalente, calibrar ensaios da arquitetura e verificar a validade.

### D. Impacto e PAD

Comparar sem PAD e com PAD nos dois materiais, inicialmente no preenchimento escolhido após estática. Impactos devem corresponder a um evento: caixa tocando a garra, fim de curso ou colisão da estrutura. Definir massa efetiva, velocidade normal, posição, direção e duração. Energia inicial `E=½m_efetiva v²`; massa efetiva do robô não é automaticamente sua carga nominal nem toda sua massa. Considerar configuração e flexibilidade do sistema.

Usar evento dinâmico com contato se a licença, o modelo de material e os recursos da versão suportarem o caso. Conferir penetração, passo temporal, balanço energético e sensibilidade de malha. Saídas: força × tempo, pico, impulso, aceleração, deformação dos PADs, tensão/deformação e contato rígido. Sem lei calibrada, classificar como estudo de sensibilidade; não alegar carga de ruptura ou vida útil. [Referência Autodesk de evento](https://help.autodesk.com/view/fusion360/ENU/?contextId=PRE-EVENT-SIM).

### E. Temperatura e durabilidade

Definir faixa térmica real, umidade, contaminantes e tempo. Estática em diferentes temperaturas requer propriedades correspondentes; impacto requer dependência da taxa quando significativa. Milhares de horas não se convertem em desgaste automaticamente: especificar ciclos, carga, amplitude, frequência, contato e deslizamento. Fadiga requer dados aplicáveis e fluência/relaxação requerem leis temporais. Preparar ensaio físico acelerado com critérios de falha e validação; não extrapolar arbitrariamente um ensaio curto.

### F. Critérios de aceitação a fechar

Carga de projeto e fator de segurança; deformação que preserva alinhamento/vácuo; contato e tensões em fixações; curso útil do PAD; pico transmitido permitido; retenção dos encaixes e da pré-carga; deformação permanente e repetibilidade; massa/centro de gravidade/inércia. Medir essas grandezas no protótipo e confrontar o modelo.

## 6. Arquitetura de baixo consumo e situação real

MCP oficial Autodesk como backend, servidor local `fusion-compact` como fachada STDIO com seis operações pequenas. Ele executa preflight, inventário, consulta de ficha, estimativa de massa e importação fixa do STEP em novo documento. Não expõe solver automático nem execução arbitrária de scripts pelo cliente. Sessão reutilizada, chamadas serializadas, respostas integrais no disco e retorno compacto. O teste de protocolo e a conexão real passaram.

Configuração de projeto: `.codex/config.toml`. O cliente carregou as seis ferramentas durante esta entrega; `inspect_active` e `estimate_mass` passaram também como chamadas MCP reais deste chat. O backend precisa do Fusion aberto com MCP habilitado. [MCP Autodesk](https://help.autodesk.com/view/fusion360/ENU/?guid=FMCP-OVERVIEW), [configuração Codex](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

Arquivo local exportado: `SAMI_PREPARACAO_PA_CF_TRITAN_PAD.f3d`, 21.693.035 bytes, integridade CRC do arquivo verificada. Contém a montagem importada para preparação; não contém resultados de solver nem atribuições validadas dos novos materiais. Não exige salvar sobre o projeto original.

Não há chamadas à API de modelos neste servidor. Reduzir retornos repetidos reduz texto enviado ao contexto, mas **não há medição de economia percentual de tokens ou garantia sobre franquia semanal**. O custo total depende do cliente, modelo e trabalho. A fachada não cria recursos de simulação ausentes no Fusion.

O fluxo usa arquivo de estado pequeno, fichas com fonte e revisão, scripts determinísticos e resultados com unidades. Não iniciar agentes paralelos por padrão. Capturas de tela somente para etapas sem API e evidência final; nada de repetir painéis inteiros no histórico. O problema de referências de restrição observado na campanha antiga permanece registrado; nenhuma baseline é aceita antes de precheck e auditoria de faces/restrições.

Situação desta entrega: ambiente preparado e servidor testado; materiais candidatos pesquisados; fórmulas de massa e plano de validação disponíveis. Identificação do material instalado, PU97A, parâmetros de impressão, distribuição de massa e cinemática continuam necessários para fechar um modelo quantitativo. **Não há novo resultado de impacto, tração, ruptura ou desgaste da SAMI.**

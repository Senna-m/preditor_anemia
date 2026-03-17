# Preditor de Anemia
Sistema de apoio ao diagnóstico de anemia baseado em marcadores hematológicos, combinando modelo preditivo com CatBoost e critérios clínicos da OMS.
🔗 Acesse o app ao vivo → (adicione o link do Streamlit Cloud após o deploy)

## Problema resolvido
Anemia é uma das condições mais prevalentes no mundo, mas seu diagnóstico precoce ainda depende de análise manual de exames laboratoriais. Este sistema analisa automaticamente os principais marcadores hematológicos e fornece dois critérios independentes de avaliação: um modelo preditivo treinado com dados reais e os valores de referência da OMS — aumentando a confiabilidade do resultado.

## Stack
CamadaTecnologiaLinguagemPython 3ML / ModeloCatBoost (.cbm)Análise de dadosPandas, Scikit-learnFrontend / DeployStreamlitTreinamentoGoogle Colab

## Como funciona
Usuário informa: sexo + hemoglobina + MCH + MCHC + MCV
        ↓
Modelo CatBoost prevê probabilidade de anemia
        ↓
Regra clínica OMS verifica hemoglobina por sexo
        ↓
App exibe os dois resultados + conclusão final
4 cenários de conclusão
ModeloOMSConclusão🔴 Anêmico🔴 Abaixo do limite⚠️ Alta probabilidade de anemia🟢 Normal🟢 Normal✅ Sem indicativo de anemia🔴 Anêmico🟢 Normal🟡 Divergente — investigar MCH/MCHC/MCV🟢 Normal🔴 Abaixo do limite🟡 Divergente — avaliação médica recomendada

## Features do modelo
FeatureDescriçãoImportânciaHemoglobinHemoglobina (g/dL)68%GenderSexo (M/F)30%MCHCConcentração de Hb corpuscular média0.75%MCHHemoglobina corpuscular média0.42%MCVVolume corpuscular médio~0%

Hemoglobina respondeu por 68% da decisão do modelo — consistente com o critério diagnóstico principal de anemia segundo a OMS.


## Valores de Referência OMS
GrupoHemoglobinaHomens< 13 g/dLMulheres< 12 g/dLGestantes< 11 g/dLCriançasVaria por idade

📂 Estrutura do projeto
preditor-anemia/
├── app.py                  # Aplicação Streamlit + lógica de diagnóstico
├── modelo_anemia.cbm       # Modelo CatBoost treinado e exportado
├── requirements.txt        # Dependências do projeto
└── notebooks/
    └── analise_anemia.py   # EDA, limpeza, treinamento e validação

## Como rodar localmente
bash
### 1. Clone o repositório
git clone https://github.com/Senna-m/preditor-anemia.git
cd preditor-anemia

### 2. Instale as dependências
pip install -r requirements.txt

### 3. Rode a aplicação
streamlit run app.py

## Decisões técnicas

CatBoost foi escolhido por lidar nativamente com variáveis categóricas (sexo) sem necessidade de encoding manual, e por generalizar bem em bases de dados pequenas.
A métrica de avaliação escolhida foi F1, pois em contexto clínico um falso negativo — paciente anêmico classificado como saudável — é mais grave que um falso positivo.
O modelo atingiu F1 = 1.0 no conjunto de teste, com zero falsos negativos, confirmando que os marcadores hematológicos são altamente discriminativos para o diagnóstico de anemia.
A combinação com os critérios da OMS adiciona uma camada de validação clínica independente do modelo.


⚠️ Aviso
Este app é uma ferramenta de apoio e não substitui avaliação médica profissional.

👩‍💻 Sobre
Desenvolvido por Nathalie Senna — GitHub · LinkedIn
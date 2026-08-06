
# 🏎️ F1 Race Strategy Predictor

> Uma aplicação Full-Stack de Machine Learning para prever o desgaste de pneus e as janelas ideais de pit stop usando dados de telemetria da Fórmula 1.

## 📌 O Projeto
Na Fórmula 1, o momento exato de um pit stop pode ser a diferença entre vencer uma corrida e terminar fora da zona de pontuação. A degradação dos pneus (o famoso "cliff") é um fenômeno complexo influenciado pela temperatura da pista, idade do composto e estilo de pilotagem.

Este projeto tem como objetivo construir um modelo preditivo de Machine Learning que consome dados reais de telemetria e prevê a janela ideal para a troca de pneus. Os insights são disponibilizados através de um dashboard web moderno e interativo, permitindo visualizar os dados e as previsões em tempo real.

## 🚀 Principais Funcionalidades
* **Pipeline de Extração de Dados:** Coleta automatizada de dados históricos de corridas e telemetria usando a API `FastF1`.
* **Engenharia de Atributos (Feature Engineering):** Cálculo de médias móveis, idade dos pneus e deltas de tempo de volta para alimentar o modelo.
* **Motor de Machine Learning:** Modelagem preditiva (métodos de Ensemble/XGBoost) para classificar e prever quedas de desempenho.
* **Dashboard Interativo:** Uma interface de usuário dinâmica para selecionar pilotos, circuitos e visualizar gráficos de telemetria lado a lado com as previsões da IA.

## 🛠️ Tecnologias Utilizadas
Este projeto foi construído com uma arquitetura desacoplada, separando o motor de IA da interface do usuário:

**Machine Learning e Dados**
* **Python:** Linguagem principal para processamento de dados.
* **FastF1 e Pandas:** Extração e manipulação dos dados brutos.
* **Scikit-Learn:** Treinamento, avaliação e ajuste de hiperparâmetros do modelo.

**Back-end (API e Banco de Dados)**
* **Flask / FastAPI:** API RESTful para servir as previsões e os dados de telemetria.
* **SQL:** Gerenciamento de banco de dados relacional para armazenar o histórico de corridas processado.

**Front-end**
* **React:** Desenvolvimento da interface baseada em componentes.
* **TypeScript:** Tipagem estática para um código escalável e livre de bugs.
* **Recharts / Chart.js:** Renderização de gráficos complexos de telemetria.

## 📂 Estrutura do Projeto
```text
f1-strategy-predictor/
├── data/               # Datasets brutos e processados (ignorados no git)
├── notebooks/          # Jupyter notebooks para análise exploratória e prototipagem
├── backend/            # API em Python, modelos de ML e conexões SQL
├── frontend/           # Aplicação do dashboard em React + TypeScript
└── README.md

# F1 Race Strategy Predictor

> Uma aplicação Full-Stack de Machine Learning para prever a degradação dos pneus e as janelas ideais de pit stop usando dados de telemetria da Fórmula 1.

## O Projeto

Na Fórmula 1, o momento exato de um pit stop pode ser a diferença entre vencer uma corrida ou terminar fora da zona de pontuação. A degradação dos pneus (o "cliff") é um fenômeno complexo influenciado pela temperatura da pista, idade do composto e estilo de pilotagem.

Este projeto tem como objetivo construir um modelo preditivo de Machine Learning que consome dados reais de telemetria e prevê a janela ideal para a troca de pneus. Na transição de scripts analíticos estáticos para uma arquitetura pronta para produção, os insights são gerados em memória e serão disponibilizados por meio de um dashboard web moderno e interativo, permitindo aos usuários visualizar dados e previsões em tempo real.

## Principais Funcionalidades

*   **Pipeline de Dados Dinâmico:** Extração automatizada e dinâmica de telemetria histórica de corridas usando a API `FastF1`. O pipeline inclui um tratamento de esquema resiliente para mapear dinamicamente os compostos de pneus (Macio, Médio, Duro, Intermediário, Chuva), independentemente do uso específico em cada corrida.
*   **Motor de ML em Memória:** Modelagem preditiva utilizando **Regressão AdaBoost** para prever quedas de desempenho dos pneus. A arquitetura de backend treina os modelos sob demanda (*on-the-fly*) na memória RAM, eliminando gargalos de I/O de disco (dependências de `.pkl`) para respostas instantâneas da API.
*   **Simulação de Estratégia e Detecção de Cliff:** Detecção algorítmica de janelas ideais de pit stop usando um "Período de Tolerância" (*Grace Period*) calculado para filtrar o ruído inicial da telemetria (ex: tanque cheio, tráfego) e identificar com precisão o verdadeiro ponto de degradação (*cliff*) do pneu.
*   **Dashboard Interativo (WIP - Em Desenvolvimento):** Uma interface de usuário dinâmica para selecionar pilotos, circuitos e visualizar gráficos de telemetria junto com as previsões de ML.

## Stack de Tecnologia

Este projeto é construído com uma arquitetura desacoplada, separando o motor de Machine Learning da interface de usuário:

**Machine Learning & Dados (Core Backend)**
*   **Python:** Linguagem principal para processamento de dados e orquestração do pipeline.
*   **FastF1 & Pandas:** Extração dinâmica, limpeza e manipulação de dados.
*   **Scikit-Learn:** Treinamento do modelo (AdaBoost), avaliação e ajuste de hiperparâmetros.

**API & Banco de Dados (Planejado)**
*   **Flask / FastAPI:** API RESTful para servir previsões em tempo real e dados de telemetria.
*   **SQL:** Gerenciamento de banco de dados relacional para armazenar dados processados de corridas e execexecuções históricas.

**Frontend (Planejado)**
*   **React:** Desenvolvimento de UI baseada em componentes.
*   **TypeScript:** Tipagem estática para código escalável e livre de bugs.
*   **Recharts / Chart.js:** Renderização de gráficos complexos de telemetria.

## 📁 Estrutura do Projeto

```text
f1-strategy-predictor/
├── backend/
│   ├── data_pipeline.py       # Extração dinâmica do FastF1 e engenharia de features
│   ├── model_pipeline.py      # Módulo de treinamento AdaBoost em memória
│   └── api/                   # (WIP) Rotas Flask/FastAPI
├── notebooks/                 # Notebooks Jupyter para EDA inicial e prototipagem
├── frontend/                  # Aplicação de dashboard em React + TypeScript
└── README.md

```
## Desenvolvido por Guilherme de Araújo Moreira

### Apaixonado por Engenharia de Software, Inteligência Artificial, Arquitetura de Dados e Design de Algoritmos.

* LinkedIn: www.linkedin.com/in/guilherme-de-araùjo-moreira-7440602b5

# F1 Race Strategy Predictor

> A Full-Stack Machine Learning application to predict tire degradation and optimal pit stop windows using Formula 1 telemetry data.

## The Project

In Formula 1, the timing of a pit stop can be the difference between winning a race and finishing outside the points. Tire degradation (the "cliff") is a complex phenomenon influenced by track temperature, compound age, and driving style.

This project aims to build a predictive Machine Learning model that ingests real telemetry data and forecasts the optimal window for a tire change. Transitioning from static analytical scripts to a production-ready architecture, the insights are generated in-memory and will be served through a modern, interactive web dashboard, allowing users to visualize data and predictions in real-time.

## Key Features

*   **Dynamic Data Pipeline:** Automated and dynamic fetching of historical race telemetry using the `FastF1` API. The pipeline includes resilient schema handling to dynamically map tire compounds (Soft, Medium, Hard, Intermediate, Wet) regardless of race-specific usage.
*   **In-Memory ML Engine:** Predictive modeling utilizing **AdaBoost Regression** to forecast tire performance drops. The backend architecture trains models on-the-fly in RAM, eliminating disk I/O bottlenecks (`.pkl` dependencies) for instant API responses.
*   **Strategy Simulation & Cliff Detection:** Algorithmic detection of optimal pit windows using a calculated "Grace Period" to filter out initial telemetry noise (e.g., heavy fuel, traffic) and accurately pinpoint the true tire cliff.
*   **Interactive Dashboard (WIP):** A dynamic user interface to select drivers, circuits, and view telemetry charts alongside ML predictions.

## Tech Stack

This project is built with a decoupled architecture, separating the ML engine from the user interface:

**Machine Learning & Data (Core Backend)**
*   **Python:** Core language for data processing and pipeline orchestration.
*   **FastF1 & Pandas:** Dynamic data extraction, cleaning, and manipulation.
*   **Scikit-Learn:** Model training (AdaBoost), evaluation, and hyperparameter tuning.

**API & Database (Planned)**
*   **Flask / FastAPI:** RESTful API to serve real-time predictions and telemetry data.
*   **SQL:** Relational database management for storing processed race data and historical runs.

**Frontend (Planned)**
*   **React:** Component-based UI development.
*   **TypeScript:** Static typing for scalable and bug-free code.
*   **Recharts / Chart.js:** Rendering complex telemetry graphs.

## 📁 Project Structure

```text
f1-strategy-predictor/
├── backend/
│   ├── data_pipeline.py       # Dynamic FastF1 extraction and feature engineering
│   ├── model_pipeline.py      # In-memory AdaBoost training module
│   └── api/                   # (WIP) Flask/FastAPI routing
├── notebooks/                 # Jupyter notebooks for initial EDA and prototyping
├── frontend/                  # React + TypeScript dashboard application
└── README.md


```
Developed by Guilherme de Araújo Moreira

Passionate about Software Engineering, Artificial Intelligence, Data Architecture, and Algorithmic Design.

LinkedIn: www.linkedin.com/in/guilherme-de-araùjo-moreira-7440602b5

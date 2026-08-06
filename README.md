#  F1 Race Strategy Predictor

> A Full-Stack Machine Learning application to predict tire degradation and optimal pit stop windows using Formula 1 telemetry data.

##  The Project
In Formula 1, the timing of a pit stop can be the difference between winning a race and finishing outside the points. Tire degradation (the "cliff") is a complex phenomenon influenced by track temperature, compound age, and driving style. 

This project aims to build a predictive Machine Learning model that ingests real telemetry data and forecasts the optimal window for a tire change. The insights are served through a modern, interactive web dashboard, allowing users to visualize the data and predictions in real-time.

##  Key Features
* **Data Extraction Pipeline:** Automated fetching of historical race and telemetry data using the `FastF1` API.
* **Feature Engineering:** Calculation of moving averages, tire age, and lap time deltas to feed the predictive model.
* **Machine Learning Engine:** Predictive modeling (Ensemble methods/XGBoost) to classify and forecast tire performance drops.
* **Interactive Dashboard:** A dynamic user interface to select drivers, circuits, and view telemetry charts alongside ML predictions.

##  Tech Stack
This project is built with a decoupled architecture, separating the ML engine from the user interface:

**Machine Learning & Data**
* **Python:** Core language for data processing.
* **FastF1 & Pandas:** Data extraction and manipulation.
* **Scikit-Learn:** Model training, evaluation, and hyperparameter tuning.

**Backend (API & Database)**
* **Flask / FastAPI:** RESTful API to serve predictions and telemetry data.
* **SQL:** Relational database management for storing processed race data.

**Frontend**
* **React:** Component-based UI development.
* **TypeScript:** Static typing for scalable and bug-free code.
* **Recharts / Chart.js:** Rendering complex telemetry graphs.

## 📂 Project Structure
```text
f1-strategy-predictor/
├── data/               # Raw and processed datasets (ignored in git)
├── notebooks/          # Jupyter notebooks for EDA and model prototyping
├── backend/            # Python API, ML models, and SQL connections
├── frontend/           # React + TypeScript dashboard application
└── README.md
```


👨‍💻 Author
Developed by Guilherme de Araujo 

Passionate about Software Engineering, Artificial Intelligence, and Data Architecture.

LinkedIn : https://www.linkedin.com/in/guilherme-de-ara%C3%B9jo-moreira-7440602b5/

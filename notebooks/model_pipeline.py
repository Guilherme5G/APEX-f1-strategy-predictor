from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor

def treinar_modelo_adaboost(X, y):
    base_estimator = DecisionTreeRegressor(max_depth=6)
    modelo = AdaBoostRegressor(
        estimator=base_estimator, 
        n_estimators=150, 
        learning_rate=0.05, 
        random_state=42
    )
    modelo.fit(X, y)
    return modelo
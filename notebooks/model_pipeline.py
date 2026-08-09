from sklearn.ensemble import AdaBoostRegressor

def treinar_modelo_adaboost(X, y):
    modelo = AdaBoostRegressor(random_state=42)
    modelo.fit(X, y)
    return modelo
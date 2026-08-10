import xgboost as xgb
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor


def treinar_modelo_xgb(X, y):
    """
    Modelo principal: XGBoost com monotonic constraint em TyreLife.

    A constraint forca a previsao de LapTime a ser monotonicamente
    NAO-DECRESCENTE conforme TyreLife aumenta -- ou seja, o modelo
    fica matematicamente proibido de prever que uma volta com pneu
    mais desgastado e mais rapida que uma anterior com pneu mais novo.
    Isso elimina os "cliffs" falsos causados por ruido/overfitting
    que aconteciam com o AdaBoostRegressor.
    """
    # constraint = 1 para TyreLife (monotonico crescente), 0 para as demais
    constraints = tuple(1 if col == 'TyreLife' else 0 for col in X.columns)

    modelo = xgb.XGBRegressor(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        monotone_constraints=constraints,
        random_state=42,
        n_jobs=-1,
    )
    modelo.fit(X, y)
    return modelo


def treinar_modelo_adaboost(X, y):
    """
    Mantido apenas para comparacao/referencia com a versao anterior.
    NAO recomendado como modelo principal -- ver treinar_modelo_xgb.
    """
    base_estimator = DecisionTreeRegressor(max_depth=6)
    modelo = AdaBoostRegressor(
        estimator=base_estimator,
        n_estimators=150,
        learning_rate=0.05,
        random_state=42,
    )
    modelo.fit(X, y)
    return modelo
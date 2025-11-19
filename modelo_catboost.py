
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error,r2_score
from sklearn.model_selection import GridSearchCV
import numpy as np



df = pd.read_csv("datos_limpios_vivienda.csv")

df["tipo_propiedad"] = df["tipo_propiedad"].astype(str)
df["barrio"] = df["barrio"].astype(str)
df["antiguedad"] = df["antiguedad"].astype(str)

# Variables predictoras y variable objetivo
x = df[['tipo_propiedad', 'area', 'habitaciones', 'banos',
       'parqueaderos','antiguedad', 'permite_mascotas', 'gimnasio',
       'ascensor', 'conjunto_cerrado', 'piscina', 'salon_comunal', 'terraza',
       'vigilancia', 'barrio']]
y = np.log1p(df["precio_venta"])
# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
X_train2, X_val, y_train2, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# Grid Search para hiperparámetros
parametros = {
    "depth": [4, 6],
    "learning_rate": [0.1, 0.03],
    "l2_leaf_reg": [3, 5],
    "iterations": [2000, 3000],
    "subsample": [0.7, 0.9],
    "bagging_temperature": [1, 3]
}


cat_categorias = [0,5,14]  # Índices de las características categóricas

catboost_modelo = CatBoostRegressor(
    eval_metric="RMSE",
    random_seed=42,
    logging_level="Silent",
)


gcv = GridSearchCV(
    estimator=catboost_modelo,
    param_grid=parametros,
    scoring="neg_root_mean_squared_error",
    cv=5,
    n_jobs=-1
)

gcv.fit(
    X_train,
    y_train,
    cat_features=cat_categorias
)

print("Mejores hiperparámetros:", gcv.best_params_)


modelo_final = CatBoostRegressor(
    **gcv.best_params_,
    eval_metric="RMSE",
    random_seed=42,
    logging_level="Silent",
    early_stopping_rounds=10,
    use_best_model=True
)

modelo_final.fit(
    X_train2, y_train2,
    eval_set=(X_val, y_val),
    cat_features=cat_categorias
)


# Predicciones en log
y_pred_log = modelo_final.predict(X_test)

# Convertir a escala real
y_pred = np.expm1(y_pred_log)
y_test_real = np.expm1(y_test)

# Métricas reales
rmse = np.sqrt(mean_squared_error(y_test_real, y_pred))
r2 = r2_score(y_test_real, y_pred)

print(f"RMSE real: {rmse:,.0f} COP")
print(f"R² real: {r2:.3f}")

y_pred_train = np.expm1(modelo_final.predict(X_train))
y_train_real = np.expm1(y_train)

r2_train = r2_score(y_train_real, y_pred_train)
print(f"R² (train, real): {r2_train:.3f}")

# Guardar modelo entrenado
ruta = "/content/drive/MyDrive/Inmobiliario/catboost_modelo.cbm"
modelo_final.save_model(ruta)
print("Modelo guardado en:", ruta)
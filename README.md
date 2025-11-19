# Proyecto: Prediccion de precio de viviendas en Bogotá

Descripción: repositorio para análisis y modelado de precios de vivienda. Incluye ETL, notebooks y un modelo entrenado con CatBoost.

**Contenido del repositorio**
- `app.py` : aplicación principal (puede ser un script/Streamlit — revisar contenido). 
- `ETL.py` : script para limpieza/transformación de datos.
- `modelo_catboost.py` : script para entrenamiento con CatBoost.
- `catboost_modelo.cbm` : modelo entrenado y serializado con CatBoost.
- `datos_limpios_vivienda.csv` : CSV con los datos limpios
- `processed_v2.0.0_august_2_2024.json` : archivo JSON con datos crudos

**Objetivos del proyecto**
- Preparar y limpiar datos de ventas de vivienda.
- Entrenar un modelo de regresión para predecir el precio de venta (CatBoost).

## Uso — Resumen rápido

  - Si quieres usar el modelo puedes entrar a :

## Entrenamiento y guardado del modelo

El notebook `Modelo_Catboost.ipynb` contiene un pipeline para dividir datos, buscar hiperparámetros con `GridSearchCV` y entrenar un `CatBoostRegressor`



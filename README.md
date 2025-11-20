🏠 Predicción del Precio de Viviendas en Bogotá

Repositorio para análisis, limpieza y modelado de datos inmobiliarios en Bogotá.
Incluye scripts ETL y un modelo de Machine Learning entrenado con CatBoost para predecir el precio de venta de una vivienda.

🔗 Para hacer uso del modelo entra a:
https://prediccion-precios-vivienda.streamlit.app/


📂 Contenido del repositorio

📄 app.py

   ▶️ Aplicación principal (script o interfaz en Streamlit).
   

🧹 ETL.py

   Script de limpieza, transformación y preparación de los datos.
   

🤖 modelo_catboost.py

   Código para entrenamiento del modelo usando CatBoostRegressor.
   Incluye división de datos, ajuste de parámetros e interpretación básica.
   

🧠 catboost_modelo.cbm

   Modelo entrenado
   

📊 datos_limpios_vivienda.csv

   Dataset procesado y limpio usado para entrenamiento.
   

📁 processed_v2.0.0_august_2_2024.json

   Dataset crudo original previo al proceso ETL.
   


🎯 Objetivos del proyecto

- Preparar, limpiar y transformar datos reales de viviendas en Bogotá.

- Analizar variables relevantes (ubicación, área, estrato, antigüedad, entre otras).

- Entrenar y validar un modelo de regresión basado en CatBoost.

- Optimizar el modelo usando GridSearchCV.

- Crear una interfaz para permitir predicciones rápidas desde scripts o aplicaciones.












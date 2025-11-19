# Proyecto: House_Pricing

Descripción: repositorio para análisis y modelado de precios de vivienda. Incluye ETL, notebooks y un modelo entrenado con CatBoost.

**Estado:** Con archivos de datos, scripts de entrenamiento y un modelo ya serializado.

**Contenido del repositorio**
- `app.py` : aplicación principal (puede ser un script/Streamlit — revisar contenido). 
- `ETL.py` : script para limpieza/transformación de datos.
- `modelo_catboost.py` : script para entrenamiento o utilidades relacionadas con CatBoost.
- `Modelo_Catboost.ipynb` : notebook de entrenamiento y búsqueda de hiperparámetros con `GridSearchCV`.
- `catboost_modelo.cbm` : modelo entrenado y serializado con CatBoost.
- `datos_limpios_vivienda.csv` : CSV con los datos limpios utilizados por los notebooks/scripts.
- `processed_v2.0.0_august_2_2024.json` : archivo JSON con datos procesados/metadata.

**Objetivos del proyecto**
- Preparar y limpiar datos de ventas de vivienda.
- Entrenar un modelo de regresión para predecir el precio de venta (CatBoost).
- Proveer un ejemplo reproducible (notebook y scripts).

---

## Requisitos
Se recomienda crear un entorno virtual (venv/conda) e instalar dependencias.

Instalación rápida (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Si no usas `PowerShell` adapta el comando de activación según tu shell.

## Dependencias principales
- `pandas`
- `numpy`
- `scikit-learn`
- `catboost`
- `jupyter` / `notebook`
- `streamlit` (si `app.py` es una app streamlit)
- `jupyter_http_over_ws` (opcional, para conectar Colab a runtime local)

Las versiones exactas están en `requirements.txt`.

---

## Uso — Resumen rápido

1) Ejecutar localmente (notebook)

- Abrir `Modelo_Catboost.ipynb` con Jupyter/VS Code y ejecutar las celdas. El notebook asume que `datos_limpios_vivienda.csv` está en la misma carpeta, por lo que la línea:

```python
df = pd.read_csv("datos_limpios_vivienda.csv")
```

debería funcionar sin cambios si ejecutas la notebook en la misma carpeta del repo.

2) Ejecutar `modelo_catboost.py` o `ETL.py`

- Revisa el contenido de los scripts para ver argumentos necesarios. Un ejemplo general:

```powershell
python ETL.py
python modelo_catboost.py
```

3) Ejecutar la app (si `app.py` es Streamlit)

```powershell
streamlit run app.py
```

---

## Cómo usar el CSV desde Google Colab

Si quieres ejecutar partes del proyecto en Google Colab (archivo CSV en tu PC), tienes tres opciones:

- Opción A — Subir el archivo temporalmente (rápido para archivos pequeños/medianos):

```python
from google.colab import files
import pandas as pd
import io

uploaded = files.upload()
filename = next(iter(uploaded.keys()))
df = pd.read_csv(io.BytesIO(uploaded[filename]))
```

- Opción B — Subir el archivo a Google Drive y montar Drive:

```python
from google.colab import drive
drive.mount('/content/drive')
df = pd.read_csv('/content/drive/MyDrive/carpeta/datos_limpios_vivienda.csv')
```

- Opción C — Conectar Colab a tu runtime local (acceso directo a `C:\...`) — requiere exponer un servidor Jupyter en tu máquina y conectar desde Colab:

En Windows PowerShell (instalar y habilitar):

```powershell
pip install jupyter_http_over_ws
jupyter serverextension enable --py jupyter_http_over_ws
jupyter notebook --NotebookApp.allow_origin="https://colab.research.google.com" --port=8888 --NotebookApp.port_retries=0
```

En Colab: Conectar → `Connect to local runtime` y pega la URL que te muestra Jupyter. Luego puedes leer el CSV con la ruta Windows, por ejemplo:

```python
import pandas as pd
df = pd.read_csv(r'C:\Practica_Analisis_De_Datos\House_Pricing\datos_limpios_vivienda.csv')
```

> Atención: conectar runtime local implica exponer puertos y usar tokens; ten cuidado con la seguridad.

---

## Entrenamiento y guardado del modelo

El notebook `Modelo_Catboost.ipynb` contiene un pipeline para dividir datos, buscar hiperparámetros con `GridSearchCV` y entrenar un `CatBoostRegressor`. Al final guarda el modelo con:

```python
modelo_final.save_model("modelo_catboost.cbm")
```

El archivo `catboost_modelo.cbm` (o `modelo_catboost.cbm`) es el modelo serializado que puedes cargar con CatBoost en producción o en otra notebook.

---

## Notas y recomendaciones
- Si tienes datos grandes, usa Google Drive en vez de `files.upload()`.
- Si vas a desplegar un servicio, exporta el modelo y crea un script/endpoint que cargue `modelo_catboost.cbm` y sirva predicciones.
- Mantén privados los archivos con datos sensibles.

---

## Próximos pasos sugeridos
- Confirmar si `app.py` es una app Streamlit: puedo añadir instrucciones concretas de ejecución y ejemplo de UI.
- Añadir ejemplos de carga del modelo y endpoint Flask/FastAPI si quieres desplegar predicciones.

---

Si quieres, pongo aquí instrucciones específicas para ejecutar `app.py` o añado un script de ejemplo para cargar `modelo_catboost.cbm` y predecir.


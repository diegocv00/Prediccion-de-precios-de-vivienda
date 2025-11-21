import streamlit as st
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor

# -----------------------------------
# Cargar modelo CatBoost
# -----------------------------------
modelo = CatBoostRegressor()
modelo.load_model("catboost_modelo.cbm")

st.title("🏡 Predicción de precio de viviendas en Bogotá(CatBoost)")
st.write("Ingrese las características de la propiedad para predecir el precio de venta.")

# -----------------------------------
# Cargar lista de barrios desde un archivo CSV o DataFrame
# -----------------------------------
df = pd.read_csv("datos_limpios_vivienda.csv")   # <-- Ajusta el nombre del archivo
barrios = sorted(df["barrio"].dropna().unique().tolist())

# Opciones de antigüedad REALES del dataset
opciones_antiguedad = [
    'ENTRE 10 Y 20 ANOS',
    'MAS DE 20 ANOS',
    'ENTRE 0 Y 5 ANOS',
    'ENTRE 5 Y 10 ANOS',
    'REMODELADO',
    'PARA ESTRENAR',
    'SOBRE PLANOS',
    'EN CONSTRUCCION'
]

# -----------------------------------
# Inputs del usuario
# -----------------------------------

tipo_propiedad = st.selectbox("Tipo de Propiedad", ["CASA", "APARTAMENTO"])

area = st.number_input("Área (m²)", min_value=10.0, max_value=1300.0, value=70.0)
habitaciones = st.number_input("Habitaciones", min_value=1, max_value=10, value=2)
banos = st.number_input("Baños", min_value=1, max_value=10, value=2)
parqueaderos = st.number_input("Parqueaderos", min_value=0, max_value=10, value=1)


barrio = st.selectbox("Barrio", barrios)
antiguedad = st.selectbox("Antigüedad", opciones_antiguedad)

permite_mascotas = st.checkbox("Permite mascotas")
gimnasio = st.checkbox("Gimnasio")
ascensor = st.checkbox("Ascensor")
conjunto_cerrado = st.checkbox("Conjunto cerrado")
piscina = st.checkbox("Piscina")
salon_comunal = st.checkbox("Salón comunal")
terraza = st.checkbox("Terraza")
vigilancia = st.checkbox("Vigilancia 24h")



def to_int(val):
    return 1 if val else 0

# -----------------------------------
# Predicción
# -----------------------------------

if st.button("Predecir precio"):

    x = np.array([[
        tipo_propiedad,
        area,
        habitaciones,
        banos,
        parqueaderos,
        antiguedad,
        to_int(permite_mascotas),
        to_int(gimnasio),
        to_int(ascensor),
        to_int(conjunto_cerrado),
        to_int(piscina),
        to_int(salon_comunal),
        to_int(terraza),
        to_int(vigilancia),
        barrio
    ]], dtype=object)

    log_pred = modelo.predict(x)[0]
    pred = np.expm1(log_pred)

    st.subheader("💰 Precio Estimado")
    st.success(f"${pred:,.0f} COP")



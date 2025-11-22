import streamlit as st
import numpy as np
import pandas as pd
from catboost import CatBoostRegressor
import base64

# -----------------------------------
# Configuración de página
# -----------------------------------
st.set_page_config(
    page_title="Brújula inmobiliaria Bogotá",
    page_icon="🧭",
    layout="wide"
)
# -----------------------------------
IMG_URL = "https://i.postimg.cc/9FNdjnN2/aerial-night-view-over-downtown-600nw-2023944962.webp"

st.markdown(f"""
    <style>
    /* Importar fuente Inter */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}
    
    /* Contenedor principal */
    .main > div {{
        padding-top: 2rem;
    }}
    
 
    .header-container {{
        /* Capa oscura (gradiente) + Imagen URL */
        background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3)), url('{IMG_URL}');
        background-size: cover;       /* La imagen cubre todo el espacio */
        background-position: center;  /* Centrar la imagen */
        background-repeat: no-repeat;
        padding: 4rem 2rem;           /* Espacio interno para dar altura */
        border-radius: 1rem;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        text-align: center;
    }}
    
    .header-container h1 {{
        color: white !important;
        font-size: 2.5rem;
        font-weight: 800;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        margin: 0;
    }}
    
    .header-container p {{
        color: #E5E7EB !important; /* Gris muy claro */
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 0.5rem;
        text-shadow: 0 1px 2px rgba(0,0,0,0.5);
    }}
    
    /* Estilo del botón */
    .stButton > button {{
        width: 100%;
        background-color: #10B981;
        color: white;
        font-weight: bold;
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        border: none;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: #059669;
        transform: scale(1.02);
    }}
    
    /* Estilo de resultados */
    .result-box {{
        background-color: #ECFDF5;
        border-left: 5px solid #10B981;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
    }}
    </style>
""", unsafe_allow_html=True)

# -----------------------------------
# Cargar modelo CatBoost
# -----------------------------------
modelo = CatBoostRegressor()
modelo.load_model("catboost_modelo.cbm")

# Título y descripción
st.markdown("""
    <div class='header-container'>
        <h1>TU BRÚJULA INMOBILIARIA EN BOGOTÁ</h1>
        <p>Conoce el precio de tu próximo hogar</p>
    </div>
""", unsafe_allow_html=True)



# Cargar lista de barrios

df = pd.read_csv("datos_limpios_vivienda.csv")   # <-- Ajusta el nombre del archivo
barrios = sorted(df["barrio"].dropna().unique().tolist())

# Opciones de antigüedad reales del dataset
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



# Formulario

st.write("") # Espacio
col1, col2 = st.columns(2)
with col1:
    tipo_propiedad = st.selectbox("**Tipo de Propiedad**", ["APARTAMENTO", "CASA"])
with col2:
    area = st.number_input("**Área (m²)**", min_value=10.0, max_value=1300.0, value=70.0)

col3, col4, col5 = st.columns(3)
with col3:
    habitaciones = st.number_input("**Habitaciones**", 1, 10, 2)
with col4:
    banos = st.number_input("**Baños**", 1, 10, 2)
with col5:
    parqueaderos = st.number_input("**Parqueaderos**", 0, 10, 1)

col6, col7 = st.columns(2)
with col6:
    barrio = st.selectbox("**Barrio**", barrios)
with col7:
    antiguedad = st.selectbox("**Antigüedad**", opciones_antiguedad)

st.markdown("**Comodidades**")

c1, c2, c3, c4 = st.columns(4)
permite_mascotas = c1.checkbox("Mascotas")
piscina = c1.checkbox("Piscina")
gimnasio = c2.checkbox("Gimnasio")
salon_comunal = c2.checkbox("Salón Comunal", True)
ascensor = c3.checkbox("Ascensor")
terraza = c3.checkbox("Terraza")
conjunto_cerrado = c4.checkbox("Conjunto", True)
vigilancia = c4.checkbox("Vigilancia", True)

# Función auxiliar
def to_int(val): return 1 if val else 0

# Botón
if st.button("Predecir Precio"):
    # Vector de características
    x = np.array([[
        tipo_propiedad, area, habitaciones, banos, parqueaderos, antiguedad,
        to_int(permite_mascotas), to_int(gimnasio), to_int(ascensor),
        to_int(conjunto_cerrado), to_int(piscina), to_int(salon_comunal),
        to_int(terraza), to_int(vigilancia), barrio
    ]], dtype=object)

    log_pred = modelo.predict(x)[0]
    pred = np.expm1(log_pred)

    st.markdown(f"""
    <div class='result-box'>
        <h5 style='margin:0; color:#065F46'>Valor estimado de mercado</h5>
        <h5 style='margin:0; color:#047857'>${pred:,.0f} COP</h5>
   
    </div>
    """, unsafe_allow_html=True)


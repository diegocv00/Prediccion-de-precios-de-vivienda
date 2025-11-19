import pandas as pd
import numpy as np

def limpiar_numberDouble(x):
    if isinstance(x, dict) and '$numberDouble' in x:
        valor = x['$numberDouble']
        if valor.lower() == 'nan':
            return np.nan
        else:
            try:
                return float(valor)
            except ValueError:
                return np.nan
    return x

def eliminar_outliers_por_estrato(df, estrato: int):
    # Filtrar estrato seleccionado
    df_estrato = df[df["estrato"] == estrato].copy()


    # Calcular IQR para precio_venta
    Q1 = df_estrato["precio_venta"].quantile(0.25)
    Q3 = df_estrato["precio_venta"].quantile(0.75)
    IQR = Q3 - Q1

    # Filtrar
    df_filtrado = df_estrato[
        (df_estrato["precio_venta"] >= Q1 - 1.5 * IQR) &
        (df_estrato["precio_venta"] <= Q3 + 1.5 * IQR)
    ].copy()

    return df_filtrado

df = pd.read_json("processed_v2.0.0_august_2_2024.json")

#Eliminar filas con estrato 0 ya que aportan informacion errónea(propiedades con valor de mas de mil millones con estrato 0)
df = df.drop(df.loc[df["estrato"] == 0].index)

# Eliminar filas con valores nulos
df = df.dropna()

# Eliminar filas con area menor a 30 metros cuadrados
df = df.drop(df.loc[df["area"] < 30].index) 

# Seleccionar solo las propiedades en venta
df = df[df["tipo_operacion"] == "VENTA"]

# Unificar categorías en 'tipo_propiedad'
df.loc[df["tipo_propiedad"] == "CASA CON CONJUNTO CERRADO", "tipo_propiedad"] = "CASA"

# Limpiar valores de tipo '$numberDouble'


# Aplicar a todo el DataFrame
df = df.map(limpiar_numberDouble)
df = df.apply(pd.to_numeric, errors='ignore')

df_limpia = pd.concat([
    eliminar_outliers_por_estrato(df, e) 
    for e in sorted(df["estrato"].unique())
], ignore_index=True)

columnas_a_borrar = ["_id","codigo","tipo_operacion","administracion",'sector', 'latitud', 'longitud', 'direccion',
        'website', 'last_view', 'datetime', 'url', 'timeline', 'compañia', 'precio_arriendo', 'jacuzzi', 'piso', 'closets',
       'chimenea','coords_modified','estacion_tm_cercana',
       'distancia_estacion_tm_m', 'is_cerca_estacion_tm', 'parque_cercano',
       'distancia_parque_m', 'is_cerca_parque',"descripcion","estado","localidad"]

df_limpia = df_limpia.drop(columns=columnas_a_borrar)
df_limpia.to_csv("datos_limpios_vivienda.csv", index=False)



import streamlit as st
import pandas as pd

st.set_page_config(page_title="Prueba Vendedores", layout="wide")

st.title("PRUEBA: Dashboard de vendedores")
st.write("Si ves este texto, github_lale.py se está ejecutando correctamente.")

st.subheader("Prueba de carga del archivo Excel")

# Intentamos leer el archivo vendedores.xlsx y mostramos qué pasa
try:
    df = pd.read_excel("vendedores.xlsx")
    st.success("✅ Archivo 'vendedores.xlsx' cargado correctamente.")
    
    st.write("**Columnas del archivo:**")
    st.write(list(df.columns))
    
    st.write("**Primeras filas de la tabla:**")
    st.dataframe(df.head())
except FileNotFoundError:
    st.error("❌ No se encontró el archivo 'vendedores.xlsx' en esta carpeta.")
except Exception as e:
    st.error(f"❌ Ocurrió un error al leer el Excel:\n\n{e}")

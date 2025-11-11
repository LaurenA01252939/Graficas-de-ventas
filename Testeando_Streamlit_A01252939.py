#Importación de librerias
import streamlit as st
import pandas as pd
import plotly.express as px

#Configuración de la pagina web
st.set_page_config(page_title="Dashboard de Vendedores", layout="wide")
#En esta funcíon se cargan los datos del excel al .py
@st.cache_data
def cargar_datos(ruta_archivo: str) -> pd.DataFrame:
    df = pd.read_excel(ruta_archivo)
    df["VENDEDOR"] = df["NOMBRE"].astype(str) + " " + df["APELLIDO"].astype(str)
    return df

st.title("Dashboard de Vendedores")

#Aquí se carga el archivo al main.py, se comprueba la subida del archivo y si presenta errores se detiene el programa.
try:
    df = cargar_datos("vendedores.xlsx")
    st.success("Archivo 'vendedores.xlsx' cargado correctamente.")
except FileNotFoundError:
    st.error("No se encontró el archivo 'vendedores.xlsx'.")
    st.stop()

except Exception as e:
    st.error(f"Ocurrió un error al leer el archivo: {e}")
    st.stop()
#Muestra las regiones 
regiones_disponibles = sorted(df["REGION"].unique())
#Barra de filtros y selección de vendedor
with st.sidebar:
    st.title("Controles")
    regiones_seleccionadas = st.multiselect(
        "Filtrar por región",
        options=regiones_disponibles,
        default=regiones_disponibles
    )
#Filtro de base de datos por región
    if len(regiones_seleccionadas) == 0:
        df_filtrado = df.copy()
    else:
        df_filtrado = df[df["REGION"].isin(regiones_seleccionadas)]
    #Selección y despliegue del vendedor
    vendedores_disponibles = sorted(df_filtrado["VENDEDOR"].unique())
    vendedor_seleccionado = st.selectbox("Selecciona un vendedor", options=vendedores_disponibles)
    #Botón para confirmar selección de vendedor
    boton_detalle = st.button("Mostrar")
#Tabla de principal de vendedores
st.subheader("Tabla de vendedores")
st.dataframe(df_filtrado, use_container_width=True)

st.subheader("Gráficas de desempeño")
#Configuración de graficas de desempeño
if df_filtrado.empty:
    st.warning("No hay datos para las regiones seleccionadas.")
else:
    col1, col2 = st.columns(2)
#Grafica de unidades vendidas
    with col1:
        st.markdown("Unidades vendidas por vendedor")
        fig_unidades = px.bar(
            df_filtrado,
            x="VENDEDOR",
            y="UNIDADES VENDIDAS",
            color="REGION",
            title="Unidades vendidas por vendedor",
            labels={"VENDEDOR": "Vendedor", "UNIDADES VENDIDAS": "Unidades vendidas", "REGION": "Región"}
        )
        fig_unidades.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_unidades, use_container_width=True)
#Grafica de ventas totales
    with col2:
        st.markdown("Ventas totales por vendedor")
        fig_ventas = px.bar(
            df_filtrado,
            x="VENDEDOR",
            y="VENTAS TOTALES",
            color="REGION",
            title="Ventas totales por vendedor",
            labels={"VENDEDOR": "Vendedor", "VENTAS TOTALES": "Ventas totales", "REGION": "Región"},
        )
        fig_ventas.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_ventas, use_container_width=True)
#Grafica de porcentaje de ventas
    st.markdown("Porcentaje de ventas por vendedor")
    fig_pct = px.pie(
        df_filtrado,
        names="VENDEDOR",
        values="PORCENTAJE DE VENTAS",
        title="Distribución porcentual de las ventas",
        hole=0.3
    )
    st.plotly_chart(fig_pct, use_container_width=True)

st.subheader("Detalle de un vendedor específico")
#Mostrar detalles del vendedor
#Si no lo encuentra manda error y si lo encuentra despliega todas las metricas para ese vendedor
if boton_detalle:
    df_vendedor = df_filtrado[df_filtrado["VENDEDOR"] == vendedor_seleccionado]
    if df_vendedor.empty:
        st.warning("No se encontraron datos para ese vendedor.")
    else:
        st.markdown(f"Vendedor: {vendedor_seleccionado}")
        st.table(df_vendedor)
        fila = df_vendedor.iloc[0]
        c1, c2, c3 = st.columns(3)
        c1.metric("Unidades vendidas", int(fila["UNIDADES VENDIDAS"]))
        c2.metric("Ventas totales", float(fila["VENTAS TOTALES"]))
        porcentaje = float(fila["PORCENTAJE DE VENTAS"]) * 100
        c3.metric("Porcentaje de ventas", f"{porcentaje:.2f}%")

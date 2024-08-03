import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import datetime
# import seaborn as sns
import plotly.express as px
# import missingno as msn
from PIL import Image

año_actual = datetime.datetime.now().year
ruta_logo = "logo3_uta.png"
logo = Image.open(ruta_logo)
tamaño_logo = (290,290)
st.set_page_config(layout="wide", page_title="Dashboard", page_icon=":chart_with_upwards_trend:", initial_sidebar_state="collapsed")
st.sidebar.image(logo,width=tamaño_logo[0])

@st.cache_data(experimental_allow_widgets=True)
 
def cargar_datos(archivo_csv):
    return pd.read_csv(archivo_csv,sep=";")

df_seleccionados = pd.DataFrame()
def filtrar():
    st.header("Filtrar por fechas")
    archivos_csv = st.file_uploader("Cargar archivos CSV", type=["csv"], accept_multiple_files=True)

    if archivos_csv:
        dataframes = []
        for archivo in archivos_csv:
            # Leer cada archivo CSV en un DataFrame de pandas y agregarlo a la lista
            df = pd.read_csv(archivo, sep=';')
            dataframes.append(df)
        # Combinar todos los DataFrames en uno solo
        if dataframes:
            df_cargados = pd.concat(dataframes, ignore_index=True)
            # Obtener los partidos y legislaturas únicos
            partidos = df_cargados['Partido'].unique()
            #legislaturas= df_cargados['ID_Legislatura'].unique()
            # Selector de partido y legislatura
            partido_seleccionado = st.selectbox("Selecciona un partido", partidos)
            # Filtrar el DataFrame por el partido y legislatura seleccionados
            df_cargados = df_cargados[(df_cargados['Partido'] == partido_seleccionado)]
            # Mostrar el DataFrame filtrado
            st.dataframe(df_cargados)
    else:
        st.write("Por favor, carga uno o más archivos CSV.")       

def principal():
    size_title = 'font-size: 24px; text-align: center; color: #000000; font-weight: lighter'
    title = "Dashboard Legislaturas"
    st.sidebar.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
   
    bd_default = "372.csv"
    df_test = cargar_datos(bd_default)

    opciones = st.sidebar.radio(" ", options=[ "filtrar"])
    if opciones == "filtrar":
        filtrar()

if __name__ == "__main__":
    principal()
    

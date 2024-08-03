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
            partido_seleccionado = st.multiselect("Selecciona un partido", partidos)
            if partido_seleccionado:
                # Filtrar el DataFrame por los partidos seleccionados
                df_filtrado = df_cargados[df_cargados['Partido'].isin(partido_seleccionado)]
                # Mostrar el DataFrame filtrado
                st.dataframe(df_filtrado)
                return df_filtrado
    else:
        st.write("Por favor, carga uno o más archivos CSV.")       
    return pd.DataFrame()


def mostrar_total_asistentes(df):
    """Mostrar número total de asistentes y ausentes."""
    st.header("Número total de asistentes y ausentes")
    partidos = df['Partido'].unique()
    for partido in partidos:
        st.subheader(f"Partido: {partido}")
        df_partido = df[df['Partido'] == partido]
        total_asistentes = df_partido['Asistencia'].value_counts()
        fig = px.bar(total_asistentes, title="Número total de asistentes y ausentes")
        st.plotly_chart(fig)

def mostrar_frecuencia_asistencia_persona(df):
    """Mostrar frecuencia de asistencia por persona."""
    st.header("Frecuencia de asistencia por persona")
    partidos = df['Partido'].unique()
    for partido in partidos:
        st.subheader(f"Partido: {partido}")
        df_partido = df[df['Partido'] == partido]
        frecuencia_asistencia_persona = df_partido.groupby('Nombre')['Asistencia'].value_counts().unstack().fillna(0)
        st.write(frecuencia_asistencia_persona)

def mostrar_tipos_observaciones(df):
    """Mostrar tipos de observaciones."""
    st.header("Tipos de observaciones")
    tipos_observaciones = df['Observacion'].value_counts()
    fig = px.bar(tipos_observaciones, title="Tipos de observaciones")
    st.plotly_chart(fig)

def mostrar_asistencia_tiempo(df):
    """Mostrar asistencia a lo largo del tiempo."""
    st.header("Asistencia a lo largo del tiempo")
    partidos = df['Partido'].unique()
    for partido in partidos:
        st.subheader(f"Partido: {partido}")
        df_partido = df[df['Partido'] == partido]
        asistencia_tiempo = df_partido.groupby(['ID_Legislatura', 'ID_Sesion'])['Asistencia'].apply(lambda x: (x == 'A').mean() * 100).reset_index()
        fig = px.line(asistencia_tiempo, x='ID_Sesion', y='Asistencia', color='ID_Legislatura', title="Asistencia a lo largo del tiempo")
        st.plotly_chart(fig)

def mostrar_ranking_asistencia(df):
    """Mostrar ranking de asistencia por persona."""
    st.header("Ranking de asistencia por persona")
    partidos = df['Partido'].unique()
    for partido in partidos:
        st.subheader(f"Partido: {partido}")
        df_partido = df[df['Partido'] == partido]
        ranking_asistencia = df_partido.groupby('Nombre')['Asistencia'].apply(lambda x: (x == 'A').mean() * 100).sort_values(ascending=False).reset_index()
        fig = px.bar(ranking_asistencia, x='Nombre', y='Asistencia', title="Ranking de asistencia por persona")
        st.plotly_chart(fig)

def graficas(df):
    mostrar_total_asistentes(df)
    mostrar_frecuencia_asistencia_persona(df)
    mostrar_tipos_observaciones(df)
    mostrar_asistencia_tiempo(df)
    mostrar_ranking_asistencia(df)
    
def principal():
    size_title = 'font-size: 24px; text-align: center; color: #000000; font-weight: lighter'
    title = "Dashboard Legislaturas"
    st.sidebar.write(f'<p style="{size_title}">{title}</p>',unsafe_allow_html=True)
    #Seleccionar disntitas opciones barra lateral izquierda
    opciones = st.sidebar.radio(" ", options=[ "filtrar"])
    if opciones == "filtrar":
        df=filtrar()
        graficas(df)
if __name__ == "__main__":
    principal()
    

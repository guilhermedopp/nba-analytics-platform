import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.database import engine

st.set_page_config(
    page_title="NBA Data Warehouse",
    layout="wide",
    page_icon="🏀"
)

st.title("NBA Analytics Platform")
st.markdown("Esse dashboard consome dados processados pelo **ETL Pipeline** e armazenados no **PostgreSQL local**")

@st.cache_data
def load_data():
    query = """
    SELECT 
        p.full_name as "Nome", 
        p.position as "Posição", 
        p.height as "Altura", 
        p.weight as "Peso (lbs)", 
        p.country as "País",
        t.full_name as "Time",
        t.conference as "Conferência"
    FROM dim_players p
    JOIN dim_teams t ON p.team_id = t.id
    WHERE p.is_active = true
    """
    return pd.read_sql(query, engine)

df = load_data()

st.sidebar.header("Filtros")

lista_times = ['Todos'] + sorted(df['Time'].unique())
time_selecionado = st.sidebar.selectbox("Escolha um time", lista_times)

lista_posicoes = ['Todas'] + sorted(df['Posição'].unique())
posicao_selecionada = st.sidebar.selectbox("Escolha uma Posição:", lista_posicoes)

df_filtrado = df.copy()

if time_selecionado != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Time'] == time_selecionado]

if posicao_selecionada != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Posição'] == posicao_selecionada]

st.divider()

col1, col2, col3 = st.columns(3)
col1.metric("Jogadores Encontrados", len(df_filtrado))

media_peso = pd.to_numeric(df_filtrado['Peso (lbs)'], errors='coerce').mean()
col2.metric("Média de Peso", f"{media_peso:.1f} lbs")
col3.metric("Países Diferentes", df_filtrado['País'].nunique())

st.subheader("Detalhes do Elenco")
st.dataframe(
    df_filtrado, 
    use_container_width=True, 
    width='stretch',
    hide_index=True,
    height=500
)
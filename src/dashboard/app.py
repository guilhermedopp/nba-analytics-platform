import streamlit as st
import pandas as pd
import altair as alt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.database import engine

st.set_page_config(page_title="NBA Scouting 2026", layout="wide", page_icon="🏀")
st.title("🏀 NBA Scouting Tool (2025-26)")

@st.cache_data
def load_data():
    query = """
    SELECT 
        p.full_name as "Nome", 
        t.full_name as "Time",
        p.position as "Posição", 
        COALESCE(s.gp, 0) as "Jogos",
        COALESCE(s.pts, 0) as "PTS_Total",
        COALESCE(s.reb, 0) as "REB_Total",
        COALESCE(s.ast, 0) as "AST_Total",
        COALESCE(s.stl, 0) as "STL_Total",
        COALESCE(s.blk, 0) as "BLK_Total",
        COALESCE(s.net_rating, 0) as "Saldo (+/-)"
    FROM dim_players p
    JOIN dim_teams t ON p.team_id = t.id
    LEFT JOIN fact_player_stats s ON p.id = s.player_id
    WHERE p.is_active = true
    """
    df = pd.read_sql(query, engine)
    
    df['PPG'] = (df['PTS_Total'] / df['Jogos']).fillna(0).round(1)
    df['RPG'] = (df['REB_Total'] / df['Jogos']).fillna(0).round(1)
    df['APG'] = (df['AST_Total'] / df['Jogos']).fillna(0).round(1)
    df['SPG'] = (df['STL_Total'] / df['Jogos']).fillna(0).round(1)
    df['BPG'] = (df['BLK_Total'] / df['Jogos']).fillna(0).round(1)
    
    return df

df = load_data()

st.sidebar.header("Configurações")

modo_visualizacao = st.sidebar.radio(
    "Tipo de Dados:",
    ("Médias por Jogo", "Totais da Temporada")
)

st.sidebar.divider()

if not df.empty:
    times = ['Todos'] + sorted(df['Time'].unique())
    time_sel = st.sidebar.selectbox("Filtrar Time:", times)
    
    posicoes = ['Todas'] + sorted(df['Posição'].unique())
    pos_sel = st.sidebar.selectbox("Filtrar Posição:", posicoes)

    df_filtrado = df.copy()
    if time_sel != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Time'] == time_sel]
    if pos_sel != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Posição'] == pos_sel]

    if modo_visualizacao == "Médias por Jogo":
        cols_metricas = {'PTS': 'PPG', 'REB': 'RPG', 'AST': 'APG', 'STL': 'SPG', 'BLK': 'BPG'}
        col_ordenacao = 'PPG'
        titulo_y = 'Pontos por Jogo (PPG)'
    else:
        cols_metricas = {'PTS': 'PTS_Total', 'REB': 'REB_Total', 'AST': 'AST_Total', 'STL': 'STL_Total', 'BLK': 'BLK_Total'}
        col_ordenacao = 'PTS_Total'
        titulo_y = 'Pontos Totais na Temporada'

    st.divider()

    st.metric("Jogadores Encontrados", len(df_filtrado))

    st.subheader(f"Eficiência x {modo_visualizacao}")
    
    chart = alt.Chart(df_filtrado).mark_circle(size=80).encode(
        x=alt.X('Saldo (+/-)', title='Saldo (+/-)'),
        y=alt.Y(cols_metricas['PTS'], title=titulo_y),
        color=alt.Color('Posição'),
        tooltip=['Nome', 'Time', cols_metricas['PTS'], cols_metricas['REB'], cols_metricas['AST'], 'Saldo (+/-)']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

    st.subheader(f"Tabela ({modo_visualizacao})")
    
    cols_display = ['Nome', 'Posição', 'Time', 'Jogos', 
                   cols_metricas['PTS'], cols_metricas['REB'], cols_metricas['AST'], 
                   cols_metricas['STL'], cols_metricas['BLK'], 'Saldo (+/-)']
    
    st.dataframe(
        df_filtrado.sort_values(col_ordenacao, ascending=False)[cols_display],
        width='stretch',
        hide_index=True
    )

else:
    st.warning("Banco de dados vazio. Rode o pipeline.py!")
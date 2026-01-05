import streamlit as st
import pandas as pd
import altair as alt
from sqlalchemy import text
import sys
import os

sys.path.append(os.getcwd())
from src.database import engine

st.set_page_config(page_title="NBA Scouting 2025-26", layout="wide", page_icon="🏀")
st.title("🏀 NBA Analytics Platform 2025-26")

@st.cache_data(ttl=3600)
def load_data():
    query = """
    SELECT 
        p.full_name AS "Jogador",
        p.position AS "Posição",
        t.abbreviation AS "Time",
        s.pts AS "PTS",
        s.reb AS "REB",
        s.ast AS "AST",
        s.stl AS "STL",
        s.blk AS "BLK",
        s.fga AS "FGA", s.fgm AS "FGM", s.fg3m AS "FG3M",
        s.fta AS "FTA", s.tov AS "TOV",
        s.games_played AS "Jogos"
    FROM fact_player_stats s
    JOIN dim_players p ON s.player_id = p.id
    JOIN dim_teams t ON s.team_id = t.id
    WHERE s.games_played > 0
    """
    with engine.connect() as conn:
        df = pd.read_sql(text(query), conn)
    return df

def calculate_metrics(df):
    df.fillna(0, inplace=True)
    
    df["PPG"] = (df["PTS"] / df["Jogos"]).round(1)
    df["RPG"] = (df["REB"] / df["Jogos"]).round(1)
    df["APG"] = (df["AST"] / df["Jogos"]).round(1)
    df["SPG"] = (df["STL"] / df["Jogos"]).round(1)
    df["BPG"] = (df["BLK"] / df["Jogos"]).round(1)

    df["TS%"] = df.apply(lambda x: x["PTS"] / (2 * (x["FGA"] + 0.44 * x["FTA"])) if (x["FGA"] + 0.44 * x["FTA"]) > 0 else 0, axis=1)
    df["eFG%"] = df.apply(lambda x: (x["FGM"] + 0.5 * x["FG3M"]) / x["FGA"] if x["FGA"] > 0 else 0, axis=1)
    df["AST/TO"] = df.apply(lambda x: x["AST"] / x["TOV"] if x["TOV"] > 0 else x["AST"], axis=1)

    df["TS%_Show"] = (df["TS%"] * 100).round(1).astype(str) + "%"
    df["eFG%_Show"] = (df["eFG%"] * 100).round(1).astype(str) + "%"
    
    return df

try:
    df_raw = load_data()
    if df_raw.empty:
        st.warning("Banco de dados vazio. Aguarde o pipeline.")
        st.stop()

    df = calculate_metrics(df_raw)

    with st.sidebar:
        st.header("Filtros")
        times = ["Todos"] + sorted(df["Time"].unique().tolist())
        sel_time = st.selectbox("Time:", times)
        posicoes = ["Todas"] + sorted(df["Posição"].unique().tolist())
        sel_pos = st.selectbox("Posição:", posicoes)
        st.divider()
        min_jogos = st.slider("Mínimo de Jogos:", 1, int(df["Jogos"].max()), 1)

    df_filtro = df[df["Jogos"] >= min_jogos].copy()
    if sel_time != "Todos": df_filtro = df_filtro[df_filtro["Time"] == sel_time]
    if sel_pos != "Todas": df_filtro = df_filtro[df_filtro["Posição"] == sel_pos]

    st.metric("Jogadores", len(df_filtro))
    st.divider()

    # Abas
    aba1, aba2 = st.tabs(["Estatísticas Tradicionais", "Estatísticas Avançadas"])

    with aba1:
        st.subheader("Desempenho Geral (Ataque & Defesa)")
        
        tipo = st.radio("Visualização:", ["Médias por Jogo", "Totais da Temporada"], horizontal=True)

        if tipo == "Médias por Jogo":
            cols = ["Jogador", "Time", "Posição", "Jogos", "PPG", "RPG", "APG", "SPG", "BPG"]
            ordem = "PPG"
            
            c1, c2, c3, c4, c5 = st.columns(5)
            if not df_filtro.empty:
                c1.metric("Cestinha", df_filtro.loc[df_filtro["PPG"].idxmax()]["Jogador"], f"{df_filtro['PPG'].max()} ppg")
                c2.metric("Assistências", df_filtro.loc[df_filtro["APG"].idxmax()]["Jogador"], f"{df_filtro['APG'].max()} apg")
                c3.metric("Rebotes", df_filtro.loc[df_filtro["RPG"].idxmax()]["Jogador"], f"{df_filtro['RPG'].max()} rpg")
                c4.metric("Roubos", df_filtro.loc[df_filtro["SPG"].idxmax()]["Jogador"], f"{df_filtro['SPG'].max()} spg")
                c5.metric("Tocos", df_filtro.loc[df_filtro["BPG"].idxmax()]["Jogador"], f"{df_filtro['BPG'].max()} bpg")

        else:
            cols = ["Jogador", "Time", "Posição", "Jogos", "PTS", "REB", "AST", "STL", "BLK"]
            ordem = "PTS"
            
            c1, c2, c3, c4, c5 = st.columns(5)
            if not df_filtro.empty:
                c1.metric("Pontos", df_filtro.loc[df_filtro["PTS"].idxmax()]["Jogador"], int(df_filtro['PTS'].max()))
                c2.metric("Assists", df_filtro.loc[df_filtro["AST"].idxmax()]["Jogador"], int(df_filtro['AST'].max()))
                c3.metric("Rebotes", df_filtro.loc[df_filtro["REB"].idxmax()]["Jogador"], int(df_filtro['REB'].max()))
                c4.metric("Roubos", df_filtro.loc[df_filtro["STL"].idxmax()]["Jogador"], int(df_filtro['STL'].max()))
                c5.metric("Tocos", df_filtro.loc[df_filtro["BLK"].idxmax()]["Jogador"], int(df_filtro['BLK'].max()))

        st.dataframe(df_filtro[cols].sort_values(ordem, ascending=False), use_container_width=True, hide_index=True)

    with aba2:
        st.subheader("Eficiência Avançada")
        scatter = alt.Chart(df_filtro).mark_circle(size=90).encode(
            x=alt.X('PPG', title='Pontos por Jogo'),
            y=alt.Y('TS%', title='True Shooting %', scale=alt.Scale(domain=[0.3, 0.8])),
            color='Posição',
            tooltip=['Jogador', 'Time', 'PPG', 'TS%', 'AST/TO']
        ).interactive()
        st.altair_chart(scatter, use_container_width=True)
        
        st.dataframe(
            df_filtro[["Jogador", "Time", "Jogos", "TS%", "eFG%", "AST/TO", "PPG"]].sort_values("PPG", ascending=False),
            use_container_width=True, hide_index=True
        )

except Exception as e:
    st.error(f"Erro no sistema: {e}")
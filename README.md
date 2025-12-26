# 🏀 NBA Analytics Platform | Data Engineering & Analytics (2025–26)

> Uma solução completa de Engenharia de Dados e Visualização para análise de performance da NBA.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Local-336791)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Sobre o Projeto

Este projeto é uma plataforma *end-to-end* (ponta a ponta) que extrai dados reais da API oficial da NBA, processa essas informações em um banco de dados relacional SQL e disponibiliza um Dashboard interativo para *scouting* e análise de jogadores.

O objetivo foi simular um ambiente real de **Engenharia de Dados**, focando na construção de um **Pipeline ETL robusto**, persistência histórica e entrega de **insights acionáveis** através de visualização de dados.

As análises são realizadas no **nível de jogador por temporada regular**.

---

## 🚀 Funcionalidades Principais

* **Pipeline ETL Automatizado:** Scripts em Python para extração de dados de Times, Jogadores e Estatísticas (Pontos, Rebotes, Assistências, Roubos e Tocos).
* **Banco de Dados Relacional:** Modelagem com **SQLAlchemy** e **PostgreSQL**, garantindo integridade e histórico dos dados.
* **Persistência Histórica:** Estrutura preparada para múltiplas temporadas.
* **Dashboard Interativo:** Aplicação Web construída com **Streamlit** e **Altair**.
* **Análise Dinâmica:**
  * Alternância entre *Médias por Jogo* e *Totais da Temporada*.
  * Gráficos de Dispersão para avaliar Eficiência (Saldo +/-) vs Volume de Pontuação.
  * Filtros avançados por Time e Posição.

---

## 🛠️ Stack Tecnológica

* **Linguagem:** Python
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy
* **API:** `nba_api` (Wrapper oficial)
* **Data Visualization:** Streamlit, Altair, Pandas
* **Versionamento:** Git / GitHub

---

## 📂 Estrutura do Projeto

```text
nba-analytics-platform/
├── src/
│   ├── dashboard/       # Front-end (Streamlit)
│   │   └── app.py
│   ├── etl/             # Extração, transformação e enriquecimento
│   │   ├── extract_data.py
│   │   ├── extract_stats.py
│   │   ├── enrich_teams.py
│   │   └── enrich_players.py
│   ├── database.py      # Conexão com o banco
│   ├── models.py        # Modelagem das tabelas
│   └── pipeline.py      # Orquestrador do ETL
├── assets/              # Screenshots do Dashboard
├── .gitignore
├── requirements.txt
└── README.md
```
# ⚙️ Como Rodar Localmente
  **Pré-requisitos**
* **Python 3.10+**
* **PostgreSQL instalado e em execução**

## 1. Clone o repositório
```bash
git clone https://github.com/guilhermedopp/nba-analytics-platform.git
cd nba-analytics-platform
```
## 2. Ative o ambiente virtual
```bash
python -m venv venv
```
## Windows
```bash
.\venv\Scripts\activate
```
## Linux / Mac
```bash
source venv/bin/activate
```
## 3. Instale as Dependências
```bash
pip install -r requirements.txt
```
## 4. Acesse o Banco de Dados
Configure a string de conexão no arquivo src/database.py ou via variáveis de ambiente.

## 5. Execute o ETL
```bash
python src/pipeline.py
```
## 6. Inicie o Dashboard
```bash
streamlit run src/dashboard/app.py
```
## 🤝 Contribuição
Pull Requests são bem-vindos.

-----

*Projeto desenvolvido por Guilherme Pontes*

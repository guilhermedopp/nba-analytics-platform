# 🏀 NBA Analytics Platform | Data Engineering & Analytics (2025–26)

> Uma solução completa de Engenharia de Dados e Visualização para análise de performance da NBA, containerizada com Docker.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Container-2496ED)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📋 Sobre o Projeto

Este projeto é uma plataforma *end-to-end* (ponta a ponta) que extrai dados reais da API oficial da NBA, processa essas informações em um banco de dados SQL isolado e disponibiliza um Dashboard interativo para *scouting* e análise de jogadores.

O objetivo foi simular um ambiente real de **Engenharia de Dados**, focando na construção de um **Pipeline ETL robusto**, arquitetura em microsserviços (Docker) e entrega de **insights acionáveis** (Moneyball).

---

## 🚀 Funcionalidades Principais

* **Arquitetura Containerizada:** Uso de **Docker e Docker Compose** para orquestrar a aplicação e o banco de dados em ambiente isolado.
* **Pipeline ETL Automatizado:** Scripts em Python para extração e tratamento de dados de Times, Jogadores e Estatísticas.
* **Métricas Avançadas (Moneyball):**
  * Cálculo automático de **True Shooting % (TS%)**, **Effective FG% (eFG%)** e **AST/TO Ratio**.
* **Dashboard Interativo (Streamlit):**
  * **Sistema de Abas:** Separação entre "Stats Tradicionais" e "Moneyball".
  * **Toggle de Visualização:** Alternância dinâmica entre *Médias por Jogo* e *Totais da Temporada*.
  * **Filtros Avançados:** Por Time, Posição e Mínimo de Jogos.
  * **Cards de Destaque:** Top performadores em Pontos, Rebotes, Assistências, Roubos e Tocos.

---

## 🛠️ Stack Tecnológica

* **Infraestrutura:** Docker & Docker Compose
* **Linguagem:** Python 3.11
* **Banco de Dados:** PostgreSQL 15 (Container)
* **ORM:** SQLAlchemy
* **API:** `nba_api` (Wrapper oficial)
* **Data Visualization:** Streamlit, Altair, Pandas

---

## 📂 Estrutura do Projeto

```text
nba-analytics-platform/
├── src/
│   ├── dashboard/       # Front-end (Streamlit)
│   │   └── app.py
│   ├── etl/             # Scripts de Extração e Tratamento
│   │   ├── enrich_players.py
│   │   └── extract_stats.py
│   ├── database.py      # Conexão com o Banco
│   ├── models.py        # Esquema do Banco (ORM)
│   └── pipeline.py      # Orquestrador do ETL
├── .gitignore
├── docker-compose.yml   # Orquestração dos Containers
├── Dockerfile           # Configuração da Imagem Python
├── requirements.txt
└── README.md
```
# ⚙️ Como Rodar Localmente
  ## Pré-requisitos
* **Docker e Docker Compose Instalados**

## 1. Clone o repositório
```bash
git clone https://github.com/guilhermedopp/nba-analytics-platform.git
cd nba-analytics-platform
```
## 2. Suba o Ambiente
```bash
docker-compose up --build
```
## 3. Acesse o Dashboard
```bash
docker-compose up --build
```

# Comandos Úteis (Docker)
  ## Caso precise rodar scripts manualmente dentro do container:
 
## Rodar o Pipeline ETL completo (Reset de dados):
Configure a string de conexão no arquivo src/database.py ou via variáveis de ambiente.
```bash
docker exec -it nba_app python src/pipeline.py
```

## Atualizar apenas as Estatísticas:
```bash
docker exec -it nba_app python src/etl/extract_stats.py
```

## Parar o projeto: Pressione Ctrl + C no terminal ou rode:
```bash
docker-compose down
```
## 🤝 Contribuição
Pull Requests são bem-vindos.

-----

*Projeto desenvolvido por Guilherme Pontes*
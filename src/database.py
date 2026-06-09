import sqlite3
import os

DB_PATH = "data/career_tracker.db"


def criar_banco():
    os.makedirs("data", exist_ok=True)

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS carreiras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome_carreira TEXT NOT NULL,
        modo TEXT NOT NULL,
        time_atual TEXT,
        selecao_atual TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS partidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        carreira_id INTEGER,
        meu_time_na_partida TEXT,
        tipo_time TEXT,
        competicao TEXT,
        time_casa TEXT NOT NULL,
        time_fora TEXT NOT NULL,
        gols_casa INTEGER NOT NULL,
        gols_fora INTEGER NOT NULL,
        data_partida TEXT,
        FOREIGN KEY (carreira_id) REFERENCES carreiras(id)
    )
    """)

    conexao.commit()
    conexao.close()


def adicionar_coluna(nome_coluna, tipo):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    try:
        cursor.execute(f"ALTER TABLE partidas ADD COLUMN {nome_coluna} {tipo}")
    except sqlite3.OperationalError:
        pass

    conexao.commit()
    conexao.close()


def atualizar_banco():
    criar_banco()

    adicionar_coluna("carreira_id", "INTEGER")
    adicionar_coluna("meu_time_na_partida", "TEXT")
    adicionar_coluna("tipo_time", "TEXT")


if __name__ == "__main__":
    atualizar_banco()
    print("Banco atualizado com suporte a carreiras, clubes e seleções!")
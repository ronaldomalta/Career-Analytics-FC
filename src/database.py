import sqlite3
import os

DB_PATH = "data/career_tracker.db"

def criar_banco():
    os.makedirs("data", exist_ok=True)

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS configuracao (
        id INTEGER PRIMARY KEY,
        meu_time TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS partidas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        competicao TEXT,
        time_casa TEXT NOT NULL,
        time_fora TEXT NOT NULL,
        gols_casa INTEGER NOT NULL,
        gols_fora INTEGER NOT NULL,
        data_partida TEXT
    )
    """)

    conexao.commit()
    conexao.close()

    print("Banco criado com sucesso!")

if __name__ == "__main__":
    criar_banco()
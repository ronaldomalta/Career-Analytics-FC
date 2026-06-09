import sqlite3

DB_PATH = "data/career_tracker.db"

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()

cursor.execute("SELECT * FROM partidas")

partidas = cursor.fetchall()

for partida in partidas:
    print(partida)

conexao.close()
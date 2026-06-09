import sqlite3

DB_PATH = "data/career_tracker.db"

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()

cursor.execute("SELECT * FROM carreiras")

for carreira in cursor.fetchall():
    print(carreira)

conexao.close()
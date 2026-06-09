import sqlite3

DB_PATH = "data/career_tracker.db"

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()

print("TABELA CARREIRAS:")
cursor.execute("PRAGMA table_info(carreiras)")
for coluna in cursor.fetchall():
    print(coluna)

print("\nTABELA PARTIDAS:")
cursor.execute("PRAGMA table_info(partidas)")
for coluna in cursor.fetchall():
    print(coluna)

conexao.close()
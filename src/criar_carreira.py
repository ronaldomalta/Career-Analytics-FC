import sqlite3
from carreira_ativa import salvar_carreira_ativa

DB_PATH = "data/career_tracker.db"

nome = input("Nome da carreira: ").strip()
modo = "treinador"
time_atual = input("Time inicial: ").strip().lower()
selecao_atual = input("Seleção atual (opcional): ").strip().lower()

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()

cursor.execute("""
INSERT INTO carreiras (
    nome_carreira,
    modo,
    time_atual,
    selecao_atual
)
VALUES (?, ?, ?, ?)
""", (nome, modo, time_atual, selecao_atual))

carreira_id = cursor.lastrowid

conexao.commit()
conexao.close()

salvar_carreira_ativa(carreira_id)

print(f"Carreira criada e ativada com sucesso! ID: {carreira_id}")
import sqlite3
from carreira_ativa import salvar_carreira_ativa

DB_PATH = "data/career_tracker.db"

nome = input("Nome da carreira: ").strip()
modo = "treinador"
time_atual = input("Time inicial: ").strip().lower()
selecao_atual = input("Seleção atual (opcional): ").strip().lower()
data_inicio = input("Data de início AAAA-MM-DD: ").strip()

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

cursor.execute("""
INSERT INTO historico_carreira (
    carreira_id,
    tipo,
    nome_time,
    data_inicio,
    data_fim
)
VALUES (?, ?, ?, ?, ?)
""", (
    carreira_id,
    "clube",
    time_atual,
    data_inicio,
    None
))

if selecao_atual:
    cursor.execute("""
    INSERT INTO historico_carreira (
        carreira_id,
        tipo,
        nome_time,
        data_inicio,
        data_fim
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        carreira_id,
        "selecao",
        selecao_atual,
        data_inicio,
        None
    ))

conexao.commit()
conexao.close()

salvar_carreira_ativa(carreira_id)

print(f"Carreira criada e ativada com sucesso! ID: {carreira_id}")
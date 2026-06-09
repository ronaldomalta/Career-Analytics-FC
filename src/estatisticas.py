import sqlite3

DB_PATH = "data/career_tracker.db"

meu_time = "sport"
adversario = input("Adversário: ").strip().lower()

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()

cursor.execute("""
SELECT *
FROM partidas
WHERE time_casa = ? OR time_fora = ?
""", (meu_time, meu_time))

partidas = cursor.fetchall()

jogos = 0
vitorias = 0
empates = 0
derrotas = 0
gols_marcados = 0
gols_sofridos = 0

for partida in partidas:
    _, _, casa, fora, gols_casa, gols_fora, _ = partida

    if adversario not in [casa, fora]:
        continue

    jogos += 1

    if casa == meu_time:
        meus_gols = gols_casa
        gols_adv = gols_fora
    else:
        meus_gols = gols_fora
        gols_adv = gols_casa

    gols_marcados += meus_gols
    gols_sofridos += gols_adv

    if meus_gols > gols_adv:
        vitorias += 1
    elif meus_gols < gols_adv:
        derrotas += 1
    else:
        empates += 1

conexao.close()

print("\n===== ESTATÍSTICAS =====")
print(f"Adversário: {adversario.title()}")
print(f"Jogos: {jogos}")
print(f"Vitórias: {vitorias}")
print(f"Empates: {empates}")
print(f"Derrotas: {derrotas}")
print(f"Gols marcados: {gols_marcados}")
print(f"Gols sofridos: {gols_sofridos}")
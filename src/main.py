import sqlite3

DB_PATH = "data/career_tracker.db"
MEU_TIME = "sport"


def cadastrar_partida():
    competicao = input("Competição: ").strip()
    time_casa = input("Time da casa: ").strip().lower()
    time_fora = input("Time de fora: ").strip().lower()
    gols_casa = int(input("Gols do time da casa: "))
    gols_fora = int(input("Gols do time de fora: "))
    data_partida = input("Data da partida: ").strip()

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    INSERT INTO partidas (
        competicao,
        time_casa,
        time_fora,
        gols_casa,
        gols_fora,
        data_partida
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        competicao,
        time_casa,
        time_fora,
        gols_casa,
        gols_fora,
        data_partida
    ))

    conexao.commit()
    conexao.close()

    print("\nPartida cadastrada com sucesso!")


def listar_partidas():
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM partidas")
    partidas = cursor.fetchall()

    print("\n===== PARTIDAS CADASTRADAS =====")

    if not partidas:
        print("Nenhuma partida cadastrada.")
    else:
        for partida in partidas:
            id_partida, competicao, casa, fora, gols_casa, gols_fora, data = partida
            print(f"{id_partida} - {competicao}: {casa.title()} {gols_casa} x {gols_fora} {fora.title()} | {data}")

    conexao.close()


def estatisticas_adversario():
    adversario = input("Adversário: ").strip().lower()

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT *
    FROM partidas
    WHERE time_casa = ? OR time_fora = ?
    """, (MEU_TIME, MEU_TIME))

    partidas = cursor.fetchall()
    conexao.close()

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

        if casa == MEU_TIME:
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

    print("\n===== ESTATÍSTICAS =====")
    print(f"Adversário: {adversario.title()}")
    print(f"Jogos: {jogos}")
    print(f"Vitórias: {vitorias}")
    print(f"Empates: {empates}")
    print(f"Derrotas: {derrotas}")
    print(f"Gols marcados: {gols_marcados}")
    print(f"Gols sofridos: {gols_sofridos}")


def menu():
    while True:
        print("\n===== CAREER ANALYTICS FC =====")
        print("1 - Cadastrar partida")
        print("2 - Listar partidas")
        print("3 - Estatísticas por adversário")
        print("4 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_partida()
        elif opcao == "2":
            listar_partidas()
        elif opcao == "3":
            estatisticas_adversario()
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
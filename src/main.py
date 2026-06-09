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
    WHERE (time_casa = ? OR time_fora = ?)
    A  ND (time_casa = ? OR time_fora = ?)
    ORDER BY data_partida ASC
    """, (MEU_TIME, MEU_TIME, adversario, adversario))
    partidas = cursor.fetchall()
    conexao.close()

    if not partidas:
        print(f"\nNenhuma partida encontrada contra {adversario.title()}.")
        return

    jogos = 0
    vitorias = 0
    empates = 0
    derrotas = 0
    gols_marcados = 0
    gols_sofridos = 0

    melhor_vitoria = None
    melhor_saldo = None

    pior_derrota = None
    pior_saldo = None

    sequencia_vitorias_atual = 0
    maior_sequencia_vitorias = 0

    sequencia_invicta_atual = 0
    maior_sequencia_invicta = 0

    ultimo_confronto = partidas[-1]

    for partida in partidas:
        _, _, casa, fora, gols_casa, gols_fora, _ = partida

        jogos += 1

        if casa == MEU_TIME:
            meus_gols = gols_casa
            gols_adv = gols_fora
        else:
            meus_gols = gols_fora
            gols_adv = gols_casa

        gols_marcados += meus_gols
        gols_sofridos += gols_adv

        saldo = meus_gols - gols_adv

        if meus_gols > gols_adv:
            vitorias += 1

            sequencia_vitorias_atual += 1
            sequencia_invicta_atual += 1

            if sequencia_vitorias_atual > maior_sequencia_vitorias:
                maior_sequencia_vitorias = sequencia_vitorias_atual

            if sequencia_invicta_atual > maior_sequencia_invicta:
                maior_sequencia_invicta = sequencia_invicta_atual

            if melhor_saldo is None or saldo > melhor_saldo:
                melhor_saldo = saldo
                melhor_vitoria = partida

        elif meus_gols < gols_adv:
            derrotas += 1

            sequencia_vitorias_atual = 0
            sequencia_invicta_atual = 0

            if pior_saldo is None or saldo < pior_saldo:
                pior_saldo = saldo
                pior_derrota = partida

        else:
            empates += 1

            sequencia_vitorias_atual = 0
            sequencia_invicta_atual += 1

            if sequencia_invicta_atual > maior_sequencia_invicta:
                maior_sequencia_invicta = sequencia_invicta_atual

    aproveitamento = ((vitorias * 3 + empates) / (jogos * 3)) * 100

    print("\n===== ESTATÍSTICAS DO CONFRONTO =====")
    print(f"Adversário: {adversario.title()}")
    print(f"Jogos: {jogos}")
    print(f"Vitórias: {vitorias}")
    print(f"Empates: {empates}")
    print(f"Derrotas: {derrotas}")
    print(f"Gols marcados: {gols_marcados}")
    print(f"Gols sofridos: {gols_sofridos}")
    print(f"Aproveitamento: {aproveitamento:.1f}%")
    print(f"Maior sequência de vitórias: {maior_sequencia_vitorias}")
    print(f"Maior sequência invicta: {maior_sequencia_invicta}")

    print("\n----- RESUMO DO CONFRONTO -----")

    if melhor_vitoria:
        _, competicao, casa, fora, gols_casa, gols_fora, data = melhor_vitoria
        print("\nMelhor vitória:")
        print(f"{casa.title()} {gols_casa} x {gols_fora} {fora.title()}")
        print(f"{competicao} | {data}")
    else:
        print("\nMelhor vitória:")
        print("Nenhuma vitória contra esse adversário.")

    if pior_derrota:
        _, competicao, casa, fora, gols_casa, gols_fora, data = pior_derrota
        print("\nPior derrota:")
        print(f"{casa.title()} {gols_casa} x {gols_fora} {fora.title()}")
        print(f"{competicao} | {data}")
    else:
        print("\nPior derrota:")
        print("Nenhuma derrota contra esse adversário.")

    _, competicao, casa, fora, gols_casa, gols_fora, data = ultimo_confronto
    print("\nÚltimo confronto:")
    print(f"{casa.title()} {gols_casa} x {gols_fora} {fora.title()}")
    print(f"{competicao} | {data}")

    print("\n----- HISTÓRICO DO CONFRONTO -----")

    for partida in partidas:
        _, competicao, casa, fora, gols_casa, gols_fora, data = partida

        print(f"\n{data} | {competicao}")
        print(f"{casa.title()} {gols_casa} x {gols_fora} {fora.title()}")

    estatisticas_competicoes = {}

    for partida in partidas:
        _, competicao, casa, fora, gols_casa, gols_fora, _ = partida

        if competicao not in estatisticas_competicoes:
            estatisticas_competicoes[competicao] = {
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_marcados": 0,
                "gols_sofridos": 0
            }

        if casa == MEU_TIME:
            meus_gols = gols_casa
            gols_adv = gols_fora
        else:
            meus_gols = gols_fora
            gols_adv = gols_casa

        estatisticas_competicoes[competicao]["jogos"] += 1
        estatisticas_competicoes[competicao]["gols_marcados"] += meus_gols
        estatisticas_competicoes[competicao]["gols_sofridos"] += gols_adv

        if meus_gols > gols_adv:
            estatisticas_competicoes[competicao]["vitorias"] += 1
        elif meus_gols < gols_adv:
            estatisticas_competicoes[competicao]["derrotas"] += 1
        else:
            estatisticas_competicoes[competicao]["empates"] += 1

    print("\n----- ESTATÍSTICAS POR COMPETIÇÃO -----")

    for competicao, dados in estatisticas_competicoes.items():
        print(f"\n{competicao}")
        print(f"Jogos: {dados['jogos']}")
        print(f"Vitórias: {dados['vitorias']}")
        print(f"Empates: {dados['empates']}")
        print(f"Derrotas: {dados['derrotas']}")
        print(f"Gols marcados: {dados['gols_marcados']}")
        print(f"Gols sofridos: {dados['gols_sofridos']}")

def estatisticas_gerais():
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

    aproveitamento = 0

    if jogos > 0:
        aproveitamento = ((vitorias * 3) / (jogos * 3)) * 100

    print("\n===== ESTATÍSTICAS GERAIS =====")
    print(f"Time: {MEU_TIME.title()}")
    print(f"Jogos: {jogos}")
    print(f"Vitórias: {vitorias}")
    print(f"Empates: {empates}")
    print(f"Derrotas: {derrotas}")
    print(f"Gols Marcados: {gols_marcados}")
    print(f"Gols Sofridos: {gols_sofridos}")
    print(f"Aproveitamento: {aproveitamento:.1f}%")


def menu():
    while True:
        print("\n===== CAREER ANALYTICS FC =====")
        print("1 - Cadastrar partida")
        print("2 - Listar partidas")
        print("3 - Estatísticas por adversário")
        print("4 - Estatísticas Gerais")
        print("5 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_partida()
        elif opcao == "2":
            listar_partidas()
        elif opcao == "3":
            estatisticas_adversario()
        elif opcao == "4":
            estatisticas_gerais()    
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
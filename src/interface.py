import customtkinter as ctk
import sqlite3

DB_PATH = "data/career_tracker.db"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("FC Career Tracker")
app.geometry("800x500")


def limpar_tela():
    for widget in app.winfo_children():
        widget.destroy()


def tela_inicial():
    limpar_tela()

    titulo = ctk.CTkLabel(app, text="FC Career Tracker", font=("Arial", 28, "bold"))
    titulo.pack(pady=30)

    subtitulo = ctk.CTkLabel(app, text="Sistema de análise para Modo Carreira", font=("Arial", 16))
    subtitulo.pack(pady=10)

    ctk.CTkButton(app, text="Cadastrar Partida", command=tela_cadastrar_partida).pack(pady=10)
    ctk.CTkButton(app, text="Estatísticas Gerais", command=tela_estatisticas_gerais).pack(pady=10)
    ctk.CTkButton(app, text="Confronto Direto", command=tela_confronto_direto).pack(pady=10)
    ctk.CTkButton(app, text="Listar Partidas", command=tela_listar_partidas).pack(pady=10)


def botao_voltar():
    ctk.CTkButton(app, text="Voltar", command=tela_inicial).pack(pady=20)


def tela_cadastrar_partida():
    limpar_tela()
    ctk.CTkLabel(app, text="Cadastrar Partida", font=("Arial", 24, "bold")).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui ficará o formulário para cadastrar partidas.").pack(pady=10)
    botao_voltar()


def tela_estatisticas_gerais():
    limpar_tela()

    ctk.CTkLabel(app, text="Estatísticas Gerais", font=("Arial", 24, "bold")).pack(pady=20)

    MEU_TIME = "sport"

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
        aproveitamento = ((vitorias * 3 + empates) / (jogos * 3)) * 100

    frame = ctk.CTkFrame(app, width=500)
    frame.pack(pady=20, padx=20)

    ctk.CTkLabel(frame, text=f"Time: {MEU_TIME.title()}", font=("Arial", 18, "bold")).pack(pady=10)

    ctk.CTkLabel(frame, text=f"Jogos: {jogos}").pack(pady=4)
    ctk.CTkLabel(frame, text=f"Vitórias: {vitorias}").pack(pady=4)
    ctk.CTkLabel(frame, text=f"Empates: {empates}").pack(pady=4)
    ctk.CTkLabel(frame, text=f"Derrotas: {derrotas}").pack(pady=4)
    ctk.CTkLabel(frame, text=f"Gols Marcados: {gols_marcados}").pack(pady=4)
    ctk.CTkLabel(frame, text=f"Gols Sofridos: {gols_sofridos}").pack(pady=4)
    ctk.CTkLabel(frame, text=f"Aproveitamento: {aproveitamento:.1f}%").pack(pady=10)

    botao_voltar()


def tela_confronto_direto():
    limpar_tela()
    ctk.CTkLabel(app, text="Confronto Direto", font=("Arial", 24, "bold")).pack(pady=30)
    ctk.CTkLabel(app, text="Aqui será possível buscar estatísticas por adversário.").pack(pady=10)
    botao_voltar()


def tela_listar_partidas():
    limpar_tela()

    ctk.CTkLabel(app, text="Partidas Cadastradas", font=("Arial", 24, "bold")).pack(pady=20)

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, competicao, time_casa, time_fora, gols_casa, gols_fora, data_partida
    FROM partidas
    ORDER BY data_partida DESC
    """)

    partidas = cursor.fetchall()
    conexao.close()

    if not partidas:
        ctk.CTkLabel(app, text="Nenhuma partida cadastrada.").pack(pady=10)
    else:
        frame = ctk.CTkScrollableFrame(app, width=700, height=300)
        frame.pack(pady=10)

        for partida in partidas:
            id_partida, competicao, casa, fora, gols_casa, gols_fora, data = partida

            texto = f"{id_partida} - {data} | {competicao} | {casa.title()} {gols_casa} x {gols_fora} {fora.title()}"

            ctk.CTkLabel(
                frame,
                text=texto,
                anchor="w"
            ).pack(fill="x", padx=10, pady=5)

    botao_voltar()


tela_inicial()
app.mainloop()
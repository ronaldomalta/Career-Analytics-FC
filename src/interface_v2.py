import customtkinter as ctk
import sqlite3
from carreira_ativa import carregar_carreira_ativa

DB_PATH = "data/career_tracker.db"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("FC Career Tracker")
app.geometry("1100x650")


def conectar():
    return sqlite3.connect(DB_PATH)


def limpar_conteudo():
    for widget in conteudo.winfo_children():
        widget.destroy()


def obter_carreira_ativa():
    carreira_id = carregar_carreira_ativa()

    if carreira_id is None:
        return None

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, nome_carreira, modo, time_atual, selecao_atual
    FROM carreiras
    WHERE id = ?
    """, (carreira_id,))

    carreira = cursor.fetchone()
    conexao.close()

    if carreira is None:
        return None

    return {
        "id": carreira[0],
        "nome": carreira[1],
        "modo": carreira[2],
        "time_atual": carreira[3],
        "selecao_atual": carreira[4]
    }


def card(parent, titulo, valor):
    frame = ctk.CTkFrame(parent, corner_radius=12)
    frame.pack(side="left", expand=True, fill="both", padx=8, pady=8)

    ctk.CTkLabel(frame, text=titulo, font=("Arial", 13)).pack(pady=(15, 5))
    ctk.CTkLabel(frame, text=valor, font=("Arial", 26, "bold")).pack(pady=(0, 15))

def calcular_resultado_partida(meu_time, time_casa, time_fora, gols_casa, gols_fora):
    if meu_time == time_casa:
        return gols_casa, gols_fora

    if meu_time == time_fora:
        return gols_fora, gols_casa

    return 0, 0



def tela_dashboard():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text="Dashboard",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(
            conteudo,
            text="Nenhuma carreira ativa selecionada.",
            font=("Arial", 16)
        ).pack(pady=20)
        return

    selecao = carreira["selecao_atual"].title() if carreira["selecao_atual"] else "Nenhuma"

    ctk.CTkLabel(
        conteudo,
        text=f"Carreira ativa: {carreira['nome']} | Clube: {carreira['time_atual'].title()} | Seleção: {selecao}",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT meu_time_na_partida, tipo_time, competicao, time_casa, time_fora, gols_casa, gols_fora, data_partida
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY data_partida ASC
    """, (carreira["id"],))

    partidas = cursor.fetchall()

    cursor.execute("""
    SELECT COUNT(*)
    FROM titulos
    WHERE carreira_id = ?
    """, (carreira["id"],))

    total_titulos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT time_casa, gols_casa, gols_fora, time_fora, competicao, data_partida
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY id DESC
    LIMIT 5
    """, (carreira["id"],))

    ultimas_partidas = cursor.fetchall()

    conexao.close()

    jogos = vitorias = empates = derrotas = 0
    gols_marcados = gols_sofridos = 0

    for partida in partidas:
        meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = partida

        if not meu_time or meu_time not in [casa, fora]:
            continue

        jogos += 1

        meus_gols, gols_adv = calcular_resultado_partida(
            meu_time,
            casa,
            fora,
            gols_casa,
            gols_fora
        )

        gols_marcados += meus_gols
        gols_sofridos += gols_adv

        if meus_gols > gols_adv:
            vitorias += 1
        elif meus_gols < gols_adv:
            derrotas += 1
        else:
            empates += 1

    aproveitamento = ((vitorias * 3 + empates) / (jogos * 3)) * 100 if jogos > 0 else 0
    saldo = gols_marcados - gols_sofridos

    frame_cards_1 = ctk.CTkFrame(conteudo, fg_color="transparent")
    frame_cards_1.pack(fill="x", padx=18, pady=(5, 0))

    card(frame_cards_1, "Jogos", str(jogos))
    card(frame_cards_1, "Vitórias", str(vitorias))
    card(frame_cards_1, "Empates", str(empates))
    card(frame_cards_1, "Derrotas", str(derrotas))

    frame_cards_2 = ctk.CTkFrame(conteudo, fg_color="transparent")
    frame_cards_2.pack(fill="x", padx=18, pady=(0, 5))

    card(frame_cards_2, "Gols Marcados", str(gols_marcados))
    card(frame_cards_2, "Gols Sofridos", str(gols_sofridos))
    card(frame_cards_2, "Saldo", str(saldo))
    card(frame_cards_2, "Títulos", str(total_titulos))

    frame_baixo = ctk.CTkFrame(conteudo, corner_radius=12)
    frame_baixo.pack(fill="both", expand=True, padx=25, pady=15)

    frame_info = ctk.CTkFrame(frame_baixo)
    frame_info.pack(fill="both", expand=True, padx=15, pady=15)

    ctk.CTkLabel(
    frame_info,
    text=f"Aproveitamento geral: {aproveitamento:.1f}%",
    font=("Arial", 18, "bold")
    ).pack(pady=(10, 15))

    ctk.CTkLabel(
    frame_info,
    text="Últimas Partidas",
    font=("Arial", 18, "bold")
).pack(pady=(10, 15))

    if ultimas_partidas:

        for casa, gols_casa, gols_fora, fora, competicao, data in ultimas_partidas:

            texto = (
            f"{data} | {competicao}\n"
            f"{casa.title()} {gols_casa} x {gols_fora} {fora.title()}"
        )

        card_partida = ctk.CTkFrame(frame_info)
        card_partida.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(
            card_partida,
            text=texto,
            justify="left",
            font=("Arial", 14)
        ).pack(anchor="w", padx=15, pady=10)

    else:
        ctk.CTkLabel(
        frame_info,
        text="Nenhuma partida cadastrada."
    ).pack(pady=10)



def tela_partidas():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text="Partidas",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(
            conteudo,
            text="Nenhuma carreira ativa selecionada.",
            font=("Arial", 16)
        ).pack(pady=20)
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT data_partida, competicao, time_casa, gols_casa, gols_fora, time_fora, tipo_time
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY id DESC
    """, (carreira["id"],))

    partidas = cursor.fetchall()
    conexao.close()

    ctk.CTkLabel(
        conteudo,
        text=f"Carreira ativa: {carreira['nome']}",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    frame_lista = ctk.CTkScrollableFrame(conteudo, width=850, height=500)
    frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

    cabecalho = ctk.CTkFrame(frame_lista)
    cabecalho.pack(fill="x", padx=5, pady=(5, 8))

    ctk.CTkLabel(cabecalho, text="Data", width=150, font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ctk.CTkLabel(cabecalho, text="Competição", width=180, font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ctk.CTkLabel(cabecalho, text="Casa", width=150, font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ctk.CTkLabel(cabecalho, text="Placar", width=90, font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ctk.CTkLabel(cabecalho, text="Fora", width=150, font=("Arial", 13, "bold")).pack(side="left", padx=5)
    ctk.CTkLabel(cabecalho, text="Tipo", width=100, font=("Arial", 13, "bold")).pack(side="left", padx=5)

    if not partidas:
        ctk.CTkLabel(
            frame_lista,
            text="Nenhuma partida cadastrada.",
            font=("Arial", 15)
        ).pack(pady=20)
        return

    for data, competicao, casa, gols_casa, gols_fora, fora, tipo_time in partidas:
        linha = ctk.CTkFrame(frame_lista)
        linha.pack(fill="x", padx=5, pady=4)

        placar = f"{gols_casa} x {gols_fora}"

        ctk.CTkLabel(linha, text=data, width=150).pack(side="left", padx=5)
        ctk.CTkLabel(linha, text=competicao, width=180).pack(side="left", padx=5)
        ctk.CTkLabel(linha, text=casa.title(), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(linha, text=placar, width=90, font=("Arial", 13, "bold")).pack(side="left", padx=5)
        ctk.CTkLabel(linha, text=fora.title(), width=150).pack(side="left", padx=5)
        ctk.CTkLabel(linha, text=tipo_time.title(), width=100).pack(side="left", padx=5)

def tela_em_breve(nome):
    limpar_conteudo()

    ctk.CTkLabel(conteudo, text=nome, font=("Arial", 28, "bold")).pack(anchor="w", padx=25, pady=20)
    ctk.CTkLabel(conteudo, text="Tela em construção na nova interface.").pack(pady=20)


# Layout principal
menu = ctk.CTkFrame(app, width=220, corner_radius=0)
menu.pack(side="left", fill="y")

conteudo = ctk.CTkFrame(app, corner_radius=0)
conteudo.pack(side="right", fill="both", expand=True)

ctk.CTkLabel(menu, text="FC Career\nTracker", font=("Arial", 22, "bold")).pack(pady=30)

ctk.CTkButton(menu, text="Dashboard", command=tela_dashboard).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Carreiras", command=lambda: tela_em_breve("Carreiras")).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Partidas", command=tela_partidas).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Estatísticas", command=lambda: tela_em_breve("Estatísticas")).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Histórico", command=lambda: tela_em_breve("Histórico da Carreira")).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Títulos", command=lambda: tela_em_breve("Títulos")).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="OCR / Captura", command=lambda: tela_em_breve("OCR / Captura")).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Configurações", command=lambda: tela_em_breve("Configurações")).pack(fill="x", padx=15, pady=6)

tela_dashboard()

app.mainloop()
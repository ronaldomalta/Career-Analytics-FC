import customtkinter as ctk
import sqlite3
import os
import pyautogui
from datetime import datetime
import shutil
import csv
import calendar

from carreira_ativa import carregar_carreira_ativa
from importar_partida import extrair_partida, salvar_partida
from carreira_ativa import carregar_carreira_ativa, salvar_carreira_ativa

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
    clube = carreira["time_atual"].title() if carreira["time_atual"] else "Nenhum"

    ctk.CTkLabel(
        conteudo,
        text=f"Carreira ativa: {carreira['nome']} | Clube: {clube} | Seleção: {selecao}",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT meu_time_na_partida, tipo_time, competicao, time_casa, time_fora, gols_casa, gols_fora, data_partida
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY id ASC
    """, (carreira["id"],))

    partidas = cursor.fetchall()

    cursor.execute("""
    SELECT COUNT(*)
    FROM titulos
    WHERE carreira_id = ?
    """, (carreira["id"],))

    total_titulos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT competicao, temporada
    FROM titulos
    WHERE carreira_id = ?
    ORDER BY id DESC
    LIMIT 1
    """, (carreira["id"],))

    ultimo_titulo = cursor.fetchone()

    cursor.execute("""
    SELECT id, time_casa, gols_casa, gols_fora, time_fora, competicao, data_partida
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY id DESC
    LIMIT 5
    """, (carreira["id"],))

    ultimas_partidas = cursor.fetchall()

    conexao.close()

    jogos = vitorias = empates = derrotas = 0
    gols_marcados = gols_sofridos = 0

    melhor_vitoria = None
    pior_derrota = None
    melhor_saldo = None
    pior_saldo = None

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

        saldo_partida = meus_gols - gols_adv

        if saldo_partida > 0 and (melhor_saldo is None or saldo_partida > melhor_saldo):
            melhor_saldo = saldo_partida
            melhor_vitoria = (casa, gols_casa, gols_fora, fora)

        if saldo_partida < 0 and (pior_saldo is None or saldo_partida < pior_saldo):
            pior_saldo = saldo_partida
            pior_derrota = (casa, gols_casa, gols_fora, fora)

        if meus_gols > gols_adv:
            vitorias += 1
        elif meus_gols < gols_adv:
            derrotas += 1
        else:
            empates += 1

    aproveitamento = ((vitorias * 3 + empates) / (jogos * 3)) * 100 if jogos > 0 else 0
    saldo = gols_marcados - gols_sofridos
    media_gols_marcados = gols_marcados / jogos if jogos > 0 else 0
    media_gols_sofridos = gols_sofridos / jogos if jogos > 0 else 0

    forma_recente = []
    partidas_validas = []

    for partida in partidas:
        meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = partida

        if not meu_time or meu_time not in [casa, fora]:
            continue

        meus_gols, gols_adv = calcular_resultado_partida(
            meu_time,
            casa,
            fora,
            gols_casa,
            gols_fora
        )

        partidas_validas.append({
            "meus_gols": meus_gols,
            "gols_adv": gols_adv,
            "casa": casa,
            "fora": fora,
            "gols_casa": gols_casa,
            "gols_fora": gols_fora,
            "competicao": competicao,
            "data": data
        })

    for partida in partidas_validas[-5:]:
        if partida["meus_gols"] > partida["gols_adv"]:
            forma_recente.append(("V"))
        elif partida["meus_gols"] < partida["gols_adv"]:
            forma_recente.append(("D"))
        else:
            forma_recente.append(("E"))

    sequencia_vitorias = 0
    sequencia_invicta = 0
    jogos_sem_vencer = 0

    for partida in reversed(partidas_validas):
        if partida["meus_gols"] > partida["gols_adv"]:
            sequencia_vitorias += 1
        else:
            break

    for partida in reversed(partidas_validas):
        if partida["meus_gols"] >= partida["gols_adv"]:
            sequencia_invicta += 1
        else:
            break

    for partida in reversed(partidas_validas):
        if partida["meus_gols"] <= partida["gols_adv"]:
            jogos_sem_vencer += 1
        else:
            break

    frame_cards_1 = ctk.CTkFrame(conteudo, fg_color="transparent")
    frame_cards_1.pack(fill="x", padx=18, pady=(5, 0))

    card(frame_cards_1, "Jogos", str(jogos))
    card(frame_cards_1, "Vitórias", str(vitorias))
    card(frame_cards_1, "Empates", str(empates))
    card(frame_cards_1, "Derrotas", str(derrotas))

    frame_cards_2 = ctk.CTkFrame(conteudo, fg_color="transparent")
    frame_cards_2.pack(fill="x", padx=18, pady=(0, 5))

    card(frame_cards_2, "GM", str(gols_marcados))
    card(frame_cards_2, "GS", str(gols_sofridos))
    card(frame_cards_2, "Saldo", str(saldo))
    card(frame_cards_2, "Títulos", str(total_titulos))

    frame_cards_3 = ctk.CTkFrame(conteudo, fg_color="transparent")
    frame_cards_3.pack(fill="x", padx=18, pady=(0, 5))

    card(frame_cards_3, "Média GM", f"{media_gols_marcados:.2f}")
    card(frame_cards_3, "Média GS", f"{media_gols_sofridos:.2f}")
    card(frame_cards_3, "Vitórias Seguidas", str(sequencia_vitorias))
    card(frame_cards_3, "Sem Vencer", str(jogos_sem_vencer))

    frame_baixo = ctk.CTkFrame(conteudo, corner_radius=12)
    frame_baixo.pack(fill="both", expand=True, padx=25, pady=15)

    frame_info = ctk.CTkFrame(frame_baixo)
    frame_info.pack(fill="both", expand=True, padx=15, pady=15)

    ctk.CTkLabel(
        frame_info,
        text=f"Aproveitamento geral: {aproveitamento:.1f}%",
        font=("Arial", 18, "bold")
    ).pack(pady=(10, 10))

    if ultimo_titulo:
        competicao_titulo, temporada_titulo = ultimo_titulo

        texto_titulo = f"🏆 Último título: {competicao_titulo.title()}"

        if temporada_titulo:
            texto_titulo += f" ({temporada_titulo})"

        ctk.CTkLabel(
            frame_info,
            text=texto_titulo,
            font=("Arial", 16, "bold")
        ).pack(pady=(5, 10))
    else:
        ctk.CTkLabel(
            frame_info,
            text="🏆 Último título: nenhum registrado",
            font=("Arial", 16)
        ).pack(pady=(5, 10))

    ctk.CTkLabel(
        frame_info,
        text=(
            f"🔥 Vitórias seguidas: {sequencia_vitorias}\n"
            f"🛡️ Jogos invicto: {sequencia_invicta}\n"
            f"⚠️ Jogos sem vencer: {jogos_sem_vencer}"
        ),
        font=("Arial", 16),
        justify="center"
    ).pack(pady=(5, 15))

    if melhor_vitoria:
        casa, gols_casa, gols_fora, fora = melhor_vitoria
        ctk.CTkLabel(
            frame_info,
            text=f"⚽ Maior vitória: {casa.title()} {gols_casa} x {gols_fora} {fora.title()}",
            font=("Arial", 15, "bold")
        ).pack(pady=(5, 5))

    if pior_derrota:
        casa, gols_casa, gols_fora, fora = pior_derrota
        ctk.CTkLabel(
            frame_info,
            text=f"💥 Pior derrota: {casa.title()} {gols_casa} x {gols_fora} {fora.title()}",
            font=("Arial", 15, "bold")
        ).pack(pady=(5, 10))

    if forma_recente:
        ctk.CTkLabel(
        frame_info,
        text="Forma recente",
        font=("Arial", 18, "bold")
    ).pack(pady=(10, 5))

    frame_forma = ctk.CTkFrame(
        frame_info,
        fg_color="transparent"
    )
    frame_forma.pack(pady=(5, 15))

    for resultado in forma_recente:

        if resultado == "V":
            cor = "#28a745"  # verde

        elif resultado == "E":
            cor = "#ffc107"  # amarelo

        else:
            cor = "#dc3545"  # vermelho

        card_forma = ctk.CTkFrame(
            frame_forma,
            width=45,
            height=45,
            corner_radius=8,
            fg_color=cor
        )

        card_forma.pack(
            side="left",
            padx=4
        )

        card_forma.pack_propagate(False)

        ctk.CTkLabel(
            card_forma,
            text=resultado,
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(expand=True)
    ctk.CTkLabel(
        frame_info,
        text="Últimas Partidas",
        font=("Arial", 18, "bold")
    ).pack(pady=(10, 15))

    if ultimas_partidas:
        for id_partida, casa, gols_casa, gols_fora, fora, competicao, data in ultimas_partidas:
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

def tela_estatisticas():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text="Estatísticas",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(conteudo, text="Nenhuma carreira ativa selecionada.").pack(pady=20)
        return

    abas = ctk.CTkFrame(conteudo, fg_color="transparent")
    abas.pack(anchor="w", padx=25, pady=(5, 10))

    area_estatisticas = ctk.CTkFrame(conteudo, fg_color="transparent")
    area_estatisticas.pack(fill="both", expand=True)

    def limpar_area():
        for widget in area_estatisticas.winfo_children():
            widget.destroy()

    def mostrar_geral():
        limpar_area()

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT meu_time_na_partida, time_casa, time_fora, gols_casa, gols_fora
        FROM partidas
        WHERE carreira_id = ?
        """, (carreira["id"],))

        partidas = cursor.fetchall()
        conexao.close()

        jogos = vitorias = empates = derrotas = 0
        gols_marcados = gols_sofridos = 0
        melhor_vitoria = None
        pior_derrota = None
        melhor_saldo = None
        pior_saldo = None

        for meu_time, casa, fora, gols_casa, gols_fora in partidas:
            if not meu_time or meu_time not in [casa, fora]:
                continue

            jogos += 1
            meus_gols, gols_adv = calcular_resultado_partida(meu_time, casa, fora, gols_casa, gols_fora)

            gols_marcados += meus_gols
            gols_sofridos += gols_adv

            saldo_partida = meus_gols - gols_adv

            if saldo_partida > 0 and (melhor_saldo is None or saldo_partida > melhor_saldo):
                melhor_saldo = saldo_partida
                melhor_vitoria = (casa, gols_casa, gols_fora, fora)

            if saldo_partida < 0 and (pior_saldo is None or saldo_partida < pior_saldo):
                pior_saldo = saldo_partida
                pior_derrota = (casa, gols_casa, gols_fora, fora)

            if meus_gols > gols_adv:
                vitorias += 1
            elif meus_gols < gols_adv:
                derrotas += 1
            else:
                empates += 1

        aproveitamento = ((vitorias * 3 + empates) / (jogos * 3)) * 100 if jogos > 0 else 0
        saldo_total = gols_marcados - gols_sofridos

        frame_cards = ctk.CTkFrame(area_estatisticas, fg_color="transparent")
        frame_cards.pack(fill="x", padx=18, pady=15)

        card(frame_cards, "Jogos", str(jogos))
        card(frame_cards, "Vitórias", str(vitorias))
        card(frame_cards, "Empates", str(empates))
        card(frame_cards, "Derrotas", str(derrotas))

        frame_cards_2 = ctk.CTkFrame(area_estatisticas, fg_color="transparent")
        frame_cards_2.pack(fill="x", padx=18, pady=5)

        card(frame_cards_2, "Gols Marcados", str(gols_marcados))
        card(frame_cards_2, "Gols Sofridos", str(gols_sofridos))
        card(frame_cards_2, "Saldo", str(saldo_total))
        card(frame_cards_2, "Aproveitamento", f"{aproveitamento:.1f}%")

        frame_baixo = ctk.CTkFrame(area_estatisticas, corner_radius=12)
        frame_baixo.pack(fill="both", expand=True, padx=25, pady=15)

        ctk.CTkLabel(
            frame_baixo,
            text="Destaques da Carreira",
            font=("Arial", 20, "bold")
        ).pack(pady=15)

        if melhor_vitoria:
            casa, gols_casa, gols_fora, fora = melhor_vitoria
            ctk.CTkLabel(
                frame_baixo,
                text=f"Melhor vitória: {casa.title()} {gols_casa} x {gols_fora} {fora.title()}",
                font=("Arial", 16)
            ).pack(pady=8)
        else:
            ctk.CTkLabel(frame_baixo, text="Melhor vitória: nenhuma registrada").pack(pady=8)

        if pior_derrota:
            casa, gols_casa, gols_fora, fora = pior_derrota
            ctk.CTkLabel(
                frame_baixo,
                text=f"Pior derrota: {casa.title()} {gols_casa} x {gols_fora} {fora.title()}",
                font=("Arial", 16)
            ).pack(pady=8)
        else:
            ctk.CTkLabel(frame_baixo, text="Pior derrota: nenhuma registrada").pack(pady=8)

    def mostrar_por_time():
        limpar_area()

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT meu_time_na_partida, tipo_time, time_casa, time_fora, gols_casa, gols_fora
        FROM partidas
        WHERE carreira_id = ?
        ORDER BY data_partida ASC
        """, (carreira["id"],))

        partidas = cursor.fetchall()

        cursor.execute("""
        SELECT nome_time, COUNT(*)
        FROM titulos
        WHERE carreira_id = ?
        GROUP BY nome_time
        """, (carreira["id"],))

        titulos_por_time = dict(cursor.fetchall())

        conexao.close()

        estatisticas = {}

        for partida in partidas:
            meu_time, tipo_time, casa, fora, gols_casa, gols_fora = partida

            if not meu_time or meu_time not in [casa, fora]:
                continue

            chave = (tipo_time, meu_time)

            if chave not in estatisticas:
                estatisticas[chave] = {
                    "jogos": 0,
                    "vitorias": 0,
                    "empates": 0,
                    "derrotas": 0,
                    "gols_marcados": 0,
                    "gols_sofridos": 0
                }

            meus_gols, gols_adv = calcular_resultado_partida(
                meu_time,
                casa,
                fora,
                gols_casa,
                gols_fora
            )

            estatisticas[chave]["jogos"] += 1
            estatisticas[chave]["gols_marcados"] += meus_gols
            estatisticas[chave]["gols_sofridos"] += gols_adv

            if meus_gols > gols_adv:
                estatisticas[chave]["vitorias"] += 1
            elif meus_gols < gols_adv:
                estatisticas[chave]["derrotas"] += 1
            else:
                estatisticas[chave]["empates"] += 1

        frame_lista = ctk.CTkScrollableFrame(area_estatisticas, width=850, height=500)
        frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

        if not estatisticas:
            ctk.CTkLabel(frame_lista, text="Nenhuma estatística por time encontrada.").pack(pady=20)
            return

        for tipo_titulo in ["clube", "selecao"]:
            titulo = "Clubes" if tipo_titulo == "clube" else "Seleções"

            ctk.CTkLabel(
                frame_lista,
                text=titulo,
                font=("Arial", 20, "bold")
            ).pack(anchor="w", padx=10, pady=(15, 10))

            encontrou = False

            for (tipo_time, nome_time), dados in estatisticas.items():
                if tipo_time != tipo_titulo:
                    continue

                encontrou = True

                jogos = dados["jogos"]
                pontos = dados["vitorias"] * 3 + dados["empates"]
                aproveitamento = (pontos / (jogos * 3)) * 100 if jogos > 0 else 0
                saldo = dados["gols_marcados"] - dados["gols_sofridos"]
                total_titulos = titulos_por_time.get(nome_time.lower(), 0)

                texto = (
                    f"{nome_time.title()}\n"
                    f"Jogos: {jogos} | V: {dados['vitorias']} | E: {dados['empates']} | D: {dados['derrotas']} | T: {total_titulos}\n"
                    f"GM: {dados['gols_marcados']} | GS: {dados['gols_sofridos']} | SG: {saldo}\n"
                    f"Aproveitamento: {aproveitamento:.1f}%"
                )

                card_time = ctk.CTkFrame(frame_lista, corner_radius=12)
                card_time.pack(fill="x", padx=10, pady=8)

                ctk.CTkLabel(
                    card_time,
                    text=texto,
                    justify="left",
                    font=("Arial", 15)
                ).pack(anchor="w", padx=15, pady=12)

            if not encontrou:
                ctk.CTkLabel(
                    frame_lista,
                    text=f"Nenhum registro de {titulo.lower()}."
                ).pack(anchor="w", padx=10, pady=5)

    def mostrar_por_competicao():
        limpar_area()

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT meu_time_na_partida, competicao, time_casa, time_fora, gols_casa, gols_fora
        FROM partidas
        WHERE carreira_id = ?
        ORDER BY data_partida ASC
        """, (carreira["id"],))

        partidas = cursor.fetchall()
        conexao.close()

        estatisticas = {}

        for partida in partidas:
            meu_time, competicao, casa, fora, gols_casa, gols_fora = partida

            if not meu_time or meu_time not in [casa, fora]:
                continue

            if competicao not in estatisticas:
                estatisticas[competicao] = {
                    "jogos": 0,
                    "vitorias": 0,
                    "empates": 0,
                    "derrotas": 0,
                    "gols_marcados": 0,
                    "gols_sofridos": 0
                }

            meus_gols, gols_adv = calcular_resultado_partida(
                meu_time,
                casa,
                fora,
                gols_casa,
                gols_fora
            )

            estatisticas[competicao]["jogos"] += 1
            estatisticas[competicao]["gols_marcados"] += meus_gols
            estatisticas[competicao]["gols_sofridos"] += gols_adv

            if meus_gols > gols_adv:
                estatisticas[competicao]["vitorias"] += 1
            elif meus_gols < gols_adv:
                estatisticas[competicao]["derrotas"] += 1
            else:
                estatisticas[competicao]["empates"] += 1

        frame_lista = ctk.CTkScrollableFrame(
            area_estatisticas,
            width=850,
            height=500
        )
        frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

        if not estatisticas:
            ctk.CTkLabel(
                frame_lista,
                text="Nenhuma competição encontrada."
            ).pack(pady=20)
            return

        for competicao, dados in estatisticas.items():

            jogos = dados["jogos"]
            pontos = dados["vitorias"] * 3 + dados["empates"]
            aproveitamento = (pontos / (jogos * 3)) * 100 if jogos > 0 else 0
            saldo = dados["gols_marcados"] - dados["gols_sofridos"]

            texto = (
                f"{competicao}\n"
                f"Jogos: {jogos} | V: {dados['vitorias']} | "
                f"E: {dados['empates']} | D: {dados['derrotas']}\n"
                f"GM: {dados['gols_marcados']} | "
                f"GS: {dados['gols_sofridos']} | "
                f"SG: {saldo}\n"
                f"Aproveitamento: {aproveitamento:.1f}%"
            )

            card_competicao = ctk.CTkFrame(
                frame_lista,
                corner_radius=12
            )
            card_competicao.pack(fill="x", padx=10, pady=8)

            ctk.CTkLabel(
                card_competicao,
                text=texto,
                justify="left",
                font=("Arial", 15)
            ).pack(anchor="w", padx=15, pady=12)

    def mostrar_por_temporada():
        limpar_area()

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT temporada, meu_time_na_partida, time_casa, time_fora, gols_casa, gols_fora
        FROM partidas
        WHERE carreira_id = ?
        ORDER BY temporada ASC, id ASC
        """, (carreira["id"],))

        partidas = cursor.fetchall()
        conexao.close()

        estatisticas = {}

        for temporada, meu_time, casa, fora, gols_casa, gols_fora in partidas:
            if not temporada:
                temporada = "Temporada não informada"

            if not meu_time or meu_time not in [casa, fora]:
                continue

            if temporada not in estatisticas:
                estatisticas[temporada] = {
                    "jogos": 0,
                    "vitorias": 0,
                    "empates": 0,
                    "derrotas": 0,
                    "gols_marcados": 0,
                    "gols_sofridos": 0
                }

            meus_gols, gols_adv = calcular_resultado_partida(
                meu_time,
                casa,
                fora,
                gols_casa,
                gols_fora
            )

            estatisticas[temporada]["jogos"] += 1
            estatisticas[temporada]["gols_marcados"] += meus_gols
            estatisticas[temporada]["gols_sofridos"] += gols_adv

            if meus_gols > gols_adv:
                estatisticas[temporada]["vitorias"] += 1
            elif meus_gols < gols_adv:
                estatisticas[temporada]["derrotas"] += 1
            else:
                estatisticas[temporada]["empates"] += 1

        frame_lista = ctk.CTkScrollableFrame(area_estatisticas, width=850, height=500)
        frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

        if not estatisticas:
            ctk.CTkLabel(
                frame_lista,
                text="Nenhuma temporada encontrada.",
                font=("Arial", 15)
            ).pack(pady=20)
            return

        for temporada, dados in estatisticas.items():
            jogos = dados["jogos"]
            pontos = dados["vitorias"] * 3 + dados["empates"]
            aproveitamento = (pontos / (jogos * 3)) * 100 if jogos > 0 else 0
            saldo = dados["gols_marcados"] - dados["gols_sofridos"]

            texto = (
                f"Temporada {temporada}\n"
                f"Jogos: {jogos} | V: {dados['vitorias']} | E: {dados['empates']} | D: {dados['derrotas']}\n"
                f"GM: {dados['gols_marcados']} | GS: {dados['gols_sofridos']} | SG: {saldo}\n"
                f"Aproveitamento: {aproveitamento:.1f}%"
            )

            card_temporada = ctk.CTkFrame(frame_lista, corner_radius=12)
            card_temporada.pack(fill="x", padx=10, pady=8)

            ctk.CTkLabel(
                card_temporada,
                text=texto,
                justify="left",
                font=("Arial", 15)
            ).pack(anchor="w", padx=15, pady=12)
        


    ctk.CTkButton(
        abas,
        text="Geral",
        command=mostrar_geral,
        width=120
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        abas,
        text="Por Time",
        command=mostrar_por_time,
        width=120
    ).pack(side="left", padx=5)

    ctk.CTkButton(
        abas,
        text="Por Competição",
        command=mostrar_por_competicao,
        width=150
    ).pack(side="left", padx=5)
    ctk.CTkButton(
    abas,
    text="Por Temporada",
    command=mostrar_por_temporada,
    width=180
).pack(side="left", padx=5)
    mostrar_geral()


def calcular_estatisticas_do_time(nome_time, tipo_time, carreira_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT time_casa, time_fora, gols_casa, gols_fora
    FROM partidas
    WHERE carreira_id = ?
    AND meu_time_na_partida = ?
    AND tipo_time = ?
    """, (carreira_id, nome_time, tipo_time))

    partidas = cursor.fetchall()

    cursor.execute("""
    SELECT COUNT(*)
    FROM titulos
    WHERE carreira_id = ?
    AND nome_time = ?
    AND tipo_time = ?
    """, (carreira_id, nome_time, tipo_time))

    total_titulos = cursor.fetchone()[0]

    conexao.close()

    jogos = vitorias = empates = derrotas = 0

    for casa, fora, gols_casa, gols_fora in partidas:
        jogos += 1

        meus_gols, gols_adv = calcular_resultado_partida(
            nome_time,
            casa,
            fora,
            gols_casa,
            gols_fora
        )

        if meus_gols > gols_adv:
            vitorias += 1
        elif meus_gols < gols_adv:
            derrotas += 1
        else:
            empates += 1

    return jogos, vitorias, empates, derrotas, total_titulos


def tela_historico():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text="Histórico da Carreira",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(conteudo, text="Nenhuma carreira ativa selecionada.").pack(pady=20)
        return

    ctk.CTkLabel(
        conteudo,
        text=f"Carreira ativa: {carreira['nome']}",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT tipo, nome_time, data_inicio, data_fim
    FROM historico_carreira
    WHERE carreira_id = ?
    ORDER BY id ASC
    """, (carreira["id"],))

    historicos = cursor.fetchall()
    conexao.close()

    frame_lista = ctk.CTkScrollableFrame(conteudo, width=850, height=520)
    frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

    if not historicos:
        ctk.CTkLabel(frame_lista, text="Nenhum histórico cadastrado.").pack(pady=20)
        return

    def mostrar_secao(titulo_secao, tipo_filtro):
        ctk.CTkLabel(
            frame_lista,
            text=titulo_secao,
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=10, pady=(15, 10))

        encontrou = False

        for tipo, nome_time, data_inicio, data_fim in historicos:
            if tipo != tipo_filtro:
                continue

            encontrou = True
            fim = data_fim if data_fim else "Atual"

            jogos, vitorias, empates, derrotas, titulos = calcular_estatisticas_do_time(
                nome_time,
                tipo,
                carreira["id"]
            )

            card_time = ctk.CTkFrame(frame_lista, corner_radius=12)
            card_time.pack(fill="x", padx=10, pady=8)

            texto = (
                f"{nome_time.title()} | {data_inicio} até {fim}\n"
                f"Jogos: {jogos} | V: {vitorias} | E: {empates} | D: {derrotas} | T: {titulos}"
            )

            ctk.CTkLabel(
                card_time,
                text=texto,
                justify="left",
                font=("Arial", 15)
            ).pack(side="left", padx=15, pady=12)

            ctk.CTkButton(
                card_time,
                text="Ver detalhes",
                width=120,
                command=lambda n=nome_time, t=tipo: tela_detalhes_time(n, t)
            ).pack(side="right", padx=15, pady=12)

        if not encontrou:
            ctk.CTkLabel(
                frame_lista,
                text=f"Nenhum registro em {titulo_secao.lower()}."
            ).pack(pady=5)

    mostrar_secao("Clubes", "clube")
    mostrar_secao("Seleções", "selecao")


def tela_detalhes_time(nome_time, tipo_time):
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text=f"Detalhes - {nome_time.title()}",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(conteudo, text="Nenhuma carreira ativa selecionada.").pack(pady=20)
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT competicao, COUNT(*)
    FROM titulos
    WHERE carreira_id = ?
    AND nome_time = ?
    AND tipo_time = ?
    GROUP BY competicao
    ORDER BY competicao ASC
    """, (carreira["id"], nome_time, tipo_time))

    titulos = cursor.fetchall()

    cursor.execute("""
    SELECT competicao, time_casa, time_fora, gols_casa, gols_fora
    FROM partidas
    WHERE carreira_id = ?
    AND meu_time_na_partida = ?
    AND tipo_time = ?
    ORDER BY competicao ASC
    """, (carreira["id"], nome_time, tipo_time))

    partidas = cursor.fetchall()

    conexao.close()

    frame_lista = ctk.CTkScrollableFrame(conteudo, width=850, height=500)
    frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

    ctk.CTkLabel(
        frame_lista,
        text="Títulos",
        font=("Arial", 20, "bold")
    ).pack(anchor="w", padx=10, pady=(15, 8))

    if not titulos:
        ctk.CTkLabel(frame_lista, text="Nenhum título conquistado.").pack(anchor="w", padx=10, pady=5)
    else:
        for competicao, total in titulos:
            ctk.CTkLabel(
                frame_lista,
                text=f"🏆 {total}x {competicao}",
                font=("Arial", 15)
            ).pack(anchor="w", padx=20, pady=4)

    ctk.CTkLabel(
        frame_lista,
        text="Competições",
        font=("Arial", 20, "bold")
    ).pack(anchor="w", padx=10, pady=(20, 8))

    estatisticas = {}

    for competicao, casa, fora, gols_casa, gols_fora in partidas:
        if competicao not in estatisticas:
            estatisticas[competicao] = {
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_marcados": 0,
                "gols_sofridos": 0
            }

        meus_gols, gols_adv = calcular_resultado_partida(
            nome_time,
            casa,
            fora,
            gols_casa,
            gols_fora
        )

        estatisticas[competicao]["jogos"] += 1
        estatisticas[competicao]["gols_marcados"] += meus_gols
        estatisticas[competicao]["gols_sofridos"] += gols_adv

        if meus_gols > gols_adv:
            estatisticas[competicao]["vitorias"] += 1
        elif meus_gols < gols_adv:
            estatisticas[competicao]["derrotas"] += 1
        else:
            estatisticas[competicao]["empates"] += 1

    if not estatisticas:
        ctk.CTkLabel(frame_lista, text="Nenhuma partida encontrada para esse time.").pack(anchor="w", padx=10, pady=5)
    else:
        for competicao, dados in estatisticas.items():
            jogos = dados["jogos"]
            pontos = dados["vitorias"] * 3 + dados["empates"]
            aproveitamento = (pontos / (jogos * 3)) * 100 if jogos > 0 else 0
            saldo = dados["gols_marcados"] - dados["gols_sofridos"]

            card_comp = ctk.CTkFrame(frame_lista, corner_radius=12)
            card_comp.pack(fill="x", padx=10, pady=7)

            texto = (
                f"{competicao}\n"
                f"Jogos: {jogos} | V: {dados['vitorias']} | E: {dados['empates']} | D: {dados['derrotas']}\n"
                f"GM: {dados['gols_marcados']} | GS: {dados['gols_sofridos']} | SG: {saldo}\n"
                f"Aproveitamento: {aproveitamento:.1f}%"
            )

            ctk.CTkLabel(
                card_comp,
                text=texto,
                justify="left",
                font=("Arial", 14)
            ).pack(anchor="w", padx=15, pady=10)

    ctk.CTkButton(
        conteudo,
        text="Voltar ao Histórico",
        command=tela_historico
    ).pack(pady=10)

def tela_titulos():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    topo = ctk.CTkFrame(conteudo, fg_color="transparent")
    topo.pack(fill="x", padx=25, pady=(20, 5))

    ctk.CTkLabel(
        topo,
        text="Títulos",
        font=("Arial", 28, "bold")
    ).pack(side="left")

    if carreira is None:
        ctk.CTkLabel(conteudo, text="Nenhuma carreira ativa selecionada.").pack(pady=20)
        return

    def abrir_cadastro_titulo():
        janela = ctk.CTkToplevel(app)
        janela.title("Cadastrar Título")
        janela.geometry("420x430")
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text="Cadastrar novo título",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 15))

        tipo_var = ctk.StringVar(value="clube")

        ctk.CTkOptionMenu(
            janela,
            values=["clube", "selecao"],
            variable=tipo_var,
            width=300
        ).pack(pady=6)

        entrada_time = ctk.CTkEntry(
            janela,
            placeholder_text="Time/Seleção campeão",
            width=300
        )
        entrada_time.pack(pady=6)

        entrada_competicao = ctk.CTkEntry(
            janela,
            placeholder_text="Competição",
            width=300
        )
        entrada_competicao.pack(pady=6)

        entrada_temporada = ctk.CTkEntry(
            janela,
            placeholder_text="Temporada ex: 2026/27",
            width=300
        )
        entrada_temporada.pack(pady=6)

        entrada_data = ctk.CTkEntry(
            janela,
            placeholder_text="Data da conquista AAAA-MM-DD",
            width=300
        )
        entrada_data.pack(pady=6)

        mensagem = ctk.CTkLabel(janela, text="")
        mensagem.pack(pady=8)

        def salvar_titulo():
            tipo_time = tipo_var.get()
            nome_time = entrada_time.get().strip().lower()
            competicao = entrada_competicao.get().strip()
            temporada = entrada_temporada.get().strip()
            data_conquista = entrada_data.get().strip()

            if not nome_time or not competicao:
                mensagem.configure(text="Preencha o time/seleção e a competição.")
                return

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
            INSERT INTO titulos (
                carreira_id,
                tipo_time,
                nome_time,
                competicao,
                temporada,
                data_conquista
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                carreira["id"],
                tipo_time,
                nome_time,
                competicao,
                temporada,
                data_conquista
            ))

            conexao.commit()
            conexao.close()

            janela.destroy()
            tela_titulos()

        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(pady=15)

        ctk.CTkButton(
            botoes,
            text="Salvar",
            command=salvar_titulo,
            width=120
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=janela.destroy,
            width=120
        ).pack(side="left", padx=8)

    ctk.CTkButton(
        topo,
        text="+ Novo Título",
        command=abrir_cadastro_titulo,
        width=140
    ).pack(side="right")

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM titulos
    WHERE carreira_id = ?
    """, (carreira["id"],))

    total_titulos = cursor.fetchone()[0]

    cursor.execute("""
    SELECT
    tipo_time,
    competicao,
    COUNT(*) as total,
    MAX(temporada) as ultima_temporada
    FROM titulos
    WHERE carreira_id = ?
    GROUP BY tipo_time, competicao
    ORDER BY total DESC
""", (carreira["id"],))

    titulos = cursor.fetchall()
    conexao.close()

    ctk.CTkLabel(
        conteudo,
        text=f"Total de títulos: {total_titulos}",
        font=("Arial", 16)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    frame_lista = ctk.CTkScrollableFrame(conteudo, width=850, height=520)
    frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

    if not titulos:
        ctk.CTkLabel(
            frame_lista,
            text="Nenhum título cadastrado.",
            font=("Arial", 15)
        ).pack(pady=20)
        return

    def mostrar_secao(titulo_secao, tipo_filtro):
        ctk.CTkLabel(
            frame_lista,
            text=titulo_secao,
            font=("Arial", 20, "bold")
        ).pack(anchor="w", padx=10, pady=(15, 10))

        encontrou = False

        for tipo_time, competicao, total, ultima_temporada in titulos:
            if tipo_time != tipo_filtro:
                continue

            encontrou = True

            card_titulo = ctk.CTkFrame(frame_lista, corner_radius=12)
            card_titulo.pack(fill="x", padx=10, pady=7)

            ctk.CTkLabel(
                card_titulo,
                text="🏆",
                font=("Arial", 32)
            ).pack(side="left", padx=15, pady=10)

            texto_titulo = (
    f"{competicao.title()}\n"
    f"Conquistas: {total}\n"
    f"Última temporada: {ultima_temporada or 'Não informada'}"
)

            ctk.CTkLabel(
            card_titulo,
            text=texto_titulo,
            justify="left",
            font=("Arial", 15)
        ).pack(side="left", padx=10, pady=10)

        if not encontrou:
            ctk.CTkLabel(
                frame_lista,
                text=f"Nenhum título em {titulo_secao.lower()}."
            ).pack(anchor="w", padx=10, pady=5)

    mostrar_secao("Clubes", "clube")
    mostrar_secao("Seleções", "selecao")


def tela_ocr_captura():
    limpar_conteudo()

    PASTA_TEMP = "temp"
    PRE_JOGO = os.path.join(PASTA_TEMP, "pre_jogo.png")
    POS_JOGO = os.path.join(PASTA_TEMP, "pos_jogo.png")

    partida_extraida = {}

    ctk.CTkLabel(
        conteudo,
        text="OCR / Captura",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    ctk.CTkLabel(
        conteudo,
        text="Capture o pré-jogo, depois o pós-jogo, gere a prévia e confirme o salvamento.",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    frame_acoes = ctk.CTkFrame(conteudo, corner_radius=12)
    frame_acoes.pack(fill="x", padx=25, pady=10)

    status = ctk.CTkLabel(
        frame_acoes,
        text="Status: aguardando captura.",
        font=("Arial", 15)
    )
    status.pack(pady=10)

    entrada_ano = ctk.CTkEntry(
        frame_acoes,
        placeholder_text="Ano da partida ex: 2026",
        width=220
    )
    entrada_ano.pack(pady=8)

    botoes = ctk.CTkFrame(frame_acoes, fg_color="transparent")
    botoes.pack(pady=10)

    previa = ctk.CTkLabel(conteudo, text="", font=("Arial", 16))
    previa.pack(pady=15)

    def preparar_pasta():
        os.makedirs(PASTA_TEMP, exist_ok=True)

    def capturar_pre():
        preparar_pasta()
        screenshot = pyautogui.screenshot()
        screenshot.save(PRE_JOGO)
        status.configure(text="Pré-jogo capturado com sucesso.")

    def capturar_pos():
        preparar_pasta()
        screenshot = pyautogui.screenshot()
        screenshot.save(POS_JOGO)
        status.configure(text="Pós-jogo capturado com sucesso.")

    def gerar_previa():
        if not os.path.exists(PRE_JOGO):
            status.configure(text="Capture o pré-jogo primeiro.")
            return

        if not os.path.exists(POS_JOGO):
            status.configure(text="Capture o pós-jogo primeiro.")
            return

        partida = extrair_partida(PRE_JOGO, POS_JOGO)

        if partida is None:
            status.configure(text="Erro: não foi possível extrair a partida.")
            return

        partida_extraida.clear()
        partida_extraida.update(partida)

        texto = (
            f"Competição: {partida['competicao']}\n"
            f"Fase: {partida['fase']}\n"
            f"Data: {partida['data']}\n\n"
            f"{partida['time_casa']} {partida['gols_casa']} x "
            f"{partida['gols_fora']} {partida['time_fora']}"
        )

        previa.configure(text=texto)
        status.configure(text="Prévia gerada. Confira antes de salvar.")

    def confirmar_salvamento():
        if not partida_extraida:
            status.configure(text="Gere a prévia antes de salvar.")
            return

        ano = entrada_ano.get().strip()

        if not ano:
            status.configure(text="Informe o ano da partida antes de salvar.")
            return

        if not ano.isdigit() or len(ano) != 4:
            status.configure(text="Ano inválido. Use o formato 2026.")
            return

        partida_para_salvar = partida_extraida.copy()
        partida_para_salvar["ano"] = ano
        partida_para_salvar["data"] = f"{partida_para_salvar['data']} / {ano}"

        sucesso, mensagem = salvar_partida(partida_para_salvar)
        status.configure(text=mensagem)

    ctk.CTkButton(
        botoes,
        text="Capturar Pré-Jogo",
        command=capturar_pre,
        width=160
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        botoes,
        text="Capturar Pós-Jogo",
        command=capturar_pos,
        width=160
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        botoes,
        text="Gerar Prévia",
        command=gerar_previa,
        width=140
    ).pack(side="left", padx=8)

    ctk.CTkButton(
        botoes,
        text="Confirmar e Salvar",
        command=confirmar_salvamento,
        width=160
    ).pack(side="left", padx=8)

    frame_info = ctk.CTkFrame(conteudo, corner_radius=12)
    frame_info.pack(fill="x", padx=25, pady=10)

    ctk.CTkLabel(
        frame_info,
        text=f"Arquivos temporários:\n{PRE_JOGO}\n{POS_JOGO}",
        justify="left"
    ).pack(anchor="w", padx=15, pady=15)

def tela_carreiras():
    limpar_conteudo()

    carreira_ativa = obter_carreira_ativa()

    topo = ctk.CTkFrame(conteudo, fg_color="transparent")
    topo.pack(fill="x", padx=25, pady=(20, 5))

    ctk.CTkLabel(
        topo,
        text="Carreiras",
        font=("Arial", 28, "bold")
    ).pack(side="left")

    def abrir_nova_carreira():
        janela = ctk.CTkToplevel(app)
        janela.title("Nova Carreira")
        janela.geometry("420x380")
        janela.resizable(False, False)

        ctk.CTkLabel(
            janela,
            text="Criar nova carreira",
            font=("Arial", 22, "bold")
        ).pack(pady=(25, 15))

        entrada_nome = ctk.CTkEntry(
            janela,
            placeholder_text="Nome da carreira",
            width=300
        )
        entrada_nome.pack(pady=6)

        entrada_time = ctk.CTkEntry(
            janela,
            placeholder_text="Time atual",
            width=300
        )
        entrada_time.pack(pady=6)

        entrada_selecao = ctk.CTkEntry(
            janela,
            placeholder_text="Seleção atual (opcional)",
            width=300
        )
        entrada_selecao.pack(pady=6)

        modo_var = ctk.StringVar(value="treinador")

        ctk.CTkOptionMenu(
            janela,
            values=["treinador"],
            variable=modo_var,
            width=300
        ).pack(pady=6)

        mensagem = ctk.CTkLabel(janela, text="")
        mensagem.pack(pady=8)

        def salvar_nova_carreira():
            nome = entrada_nome.get().strip()
            time_atual = entrada_time.get().strip().lower()
            selecao_atual = entrada_selecao.get().strip().lower()
            modo = modo_var.get()

            if not nome or not time_atual:
                mensagem.configure(text="Preencha o nome e o time atual.")
                return

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
            INSERT INTO carreiras (
                nome_carreira,
                modo,
                time_atual,
                selecao_atual
            )
            VALUES (?, ?, ?, ?)
            """, (
                nome,
                modo,
                time_atual,
                selecao_atual
            ))

            nova_carreira_id = cursor.lastrowid

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
                nova_carreira_id,
                "clube",
                time_atual,
                "início",
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
                    nova_carreira_id,
                    "selecao",
                    selecao_atual,
                    "início",
                    None
                ))

            conexao.commit()
            conexao.close()

            salvar_carreira_ativa(nova_carreira_id)

            janela.destroy()
            tela_carreiras()

        botoes = ctk.CTkFrame(janela, fg_color="transparent")
        botoes.pack(pady=15)

        ctk.CTkButton(
            botoes,
            text="Salvar",
            command=salvar_nova_carreira,
            width=120
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Cancelar",
            command=janela.destroy,
            width=120
        ).pack(side="left", padx=8)

    ctk.CTkButton(
        topo,
        text="+ Nova Carreira",
        command=abrir_nova_carreira,
        width=150
    ).pack(side="right")

    if carreira_ativa:
        texto_ativa = (
            f"Carreira ativa: {carreira_ativa['nome']} | "
            f"Clube: {carreira_ativa['time_atual'].title()}"
        )

        if carreira_ativa["selecao_atual"]:
            texto_ativa += f" | Seleção: {carreira_ativa['selecao_atual'].title()}"

        ctk.CTkLabel(
            conteudo,
            text=texto_ativa,
            font=("Arial", 16)
        ).pack(anchor="w", padx=25, pady=(0, 15))
    else:
        ctk.CTkLabel(
            conteudo,
            text="Nenhuma carreira ativa selecionada.",
            font=("Arial", 16)
        ).pack(anchor="w", padx=25, pady=(0, 15))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, nome_carreira, modo, time_atual, selecao_atual
    FROM carreiras
    ORDER BY id DESC
    """)

    carreiras = cursor.fetchall()
    conexao.close()

    frame_lista = ctk.CTkScrollableFrame(conteudo, width=850, height=520)
    frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

    if not carreiras:
        ctk.CTkLabel(
            frame_lista,
            text="Nenhuma carreira cadastrada.",
            font=("Arial", 15)
        ).pack(pady=20)
        return

    for carreira_id, nome, modo, time_atual, selecao_atual in carreiras:
        card_carreira = ctk.CTkFrame(frame_lista, corner_radius=12)
        card_carreira.pack(fill="x", padx=10, pady=8)

        selecao_texto = selecao_atual.title() if selecao_atual else "Nenhuma"

        texto = (
            f"{nome}\n"
            f"Modo: {modo.title()} | Clube: {time_atual.title()} | Seleção: {selecao_texto}"
        )

        ctk.CTkLabel(
            card_carreira,
            text=texto,
            justify="left",
            font=("Arial", 15)
        ).pack(side="left", padx=15, pady=12)

        botoes_card = ctk.CTkFrame(card_carreira, fg_color="transparent")
        botoes_card.pack(side="right", padx=15, pady=12)

        def ativar(id_carreira=carreira_id):
            salvar_carreira_ativa(id_carreira)
            tela_carreiras()

        ctk.CTkButton(
            botoes_card,
            text="Ativar",
            width=90,
            command=ativar
        ).pack(side="left", padx=5)

        def confirmar_exclusao(id_carreira=carreira_id, nome_carreira=nome):
            janela = ctk.CTkToplevel(app)
            janela.title("Excluir Carreira")
            janela.geometry("420x260")
            janela.resizable(False, False)

            ctk.CTkLabel(
                janela,
                text="Excluir carreira?",
                font=("Arial", 22, "bold")
            ).pack(pady=(25, 10))

            ctk.CTkLabel(
                janela,
                text=(
                    f"Tem certeza que deseja excluir '{nome_carreira}'?\n\n"
                    "Isso apagará partidas, histórico e títulos dessa carreira."
                ),
                font=("Arial", 14),
                justify="center"
            ).pack(pady=10)

            def excluir_carreira():
                conexao = conectar()
                cursor = conexao.cursor()

                cursor.execute("DELETE FROM partidas WHERE carreira_id = ?", (id_carreira,))
                cursor.execute("DELETE FROM historico_carreira WHERE carreira_id = ?", (id_carreira,))
                cursor.execute("DELETE FROM titulos WHERE carreira_id = ?", (id_carreira,))
                cursor.execute("DELETE FROM carreiras WHERE id = ?", (id_carreira,))

                conexao.commit()
                conexao.close()

                carreira_atual = carregar_carreira_ativa()

                if carreira_atual == id_carreira:
                    salvar_carreira_ativa(None)

                janela.destroy()
                tela_carreiras()

            botoes_modal = ctk.CTkFrame(janela, fg_color="transparent")
            botoes_modal.pack(pady=20)

            ctk.CTkButton(
                botoes_modal,
                text="Cancelar",
                width=120,
                command=janela.destroy
            ).pack(side="left", padx=8)

            ctk.CTkButton(
                botoes_modal,
                text="Excluir",
                width=120,
                fg_color="#b3261e",
                hover_color="#8c1d18",
                command=excluir_carreira
            ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes_card,
            text="Excluir",
            width=90,
            fg_color="#b3261e",
            hover_color="#8c1d18",
            command=confirmar_exclusao
        ).pack(side="left", padx=5)    

def tela_competicoes():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text="Estatísticas por Competição",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(
            conteudo,
            text="Nenhuma carreira ativa selecionada.",
            font=("Arial", 16)
        ).pack(pady=20)
        return

    ctk.CTkLabel(
        conteudo,
        text=f"Carreira ativa: {carreira['nome']}",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT meu_time_na_partida, competicao, time_casa, time_fora, gols_casa, gols_fora
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY data_partida ASC
    """, (carreira["id"],))

    partidas = cursor.fetchall()
    conexao.close()

    estatisticas = {}

    for partida in partidas:
        meu_time, competicao, casa, fora, gols_casa, gols_fora = partida

        if not meu_time or meu_time not in [casa, fora]:
            continue

        if competicao not in estatisticas:
            estatisticas[competicao] = {
                "jogos": 0,
                "vitorias": 0,
                "empates": 0,
                "derrotas": 0,
                "gols_marcados": 0,
                "gols_sofridos": 0
            }

        meus_gols, gols_adv = calcular_resultado_partida(
            meu_time,
            casa,
            fora,
            gols_casa,
            gols_fora
        )

        estatisticas[competicao]["jogos"] += 1
        estatisticas[competicao]["gols_marcados"] += meus_gols
        estatisticas[competicao]["gols_sofridos"] += gols_adv

        if meus_gols > gols_adv:
            estatisticas[competicao]["vitorias"] += 1
        elif meus_gols < gols_adv:
            estatisticas[competicao]["derrotas"] += 1
        else:
            estatisticas[competicao]["empates"] += 1

    frame_lista = ctk.CTkScrollableFrame(conteudo, width=850, height=520)
    frame_lista.pack(fill="both", expand=True, padx=25, pady=10)

    if not estatisticas:
        ctk.CTkLabel(
            frame_lista,
            text="Nenhuma competição encontrada.",
            font=("Arial", 15)
        ).pack(pady=20)
        return

    for competicao, dados in estatisticas.items():
        jogos = dados["jogos"]
        pontos = dados["vitorias"] * 3 + dados["empates"]
        aproveitamento = (pontos / (jogos * 3)) * 100 if jogos > 0 else 0
        saldo = dados["gols_marcados"] - dados["gols_sofridos"]

        card_competicao = ctk.CTkFrame(frame_lista, corner_radius=12)
        card_competicao.pack(fill="x", padx=10, pady=8)

        texto = (
            f"{competicao}\n"
            f"Jogos: {jogos} | V: {dados['vitorias']} | E: {dados['empates']} | D: {dados['derrotas']}\n"
            f"GM: {dados['gols_marcados']} | GS: {dados['gols_sofridos']} | SG: {saldo}\n"
            f"Aproveitamento: {aproveitamento:.1f}%"
        )

        ctk.CTkLabel(
            card_competicao,
            text=texto,
            justify="left",
            font=("Arial", 15)
        ).pack(anchor="w", padx=15, pady=12)
    

def tela_calendario():
    limpar_conteudo()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(
        conteudo,
        text="Calendário da Carreira",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    if carreira is None:
        ctk.CTkLabel(
            conteudo,
            text="Nenhuma carreira ativa selecionada.",
            font=("Arial", 16)
        ).pack(pady=20)
        return

    meses = {
        "Janeiro": "JAN",
        "Fevereiro": "FEV",
        "Março": "MAR",
        "Abril": "ABR",
        "Maio": "MAI",
        "Junho": "JUN",
        "Julho": "JUL",
        "Agosto": "AGO",
        "Setembro": "SET",
        "Outubro": "OUT",
        "Novembro": "NOV",
        "Dezembro": "DEZ"
    }

    mes_numero = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12
    }

    anos = ["2026", "2027", "2028", "2029", "2030"]
    ano_var = ctk.StringVar(value="2026")
    mes_var = ctk.StringVar(value="Janeiro")

    filtros = ctk.CTkFrame(conteudo, fg_color="transparent")
    filtros.pack(anchor="w", padx=25, pady=10)

    ctk.CTkOptionMenu(
        filtros,
        values=anos,
        variable=ano_var,
        width=120
    ).pack(side="left", padx=5)

    ctk.CTkOptionMenu(
        filtros,
        values=list(meses.keys()),
        variable=mes_var,
        width=160
    ).pack(side="left", padx=5)

    area_calendario = ctk.CTkFrame(conteudo, fg_color="transparent")
    area_calendario.pack(fill="both", expand=True, padx=25, pady=10)

    def limpar_calendario():
        for widget in area_calendario.winfo_children():
            widget.destroy()

    def extrair_dia_mes_ano(data_texto):
        if not data_texto:
            return None, None, None

        texto = data_texto.upper()

        ano_encontrado = None
        for ano in anos:
            if ano in texto:
                ano_encontrado = ano
                break

        dia_encontrado = None
        partes = texto.replace(",", " ").replace("/", " ").split()

        for parte in partes:
            if parte.isdigit():
                numero = int(parte)
                if 1 <= numero <= 31:
                    dia_encontrado = numero
                    break

        mes_encontrado = None
        for nome_mes, sigla in meses.items():
            if sigla in texto:
                mes_encontrado = nome_mes
                break

        return dia_encontrado, mes_encontrado, ano_encontrado

    def carregar_partidas():
        limpar_calendario()

        ano = ano_var.get()
        mes = mes_var.get()
        numero_mes = mes_numero[mes]

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT meu_time_na_partida, competicao, time_casa, gols_casa, gols_fora, time_fora, data_partida
        FROM partidas
        WHERE carreira_id = ?
        ORDER BY id ASC
        """, (carreira["id"],))

        partidas = cursor.fetchall()
        conexao.close()

        partidas_por_dia = {}

        for meu_time, competicao, casa, gols_casa, gols_fora, fora, data in partidas:
            dia, mes_detectado, ano_detectado = extrair_dia_mes_ano(data)

            if dia is None or mes_detectado is None or ano_detectado is None:
                continue

            if ano_detectado != ano or mes_detectado != mes:
                continue

            meus_gols, gols_adv = calcular_resultado_partida(
                meu_time,
                casa,
                fora,
                gols_casa,
                gols_fora
            )

            if meus_gols > gols_adv:
                resultado = "V"
                cor = "#28a745"
            elif meus_gols < gols_adv:
                resultado = "D"
                cor = "#dc3545"
            else:
                resultado = "E"
                cor = "#ffc107"

            partidas_por_dia[dia] = {
                "competicao": competicao,
                "casa": casa,
                "fora": fora,
                "placar": f"{gols_casa}x{gols_fora}",
                "resultado": resultado,
                "cor": cor
            }

        ctk.CTkLabel(
            area_calendario,
            text=f"{mes} {ano}",
            font=("Arial", 24, "bold")
        ).pack(pady=(5, 15))

        dias_semana = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"]

        header = ctk.CTkFrame(area_calendario, fg_color="transparent")
        header.pack(fill="x")

        for dia_semana in dias_semana:
            ctk.CTkLabel(
                header,
                text=dia_semana,
                font=("Arial", 14, "bold"),
                width=110
            ).pack(side="left", padx=3)

        calendario_mes = calendar.Calendar(firstweekday=6).monthdayscalendar(
            int(ano),
            numero_mes
        )

        for semana in calendario_mes:
            linha = ctk.CTkFrame(area_calendario, fg_color="transparent")
            linha.pack(fill="x", pady=3)

            for dia in semana:
                card_dia = ctk.CTkFrame(
                    linha,
                    width=110,
                    height=95,
                    corner_radius=8
                )
                card_dia.pack(side="left", padx=3)
                card_dia.pack_propagate(False)

                if dia == 0:
                    ctk.CTkLabel(card_dia, text="").pack()
                    continue

                ctk.CTkLabel(
                    card_dia,
                    text=str(dia),
                    font=("Arial", 13, "bold")
                ).pack(anchor="nw", padx=6, pady=(5, 0))

                if dia in partidas_por_dia:
                    jogo = partidas_por_dia[dia]

                    ctk.CTkLabel(
                        card_dia,
                        text=f"{jogo['casa'].title()}",
                        font=("Arial", 10)
                    ).pack(pady=(3, 0))

                    ctk.CTkLabel(
                        card_dia,
                        text=jogo["placar"],
                        font=("Arial", 13, "bold")
                    ).pack()

                    badge = ctk.CTkFrame(
                        card_dia,
                        fg_color=jogo["cor"],
                        corner_radius=6
                    )
                    badge.pack(pady=3)

                    ctk.CTkLabel(
                        badge,
                        text=jogo["resultado"],
                        text_color="white",
                        font=("Arial", 11, "bold"),
                        width=28
                    ).pack()

        ctk.CTkLabel(
            area_calendario,
            text="Legenda: V = vitória | E = empate | D = derrota",
            font=("Arial", 13)
        ).pack(pady=10)

    ctk.CTkButton(
        filtros,
        text="Atualizar",
        command=carregar_partidas,
        width=120
    ).pack(side="left", padx=5)

    carregar_partidas()


def tela_configuracoes():
    limpar_conteudo()

    ctk.CTkLabel(
        conteudo,
        text="Configurações",
        font=("Arial", 28, "bold")
    ).pack(anchor="w", padx=25, pady=(20, 5))

    ctk.CTkLabel(
        conteudo,
        text="Gerencie backup, exportação e arquivos temporários do projeto.",
        font=("Arial", 15)
    ).pack(anchor="w", padx=25, pady=(0, 15))

    frame = ctk.CTkScrollableFrame(conteudo, width=850, height=520)
    frame.pack(fill="both", expand=True, padx=25, pady=10)

    mensagem = ctk.CTkLabel(frame, text="", font=("Arial", 14))
    mensagem.pack(pady=10)

    def fazer_backup():
        os.makedirs("backups", exist_ok=True)

        if not os.path.exists(DB_PATH):
            mensagem.configure(text="Banco de dados não encontrado.")
            return

        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        destino = f"backups/career_tracker_backup_{data_hora}.db"

        shutil.copy(DB_PATH, destino)

        mensagem.configure(text=f"Backup criado com sucesso: {destino}")

    def exportar_partidas_csv():
        os.makedirs("exports", exist_ok=True)

        carreira = obter_carreira_ativa()

        if carreira is None:
            mensagem.configure(text="Nenhuma carreira ativa selecionada.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT data_partida, competicao, time_casa, gols_casa, gols_fora, time_fora, tipo_time
        FROM partidas
        WHERE carreira_id = ?
        ORDER BY id ASC
        """, (carreira["id"],))

        partidas = cursor.fetchall()
        conexao.close()

        if not partidas:
            mensagem.configure(text="Nenhuma partida encontrada para exportar.")
            return

        data_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        caminho_csv = f"exports/partidas_{carreira['nome']}_{data_hora}.csv"

        with open(caminho_csv, "w", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)

            escritor.writerow([
                "Data",
                "Competição",
                "Casa",
                "Gols Casa",
                "Gols Fora",
                "Fora",
                "Tipo"
            ])

            for partida in partidas:
                escritor.writerow(partida)

        mensagem.configure(text=f"CSV exportado com sucesso: {caminho_csv}")

    def limpar_temporarios():
        arquivos = [
            "temp/pre_jogo.png",
            "temp/pos_jogo.png"
        ]

        removidos = 0

        for arquivo in arquivos:
            if os.path.exists(arquivo):
                os.remove(arquivo)
                removidos += 1

        mensagem.configure(text=f"Arquivos temporários removidos: {removidos}")

    # Backup
    card_backup = ctk.CTkFrame(frame, corner_radius=12)
    card_backup.pack(fill="x", padx=10, pady=8)

    ctk.CTkLabel(
        card_backup,
        text="💾 Backup do Banco",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 4))

    ctk.CTkLabel(
        card_backup,
        text="Cria uma cópia de segurança do arquivo career_tracker.db.",
        font=("Arial", 14)
    ).pack(anchor="w", padx=15, pady=4)

    ctk.CTkButton(
        card_backup,
        text="Fazer Backup",
        command=fazer_backup,
        width=160
    ).pack(anchor="w", padx=15, pady=(8, 12))

    # Exportação
    card_exportar = ctk.CTkFrame(frame, corner_radius=12)
    card_exportar.pack(fill="x", padx=10, pady=8)

    ctk.CTkLabel(
        card_exportar,
        text="📤 Exportação CSV",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 4))

    ctk.CTkLabel(
        card_exportar,
        text="Exporta as partidas da carreira ativa para um arquivo CSV.",
        font=("Arial", 14)
    ).pack(anchor="w", padx=15, pady=4)

    ctk.CTkButton(
        card_exportar,
        text="Exportar Partidas",
        command=exportar_partidas_csv,
        width=160
    ).pack(anchor="w", padx=15, pady=(8, 12))

    # Temporários
    card_temp = ctk.CTkFrame(frame, corner_radius=12)
    card_temp.pack(fill="x", padx=10, pady=8)

    ctk.CTkLabel(
        card_temp,
        text="🧹 Arquivos Temporários",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 4))

    ctk.CTkLabel(
        card_temp,
        text="Remove as últimas capturas de pré-jogo e pós-jogo da pasta temp.",
        font=("Arial", 14)
    ).pack(anchor="w", padx=15, pady=4)

    ctk.CTkButton(
        card_temp,
        text="Limpar Temporários",
        command=limpar_temporarios,
        width=160
    ).pack(anchor="w", padx=15, pady=(8, 12))

    # Sistema
    card_sistema = ctk.CTkFrame(frame, corner_radius=12)
    card_sistema.pack(fill="x", padx=10, pady=8)

    info = (
        "FC Career Tracker v1.0\n"
        "Interface: CustomTkinter\n"
        "Banco de Dados: SQLite\n"
        "OCR: Tesseract / PyTesseract"
    )

    ctk.CTkLabel(
        card_sistema,
        text="ℹ️ Informações do Sistema",
        font=("Arial", 18, "bold")
    ).pack(anchor="w", padx=15, pady=(12, 4))

    ctk.CTkLabel(
        card_sistema,
        text=info,
        justify="left",
        font=("Arial", 14)
    ).pack(anchor="w", padx=15, pady=(4, 12))

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
ctk.CTkButton(menu, text="Carreiras", command=tela_carreiras).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Partidas", command=tela_partidas).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Calendário", command=tela_calendario).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Estatísticas", command=tela_estatisticas).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu,text="Competições",command=tela_competicoes).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Histórico", command=tela_historico).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Títulos", command=tela_titulos).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="OCR / Captura", command=tela_ocr_captura).pack(fill="x", padx=15, pady=6)
ctk.CTkButton(menu, text="Configurações", command=tela_configuracoes).pack(fill="x", padx=15, pady=6)

tela_dashboard()

app.mainloop()
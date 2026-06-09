import customtkinter as ctk
import sqlite3
from carreira_ativa import carregar_carreira_ativa, salvar_carreira_ativa

DB_PATH = "data/career_tracker.db"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("FC Career Tracker")
app.geometry("900x600")


def limpar_tela():
    for widget in app.winfo_children():
        widget.destroy()


def conectar():
    return sqlite3.connect(DB_PATH)


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


def botao_voltar():
    ctk.CTkButton(app, text="Voltar", command=tela_inicial).pack(pady=20)


def tela_inicial():
    limpar_tela()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(app, text="FC Career Tracker", font=("Arial", 30, "bold")).pack(pady=25)
    ctk.CTkLabel(app, text="Sistema de análise para Modo Carreira", font=("Arial", 16)).pack(pady=5)

    if carreira:
        texto = f"Carreira ativa: {carreira['nome']} | Time: {carreira['time_atual'].title()}"
        if carreira["selecao_atual"]:
            texto += f" | Seleção: {carreira['selecao_atual'].title()}"
    else:
        texto = "Nenhuma carreira ativa selecionada."

    ctk.CTkLabel(app, text=texto, font=("Arial", 14)).pack(pady=15)

    ctk.CTkButton(app, text="Cadastrar Partida", command=tela_cadastrar_partida).pack(pady=8)
    ctk.CTkButton(app, text="Estatísticas Gerais", command=tela_estatisticas_gerais).pack(pady=8)
    ctk.CTkButton(app, text="Confronto Direto", command=tela_confronto_direto).pack(pady=8)
    ctk.CTkButton(app, text="Listar Partidas", command=tela_listar_partidas).pack(pady=8)
    ctk.CTkButton(app, text="Gerenciar Carreiras", command=tela_gerenciar_carreiras).pack(pady=8)

    
def tela_gerenciar_carreiras():
    limpar_tela()

    ctk.CTkLabel(app, text="Gerenciar Carreiras", font=("Arial", 24, "bold")).pack(pady=20)

    entrada_nome = ctk.CTkEntry(app, placeholder_text="Nome da carreira", width=300)
    entrada_nome.pack(pady=5)

    entrada_time = ctk.CTkEntry(app, placeholder_text="Time atual", width=300)
    entrada_time.pack(pady=5)

    entrada_selecao = ctk.CTkEntry(app, placeholder_text="Seleção atual (opcional)", width=300)
    entrada_selecao.pack(pady=5)

    modo_var = ctk.StringVar(value="treinador")
    ctk.CTkOptionMenu(app, values=["treinador"], variable=modo_var, width=300).pack(pady=5)

    mensagem = ctk.CTkLabel(app, text="")
    mensagem.pack(pady=8)

    carreira_ativa = obter_carreira_ativa()

    if carreira_ativa:
        ctk.CTkLabel(
            app,
            text=f"Carreira ativa: {carreira_ativa['nome']}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)

        ctk.CTkLabel(
            app,
            text=f"Time atual: {carreira_ativa['time_atual'].title()}"
        ).pack(pady=3)

        selecao_texto = carreira_ativa["selecao_atual"].title() if carreira_ativa["selecao_atual"] else "Nenhuma"

        ctk.CTkLabel(
            app,
            text=f"Seleção atual: {selecao_texto}"
        ).pack(pady=3)

        entrada_novo_time = ctk.CTkEntry(app, placeholder_text="Novo time atual", width=300)
        entrada_novo_time.pack(pady=5)

        entrada_nova_selecao = ctk.CTkEntry(app, placeholder_text="Nova seleção atual (opcional)", width=300)
        entrada_nova_selecao.pack(pady=5)

        mensagem_atualizacao = ctk.CTkLabel(app, text="")
        mensagem_atualizacao.pack(pady=5)

        def atualizar_carreira_ativa():
            novo_time = entrada_novo_time.get().strip().lower()
            nova_selecao = entrada_nova_selecao.get().strip().lower()

            if not novo_time:
                mensagem_atualizacao.configure(text="Digite o novo time.")
                return

            conexao = conectar()
            cursor = conexao.cursor()

            cursor.execute("""
            UPDATE carreiras
            SET time_atual = ?, selecao_atual = ?
            WHERE id = ?
            """, (
                novo_time,
                nova_selecao,
                carreira_ativa["id"]
            ))

            conexao.commit()
            conexao.close()

            mensagem_atualizacao.configure(text="Carreira atualizada com sucesso!")
            tela_gerenciar_carreiras()

        ctk.CTkButton(
            app,
            text="Atualizar Time/Seleção",
            command=atualizar_carreira_ativa
        ).pack(pady=10)
        
    def criar_carreira():
        nome = entrada_nome.get().strip()
        time_atual = entrada_time.get().strip().lower()
        selecao_atual = entrada_selecao.get().strip().lower()
        modo = modo_var.get()

        if not nome or not time_atual:
            mensagem.configure(text="Preencha o nome da carreira e o time atual.")
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
        """, (nome, modo, time_atual, selecao_atual))

        carreira_id = cursor.lastrowid

        conexao.commit()
        conexao.close()

        salvar_carreira_ativa(carreira_id)
        mensagem.configure(text="Carreira criada e ativada com sucesso!")

        tela_gerenciar_carreiras()

    ctk.CTkButton(app, text="Criar Carreira", command=criar_carreira).pack(pady=10)

    ctk.CTkLabel(app, text="Carreiras cadastradas", font=("Arial", 18, "bold")).pack(pady=10)

    frame = ctk.CTkScrollableFrame(app, width=750, height=180)
    frame.pack(pady=5)

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, nome_carreira, modo, time_atual, selecao_atual
    FROM carreiras
    ORDER BY id DESC
    """)

    carreiras = cursor.fetchall()
    conexao.close()

    if not carreiras:
        ctk.CTkLabel(frame, text="Nenhuma carreira cadastrada.").pack(pady=10)
    else:
        for carreira in carreiras:
            carreira_id, nome, modo, time_atual, selecao_atual = carreira

            texto = f"{nome} | {modo} | Time: {time_atual.title()}"

            if selecao_atual:
                texto += f" | Seleção: {selecao_atual.title()}"

            linha = ctk.CTkFrame(frame)
            linha.pack(fill="x", pady=5, padx=5)

            ctk.CTkLabel(linha, text=texto, anchor="w").pack(side="left", padx=10)

            ctk.CTkButton(
                linha,
                text="Ativar",
                width=80,
                command=lambda id=carreira_id: ativar_carreira(id)
            ).pack(side="right", padx=10)

    botao_voltar()


def ativar_carreira(carreira_id):
    salvar_carreira_ativa(carreira_id)
    tela_inicial()


def tela_cadastrar_partida():
    limpar_tela()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(app, text="Cadastrar Partida", font=("Arial", 24, "bold")).pack(pady=20)

    if carreira is None:
        ctk.CTkLabel(app, text="Nenhuma carreira ativa selecionada.").pack(pady=10)
        botao_voltar()
        return

    ctk.CTkLabel(app, text=f"Carreira: {carreira['nome']}").pack(pady=5)

    tipo_var = ctk.StringVar(value="clube")
    ctk.CTkOptionMenu(app, values=["clube", "selecao"], variable=tipo_var, width=300).pack(pady=5)

    entrada_competicao = ctk.CTkEntry(app, placeholder_text="Competição", width=300)
    entrada_competicao.pack(pady=5)

    entrada_time_casa = ctk.CTkEntry(app, placeholder_text="Time da casa", width=300)
    entrada_time_casa.pack(pady=5)

    entrada_time_fora = ctk.CTkEntry(app, placeholder_text="Time de fora", width=300)
    entrada_time_fora.pack(pady=5)

    entrada_gols_casa = ctk.CTkEntry(app, placeholder_text="Gols do time da casa", width=300)
    entrada_gols_casa.pack(pady=5)

    entrada_gols_fora = ctk.CTkEntry(app, placeholder_text="Gols do time de fora", width=300)
    entrada_gols_fora.pack(pady=5)

    entrada_data = ctk.CTkEntry(app, placeholder_text="Data da partida AAAA-MM-DD", width=300)
    entrada_data.pack(pady=5)

    mensagem = ctk.CTkLabel(app, text="")
    mensagem.pack(pady=8)

    def salvar_partida():
        tipo_time = tipo_var.get()

        if tipo_time == "clube":
            meu_time_na_partida = carreira["time_atual"]
        else:
            meu_time_na_partida = carreira["selecao_atual"]

        if not meu_time_na_partida:
            mensagem.configure(text="Erro: essa carreira não possui seleção cadastrada.")
            return

        competicao = entrada_competicao.get().strip()
        time_casa = entrada_time_casa.get().strip().lower()
        time_fora = entrada_time_fora.get().strip().lower()
        data_partida = entrada_data.get().strip()

        try:
            gols_casa = int(entrada_gols_casa.get())
            gols_fora = int(entrada_gols_fora.get())
        except ValueError:
            mensagem.configure(text="Erro: os gols precisam ser números.")
            return

        if not competicao or not time_casa or not time_fora or not data_partida:
            mensagem.configure(text="Erro: preencha todos os campos.")
            return

        if meu_time_na_partida not in [time_casa, time_fora]:
            mensagem.configure(text=f"Erro: {meu_time_na_partida.title()} precisa estar na partida.")
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        INSERT INTO partidas (
            carreira_id,
            meu_time_na_partida,
            tipo_time,
            competicao,
            time_casa,
            time_fora,
            gols_casa,
            gols_fora,
            data_partida
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            carreira["id"],
            meu_time_na_partida,
            tipo_time,
            competicao,
            time_casa,
            time_fora,
            gols_casa,
            gols_fora,
            data_partida
        ))

        conexao.commit()
        conexao.close()

        mensagem.configure(text="Partida cadastrada com sucesso!")

        entrada_competicao.delete(0, "end")
        entrada_time_casa.delete(0, "end")
        entrada_time_fora.delete(0, "end")
        entrada_gols_casa.delete(0, "end")
        entrada_gols_fora.delete(0, "end")
        entrada_data.delete(0, "end")

    ctk.CTkButton(app, text="Salvar Partida", command=salvar_partida).pack(pady=10)
    botao_voltar()


def calcular_resultado_partida(meu_time, casa, fora, gols_casa, gols_fora):
    if casa == meu_time:
        meus_gols = gols_casa
        gols_adv = gols_fora
    else:
        meus_gols = gols_fora
        gols_adv = gols_casa

    return meus_gols, gols_adv


def tela_estatisticas_gerais():
    limpar_tela()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(app, text="Estatísticas Gerais", font=("Arial", 24, "bold")).pack(pady=20)

    if carreira is None:
        ctk.CTkLabel(app, text="Nenhuma carreira ativa selecionada.").pack(pady=10)
        botao_voltar()
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT meu_time_na_partida, tipo_time, competicao, time_casa, time_fora, gols_casa, gols_fora, data_partida
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY data_partida ASC
    """, (carreira["id"],))

    partidas = cursor.fetchall()
    conexao.close()

    jogos = vitorias = empates = derrotas = 0
    gols_marcados = gols_sofridos = 0

    for partida in partidas:
        meu_time, _, _, casa, fora, gols_casa, gols_fora, _ = partida

        if not meu_time or meu_time not in [casa, fora]:
            continue

        jogos += 1

        meus_gols, gols_adv = calcular_resultado_partida(meu_time, casa, fora, gols_casa, gols_fora)

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

    frame = ctk.CTkFrame(app, width=550)
    frame.pack(pady=20, padx=20)

    ctk.CTkLabel(frame, text=carreira["nome"], font=("Arial", 18, "bold")).pack(pady=10)
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

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(app, text="Confronto Direto", font=("Arial", 24, "bold")).pack(pady=20)

    if carreira is None:
        ctk.CTkLabel(app, text="Nenhuma carreira ativa selecionada.").pack(pady=10)
        botao_voltar()
        return

    entrada_adversario = ctk.CTkEntry(app, placeholder_text="Digite o adversário", width=300)
    entrada_adversario.pack(pady=10)

    resultado_frame = ctk.CTkScrollableFrame(app, width=800, height=360)
    resultado_frame.pack(pady=10)

    def buscar_confronto():
        for widget in resultado_frame.winfo_children():
            widget.destroy()

        adversario = entrada_adversario.get().strip().lower()

        if not adversario:
            ctk.CTkLabel(resultado_frame, text="Digite um adversário.").pack(pady=10)
            return

        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
        SELECT meu_time_na_partida, tipo_time, competicao, time_casa, time_fora, gols_casa, gols_fora, data_partida
        FROM partidas
        WHERE carreira_id = ?
        AND (time_casa = ? OR time_fora = ?)
        ORDER BY data_partida ASC
        """, (carreira["id"], adversario, adversario))

        partidas = cursor.fetchall()
        conexao.close()

        if not partidas:
            ctk.CTkLabel(resultado_frame, text=f"Nenhuma partida encontrada contra {adversario.title()}.").pack(pady=10)
            return

        jogos = vitorias = empates = derrotas = 0
        gols_marcados = gols_sofridos = 0

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
            meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = partida

            if not meu_time or meu_time not in [casa, fora]:
                continue

            jogos += 1

            meus_gols, gols_adv = calcular_resultado_partida(meu_time, casa, fora, gols_casa, gols_fora)

            gols_marcados += meus_gols
            gols_sofridos += gols_adv

            saldo = meus_gols - gols_adv

            if meus_gols > gols_adv:
                vitorias += 1
                sequencia_vitorias_atual += 1
                sequencia_invicta_atual += 1

                maior_sequencia_vitorias = max(maior_sequencia_vitorias, sequencia_vitorias_atual)
                maior_sequencia_invicta = max(maior_sequencia_invicta, sequencia_invicta_atual)

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
                maior_sequencia_invicta = max(maior_sequencia_invicta, sequencia_invicta_atual)

        if jogos == 0:
            ctk.CTkLabel(resultado_frame, text="Nenhuma partida válida encontrada.").pack(pady=10)
            return

        aproveitamento = ((vitorias * 3 + empates) / (jogos * 3)) * 100

        ctk.CTkLabel(resultado_frame, text=f"Estatísticas contra {adversario.title()}", font=("Arial", 18, "bold")).pack(pady=10)

        dados = [
            f"Jogos: {jogos}",
            f"Vitórias: {vitorias}",
            f"Empates: {empates}",
            f"Derrotas: {derrotas}",
            f"Gols marcados: {gols_marcados}",
            f"Gols sofridos: {gols_sofridos}",
            f"Aproveitamento: {aproveitamento:.1f}%",
            f"Maior sequência de vitórias: {maior_sequencia_vitorias}",
            f"Maior sequência invicta: {maior_sequencia_invicta}"
        ]

        for item in dados:
            ctk.CTkLabel(resultado_frame, text=item).pack(pady=2)

        ctk.CTkLabel(resultado_frame, text="Resumo do confronto", font=("Arial", 16, "bold")).pack(pady=12)

        if melhor_vitoria:
            meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = melhor_vitoria
            ctk.CTkLabel(resultado_frame, text=f"Melhor vitória: {casa.title()} {gols_casa} x {gols_fora} {fora.title()} | {competicao} | {data}").pack(pady=3)
        else:
            ctk.CTkLabel(resultado_frame, text="Melhor vitória: nenhuma vitória.").pack(pady=3)

        if pior_derrota:
            meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = pior_derrota
            ctk.CTkLabel(resultado_frame, text=f"Pior derrota: {casa.title()} {gols_casa} x {gols_fora} {fora.title()} | {competicao} | {data}").pack(pady=3)
        else:
            ctk.CTkLabel(resultado_frame, text="Pior derrota: nenhuma derrota.").pack(pady=3)

        meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = ultimo_confronto
        ctk.CTkLabel(resultado_frame, text=f"Último confronto: {casa.title()} {gols_casa} x {gols_fora} {fora.title()} | {competicao} | {data}").pack(pady=3)

        ctk.CTkLabel(resultado_frame, text="Histórico do confronto", font=("Arial", 16, "bold")).pack(pady=12)

        for partida in partidas:
            meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = partida
            ctk.CTkLabel(resultado_frame, text=f"{data} | {tipo_time} | {competicao} | {casa.title()} {gols_casa} x {gols_fora} {fora.title()}").pack(pady=2)

    ctk.CTkButton(app, text="Buscar", command=buscar_confronto).pack(pady=10)
    botao_voltar()


def tela_listar_partidas():
    limpar_tela()

    carreira = obter_carreira_ativa()

    ctk.CTkLabel(app, text="Partidas Cadastradas", font=("Arial", 24, "bold")).pack(pady=20)

    if carreira is None:
        ctk.CTkLabel(app, text="Nenhuma carreira ativa selecionada.").pack(pady=10)
        botao_voltar()
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id, meu_time_na_partida, tipo_time, competicao, time_casa, time_fora, gols_casa, gols_fora, data_partida
    FROM partidas
    WHERE carreira_id = ?
    ORDER BY data_partida DESC
    """, (carreira["id"],))

    partidas = cursor.fetchall()
    conexao.close()

    if not partidas:
        ctk.CTkLabel(app, text="Nenhuma partida cadastrada nessa carreira.").pack(pady=10)
    else:
        frame = ctk.CTkScrollableFrame(app, width=800, height=350)
        frame.pack(pady=10)

        for partida in partidas:
            id_partida, meu_time, tipo_time, competicao, casa, fora, gols_casa, gols_fora, data = partida

            texto = f"{id_partida} - {data} | {tipo_time} | {competicao} | {casa.title()} {gols_casa} x {gols_fora} {fora.title()}"

            ctk.CTkLabel(frame, text=texto, anchor="w").pack(fill="x", padx=10, pady=5)

    botao_voltar()


tela_inicial()
app.mainloop()
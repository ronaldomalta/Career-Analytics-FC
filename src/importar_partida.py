import re
import sys
import sqlite3
import pytesseract
from PIL import Image
from carreira_ativa import carregar_carreira_ativa

DB_PATH = "data/career_tracker.db"

DEBUG_OCR = False

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def normalizar_nome_time(nome):
    nome = nome.replace("_", " ")
    nome = nome.replace("|", " ")
    nome = nome.replace("]", " ")
    nome = nome.replace("[", " ")
    nome = nome.replace("º", "")
    nome = nome.replace("°", "")
    nome = re.sub(r"\d+", "", nome)
    nome = nome.strip()

    return " ".join(nome.split()).title()


def identificar_competicao(linha):
    linha_upper = linha.upper()

    if "COPA DO NORDESTE" in linha_upper:
        return "Copa do Nordeste"

    if "COPA DO BRASIL" in linha_upper:
        return "Copa do Brasil"

    if "COPA DO MUNDO" in linha_upper:
        return "Copa do Mundo"

    if "PERNAMBUCANO" in linha_upper:
        return "Pernambucano"

    if "BRASILEIR" in linha_upper:
        return "Brasileirão"

    return ""


def limpar_linha_ocr(linha):
    linha = linha.replace("|", " ")
    linha = linha.replace("=", " ")
    linha = linha.replace("_", " ")
    linha = linha.strip()

    return " ".join(linha.split())


def extrair_pre_jogo(caminho_imagem):
    imagem = Image.open(caminho_imagem)

    largura, altura = imagem.size

    recorte = imagem.crop((
        int(largura * 0.00),
        int(altura * 0.05),
        int(largura * 0.60),
        int(altura * 0.55)
    ))

    texto = pytesseract.image_to_string(recorte)

    linhas = []

    for linha in texto.splitlines():
        linha = limpar_linha_ocr(linha)

        if linha:
            linhas.append(linha)

    if DEBUG_OCR:
        print("\n===== OCR PRÉ-JOGO =====")
        for linha in linhas:
            print(linha)

    data = ""
    fase = ""
    competicao = ""

    for linha in linhas:
        linha_upper = linha.upper()

        if "," in linha and (
            "DE" in linha_upper
            or "JAN" in linha_upper
            or "FEV" in linha_upper
            or "MAR" in linha_upper
            or "ABR" in linha_upper
            or "MAI" in linha_upper
            or "JUN" in linha_upper
            or "JUL" in linha_upper
            or "AGO" in linha_upper
            or "SET" in linha_upper
            or "OUT" in linha_upper
            or "NOV" in linha_upper
            or "DEZ" in linha_upper
        ):
            data = linha

        if (
            "RODADA" in linha_upper
            or "OITAVAS" in linha_upper
            or "QUARTAS" in linha_upper
            or "SEMI" in linha_upper
            or "FINAL" in linha_upper
        ):
            fase = linha

        competicao_identificada = identificar_competicao(linha)

        if competicao_identificada:
            competicao = competicao_identificada

    linhas_times = []

    palavras_ignoradas = [
        "DIA",
        "JOGO",
        "HOJE",
        "RODADA",
        "COPA",
        "BRASILEIR",
        "PERNAMBUCANO",
        "MUNDIAL",
        "ANÁLISE",
        "ANALISE",
        "TREINAMENTO",
        "COLETIVA",
        "TAREFAS",
        "SELECIONAR",
        "SAIR",
        "FEED",
        "NOTÍCIAS",
        "NOTICIAS",
        "TUTORIAIS",
        "OPÇÕES",
        "OPCOES",
        "AVANÇO",
        "AVANCO",
        "FC HUB",
        "INICIO",
        "INÍCIO",
        "CENTRAL",
        "NOTIFICACOES",
        "NOTIFICAÇÕES",
        "ELENCO",
        "TRANSFERENCIAS",
        "TRANSFERÊNCIAS",
        "ACADEMIA",
        "ESCRITORIO",
        "ESCRITÓRIO",
        "PERSONALIZAR",
    ]

    for linha in linhas:
        linha_upper = linha.upper()

        if any(palavra in linha_upper for palavra in palavras_ignoradas):
            continue

        if "," in linha:
            continue

        if len(linha.strip()) >= 3:
            linhas_times.append(linha.strip())

    time_casa = ""
    time_fora = ""

    if len(linhas_times) >= 2:
        time_casa = normalizar_nome_time(linhas_times[-2])
        time_fora = normalizar_nome_time(linhas_times[-1])

    if not competicao:
        competicao = "Competição não identificada"

    if not fase:
        fase = "Fase não identificada"

    if not data:
        data = "Data não identificada"

    return {
        "data": data,
        "fase": fase,
        "competicao": competicao,
        "time_casa": time_casa,
        "time_fora": time_fora,
    }


def extrair_pos_jogo(caminho_imagem):
    imagem = Image.open(caminho_imagem)

    largura, altura = imagem.size

    recorte = imagem.crop((
        int(largura * 0.45),
        int(altura * 0.00),
        int(largura * 1.00),
        int(altura * 0.22)
    ))

    texto = pytesseract.image_to_string(recorte)

    if DEBUG_OCR:
        print("\n===== OCR PÓS-JOGO =====")
        print(texto)

    padrao_placar = r"(\d+)\s*[-xX]\s*(\d+)"
    resultado = re.search(padrao_placar, texto)

    if not resultado:
        return None

    gols_casa = int(resultado.group(1))
    gols_fora = int(resultado.group(2))

    return {
        "gols_casa": gols_casa,
        "gols_fora": gols_fora,
    }


def extrair_partida(pre_jogo, pos_jogo):
    dados_pre = extrair_pre_jogo(pre_jogo)
    dados_pos = extrair_pos_jogo(pos_jogo)

    if dados_pos is None:
        return None

    if not dados_pre["time_casa"] or not dados_pre["time_fora"]:
        return None

    return {
        "competicao": dados_pre["competicao"],
        "fase": dados_pre["fase"],
        "data": dados_pre["data"],
        "time_casa": dados_pre["time_casa"],
        "gols_casa": dados_pos["gols_casa"],
        "gols_fora": dados_pos["gols_fora"],
        "time_fora": dados_pre["time_fora"],
    }


def obter_carreira(carreira_id):
    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT time_atual, selecao_atual
    FROM carreiras
    WHERE id = ?
    """, (carreira_id,))

    carreira = cursor.fetchone()
    conexao.close()

    if not carreira:
        return None

    return {
        "time_atual": carreira[0],
        "selecao_atual": carreira[1],
    }


def definir_meu_time_e_tipo(partida, carreira_id):
    carreira = obter_carreira(carreira_id)

    if carreira is None:
        return partida["time_fora"].lower(), "clube"

    time_atual = carreira["time_atual"].lower() if carreira["time_atual"] else ""
    selecao_atual = carreira["selecao_atual"].lower() if carreira["selecao_atual"] else ""

    time_casa = partida["time_casa"].lower()
    time_fora = partida["time_fora"].lower()

    if time_casa == time_atual or time_fora == time_atual:
        return time_atual, "clube"

    if selecao_atual and (time_casa == selecao_atual or time_fora == selecao_atual):
        return selecao_atual, "selecao"

    return partida["time_fora"].lower(), "clube"


def salvar_partida(partida):
    carreira_id = carregar_carreira_ativa()

    if carreira_id is None:
        return False, "Nenhuma carreira ativa selecionada."

    meu_time_na_partida, tipo_time = definir_meu_time_e_tipo(partida, carreira_id)

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute("""
    SELECT id
    FROM partidas
    WHERE carreira_id = ?
    AND competicao = ?
    AND data_partida = ?
    AND time_casa = ?
    AND time_fora = ?
    """, (
        carreira_id,
        partida["competicao"],
        partida["data"],
        partida["time_casa"].lower(),
        partida["time_fora"].lower(),
    ))

    partida_existente = cursor.fetchone()

    if partida_existente:
        conexao.close()
        return False, "Esta partida já foi importada."

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
        data_partida,
        temporada           
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        carreira_id,
        meu_time_na_partida,
        tipo_time,
        partida["competicao"],
        partida["time_casa"].lower(),
        partida["time_fora"].lower(),
        partida["gols_casa"],
        partida["gols_fora"],
        partida["data"],
        partida.get("ano", "")
    ))

    conexao.commit()
    conexao.close()

    return True, "Partida salva no banco com sucesso."


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        pre_jogo = sys.argv[1]
        pos_jogo = sys.argv[2]
    else:
        pre_jogo = "temp/pre_jogo.png"
        pos_jogo = "temp/pos_jogo.png"

    partida = extrair_partida(pre_jogo, pos_jogo)

    if partida is None:
        print("Erro: não foi possível extrair a partida.")
    else:
        print("===== PARTIDA IMPORTADA =====")
        print(f"Competição: {partida['competicao']}")
        print(f"Fase: {partida['fase']}")
        print(f"Data: {partida['data']}")
        print(
            f"{partida['time_casa']} {partida['gols_casa']} x "
            f"{partida['gols_fora']} {partida['time_fora']}"
        )

        sucesso, mensagem = salvar_partida(partida)
        print(mensagem)
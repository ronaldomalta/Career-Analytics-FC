import re
import pytesseract
from PIL import Image
import sqlite3
from carreira_ativa import carregar_carreira_ativa

DB_PATH = "data/career_tracker.db"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

PRE_JOGO = "screenshots/pre_jogo.png"
POS_JOGO = "screenshots/pos_jogo.png"


def limpar_texto_time(texto):
    texto = texto.replace("_", " ")
    texto = texto.replace("|", " ")
    texto = texto.replace("]", " ")
    texto = texto.replace("[", " ")
    texto = texto.replace("s ", " ")

    partes = texto.strip().split()
    partes_limpas = []

    for parte in partes:
        if not any(char.isdigit() for char in parte):
            partes_limpas.append(parte)

    return " ".join(partes_limpas).strip().title()


def extrair_pre_jogo(caminho_imagem):
    imagem = Image.open(caminho_imagem)

    texto = pytesseract.image_to_string(imagem)

    linhas = []

    for linha in texto.splitlines():
        linha = linha.strip()

        if linha:
            linhas.append(linha)

    data = linhas[0]
    fase = linhas[1]
    time_casa = linhas[-2].title()
    time_fora = linhas[-1].title()

    competicao = "Copa do Mundo"

    return {
        "data": data,
        "fase": fase,
        "competicao": competicao,
        "time_casa": time_casa,
        "time_fora": time_fora
    }


def extrair_pos_jogo(caminho_imagem):
    imagem = Image.open(caminho_imagem)

    largura, altura = imagem.size

    recorte = imagem.crop((
        int(largura * 0.62),
        int(altura * 0.03),
        int(largura * 0.97),
        int(altura * 0.15)
    ))

    texto = pytesseract.image_to_string(recorte)

    padrao_placar = r"(\d+)\s*-\s*(\d+)"
    resultado = re.search(padrao_placar, texto)

    if not resultado:
        return None

    gols_casa = int(resultado.group(1))
    gols_fora = int(resultado.group(2))

    antes_placar = texto[:resultado.start()]
    depois_placar = texto[resultado.end():]

    antes_placar = re.sub(r"\d{1,3}:\d{2}\s*\w*", "", antes_placar)

    time_casa = limpar_texto_time(antes_placar)
    time_fora = limpar_texto_time(depois_placar)

    return {
        "time_casa": time_casa,
        "gols_casa": gols_casa,
        "gols_fora": gols_fora,
        "time_fora": time_fora
    }


pre_jogo = extrair_pre_jogo(PRE_JOGO)
pos_jogo = extrair_pos_jogo(POS_JOGO)

if pos_jogo is None:
    print("Erro: não foi possível extrair o placar do pós-jogo.")
else:
    partida = {
        "competicao": pre_jogo["competicao"],
        "fase": pre_jogo["fase"],
        "data": pre_jogo["data"],
        "time_casa": pre_jogo["time_casa"],
        "gols_casa": pos_jogo["gols_casa"],
        "gols_fora": pos_jogo["gols_fora"],
        "time_fora": pre_jogo["time_fora"]
    }

    print("===== PARTIDA IMPORTADA =====")
    print(f"Competição: {partida['competicao']}")
    print(f"Fase: {partida['fase']}")
    print(f"Data: {partida['data']}")
    print(f"{partida['time_casa']} {partida['gols_casa']} x {partida['gols_fora']} {partida['time_fora']}")

carreira_id = carregar_carreira_ativa()

if carreira_id is None:
    print("Erro: nenhuma carreira ativa selecionada.")
else:
    meu_time_na_partida = partida["time_fora"].lower()
    tipo_time = "selecao"

    conexao = sqlite3.connect(DB_PATH)
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
        carreira_id,
        meu_time_na_partida,
        tipo_time,
        partida["competicao"],
        partida["time_casa"].lower(),
        partida["time_fora"].lower(),
        partida["gols_casa"],
        partida["gols_fora"],
        partida["data"]
    ))

    conexao.commit()
    conexao.close()

    print("\nPartida salva no banco com sucesso!")
    print("Carreira ID:", carreira_id)
    print("Meu time na partida:", meu_time_na_partida)
    print("Tipo:", tipo_time)

    print("\nPartida salva no banco com sucesso!")
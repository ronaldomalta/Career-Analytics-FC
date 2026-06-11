import re
import sys
import sqlite3
import pytesseract
from PIL import Image
from carreira_ativa import carregar_carreira_ativa

DB_PATH = "data/career_tracker.db"

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


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

    return {
        "gols_casa": gols_casa,
        "gols_fora": gols_fora
    }


def extrair_partida(pre_jogo, pos_jogo):
    dados_pre = extrair_pre_jogo(pre_jogo)
    dados_pos = extrair_pos_jogo(pos_jogo)

    if dados_pos is None:
        return None

    return {
        "competicao": dados_pre["competicao"],
        "fase": dados_pre["fase"],
        "data": dados_pre["data"],
        "time_casa": dados_pre["time_casa"],
        "gols_casa": dados_pos["gols_casa"],
        "gols_fora": dados_pos["gols_fora"],
        "time_fora": dados_pre["time_fora"]
    }


def salvar_partida(partida):
    carreira_id = carregar_carreira_ativa()

    if carreira_id is None:
        return False, "Nenhuma carreira ativa selecionada."

    meu_time_na_partida = partida["time_fora"].lower()
    tipo_time = "selecao"

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
    partida["time_fora"].lower()
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

    return True, "Partida salva no banco com sucesso."


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        pre_jogo = sys.argv[1]
        pos_jogo = sys.argv[2]
    else:
        pre_jogo = "screenshots/pre_jogo.png"
        pos_jogo = "screenshots/pos_jogo.png"

    partida = extrair_partida(pre_jogo, pos_jogo)

    if partida is None:
        print("Erro: não foi possível extrair a partida.")
    else:
        print("===== PARTIDA IMPORTADA =====")
        print(f"Competição: {partida['competicao']}")
        print(f"Fase: {partida['fase']}")
        print(f"Data: {partida['data']}")
        print(f"{partida['time_casa']} {partida['gols_casa']} x {partida['gols_fora']} {partida['time_fora']}")

        sucesso, mensagem = salvar_partida(partida)
        print(mensagem)
import re
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

CAMINHO_IMAGEM = "temp/pos_jogo.png"


def limpar_texto_time(texto):
    texto = texto.replace("_", " ")
    texto = texto.replace("|", " ")
    texto = texto.replace("]", " ")
    texto = texto.replace("[", " ")
    texto = texto.replace("s ", " ")
    texto = texto.strip()

    partes = texto.split()

    partes_limpas = []

    for parte in partes:
        if not any(char.isdigit() for char in parte):
            partes_limpas.append(parte)

    return " ".join(partes_limpas).strip()


imagem = Image.open(CAMINHO_IMAGEM)

largura, altura = imagem.size

recorte = imagem.crop((
    int(largura * 0.62),
    int(altura * 0.03),
    int(largura * 0.97),
    int(altura * 0.15)
))

texto = pytesseract.image_to_string(recorte)

print("===== TEXTO ENCONTRADO =====")
print(texto)

padrao_placar = r"(\d+)\s*-\s*(\d+)"
resultado = re.search(padrao_placar, texto)

if not resultado:
    print("Placar não encontrado.")
else:
    gols_casa = int(resultado.group(1))
    gols_fora = int(resultado.group(2))

    antes_placar = texto[:resultado.start()]
    depois_placar = texto[resultado.end():]

    # Remove tempo do começo, tipo 90:00, 120:00PR, 45:00
    antes_placar = re.sub(r"\d{1,3}:\d{2}\s*\w*", "", antes_placar)

    time_casa = limpar_texto_time(antes_placar)
    time_fora = limpar_texto_time(depois_placar)

    print("\n===== DADOS EXTRAÍDOS =====")
    print(f"Time casa: {time_casa}")
    print(f"Gols casa: {gols_casa}")
    print(f"Gols fora: {gols_fora}")
    print(f"Time fora: {time_fora}")
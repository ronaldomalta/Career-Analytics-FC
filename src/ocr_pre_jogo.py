import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

CAMINHO_IMAGEM = "screenshots/pre_jogo.png"

imagem = Image.open(CAMINHO_IMAGEM)

texto = pytesseract.image_to_string(imagem)

print("===== TEXTO PRÉ-JOGO =====")
print(texto)
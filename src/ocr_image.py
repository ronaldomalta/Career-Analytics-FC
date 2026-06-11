import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

CAMINHO_IMAGEM = "screenshots/pos_jogo.png"

imagem = Image.open(CAMINHO_IMAGEM)

largura, altura = imagem.size

# recorte do canto superior direito
recorte = imagem.crop((
    int(largura * 0.62),
    int(altura * 0.03),
    int(largura * 0.97),
    int(altura * 0.15)
))

texto = pytesseract.image_to_string(recorte)

print("===== TEXTO ENCONTRADO =====")
print(texto)
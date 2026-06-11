import pytesseract

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

try:
    versao = pytesseract.get_tesseract_version()

    print("Tesseract funcionando!")
    print("Versão:", versao)

except Exception as erro:
    print("Erro ao usar o Tesseract:")
    print(erro)
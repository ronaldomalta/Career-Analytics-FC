texto = """
SEXTA, 17 DE JUL

Oitavas

BE Copa co Mundo tie

AUSTRALIA
BRASIL
"""

linhas = []

for linha in texto.splitlines():
    linha = linha.strip()

    if linha:
        linhas.append(linha)

print("Linhas encontradas:")
print(linhas)

data = linhas[0]
fase = linhas[1]

time_casa = linhas[-2]
time_fora = linhas[-1]

competicao = "Copa do Mundo"

print("\n===== DADOS EXTRAÍDOS =====")
print("Data:", data)
print("Fase:", fase)
print("Competição:", competicao)
print("Time casa:", time_casa)
print("Time fora:", time_fora)
import re

texto = "120:00PR_ Australia 2] 1-3 s Brasil"

padrao_placar = r"(\d+)\s*-\s*(\d+)"

resultado = re.search(padrao_placar, texto)

if resultado:
    gols_casa = int(resultado.group(1))
    gols_fora = int(resultado.group(2))

    print("Placar encontrado!")
    print("Gols casa:", gols_casa)
    print("Gols fora:", gols_fora)
else:
    print("Placar não encontrado.")
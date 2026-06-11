def extrair_times(texto):
    linhas = texto.splitlines()

    for i, linha in enumerate(linhas):
        if "AUSTRALIA" in linha.upper():
            if i + 1 < len(linhas):
                return (
                    linha.strip(),
                    linhas[i + 1].strip()
                )

    return None, None
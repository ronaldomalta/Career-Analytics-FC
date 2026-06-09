import json
import os

CONFIG_PATH = "data/config.json"


def salvar_carreira_ativa(carreira_id):
    os.makedirs("data", exist_ok=True)

    with open(CONFIG_PATH, "w", encoding="utf-8") as arquivo:
        json.dump({"carreira_ativa_id": carreira_id}, arquivo)


def carregar_carreira_ativa():
    if not os.path.exists(CONFIG_PATH):
        return None

    with open(CONFIG_PATH, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)

    return dados.get("carreira_ativa_id")
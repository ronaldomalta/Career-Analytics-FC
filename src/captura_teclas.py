import os
import keyboard
import pyautogui

from importar_partida import extrair_partida, salvar_partida

PASTA_TEMP = "temp"

PRE_JOGO = os.path.join(PASTA_TEMP, "pre_jogo.png")
POS_JOGO = os.path.join(PASTA_TEMP, "pos_jogo.png")


def preparar_pasta():
    os.makedirs(PASTA_TEMP, exist_ok=True)


def capturar_pre_jogo():
    preparar_pasta()

    screenshot = pyautogui.screenshot()
    screenshot.save(PRE_JOGO)

    print("\nPré-jogo capturado com F7!")
    print(f"Arquivo: {PRE_JOGO}")


def capturar_pos_jogo():
    preparar_pasta()

    screenshot = pyautogui.screenshot()
    screenshot.save(POS_JOGO)

    print("\nPós-jogo capturado com F8!")
    print(f"Arquivo: {POS_JOGO}")

    importar_partida_capturada()


def importar_partida_capturada():
    if not os.path.exists(PRE_JOGO):
        print("\nErro: capture o pré-jogo primeiro usando F7.")
        return

    if not os.path.exists(POS_JOGO):
        print("\nErro: capture o pós-jogo primeiro usando F8.")
        return

    print("\nImportando partida capturada...")

    partida = extrair_partida(PRE_JOGO, POS_JOGO)

    if partida is None:
        print("Erro: não foi possível extrair os dados da partida.")
        return

    print("\n===== PRÉVIA DA PARTIDA =====")
    print(f"Competição: {partida['competicao']}")
    print(f"Fase: {partida['fase']}")
    print(f"Data: {partida['data']}")
    print(f"{partida['time_casa']} {partida['gols_casa']} x {partida['gols_fora']} {partida['time_fora']}")

    confirmar = input("\nDeseja salvar essa partida? (s/n): ").strip().lower()

    if confirmar != "s":
        print("Importação cancelada.")
        return

    sucesso, mensagem = salvar_partida(partida)

    print(mensagem)


print("Sistema de captura iniciado.")
print("F7 = capturar pré-jogo")
print("F8 = capturar pós-jogo + importar")
print("ESC = sair")

keyboard.add_hotkey("f7", capturar_pre_jogo)
keyboard.add_hotkey("f8", capturar_pos_jogo)

keyboard.wait("esc")

print("Sistema encerrado.")
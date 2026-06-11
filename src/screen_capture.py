import pyautogui
import cv2
import numpy as np


def capturar_tela():
    screenshot = pyautogui.screenshot()

    frame = np.array(screenshot)

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    return frame


if __name__ == "__main__":
    frame = capturar_tela()

    print("Tela capturada em memória!")
    print("Tamanho da imagem:", frame.shape)

    cv2.imshow("Captura em tempo real", frame)
    cv2.waitKey(0)
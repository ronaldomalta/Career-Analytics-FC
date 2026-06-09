import pyautogui
from datetime import datetime
import os

SCREENSHOT_DIR= "screenshots"

os.makedir(SCREENSHOT_DIR, exist_ok=True)

def capture_screen():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    filename = f"{SCREENSHOT_DIR}/match_{timestamp}.png"

    screenshot = pyautogui.screenshot()
    screenshot.save(filename)

    print(f"Screenshot salva: {filename}")

if __name__ == "__main__":
    input("Pressione ENTER para capturar a tela...")

    capture_screen()
import pyautogui
import time
from PIL import ImageGrab

# printMousePosition()
def printMousePosition():
    while True:
        time.sleep(1)
        print(pyautogui.position())

# takeScreen(x1,y1,x2,y2)
def takeScreen(x1,y1,x2,y2):
    img = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    return img

# showScreen(screen)
def showScreen(screen):
    screen.show()

# altTab()
def altTab():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('tab')
    pyautogui.keyUp('alt')
    pyautogui.keyUp('tab')

# checkPods()
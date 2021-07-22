import pyautogui
from time import time, sleep
from PIL import ImageGrab
from threading import Lock, Thread
import sys

# printMousePosition()
def printMousePosition():
    while True:
        sleep(1)
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
    pyautogui.keyUp('tab')
    pyautogui.keyUp('alt')

#Décorateur chrono !
def chrono(fonction):
    def lancer(*args, **kwargs):
        t_i = time()
        resultat = fonction(*args, **kwargs)
        t_f = time()
        print("temps d'execution (en s):", t_f-t_i)
        return resultat
    return lancer

def zero_pause_pyautogui_decorator(func):
    def wrapper():
        pyautogui.PAUSE = 0
        func()
        pyautogui.PAUSE = 0.1
    return wrapper

def FOCUS_DOFUS_SCREEN():
    dofus_window = pyautogui.getWindowsWithTitle("Dofus")[0]
    if not dofus_window.isActive:
        if dofus_window.isMaximized:
            dofus_window.minimize()
        dofus_window.maximize()
    sleep(1)

def check_color(top_left_corner, bottom_right_corner, color):
    # TODO: fix because it's doesn't work, it is fitted to red only
    x1, y1 = top_left_corner
    x2, y2 = bottom_right_corner
    red, green, blue = color
    
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    pix = img.load()
    
    for pix_x in range(img.size[0]):
        for pix_y in range(img.size[1]):
            r, g, b = pix[(pix_x, pix_y)]
            if r > red and g < green and b < blue:
                return True
    return False

def check_pixel_color(pixel_position, color):
    x, y = pixel_position
    im = pyautogui.screenshot(region=(x, y, 1, 1))
    return im.getpixel((0,0)) == color

def check_image(image_path, region, grayscale=True, confidence=.65):
    coordinates = pyautogui.locateOnScreen(image_path, grayscale=grayscale, confidence=confidence, region=region)
    return coordinates is not None

class KillableThread(Thread):
    def __init__(self, *args, **keywords):
        Thread.__init__(self, *args, **keywords)
        self.killed = False
    
    def start(self):
        self.__run_backup = self.run
        self.run = self.__run      
        Thread.start(self)
    
    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup
    
    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None
    
    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace
    
    def kill(self):
        self.killed = True

class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    Source: https://refactoring.guru/fr/design-patterns/singleton/python/example#example-0
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
# checkPods()
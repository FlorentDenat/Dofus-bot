import pyautogui
import pyperclip
from time import time, sleep
from PIL import ImageGrab
from threading import Lock, Thread
import sys
import cv2
import numpy as np

#############################################################
# Goal: return the position of the template on the image
# Author: Dauriac Paul, Denat Florent
#############################################################
def find_position(image,template):
	img_rgb = cv2.imread(image)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

	template = cv2.imread(template,0)
	w, h = template.shape[::-1]

	# Apply template Matching
	res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
	# Specify a threshold for the template matching
	threshold = 0.8
	# Store the location of the template in the image
	loc = np.where( res >= threshold)
	# If we don't find the template, we return (-1,-1) to say that we don't have position.
	if(len(loc[0]) == 0):
		return (-1,-1)
	# * to get the value of the array
	# zip returns an iterator of tuples based on the iterable objects.
	for pt in zip(*loc[::-1]):
		return (pt[0],pt[1]+h)

# print_mouse_position()
def print_mouse_position():
    while True:
        sleep(1)
        print(pyautogui.position())

# take_screen(x1,y1,x2,y2)
def take_screen(pixelregion):
    (x1,y1),(x2,y2) = pixelregion
    img = ImageGrab.grab(bbox=(x1,y1,x2,y2))
    return img

# show_screen(screen)
def show_screen(screen):
    screen.show()

def click(pos):
    x,y = pos
    pyautogui.moveTo(x, y)
    pyautogui.click()

# alt_tab()
def alt_tab():
    pyautogui.keyDown('alt')
    pyautogui.keyDown('tab')
    pyautogui.keyUp('tab')
    pyautogui.keyUp('alt')

# new_tab()
def new_tab():
    pyautogui.keyDown('ctrl')
    pyautogui.keyDown('t')
    pyautogui.keyUp('ctrl')
    pyautogui.keyUp('t')

# write(string word)
def write(word):
    pyautogui.write(word, interval=0.01)

def write_special(word):
    pyperclip.copy(word)
    pyautogui.hotkey("ctrl", "v")

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

def find_color(top_left_corner, bottom_right_corner, color):
    x1, y1 = top_left_corner
    x2, y2 = bottom_right_corner
    red, green, blue = color
    
    img = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    pix = img.load()
    
    for pix_x in range(img.size[0]):
        for pix_y in range(img.size[1]):
            r, g, b = pix[(pix_x, pix_y)]
            if r == red and g == green and b == blue:
                return (pix_x,pix_y)
    return (-1,-1)

def check_pixel_color(pixel_position, color):
    x, y = pixel_position
    im = pyautogui.screenshot(region=(x, y, 1, 1))
    return im.getpixel((0,0)) == color

def check_area_color(start_position,end_position, color):
    x1, y1 = start_position
    x2, y2 = end_position
    sizex = x2 -x1
    sizey = y2 -y1
    im = pyautogui.screenshot(region=(x1, y1, sizex, sizey))
    for i in range(sizex):
        for j in range(sizey):
            if im.getpixel((i,j)) == color:
                return True
    return False

def get_pixel_color(pixel_position):
    x, y = pixel_position
    im = pyautogui.screenshot(region=(x, y, 1, 1))
    return im.getpixel((0,0))

def check_image(image_path, region, grayscale=True, confidence=.65):
    coordinates = pyautogui.locateOnScreen(image_path, grayscale=grayscale, confidence=confidence, region=region)
    return coordinates is not None

def manhattan_distance(p1,p2):
    return (abs(p1[0]-p2[0]) + abs(p1[1]-p2[1]))

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
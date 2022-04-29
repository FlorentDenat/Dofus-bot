from src.navigation import *

class GenerateGraph:
    def __init__(self):
        self.navigation = Navigation()
        self.graphGenerate = {}
        self.mapsKnown = []
        self.mapsToCheck = []

    #Creer le graph auto : Sur une map, check les accessibles autour et où cliquer.
    # Noter dans le graph, et mettre les maps notées dans les maps a voir. (save dans un fichier pour recommencer)
    # Aller dans la map connu la plus proche et recommencer.

    # Pour faire ça commencer par tester sur un petit echantillon créé a la main. 
    # Quand les fonctions de déplacement fonctionnent, on rempli.

    def checkAdjMapPixels(start,end,mid):
        pyautogui.moveTo(mid[0],mid[1])
        sleep(0.1)
        checkArrow()
        for i in range(1,20):
            pyautogui.moveTo(start[0] + i*((start[0]-end[0])/20),start[1] + i*((start[1]-end[1])/20))
            # ON CHERCHE UN PIXEL NOIR DANS UN SCREEN TACTIK
            checkArrow()

    def checkAdjMap(self,direction):
        if direction == 'u':
            coord_click = self.checkAdjMapPixels(PixelMoove.UP_START,PixelMoove.UP_END,PixelMoove.UP_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0],self.navigation.position[1]-1),coord_click)
            else:
                return coord_click
        elif direction == 'r':
            coord_click = self.checkAdjMapPixels(PixelMoove.RIGHT_START,PixelMoove.RIGHT_END,PixelMoove.RIGHT_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0]+1,self.navigation.position[1]),coord_click)
            else:
                return coord_click
        elif direction == 'd' : 
            coord_click = self.checkAdjMapPixels(PixelMoove.DOWN_START,PixelMoove.DOWN_END,PixelMoove.DOWN_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0],self.navigation.position[1]+1),coord_click)
            else:
                return coord_click
        else:
            coord_click = self.checkAdjMapPixels(PixelMoove.LEFT_START,PixelMoove.LEFT_END,PixelMoove.LEFT_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0]-1,self.navigation.position[1]),coord_click)
            else:
                return coord_click

    def findAdjMaps(self):
        self.graphGenerate[self.navigation.position] = {}
        listDir = ['u','r','d','l']
        for dir in listDir:
            map,coord_click = self.checkAdjMap(dir)
            if map != -1:
                self.graphGenerate[self.navigation.position][map] = coord_click
                self.mapsToCheck.append(map)
        self.mapsKnown.append(self.navigation.position)
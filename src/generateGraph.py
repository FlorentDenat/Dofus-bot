from src.navigation import *
import pickle

class GenerateGraph:
    def __init__(self,graphGenerate,mapsKnown,mapsToCheck):
        self.navigation = Navigation()
        self.graphGenerate = graphGenerate
        self.mapsKnown = mapsKnown
        self.mapsToCheck = mapsToCheck

    #Creer le graph auto : Sur une map, check les accessibles autour et où cliquer.
    # Noter dans le graph, et mettre les maps notées dans les maps a voir. (save dans un fichier pour recommencer)
    # Aller dans la map connu la plus proche et recommencer.
    def check_arrow(self,posx,posy):
        # TROUVER LA BONNE ZONE Où cherche LE NOIR
        # PEUT ETRE FAIRE DES CAS SELON LA FLECHE QU'ON CHERCHE ?
        return check_area_color((posx,posy),(posx+50,posy+50), (0,0,0))

    def check_adj_map_pixels(self,start,end,mid):
        pyautogui.moveTo(mid[0],mid[1])
        sleep(0.1)
        if self.check_arrow(mid[0],mid[1]):
            return (mid[0],mid[1])
        for i in range(1,20):
            pyautogui.moveTo(start[0] + i*((start[0]-end[0])/20),start[1] + i*((start[1]-end[1])/20))
            sleep(0.1)
            if self.check_arrow(start[0] + i*((start[0]-end[0])/20),start[1] + i*((start[1]-end[1])/20)):
                return (start[0] + i*((start[0]-end[0])/20),start[1] + i*((start[1]-end[1])/20))

    def check_adj_map(self,direction):
        if direction == 'u':
            coord_click = self.check_adj_map_pixels(PixelMoove.UP_START,PixelMoove.UP_END,PixelMoove.UP_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0],self.navigation.position[1]-1),coord_click)
            else:
                return coord_click
        elif direction == 'r':
            coord_click = self.check_adj_map_pixels(PixelMoove.RIGHT_START,PixelMoove.RIGHT_END,PixelMoove.RIGHT_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0]+1,self.navigation.position[1]),coord_click)
            else:
                return coord_click
        elif direction == 'd' : 
            coord_click = self.check_adj_map_pixels(PixelMoove.DOWN_START,PixelMoove.DOWN_END,PixelMoove.DOWN_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0],self.navigation.position[1]+1),coord_click)
            else:
                return coord_click
        else:
            coord_click = self.check_adj_map_pixels(PixelMoove.LEFT_START,PixelMoove.LEFT_END,PixelMoove.LEFT_MIDDLE)
            if coord_click != (-1,-1):
                return ((self.navigation.position[0]-1,self.navigation.position[1]),coord_click)
            else:
                return coord_click

    def find_adj_maps(self):
        self.graphGenerate[self.navigation.position] = {}
        listDir = ['u','r','d','l']
        for dir in listDir:
            map,coord_click = self.check_adj_map(dir)
            if map != -1:
                self.graphGenerate[self.navigation.position][map] = coord_click
                if not((map in self.mapsToCheck) or (map in self.mapsKnown)):
                    self.mapsToCheck.append(map)
        self.mapsKnown.append(self.navigation.position)
        if self.navigation.position in self.mapsToCheck:
            self.mapsToCheck.remove(self.navigation.position)
    
    def find_nearest_map(self):
        nearest = self.mapsToCheck[0]
        distance = manhattan_distance(nearest,self.navigation.position)
        for map in self.mapsToCheck[1:]:
            distTest = manhattan_distance(map,self.navigation.position)
            if distTest < distance:
                nearest = map
                distance = distTest
        return nearest

    def start_generate_map(self):
        if (len(self.mapsToCheck) == 0) and (self.navigation.position in self.mapsKnown):
            print("Finish !")
            return True
        elif self.navigation.position in self.mapsKnown:
            self.navigation.move_to(self.find_nearest_map())
        while not((len(self.mapsToCheck) == 0) and (self.navigation.position in self.mapsKnown)):
            self.find_adj_maps()
            #SAVE DATAS
            with open('/data/mapsToCheck.pickle', 'wb') as handle:
                pickle.dump(self.mapsToCheck, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open('/data/mapsKnown.pickle', 'wb') as handle:
                pickle.dump(self.mapsKnown, handle, protocol=pickle.HIGHEST_PROTOCOL)
            with open('/data/graphGenerate.pickle', 'wb') as handle:
                pickle.dump(self.graphGenerate, handle, protocol=pickle.HIGHEST_PROTOCOL)
            #UPDATE GRAPH
            self.navigation.graph = self.graphGenerate
            if (len(self.mapsToCheck) != 0):
                self.navigation.move_to(self.find_nearest_map())
        print("Finish !")
        return True

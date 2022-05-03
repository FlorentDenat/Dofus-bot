import cv2
from PIL import ImageGrab, Image
import pytesseract
from src.utils import *
from src.enum.map import *
from src.graph import *
import numpy as np

class Navigation:
    def __init__(self):
        self.position = (0,0)
        #CHANGER LA MANIERE DE LOAD LE GRAPH
        self.graph = Graph(MapsGraph.ADJAC_GRAPH.value)


    # find_path(begin,end):
    ## Use simple graph to find path
    def find_path(self,stop):
        return self.graph.a_star_algorithm(self.position, stop)

    # find_direction(map1, map2):
    # Find the direction from one map to another
    def find_direction(self,map1,map2):
        if(map1[0] < map2[0]):
            return 'r'
        elif(map1[0] > map2[0]):
            return 'l'
        elif(map1[1] < map2[1]):
            return 'd'
        else :
            return 'u'

    # convert_path_to_instructions(path)
    ## using the path and a dict of mouse position for each map changement, convert path to clicks
    def convert_path_to_instructions(self,path):
        instructions = []
        self.convert_path_rec(path,instructions)
        return instructions
        
    def convert_path_rec(self,path,res):
        if len(path) == 2:
            res.append(self.find_direction(path[0],path[1]))
        else:
            res.append(self.find_direction(path[0],path[1]))
            self.convert_path_rec(path[1:],res)

    # Move(direction)
    ## Click using the dict of mouse positions for each map
    def move(self,direction):
        if direction == 'u':
            click(self.graph.adjac_lis[self.position][(self.position[0],self.position[1]-1)])
            self.position = (self.position[0],self.position[1]-1)
        elif direction == 'd':
            click(self.graph.adjac_lis[self.position][(self.position[0],self.position[1]+1)])
            self.position = (self.position[0],self.position[1]+1)
        elif direction == 'r':
            click(self.graph.adjac_lis[self.position][(self.position[0]+1,self.position[1])])
            self.position = (self.position[0]+1,self.position[1])
        else:
            click(self.graph.adjac_lis[self.position][(self.position[0]-1,self.position[1])])
            self.position = (self.position[0]-1,self.position[1])

    # Attends que nous changions de map.
    def wait_finish_move(self):
        while(not(check_pixel_color((1000,500), (0,0,0)))):
            sleep(0.1)
        #On a eu l'écran de chargement.
        while(check_pixel_color((1000,500), (0,0,0))):
            sleep(0.1)
        sleep(0.1)
        # On est sur la nouvelle map.

    # follow_instructions(instructions)
    ## suis les instructions de direction (points cardinaux). En gros bouge et attends
    def follow_instructions(self,instructions):
        for instruction in instructions:
            self.move(instruction)
            # SECURITE AU BOUT DE X SECONDES ON CHECK NOTRE POS ?
            self.wait_finish_move()

    # move_to(stop)
    ## Find path, instructions, and then move. Have to wait map change each time.
    def move_to(self,stop):
        path = self.find_path(stop)
        instructions = self.convert_path_to_instructions(path)
        self.follow_instructions(instructions)

    # find_POS()
    def find_POS(self):
        # Le pixel de l'écriture des POS vaut [228 228 226]
        imgGrab = ImageGrab.grab(bbox=(14,74,95,104))
        
        # img = np.array(merged)
        # def get_weight(non_zeros_values):
        #         map_non_zeros_values_to_weight_values = {
        #             0: 0,
        #             3: 1,
        #             5: 2,
        #             255: 3
        #         }
        #         return map_non_zeros_values_to_weight_values[non_zeros_values]

        img = np.array(imgGrab)
        for lines in img:
            for pixels in lines:
                if pixels[0] < 220 or pixels[1] < 220 or pixels[2] < 220:
                    pixels[0] = 0
                    pixels[1] = 0
                    pixels[2] = 0
                else:
                    pixels[0] = 255
                    pixels[1] = 255
                    pixels[2] = 255
        # test = np.count_nonzero(img, axis=2)
        # v_get_weight = np.vectorize(get_weight)
        # test = np.array(list(map(v_get_weight, test)))

        # Connect text with a horizontal shaped kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,1))
        img = cv2.dilate(img, kernel, iterations=2)

        # Invert image and OCR
        result = 255 - img
        # cv2.imshow("result", result)
        # cv2.waitKey(0)
        # cv2.imwrite("merged.png", result)
        data = pytesseract.image_to_string(result, lang='eng',config='--psm 6 -c tessedit_char_whitelist=0123456789-,')
        pos_string = data.strip()
        if pos_string[-1] == ",":
            pos_string = pos_string[:-1]
        pos_split = pos_string.split(",")
        self.position = (int(pos_split[0]),int(pos_split[1]))
        return self.position

# pos = Navigation()
# path = [(0, 0), (0, 1), (1, 1),(0,1),(0,0)]
# print(pos.convertPath(path))    
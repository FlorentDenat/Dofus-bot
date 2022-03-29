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
        self.graph = Graph(MapsGraph.adjac_lis_dof)


    # FindPath(begin,end):
    ## Use simple graph to find path
    def findPath(self,stop):
        return self.graph.a_star_algorithm(self.position, stop)

    # findDirection(map1, map2):
    # Find the direction from one map to another
    def findDirection(self,map1,map2):
        if(map1[0] < map2[0]):
            return 'r'
        elif(map1[0] > map2[0]):
            return 'l'
        elif(map1[1] < map2[1]):
            return 'u'
        else :
            return 'd'

    # ConvertPathToInstructions(path)
    ## using the path and a dict of mouse position for each map changement, convert path to clicks
    def convertPathToInstructions(self,path):
        instructions = []
        self.convertPathRec(path,instructions)
        return instructions
        
    def convertPathRec(self,path,res):
        if len(path) == 2:
            res.append(self.findDirection(path[0],path[1]))
        else:
            res.append(self.findDirection(path[0],path[1]))
            self.convertPathRec(path[1:],res)

    # Move(direction)
    ## Click using the dict of mouse positions for each map
    def move(self,direction):
        if direction == 'u':
            click(MapsGraph.adjac_lis_dof[self.position][(self.position[0]+1,self.position[1])])
        elif direction == 'd':
            click(MapsGraph.adjac_lis_dof[self.position][(self.position[0]-1,self.position[1])])
        elif direction == 'r':
            click(MapsGraph.adjac_lis_dof[self.position][(self.position[0],self.position[1]+1)])
        else:
            click(MapsGraph.adjac_lis_dof[self.position][(self.position[0],self.position[1]-1)])

    # followInstructions(instructions)
    ## suis les instructions de direction (points cardinaux). En gros bouge et attends
    def followInstructions(self,instructions):
        for instruction in instructions:
            self.move(instruction)
            # IMPLEMENTER UNE FONCTION QUI VERIFIE QU'ON A BOUGE
            # ATTENDRE DE VOIR UN PIXEL NOIR, PUIS PLUS NOIR ?
            # SECURITE AU BOUT DE X SECONDES ON CHECK NOTRE POS ?
            sleep(5)

    # MoveTo(stop)
    ## Find path, instructions, and then move. Have to wait map change each time.
    def moveTo(self,stop):
        path = self.findPath(stop)
        instructions = self.convertPathToInstructions(path)

    # findPOS()
    def findPOS(self):
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
        self.position = data.strip()
        return self.position

# pos = Navigation()
# path = [(0, 0), (0, 1), (1, 1),(0,1),(0,0)]
# print(pos.convertPath(path))    
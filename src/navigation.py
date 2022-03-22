import cv2
from PIL import ImageGrab, Image
import pytesseract
from src.utils import *
import numpy as np

class Navigation:
    def __init__(self):
        self.vertical_position = 0
        self.horizontal_position = 0


    # FindPath(begin,end):
    ## Use simple graph to find path
    # graph = {'A': ['B', 'E', 'C'],
    #             'B': ['A', 'D', 'E'],
    #             'C': ['A', 'F', 'G'],
    #             'D': ['B', 'E'],
    #             'E': ['A', 'B', 'D'],
    #             'F': ['C'],
    #             'G': ['C']}
    # ConvertPathToInstructions(path)
    ## using the path and a dict of mouse position for each map changement, convert path to clicks
    # Move(direction)
    ## Click using the dict of mouse positions for each map
    # MoveTo(position)
    ## Find path, instructions, and then move. Have to wait map change each time.
    # findPOS()
    def findPOS():
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
        return data.strip()
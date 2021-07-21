import cv2
from PIL import ImageGrab, Image
import pytesseract
from src.utils import *
import numpy as np

# Move(direction)
# MoveTo(position)
# findPOS()
def findPOS():
    imgGrab = ImageGrab.grab(bbox=(14,74,95,104))
    # merged = Image.new("RGB", (1150, 115))
    # number_box_start = [(585,395), (737, 395), (890, 395), (1040, 395), (1195, 395), (585,548), (737, 548), (890, 548), (1040, 548), (1195, 548)]
        
    # for i in range(10):
    #     img = ImageGrab.grab(bbox=(number_box_start[i][0]+10,number_box_start[i][1]+10,number_box_start[i][0]+125,number_box_start[i][1]+125))
    #     merged.paste(img, (int(i * 115),0))
    
    # img = np.array(merged)
    def get_weight(non_zeros_values):
            map_non_zeros_values_to_weight_values = {
                0: 0,
                3: 1,
                5: 2,
                255: 3
            }
            return map_non_zeros_values_to_weight_values[non_zeros_values]

    img = np.array(imgGrab)
    test = np.count_nonzero(img, axis=2)
    v_get_weight = np.vectorize(get_weight)
    test = np.array(list(map(v_get_weight, test)))
    print(test)
    # img = img[:, :, ::-1].copy()
    # img[:,:,0] = np.zeros([img.shape[0], img.shape[1]])
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("Output In Grayscale", gray)
    # cv2.waitKey(0)
    # thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # cv2.imshow("threshold", thresh)
    # cv2.waitKey(0)

    # Connect text with a horizontal shaped kernel
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,3))
    # cv2.imshow("kernel", kernel)
    # cv2.waitKey(0)
    # dilate = cv2.dilate(thresh, kernel, iterations=1)
    # cv2.imshow("dilate", dilate)
    # cv2.waitKey(0)
    # PEUT ETRE ?
    # closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

    # Remove non-text contours using aspect ratio filtering
    # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    # for c in cnts:
    #     x,y,w,h = cv2.boundingRect(c)
    #     aspect = w/h
    #     if aspect < 3:
    #         cv2.drawContours(thresh, [c], -1, (0,0,0), -1)
    # cv2.imshow("thresh2", thresh)
    # cv2.waitKey(0)

    # Invert image and OCR
    result = 255 - img
    # result = cv2.GaussianBlur(result,(5,5),cv2.BORDER_DEFAULT)
    cv2.imshow("result", result)
    cv2.waitKey(0)
    cv2.imwrite("merged.png", result)
    data = pytesseract.image_to_string(result, lang='eng',config='--psm 6 -c tessedit_char_whitelist=123456789-,')
    return data.strip()
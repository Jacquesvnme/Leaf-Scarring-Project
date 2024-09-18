import cv2
import numpy as np
from matplotlib import pyplot as plt

def calibration_cube_filter(path):
    input_image = cv2.imread(path)
    h, w = input_image.shape[:2]
    
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV) 

    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Grayscale', input_image)

    sensitivity = 10
    lower_white = np.array([0,0,100-sensitivity])
    upper_white = np.array([0,sensitivity,255])
    
    mask = cv2.inRange(hsv, lower_white, upper_white)
    result = cv2.bitwise_and(input_image, input_image, mask = mask)

    cv2.imshow("Calibration Cube Filter Image", result)
    cv2.imwrite("./images/results/calibration_cube_filter.jpg", result)



    image = cv2.imread(path)
    mask = np.zeros(image.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
    rectangle = (1, 1, int(w/5), int(h/5))
    cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 3, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    image_segmented = image * mask2[:, :, np.newaxis]
    cv2.imshow("Result", image_segmented)


    cv2.waitKey(0) 

cv2.destroyAllWindows() 

#path = './images/data1.png'
path = './images/data2.jpg'
calibration_cube_filter(path)
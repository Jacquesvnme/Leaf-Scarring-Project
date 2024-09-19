import cv2
import numpy as np
from matplotlib import pyplot as plt

def calibration_cube_filter(path):
    input_image = cv2.imread(path)
    h, w = input_image.shape[:2]
    
    hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV) 

    sensitivity = 10
    lower_red = np.array([0,50,50]) #example value
    upper_red = np.array([10,255,255]) #example value
    
    mask = cv2.inRange(hsv, lower_red, upper_red)
    input_image = cv2.bitwise_and(input_image, input_image, mask = mask)

    #input_image = cv2.dilate(input_image, kernel, iterations=2)
    #cv2.imshow("Dilation", input_image)

    cv2.imshow("Calibration Cube Filter Image", input_image)
    cv2.imwrite("./images/results/calibration_cube_filter.jpg", input_image)

    cv2.waitKey(0) 

cv2.destroyAllWindows() 

path = './images/data1.png'
#path = './images/data2.jpg'
calibration_cube_filter(path)
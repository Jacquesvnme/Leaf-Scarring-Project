import cv2
import numpy as np

def filter_leaf(path):
    image = cv2.imread(path)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green) 
    
    result = cv2.bitwise_and(image, image, mask = mask) 
    
    cv2.imshow('image', image) 
    cv2.imshow('mask', mask) 
    cv2.imshow('result', result)

    cv2.waitKey(0) 

cv2.destroyAllWindows() 

path = './images/data1.png'
#path = './images/data2.jpg'
filter_leaf(path)
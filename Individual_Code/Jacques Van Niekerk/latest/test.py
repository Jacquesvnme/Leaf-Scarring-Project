import cv2
import numpy as np

def calibration_cube_edge():
    img = cv2.imread('./images/results/calibration_cube_filter.jpg')
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    edges = cv2.Canny(image= image_rgb, threshold1=100, threshold2=700)
    cv2.imshow("Edge", edges)
    
    cv2.waitKey(0)


calibration_cube_edge()
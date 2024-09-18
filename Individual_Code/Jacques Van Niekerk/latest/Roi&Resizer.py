import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import sys

coordinateListY_cube = []
coordinateListX_cube = []


def cube_filter(path):
    cube = cv2.imread(path)
    
    kernel = np.ones((9, 9), np.uint8) 
    input_image = cv2.erode(cube, kernel, cv2.BORDER_REFLECT) 
    
    kernel = np.ones((6, 6), np.uint8) 
    input_image = cv2.erode(input_image, kernel, cv2.BORDER_REFLECT) 

    Gaussian = cv2.GaussianBlur(input_image, (9, 9), 0) 
    
    hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGRA2BGR)
    lower_cube = np.array([201, 191, 191]) 
    upper_cube = np.array([255, 255, 255]) 
    mask = cv2.inRange(hsv, lower_cube, upper_cube)  
    
    result_cube = cv2.bitwise_and(Gaussian, Gaussian, mask = mask) 
    
    kernel = np.ones((9, 9), np.uint8) 
    cube_dilation = cv2.dilate(result_cube, kernel, iterations=2) 
    
    #resize_cube = cv2.resize(cube_dilation, (600, 800))
    
    #cv2.imshow("Resized Cube", cube_dilation)
    cv2.imwrite("./images/results/pre_filer_cube.png", cube_dilation)

    calibration_cube_coordinates("./images/results/pre_filer_cube.png")

    cv2.waitKey(0)



def leaf_filter(path):
    leaf = cv2.imread(path)
    
    hsv = cv2.cvtColor(leaf, cv2.COLOR_BGR2HSV)
    lower_leaf = np.array([35, 40, 40])
    upper_leaf = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_leaf, upper_leaf) 
    
    result_leaf = cv2.bitwise_and(leaf, leaf, mask = mask) 
    
    #resize_leaf = cv2.resize(result_leaf, (600, 800))
    
    #cv2.imshow("Resized Leaf", result_leaf)
    cv2.imwrite("./images/results/pre_filer_leaf.png", result_leaf)

    calibration_cube_coordinates("./images/results/pre_filer_leaf.png")

    cv2.waitKey(0)



def calibration_cube_coordinates(path):
    font = cv2.FONT_HERSHEY_COMPLEX 
    img2 = cv2.imread(str(path), cv2.IMREAD_COLOR) 
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE) 
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY) 
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    for cnt in contours : 
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 
        cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)  
        
        n = approx.ravel()  
        i = 0
        
        for j in n : 
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 
                
                # String containing the co-ordinates. 
                string_Coordinates_cube = str(x) + " " + str(y)
                coordinateListY_cube.append(y) 
                coordinateListX_cube.append(x)
            i = i + 1
            
    return coordinateListY_cube, coordinateListX_cube



def roi(path):
    roi = cv2.imread(path)
    h, w = roi.shape[:2]
    area = h*w
    print("-----------------------------------------")
    print("Full Image Height: ", h)
    print("Full Image Width: ", w)
    print("Full Image Area: ", area)
    
    coordinateListY_cube.sort()
    coordinateListX_cube.sort()

    top_roi = coordinateListY_cube[len(coordinateListY_cube)-1]
    bottom_roi = coordinateListY_cube[0]
    left_roi = coordinateListX_cube[0]
    right_roi = coordinateListX_cube[len(coordinateListX_cube)-1]
    
    roi_height = top_roi - bottom_roi
    roi_width = right_roi - left_roi
    roi_area = roi_height * roi_width
    
    percentage_area = math.ceil((roi_area/area)*100) 
    
    print("-----------------------------------------")
    print("OBJ Height: ", roi_height)
    print("OBJ Width: ", roi_width)
    print("OBJ Area: ", roi_area)
    print("-----------------------------------------")
    print("Area %: ", percentage_area)
    print("-----------------------------------------")
    print("Top Value: " + str(top_roi))
    print("Bottom Value: " + str(bottom_roi))
    print("Left Value: " + str(left_roi))
    print("Right Value: " + str(right_roi))

    mask = np.zeros(roi.shape[:2], np.uint8)
    backgroundModel = np.zeros((1, 65), np.float64)
    foregroundModel = np.zeros((1, 65), np.float64)
    # (startingPoint_x, startingPoint_y, width, height)
    rectangle = (left_roi-150, top_roi-150, roi_width+300, roi_height+300)
    cv2.grabCut(roi, mask, rectangle, backgroundModel, foregroundModel, 3, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')
    image_segmented = roi * mask2[:, :, np.newaxis]

    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(roi, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Segmented Image')
    plt.imshow(cv2.cvtColor(image_segmented, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    
    plt.show()

    # start_point | end_point | color | thickness
    roi = cv2.rectangle(roi, (left_roi, top_roi), (right_roi, bottom_roi), (0, 0, 255), 10)

    if percentage_area > 50:
        margin = 50
    elif percentage_area > 40:
        margin = 100
    elif percentage_area > 30:
        margin = 200
    elif percentage_area > 20:
        margin = 300
    elif percentage_area > 10:
        margin = 500
    
    roi = roi[bottom_roi-margin:top_roi+margin , left_roi-margin:right_roi+margin]
    
    if h > 3000 or w > 3000:
        roi = cv2.resize(roi, (int(w/10), int(h/10)))
    elif h > 2000 or w > 2000:
        roi = cv2.resize(roi, (int(w/5), int(h/5)))
    elif h > 1000 or w > 1000:
        roi = cv2.resize(roi, (int(w/2), int(h/2)))
    elif h < 1000 or w < 1000:
        roi = cv2.resize(roi, (w, h))
    
    cv2.imshow("ROI", roi)
    
    cv2.waitKey(0)

# ! Used to generate a ROI - Region of interest
# ! to crop the image according to co-ordinates of calibration cube & leaf

path = "./images/data3.jpg"
cube_filter(path)
leaf_filter(path)
roi(path)

#TODO: Might need to tweak roi & resizer
# ! Vigorous testing needed
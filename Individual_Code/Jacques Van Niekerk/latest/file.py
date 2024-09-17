import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import sys

stdout = sys.stdout
file = open('./images/results/output.txt', 'w')
sys.stdout = file

def calibration_cube_filter(path):
    input_image = cv2.imread(path)

    kernel = np.ones((9, 9), np.uint8) 
    input_image = cv2.erode(input_image, kernel, cv2.BORDER_REFLECT) 
    
    kernel = np.ones((6, 6), np.uint8) 
    input_image = cv2.erode(input_image, kernel, cv2.BORDER_REFLECT) 
    #cv2.imshow("Erode", input_image) 

    Gaussian = cv2.GaussianBlur(input_image, (9, 9), 0) 
    #cv2.imshow('Gaussian Blurring', Gaussian) 

    hsv = cv2.cvtColor(Gaussian, cv2.COLOR_BGRA2BGR) 
    lower_white = np.array([201, 191, 191]) 
    upper_white = np.array([255, 255, 255]) 
    mask = cv2.inRange(hsv, lower_white, upper_white) 
    result = cv2.bitwise_and(Gaussian, Gaussian, mask = mask) 
    
    kernel = np.ones((9, 9), np.uint8) 
    img_dilation = cv2.dilate(result, kernel, iterations=2) 

    #cv2.imshow("Calibration Cube Filter Image", img_dilation)
    cv2.imwrite("./images/results/calibration_cube_filter.jpg", img_dilation)
    return



def calibration_cube_coordinates():
    font = cv2.FONT_HERSHEY_COMPLEX 
    img2 = cv2.imread('./images/results/calibration_cube_filter.jpg', cv2.IMREAD_COLOR) 
    img = cv2.imread('./images/results/calibration_cube_filter.jpg', cv2.IMREAD_GRAYSCALE) 
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY) 
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    coordinateListY_cube = []
    coordinateListX_cube = []

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

                if(i == 0): 
                    # text on topmost co-ordinate. 
                    cv2.putText(img2, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))  
                else: 
                    # text on remaining co-ordinates. 
                    cv2.putText(img2, string_Coordinates_cube, (x, y), font, 0.5, (0, 255, 0))  
            i = i + 1

    coordinateListY_cube.sort()
    coordinateListX_cube.sort()

    top_cube = coordinateListY_cube[len(coordinateListY_cube)-1]
    bottom_cube = coordinateListY_cube[0]
    left_cube = coordinateListX_cube[0]
    right_cube = coordinateListX_cube[len(coordinateListX_cube)-1]

    width_cube = top_cube - bottom_cube
    length_cube = right_cube - left_cube
    ratio = math.ceil( (width_cube + length_cube) / 2 )

    print("==============================================")
    print("CALIBRATION CUBE DETAILS\n")
    print("Length: " + str(length_cube) + " px")
    print("Width: " + str(width_cube) + " px")
    print("Ratio: " + str(ratio)+ " (amount of pixel = 2cm)")
    
    return ratio



def leaf_filter(path):
    image = cv2.imread(path)
    
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green) 
    
    filter_result = cv2.bitwise_and(image, image, mask = mask) 

    check = cv2.imwrite("./images/results/filter_result.png", filter_result)


def main_edge_analysis():
    leaf_filter(path)
    
    img = cv2.imread("./images/results/filter_result.png")

    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    edges = cv2.Canny(image= image_rgb, threshold1=100, threshold2=700)

    fig, axs = plt.subplots(1, 2, figsize=(7, 4))

    check = cv2.imwrite("./images/results/edge.png", edges)
    return



def main_coordinates():
    
    main_edge_analysis()

    font = cv2.FONT_HERSHEY_COMPLEX 
    img2 = cv2.imread('./images/results/edge.png', cv2.IMREAD_COLOR) 
    img = cv2.imread('./images/results/edge.png', cv2.IMREAD_GRAYSCALE) 
    l, w = img.shape[:2]
    _, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY) 
    contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

    coordinateListY = []
    coordinateListX = []

    for cnt in contours : 
        approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True)  
        cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)  

        n = approx.ravel()  
        i = 0

        for j in n : 
            if(i % 2 == 0): 
                x = n[i] 
                y = n[i + 1] 

                string_Coordinates = str(x) + " " + str(y)
                coordinateListY.append(y) 
                coordinateListX.append(x)

                if(i == 0):  
                    cv2.putText(img2, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))  
                else: 
                    cv2.putText(img2, string_Coordinates, (x, y), font, 0.5, (0, 255, 0))  
            i = i + 1

    coordinateListY.sort()
    coordinateListX.sort()

    top = coordinateListY[len(coordinateListY)-1]
    bottom = coordinateListY[0]
    left = coordinateListX[0]
    right = coordinateListX[len(coordinateListX)-1]

    ratio = calibration_cube_coordinates()

    pixel_width = (top - bottom)
    pixel_length = (right - left)

    width_of_object = round(((top - bottom)/ratio) * 2, 4)
    length_of_object = round(((right - left)/ratio) * 2, 4)
    print("==============================================")
    print("LENGTH & WIDTH RESULTS\n")
    print("These results are for the object in\nquestion (the Leaf)")
    print("----------------------------------------------")
    print("Pixel Length: " + str(pixel_length) + " px")
    print("Pixel Width: " + str(pixel_width) + " px")
    print("Length: " + str(length_of_object) + " cm")
    print("Width: " + str(width_of_object) + " cm")
    #print("Area: " + round(width_of_object*length_of_object,2 + "cm^2"))

    start_point = (left, top)
    end_point = (right, bottom)
    color = (255, 0, 0)
    thickness = 2
    img2 = cv2.rectangle(img2, start_point, end_point, color, thickness)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (int(right/2), top)
    fontScale = 0.5
    color = (255, 255, 255)
    thickness = 1
    img2 = cv2.putText(img2, "Length: {}".format(round(length_of_object,2)), org, font, fontScale, color, thickness, cv2.LINE_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (left, int(top/2))
    fontScale = 0.5
    color = (255, 255, 255)
    thickness = 1
    img2 = cv2.putText(img2, "Width: {}".format(round(width_of_object,2)), org, font, fontScale, color, thickness, cv2.LINE_AA)

    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (int(right/2), int(top/2))
    fontScale = 0.5
    color = (255, 255, 255)
    thickness = 1
    img2 = cv2.putText(img2, "Area: {}".format(round(width_of_object*length_of_object,2)), org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    check = cv2.imwrite("./images/results/final.png", img2)

    cv2.imshow('img2', img2)  

    if cv2.waitKey(0) & 0xFF == ord('q'):  
        cv2.destroyAllWindows() 
    return




def final_data(path):
    calibration_cube_filter(path)
    ratio = calibration_cube_coordinates()
    main_coordinates()
    image = cv2.imread("./images/results/filter_result.png") # TODO fix code here
    
    l, w = image.shape[:2]

    real_l = round((l/ratio)*2, 4)
    real_w = round((w/ratio)*2, 4)
    real_area = round(real_l * real_w, 4)

    print("==============================================")
    print("WHOLE IMAGE DETAILS\n")
    print("Details here are determined using the\nfull image and does not focus on a\nspecific area as it takes the full\n"
        + "image as data")
    print("----------------------------------------------")
    print("Example\nPixel Length & width is the length & width\nof the image and not just the object (leaf)")
    print("----------------------------------------------")
    print("Pixel Length: " + str(l) + " px")
    print("Pixel Width: " + str(w) + " px")
    print("Pixel area: " + str(l*w) + " px")
    print("----------------------------------------------")
    print("Real length: " + str(real_l) + " cm") 
    print("Real Width: " + str(real_w) + " cm")
    print("Real Area: " + str(real_area) + " cm")

    #kernel = np.ones((9, 9), np.uint8) 
    #image = cv2.dilate(image, kernel, iterations=1) 

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("Gray Filter",gray)
    area = cv2.countNonZero(gray)

    taken_area = math.ceil( (area / (l*w))*100 )
    object_area = round((taken_area/100)*real_area, 4)

    print("==============================================")
    print("OBJECT ONLY DETAILS\n")
    print("Details here focuses only on the object\nidentified. This would be the leaf")
    print("----------------------------------------------")
    print("Area: " + str(area))
    print("% Area of Leaf on image: " + str(taken_area) + " %")
    print("Area of Object (leaf): " + str(object_area) + " cm^2")
    print("----------------------------------------------")

    acuTest(data, object_area, inputData_r)

    #cv2.imshow("Gray", gray)
    cv2.waitKey(0)
    return



def acuTest(data, object_area, inputData_r):
    # Data measured by program
    inputData_p = object_area 
    data_Percentage = round(100 -  (inputData_p/inputData_r)*100,4)
    
    print("Real measured data: " + str(inputData_r) + " cm^2")
    print("Data measured by program: " + str(inputData_p) + " cm^2")
    print("Percentage of accuracy: " + str(data_Percentage) + " %")
    print("----------------------------------------------")



data = "data6"

if data == "data1":
    path = './images/data1.png' 
    inputData_r = 126.04
elif data == "data4":
    path = './images/data4.jpg' 
    inputData_r = 126.04
elif data == "data4":
    path = './images/data5.png'
    inputData_r = 170.97
elif data == "data6":
    path = './images/data6.png'
    inputData_r = 126.04
elif data == "data7":
    path = './images/data7.png'
    inputData_r = 93.10
elif data == "data8":
    path = './images/data8.png'
    inputData_r = 18.24

final_data(path)


file.close()
sys.stdout = stdout
print("Output Data found in text file at ./images/results/")

#TODO fix output for calibration cube details on output file
#! output data gets printed twice as ratio is gained on two separate times
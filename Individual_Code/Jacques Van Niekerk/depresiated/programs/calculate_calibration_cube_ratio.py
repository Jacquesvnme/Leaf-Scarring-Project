import cv2
import numpy as np
from matplotlib import pyplot as plt
import math

# CALIBRATION CUBE RATIO

image = cv2.imread('./data.jpg')

h, w = image.shape[:2]
print("Height = {}, Width = {}".format(h, w))
#ratio = 800 / w
#dim = (800, int(h * ratio)) 

#lower_red = np.array([255, 98, 98]) #darker color
#upper_red = np.array([255, 171, 171]) #brigther color

hsv = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR) 
lower_red = np.array([201, 191, 191])
upper_red = np.array([255, 255, 255]) 
mask = cv2.inRange(hsv, lower_red, upper_red) 
result = cv2.bitwise_and(image, image, mask = mask) 

#resize_aspect = cv2.resize(result, dim)
cv2.imshow("Resized Image", result)
cv2.waitKey(0)

#filename = 'savedImage.jpg'
cv2.imwrite("./new_img_filter.jpg", result)


font = cv2.FONT_HERSHEY_COMPLEX 
img2 = cv2.imread('./new_img_filter.jpg', cv2.IMREAD_COLOR) 
img = cv2.imread('./new_img_filter.jpg', cv2.IMREAD_GRAYSCALE) 
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
            
            # String containing the co-ordinates. 
            string_Coordinates = str(x) + " " + str(y)
            coordinateListY.append(y) 
            coordinateListX.append(x)
            print(string_Coordinates)

            if(i == 0): 
                # text on topmost co-ordinate. 
                cv2.putText(img2, "Arrow tip", (x, y), font, 0.5, (255, 0, 0))  
            else: 
                # text on remaining co-ordinates. 
                cv2.putText(img2, string_Coordinates, (x, y), font, 0.5, (0, 255, 0))  
        i = i + 1



print("----------------------------------")
coordinateListY.sort()
coordinateListX.sort()

top = coordinateListY[len(coordinateListY)-1]
bottom = coordinateListY[0]
left = coordinateListX[0]
right = coordinateListX[len(coordinateListX)-1]

width = top - bottom
length = right - left
ratio = math.ceil( (width + length) / 2 )

print("Top: " + str(top) + " | Bottom: " + str(bottom) + " | Left:" + str(left) + " | Right: " + str(right))
print("Length is: " + str(length) + " | Width is: " + str(width))
print("Ratio is: " + str(ratio))
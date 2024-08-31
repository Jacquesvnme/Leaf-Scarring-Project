
# Python code to find the co-ordinates of 
# the contours detected in an image. 
import numpy as np 
import cv2 
import matplotlib.pyplot as plt

# Reading image 
font = cv2.FONT_HERSHEY_COMPLEX 
img2 = cv2.imread('./images/img_edge.png', cv2.IMREAD_COLOR) 

# Reading same image in another  
# variable and converting to gray scale. 
img = cv2.imread('./images/img_edge.png', cv2.IMREAD_GRAYSCALE) 

#Getting Length and Width of image
l, w = img.shape[:2]

# Converting image to a binary image 
# ( black and white only image). 
_, threshold = cv2.threshold(img, 110, 255, cv2.THRESH_BINARY) 

# Detecting contours in image. 
contours, _= cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 

coordinateListY = []
coordinateListX = []

print("----------------------------------")
print("Outline's Co-ordinates:")
print("X  |  Y")
print("----------------------------------")

# Going through every contours found in the image. 
for cnt in contours : 

    approx = cv2.approxPolyDP(cnt, 0.009 * cv2.arcLength(cnt, True), True) 

    # draws boundary of contours. 
    cv2.drawContours(img2, [approx], 0, (0, 0, 255), 5)  

    # Used to flatted the array containing 
    # the co-ordinates of the vertices. 
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
area = width * length

fake_area = int((width/36)*(length/36))

print("Testing pixel based area calculation")
print("Length is: " + str(length) + " | Width is: " + str(width))
print("Area of Leaf is: " + str(area) + " pixels")
print("Top: " + str(top) + " | Bottom: " + str(bottom) + " | Left:" + str(left) + " | Right: " + str(right))
print("----------------------------------")
print("Testing Fabricated Realistic area calculation")
print("* Assumption - 36pixels = 1cm *")
print("Length is: " + str(length/36) + " | Width is: " + str(width/36))
print("Area of Leaf is: " + str(fake_area) + " pixels")
print("----------------------------------")

#Create Rectangle on image
start_point = (left, top) # left | top
end_point = (right, bottom) # bottom | right
color = (255, 0, 0)
thickness = 2
img2 = cv2.rectangle(img2, start_point, end_point, color, thickness)

#Height text output
font = cv2.FONT_HERSHEY_SIMPLEX
org = (int(right/2), top)
fontScale = 1
color = (255, 255, 255)
thickness = 2
img2 = cv2.putText(img2, "Width: {}".format(width), org, font, fontScale, color, thickness, cv2.LINE_AA)

#Width text output
font = cv2.FONT_HERSHEY_SIMPLEX
org = (left, int(top/2))
fontScale = 1
color = (255, 255, 255)
thickness = 2
img2 = cv2.putText(img2, "Length: {}".format(length), org, font, fontScale, color, thickness, cv2.LINE_AA)

#Area text output
font = cv2.FONT_HERSHEY_SIMPLEX
org = (int(right/2), int(top/2))
fontScale = 1
color = (255, 255, 255)
thickness = 2
img2 = cv2.putText(img2, "Area: {}".format(str(fake_area)), org, font, fontScale, color, thickness, cv2.LINE_AA)

# Showing the final image. 
cv2.imshow('img2', img2)  

# Exiting the window if 'q' is pressed on the keyboard. 
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 

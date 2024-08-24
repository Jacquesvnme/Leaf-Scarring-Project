import cv2 
import numpy as np

# Reading the image using imread() function
image = cv2.imread('image.jpg')

# Extracting the height and width of an image
h, w = image.shape[:2]
# Displaying the height and width
print("Height = {}, Width = {}".format(h, w))

# Calculating the ratio
ratio = 800 / w
# Creating a tuple containing width and height
dim = (800, int(h * ratio))

#cap = cv2.VideoCapture(0) 

while(1): 
    #_, frame = cap.read() 
    # It converts the BGR color space of image to HSV color space 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR) 

    # Threshold of blue in HSV space 
    lower_green = np.array([86, 116, 86])
    upper_green = np.array([185, 217, 191]) 

    # preparing the mask to overlay 
    mask = cv2.inRange(hsv, lower_green, upper_green) 

    Gaussian = cv2.GaussianBlur(image, (7, 7), 0) 
    #cv2.imshow('Gaussian Blurring', Gaussian) 

    # The black region in the mask has the value of 0, 
    # so when multiplied with original image removes all non-blue regions 
    result = cv2.bitwise_and(Gaussian, Gaussian, mask = mask) 
    
    color = (0,0,255)
    thickness = 10
    
    #(x,y)
    y = h
    x = w
    
    x1 = int(x/4)
    x2 = int(x/2)
    x3 = int(x/(4/3))
    
    y1 = int(y/4)
    y2 = int(y/2)
    y3 = int(y/(4/3))
    
    #for all x's
    result = cv2.line(result, (0,y1), (x,y1), color, thickness) #line1
    result = cv2.line(result, (0,y2), (x,y2), color, thickness) #line2
    result = cv2.line(result, (0,y3), (x,y3), color, thickness) #line3
    
    #for all y's
    result = cv2.line(result, (x1,y), (x1,0), color, thickness) #line4
    result = cv2.line(result, (x2,y), (x2,0), color, thickness) #line5
    result = cv2.line(result, (x3,y), (x3,0), color, thickness) #line6
    
    #cv2.imshow('image', image) 
    #cv2.imshow('mask', mask) 
    #cv2.imshow('result', result) 
    
    (B, G, R) = image[320,0]
    print(image[320,0])
    print("R = {}, G = {}, B = {}".format(R, G, B))
    
    #B = image[100, 100, 0]
    #print("B = {}".format(B))
    
    #for i in range(0,960,10):
        #(B, G, R) = image[320,0]
        #if image[320,i] != 0:
            #print("pixel found")
            #break

    resize_aspect = cv2.resize(result, dim)
    #cv2.imshow("Resized Image", resize_aspect)

    cv2.waitKey(0) 

cv2.destroyAllWindows() 
cap.release() 
import numpy as np
import cv2
from matplotlib import pyplot as plt
import math

# MAIN PROGRAM - Foreground remover

image = cv2.imread('./images/img_with_calibration_cube.png')
l, w = image.shape[:2]
mask = np.zeros(image.shape[:2], np.uint8)

backgroundModel = np.zeros((1, 65), np.float64)
foregroundModel = np.zeros((1, 65), np.float64)

rectangle = (0, 100, w, l)

cv2.grabCut(image, mask, rectangle, backgroundModel, foregroundModel, 3, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2)|(mask == 0), 0, 1).astype('uint8')

image_segmented = image * mask2[:, :, np.newaxis]

# Display the segmented image
#plt.subplot(1, 2, 2)
#plt.title('Segmented Image')
#plt.imshow(cv2.cvtColor(image_segmented, cv2.COLOR_BGR2RGB))
#plt.axis('off')

check = cv2.imwrite("./images/new_img_foreground.png", image_segmented)


# MAIN PROGRAM - EDGE IDENTIFIER


img = cv2.imread('./images/new_img_foreground.png')
# Convert BGR image to RGB
image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Apply Canny edge detection
edges = cv2.Canny(image= image_rgb, threshold1=100, threshold2=700)

# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(7, 4))

# Plot the original image
#axs[0].imshow(image_rgb)
#axs[0].set_title('Original Image')

# Plot the blurred image
#axs[1].imshow(edges)
#axs[1].set_title('Image edges')

check = cv2.imwrite("./images/new_img_edge.png", edges)



# MAIN PROGRAM - COORDINATES



# Reading image 
font = cv2.FONT_HERSHEY_COMPLEX 
img2 = cv2.imread('./images/new_img_edge.png', cv2.IMREAD_COLOR) 

# Reading same image in another  
# variable and converting to gray scale. 
img = cv2.imread('./images/new_img_edge.png', cv2.IMREAD_GRAYSCALE) 

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

ratio = 513

width = ((top - bottom)/ratio) * 2 #2cm for cube
length = ((right - left)/ratio) * 2
area = width * length

print("Testing pixel based area calculation")
print("Length is: " + str(length) + " | Width is: " + str(width))
print("Area of Leaf is: " + str(area) + " pixels")
print("Top: " + str(top) + " | Bottom: " + str(bottom) + " | Left:" + str(left) + " | Right: " + str(right))
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
img2 = cv2.putText(img2, "Area: {}".format(str(area)), org, font, fontScale, color, thickness, cv2.LINE_AA)

check = cv2.imwrite("./images/new_img_final.png", img2)

# Showing the final image. 
cv2.imshow('img2', img2)  

# Exiting the window if 'q' is pressed on the keyboard. 
if cv2.waitKey(0) & 0xFF == ord('q'):  
    cv2.destroyAllWindows() 

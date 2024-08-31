import cv2 

# Use to create a more or less realistic calibration cube
path = './images/scrap2.png'
image = cv2.imread(path)
window_name = 'Image'
start_point = (10, 10)
end_point = (82, 82)
color = (255, 255, 255)
thickness = -1
image = cv2.rectangle(image, start_point, end_point, color, thickness)
check = cv2.imwrite("./images/img_with_calibration_cube.png", image)
cv2.imshow(window_name, image) 

cv2.waitKey(0) 
cv2.destroyAllWindows() 
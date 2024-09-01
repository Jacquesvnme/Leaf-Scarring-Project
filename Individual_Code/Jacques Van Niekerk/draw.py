import cv2 as cv

# Use to create a more or less realistic calibration cube
path = './images/img_final.png'
image = cv.imread(path)
window_name = 'Image'
start_point = (10, 10)
end_point = (82, 82)
color = (255, 255, 255)
thickness = -1
image = cv.rectangle(image, start_point, end_point, color, thickness)
check = cv.imwrite("./images/img_with_calibration_cube.png", image)
cv.imshow(window_name, image) 

cv.waitKey(0) 
cv.destroyAllWindows() 
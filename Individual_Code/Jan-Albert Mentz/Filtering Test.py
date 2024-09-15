import cv2
import numpy as np

# Load the image from the file
image_path = 'ImageData.png'
frame = cv2.imread(image_path)

if frame is not None:
    # Convert the BGR color space of image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define threshold for the white cube in HSV space
    lower_white = np.array([0, 0, 200])   # Adjust if necessary
    upper_white = np.array([180, 30, 255])

    # Preparing the mask for the white cube
    cube_mask = cv2.inRange(hsv, lower_white, upper_white)

    # Find contours in the mask to locate the cube
    contours, _ = cv2.findContours(cube_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming the largest white contour is the cube
    cube_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cube_contour)

    # Calculate pixel-to-cm ratio using the width or height of the cube
    cube_size_in_pixels = max(w, h)  # Taking the larger side
    pixel_to_cm_ratio = cube_size_in_pixels / 5.0  # 5 cm cube

    # Print pixel to cm ratio
    print(f'Pixel-to-cm Ratio: {pixel_to_cm_ratio} pixels/cm')

    # Now, detect the leaf using the same green threshold
    lower_green = np.array([35, 40, 40])
    upper_green = np.array([85, 255, 255])

    # Preparing the mask for the green leaf
    leaf_mask = cv2.inRange(hsv, lower_green, upper_green)

    # Apply the mask to the original image to extract the leaf
    leaf = cv2.bitwise_and(frame, frame, mask=leaf_mask)

    # Calculate the number of non-zero (non-black) pixels in the mask (leaf area in pixels)
    leaf_pixels = cv2.countNonZero(leaf_mask)

    # Calculate the leaf area in cm² using the pixel-to-cm ratio
    leaf_area_cm2 = (leaf_pixels / (pixel_to_cm_ratio ** 2))

    # Print the results
    print(f'Number of Leaf Pixels: {leaf_pixels} pixels')
    print(f'Leaf Area: {leaf_area_cm2:.2f} cm²')

    # Resize image for display
    scale_percent = 50  # percent of original size
    width = int(frame.shape[1] * scale_percent / 100)
    height = int(frame.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
    resized_cube = cv2.resize(cv2.bitwise_and(frame, frame, mask=cube_mask), dim, interpolation=cv2.INTER_AREA)
    resized_leaf = cv2.resize(leaf, dim, interpolation=cv2.INTER_AREA)

    # Display the resized images
    cv2.imshow('Original Image', resized_frame)
    cv2.imshow('Extracted Cube', resized_cube)
    cv2.imshow('Extracted Leaf', resized_leaf)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Image not found or path is incorrect!")
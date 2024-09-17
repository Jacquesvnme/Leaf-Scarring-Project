import cv2
import numpy as np

# Load the image from the file
image_path = 'Sample Data/RealImage1.jpg'
frame = cv2.imread(image_path)

if frame is not None:
    # Convert the BGR color space of the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect the white cube for pixel-to-cm ratio
    lower_white = np.array([0, 0, 200])  # Lower bound for white (low saturation, high value)
    upper_white = np.array([180, 55, 255])  # Upper bound for white
    cube_mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(cube_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Assuming the largest purple contour is the cube
        cube_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cube_contour)
        cube_size_in_pixels = max(w, h)  # Taking the larger side
        pixel_to_cm_ratio = cube_size_in_pixels / 5.0  # 5 cm cube
        print(f'Pixel-to-cm Ratio: {pixel_to_cm_ratio} pixels/cm')

        # Detect the green (healthy leaf), brown (scars), and yellow (potential dying) parts of the leaf
        lower_green = np.array([35, 40, 40])  # Hex: #2E3D28
        upper_green = np.array([85, 255, 255])  # Hex: #00FF80
        lower_yellow = np.array([20, 100, 100])  # Hex: #805519
        upper_yellow = np.array([30, 255, 255])  # Hex: #FFFF00
        lower_brown = np.array([10, 50, 20])  # Hex: #332619
        upper_brown = np.array([20, 255, 200])  # Hex: #C89600

        # Masks for green (leaf), yellow (dying parts), and brown (scars)
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)

        # Combine green, yellow, and brown masks to detect the entire leaf
        leaf_mask = cv2.bitwise_or(green_mask, brown_mask)  # Leaf (green + brown)
        leaf_mask = cv2.bitwise_or(leaf_mask, yellow_mask)   # Adding yellow (dying parts)

        # Apply the mask to the original image to extract the leaf, dying parts, and scars
        leaf = cv2.bitwise_and(frame, frame, mask=leaf_mask)
        scars = cv2.bitwise_and(frame, frame, mask=brown_mask)
        unhealthy_part = cv2.bitwise_and(frame, frame, mask=yellow_mask)  # Unhealthy (yellow) part of the leaf

        # Calculate areas (in pixels)
        total_image_pixels = frame.shape[0] * frame.shape[1]  # Total pixels in the image
        cube_pixels = cv2.countNonZero(cube_mask)  # Pixels in the calibration cube
        total_leaf_pixels = cv2.countNonZero(leaf_mask)  # Total leaf (green + yellow + brown) area in pixels
        scar_pixels = cv2.countNonZero(brown_mask)  # Scar area in pixels
        dying_pixels = cv2.countNonZero(yellow_mask)  # Dying parts (yellow) area in pixels
        healthy_pixels = cv2.countNonZero(green_mask)  # Healthy (green) part of the leaf

        # Convert to cm² using the pixel-to-cm ratio
        leaf_area_cm2 = total_leaf_pixels / (pixel_to_cm_ratio ** 2)
        scar_area_cm2 = scar_pixels / (pixel_to_cm_ratio ** 2)
        dying_area_cm2 = dying_pixels / (pixel_to_cm_ratio ** 2)
        healthy_area_cm2 = healthy_pixels / (pixel_to_cm_ratio ** 2)

        # Calculate damage percentage and unhealthy percentage
        damage_percentage = (scar_area_cm2 / leaf_area_cm2) * 100
        unhealthy_percentage = (dying_area_cm2 / leaf_area_cm2) * 100
        healthy_percentage = (healthy_area_cm2 / leaf_area_cm2) * 100

        # Print the results
        print(f'Total Leaf Area (Healthy + Dying + Scars): {leaf_area_cm2:.2f} cm²')
        print(f'Scar Area: {scar_area_cm2:.2f} cm²')
        print(f'Dying Area: {dying_area_cm2:.2f} cm²')
        print(f'Healthy Area: {healthy_area_cm2:.2f} cm²')
        print(f'Damage Percentage: {damage_percentage:.2f}%')
        print(f'Unhealthy (Yellow) Percentage: {unhealthy_percentage:.2f}%')
        print(f'Healthy (Green) Percentage: {healthy_percentage:.2f}%')

        # Print the number of pixels in various parts of the image
        print(f'Total Image Pixels: {total_image_pixels}')
        print(f'Calibration Cube Pixels: {cube_pixels}')
        print(f'Total Leaf Pixels: {total_leaf_pixels}')
        print(f'Scar Pixels: {scar_pixels}')
        print(f'Unhealthy (Yellow) Pixels: {dying_pixels}')
        print(f'Healthy (Green) Pixels: {healthy_pixels}')

        # Resize image for display
        scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        resized_leaf = cv2.resize(leaf, dim, interpolation=cv2.INTER_AREA)
        resized_scars = cv2.resize(scars, dim, interpolation=cv2.INTER_AREA)
        resized_unhealthy = cv2.resize(unhealthy_part, dim, interpolation=cv2.INTER_AREA)
        resized_cube_mask = cv2.resize(cube_mask, dim, interpolation=cv2.INTER_AREA)

        # Display the resized images
        cv2.imshow('Original Image', resized_frame)
        cv2.imshow('Extracted Leaf (Healthy + Dying + Scars)', resized_leaf)
        cv2.imshow('Extracted Scars', resized_scars)
        cv2.imshow('Unhealthy Parts (Yellow)', resized_unhealthy)
        cv2.imshow('Calibration Cube Filter', resized_cube_mask)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Cube not found for pixel-to-cm ratio!")
else:
    print("Image not found or path is incorrect!")


import cv2
import numpy as np

# Load the image from the file
image_path = 'Sample Data/Leaf-with-scars-6.png'
frame = cv2.imread(image_path)

if frame is not None:
    # Convert the BGR color space of the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect the purple cube for pixel-to-cm ratio
    lower_purple = np.array([125, 50, 50])
    upper_purple = np.array([155, 255, 255])
    cube_mask = cv2.inRange(hsv, lower_purple, upper_purple)
    contours, _ = cv2.findContours(cube_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        # Assuming the largest purple contour is the cube
        cube_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(cube_contour)
        cube_size_in_pixels = max(w, h)  # Taking the larger side
        pixel_to_cm_ratio = cube_size_in_pixels / 5.0  # 5 cm cube
        print(f'Pixel-to-cm Ratio: {pixel_to_cm_ratio} pixels/cm')

        # Detect the green (healthy leaf), brown (scars), and yellow (potential dying) parts of the leaf
        lower_green = np.array([35, 40, 40])
        upper_green = np.array([85, 255, 255])
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])
        lower_brown = np.array([10, 50, 20])
        upper_brown = np.array([20, 255, 200])

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

        # Calculate areas (in pixels)
        total_leaf_pixels = cv2.countNonZero(leaf_mask)  # Total leaf (green + yellow + brown) area in pixels
        scar_pixels = cv2.countNonZero(brown_mask)  # Scar area in pixels
        dying_pixels = cv2.countNonZero(yellow_mask)  # Dying parts (yellow) area in pixels

        # Convert to cm² using the pixel-to-cm ratio
        leaf_area_cm2 = total_leaf_pixels / (pixel_to_cm_ratio ** 2)
        scar_area_cm2 = scar_pixels / (pixel_to_cm_ratio ** 2)
        dying_area_cm2 = dying_pixels / (pixel_to_cm_ratio ** 2)

        # Calculate damage percentage
        damage_percentage = (scar_area_cm2 / leaf_area_cm2) * 100

        # Print the results
        print(f'Total Leaf Area (Healthy + Dying + Scars): {leaf_area_cm2:.2f} cm²')
        print(f'Scar Area: {scar_area_cm2:.2f} cm²')
        print(f'Dying Area: {dying_area_cm2:.2f} cm²')
        print(f'Damage Percentage: {damage_percentage:.2f}%')

        # Resize image for display
        scale_percent = 50  # percent of original size
        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)

        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        resized_leaf = cv2.resize(leaf, dim, interpolation=cv2.INTER_AREA)
        resized_scars = cv2.resize(scars, dim, interpolation=cv2.INTER_AREA)

        # Display the resized images
        cv2.imshow('Original Image', resized_frame)
        cv2.imshow('Extracted Leaf (Healthy + Dying + Scars)', resized_leaf)
        cv2.imshow('Extracted Scars', resized_scars)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Cube not found for pixel-to-cm ratio!")
else:
    print("Image not found or path is incorrect!")

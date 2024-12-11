def scar_counting(image_path):
    import cv2
    import numpy as np

    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print("Error: Image not found!")
        return None

    # Convert the image to HSV color space
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV color range for green color of the leaf
    lower_green = np.array([35, 50, 50], dtype=np.uint8)  # Lower bound for green hues
    upper_green = np.array([85, 255, 255], dtype=np.uint8)  # Upper bound for green hues

    # Create a mask for the green regions
    green_mask = cv2.inRange(image_hsv, lower_green, upper_green)

    # Find contours in the green mask
    contours, _ = cv2.findContours(green_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Select the largest contour (assuming it's the main leaf area)
    if len(contours) == 0:
        print("No leaf contour found!")
        return None

    main_contour = max(contours, key=cv2.contourArea)

    # Create a blank mask for the main leaf
    leaf_mask = np.zeros_like(green_mask)
    cv2.drawContours(leaf_mask, [main_contour], -1, 255, thickness=cv2.FILLED)

    # Detect gaps by finding areas within the leaf mask that are not filled
    gaps_mask = cv2.bitwise_and(cv2.bitwise_not(green_mask), leaf_mask)

    # Find contours for gaps
    gap_contours, _ = cv2.findContours(gaps_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize the gap counter
    scar_count = 0

    # Minimum area threshold for a gap (in pixels)
    min_gap_area = 100  # Adjust this value as needed

    # Draw the gaps on the original image
    image_with_gaps = image.copy()

    for contour in gap_contours:
        area = cv2.contourArea(contour)
        if area > min_gap_area:  # Only count gaps above the area threshold
            scar_count += 1
            cv2.drawContours(image_with_gaps, [contour], -1, (0, 0, 255), 2)  # Highlight gap in red

    # Display the results
    resized_original = cv2.resize(image, (300, 300))
    resized_gaps = cv2.resize(image_with_gaps, (800, 800))
    cv2.imshow("Original Image", resized_original)
    cv2.imshow("Image with Gaps Highlighted", resized_gaps)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return scar_count


def process_image(image_path):
    import cv2
    import numpy as np

    # Load the image
    frame = cv2.imread(image_path)
    if frame is None:
        return None

    # Convert the BGR color space of the image to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect the white cube for pixel-to-cm ratio
    lower_white = np.array([0, 0, 200])  # Lower bound for white
    upper_white = np.array([180, 55, 255])  # Upper bound for white
    cube_mask = cv2.inRange(hsv, lower_white, upper_white)
    contours, _ = cv2.findContours(cube_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) == 0:
        return None  # Return None if no cube found for calibration

    # Assuming the largest white contour is the cube
    cube_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cube_contour)

    if w == 0 or h == 0:
        return None

    # Pixel-to-cm ratio calculation
    cube_size_in_pixels = max(w, h)  # Taking the larger side
    pixel_to_cm_ratio = cube_size_in_pixels / 5.0  # 5 cm cube

    # Define color ranges for healthy and scar areas
    lower_Healthy = np.array([40, 100, 60])
    upper_Healthy = np.array([80, 255, 180])
    lower_Unhealthy = np.array([15, 100, 100])
    upper_Unhealthy = np.array([35, 255, 255])
    lower_Scar = np.array([0, 50, 50])
    upper_Scar = np.array([20, 150, 200])

    # Masks for healthy (green), unhealthy (yellow), and scar (brown)
    green_mask = cv2.inRange(hsv, lower_Healthy, upper_Healthy)
    yellow_mask = cv2.inRange(hsv, lower_Unhealthy, upper_Unhealthy)
    brown_mask = cv2.inRange(hsv, lower_Scar, upper_Scar)

    # Combine masks to detect the entire leaf area (including scarred regions)
    leaf_mask = cv2.bitwise_or(green_mask, brown_mask)
    leaf_mask = cv2.bitwise_or(leaf_mask, yellow_mask)

    # Calculate areas in pixels
    total_leaf_pixels = cv2.countNonZero(leaf_mask)
    scar_pixels = cv2.countNonZero(brown_mask)

    # Convert areas to cm² using the pixel-to-cm ratio
    lamina_area_cm2 = total_leaf_pixels / (pixel_to_cm_ratio ** 2)
    scar_area_cm2 = scar_pixels / (pixel_to_cm_ratio ** 2)

    # Calculate damage percentage
    damage_percentage = (scar_area_cm2 / lamina_area_cm2) * 100 if lamina_area_cm2 > 0 else 0

    # Leaf length and width in cm
    x_leaf, y_leaf, w_leaf, h_leaf = cv2.boundingRect(leaf_mask)
    lamina_length_cm = h_leaf / pixel_to_cm_ratio
    lamina_width_cm = w_leaf / pixel_to_cm_ratio

    # Create and return the dictionary with the rounded values
    return {
        "lamina_area": round(lamina_area_cm2, 2),
        "lamina_length": round(lamina_length_cm, 2),
        "lamina_width": round(lamina_width_cm, 2),
        "scar_count": 0,  
        "scar_area": round(scar_area_cm2, 2),
        "damagepercentage": round(damage_percentage, 2)
    }


def analyse_image(image_path):
    output = process_image(image_path)

    scar_count = scar_counting(image_path)
    output["scar_count"] = scar_count

    return output
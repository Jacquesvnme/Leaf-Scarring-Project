import cv2
import numpy as np

# Load the water hyacinth scar image
image_path = r"Leaf_1.png"
image = cv2.imread(image_path)
cv2.imshow("Original", image)

# Copy the image for masking
result = image.copy()

# Convert image to HSV color space
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define HSV color range for brownish scars on water hyacinth
lower_brown = np.array([10, 50, 20])   # Lower bound for brown hues
upper_brown = np.array([20, 255, 200]) # Upper bound for brown hues

# Create mask based on the defined brown color range
brown_mask = cv2.inRange(image_hsv, lower_brown, upper_brown)

# Apply mask to get only the brown regions
result = cv2.bitwise_and(result, result, mask=brown_mask)

# Find contours in the brown mask
contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize a list to keep track of merged contours
merged_contours = []

# Distance threshold in pixels (for 0.1 cm)
distance_threshold = 10  # 0.1 cm in pixels (100 pixels/cm * 0.1 cm)

# Process contours to merge close scars
for contour in contours:
    if len(contour) > 0:
        # Calculate the centroid of the current contour
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            continue

        # Check if this centroid is too close to any existing merged contour centroid
        too_close = False
        for merged_contour in merged_contours:
            # Calculate the distance between the centroids
            merged_M = cv2.moments(merged_contour)
            merged_cX = int(merged_M["m10"] / merged_M["m00"])
            merged_cY = int(merged_M["m01"] / merged_M["m00"])

            distance = np.sqrt((cX - merged_cX) ** 2 + (cY - merged_cY) ** 2)
            if distance < distance_threshold:
                too_close = True
                break

        # If it's not too close to any merged contour, add it
        if not too_close:
            merged_contours.append(contour)

# Count the number of merged scars
scar_count = len(merged_contours)

# Show results
print(f"Total scars identified (merged): {scar_count}")
cv2.imshow('Brown Mask', brown_mask)
cv2.imshow('Result with Brown Scars Highlighted', result)

cv2.waitKey(0)
cv2.destroyAllWindows()
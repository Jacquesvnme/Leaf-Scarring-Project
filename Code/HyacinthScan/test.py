import cv2
import numpy as np
import matplotlib.pyplot as plt

from sections import LeafOutline

image, leaf_contour = LeafOutline.leaf_outline("./assets/input/ImageData.png")

print(leaf_contour)

# Display the segmented image
plt.subplot(1, 2, 1)
plt.title('Original Image')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.axis('off')

cv2.imshow("Heal",image)
cv2.waitKey(0)
cv2.destroyAllWindows()
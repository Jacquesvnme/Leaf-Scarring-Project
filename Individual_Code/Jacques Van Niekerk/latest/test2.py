import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
import sys

#image = cv2.imread("./images/results/filter_result.png")
image = cv2.imread("./images/data6.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
area = cv2.countNonZero(gray)
print(area)
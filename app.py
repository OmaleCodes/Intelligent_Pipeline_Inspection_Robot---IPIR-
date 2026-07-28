import cv2 as cv
import numpy as np

print("OpenCV version:", cv.__version__)
print("NumPy version:", np.__version__)

# Quick sanity check: create and display a blank image
blank = np.zeros((300, 300, 3), dtype=np.uint8)
cv.imshow("Sanity Check", blank)
cv.waitKey(0)
cv.destroyAllWindows()
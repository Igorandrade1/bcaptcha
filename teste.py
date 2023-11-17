import cv2
from os import path
import glob

import cv2

MIN_CONTOUR_AREA = 800
img = cv2.imread("treat_imgs/telanova0.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.blur(gray, (5, 5), 0)
img_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

Contours, Hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for contour in Contours:
    if MIN_CONTOUR_AREA < cv2.contourArea(contour) < 2400:
        [X, Y, W, H] = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        if area > 115:
            print()
        cv2.rectangle(img, (X, Y), (X + W, Y + H), (0, 0, 255), 2)
        #cv2.rectangle(img, (X - 2, Y - 2), (X + W + 2, Y + H + 2), (0, 255, 0), 1)

cv2.imshow('contour', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

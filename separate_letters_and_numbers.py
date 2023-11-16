import cv2
import os
import glob

files = glob.glob('treat_imgs/*')

for file in files:
    img = cv2.imread(file)

    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
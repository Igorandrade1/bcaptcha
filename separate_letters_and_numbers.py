import cv2
from os import path
import glob
import numpy as np
import matplotlib.pyplot as plt
# files = glob.glob('treat_imgs/*')

files = glob.glob('img_for_testing/*')

MIN_CONTOUR_AREA = 300
MAX_CONTOUR_AREA = 2400
MAX_HORIZONTAL_LIMIT = 150
MIN_HORIZONTAL_LIMIT = 30
for file in files:
    img = cv2.imread(file)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.blur(gray, (5, 5), 0)
    img_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Dilatação para unir regiões próximas
    kernel_dilate = np.ones((3, 3), np.uint8)
    img_dilated = cv2.dilate(img_thresh, kernel_dilate, iterations=1)

    # Erosão para remover pequenas conexões
    kernel_erode = np.ones((3, 3), np.uint8)
    img_eroded = cv2.erode(img_dilated, kernel_erode, iterations=1)

    # Remover linhas finas
    kernel_line = np.ones((1, 5), np.uint8)

    img_removed_lines = cv2.morphologyEx(img_eroded, cv2.MORPH_OPEN, kernel_line)

    contours, hierarchy = cv2.findContours(img_removed_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    letter_regions = []

    # Filtrar contornos por letras
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)

        if MIN_CONTOUR_AREA < area < MAX_CONTOUR_AREA:
            [x, y, l, a] = cv2.boundingRect(contour)
            # Adicionar uma condição para verificar o limite horizontal
            if MIN_HORIZONTAL_LIMIT < l < MAX_HORIZONTAL_LIMIT:
                # Check if the contour has no parent (inner contour)
                if hierarchy[0][i][3] == -1:
                    letter_regions.append([x, y, l, a])
                    cv2.rectangle(gray, (x, y), (x + l, y + a), (0, 255, 0), 2)


    # Desenhe retângulos ao redor dos contornos em letter_regions
    for (x, y, l, a) in letter_regions:
        cv2.rectangle(img, (x, y), (x + l, y + a), (0, 255, 0), 2)

    if len(letter_regions) != 5:
        continue
        # Desenhe retângulos ao redor dos contornos encontrados
    img_with_contours = img.copy()

    final_img = cv2.merge([img_thresh] * 3)
    i = 0
    for i, rectangle in enumerate(letter_regions):
        x, y, l, a = rectangle

        img_letter = gray[y - 2:y + a + 2, x - 2:x + l + 2]

        file_name = path.basename(file).replace(".png", f"letter{i}")
        i += 1
        try:
            cv2.imwrite(f'letters/{file_name}.png', img_letter)
        except Exception as e:
            print(e)
        cv2.rectangle(final_img, (x-2, y-2), (x+l+2, y+l+2), (0, 255, 0), 1)
    file_name = path.basename(file)
    cv2.imwrite(f'identify/{file_name}', final_img)



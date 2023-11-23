import cv2
from os import path
import glob
import numpy as np
import matplotlib.pyplot as plt
# files = glob.glob('treat_imgs/*')

files = glob.glob('img_for_testing/*')

for file in files:
    img = cv2.imread(file)

    # cv2.imshow('Original Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blured = cv2.blur(img_gray, (5, 5), 0)
    img_thresh = cv2.adaptiveThreshold(blured, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contours, _ = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    letter_regions = []
    start_value = 810
    while True:

        # Filtrar contornos por letras
        for contour in contours:
            (x, y, l, a) = cv2.boundingRect(contour)

            area = cv2.contourArea(contour)

            if start_value < area < 2400:
                letter_regions.append((x, y, l, a))

        if len(letter_regions) != 5:
            start_value -= 1
            letter_regions = []

        if len(letter_regions) == 5 or start_value == 770:
            break

    # Desenhe retângulos ao redor dos contornos em letter_regions
    for (x, y, l, a) in letter_regions:
        cv2.rectangle(img, (x, y), (x + l, y + a), (0, 255, 0), 2)
    #
    # # Exiba a imagem com os retângulos desenhados
    cv2.imshow('Contornos das Letras', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(letter_regions) != 5:
        continue
        # Desenhe retângulos ao redor dos contornos encontrados
    img_with_contours = img.copy()
    for rectangle in letter_regions:
        x, y, l, a = rectangle
        cv2.rectangle(img_with_contours, (x-2, y-2), (x+l+2, y+l+2), (0, 255, 0), 1)

    final_img = cv2.merge([img_thresh] * 3)
    i = 0
    for rectangle in letter_regions:
        x, y, l, a = rectangle
        img_letter = img_thresh[y-2:y+a+2, x-2:x+l+2]
        file_name = path.basename(file).replace(".png", f"letter{i}")
        i += 1
        try:
            cv2.imwrite(f'letters/{file_name}.png', img_letter)
        except Exception as e:
            print(e)
        cv2.rectangle(final_img, (x-2, y-2), (x+l+2, y+l+2), (0, 255, 0), 1)
    file_name = path.basename(file)
    cv2.imwrite(f'identify/{file_name}', final_img)

    # Aguarde um tempo antes de fechar a janela
    cv2.waitKey(0)
    cv2.destroyAllWindows()

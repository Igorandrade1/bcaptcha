import cv2
from os import path
import glob
import matplotlib.pyplot as plt
files = glob.glob('treat_imgs/*')

for file in files:
    img = cv2.imread(file)

    # cv2.imshow('Original Image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blured = cv2.blur(gray, (5, 5), 0)
    img_thresh = cv2.adaptiveThreshold(blured, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contours, _ = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    letter_regions = []

    # Filtrar contornos por letras
    for contour in contours:
        (x, y, l, a) = cv2.boundingRect(contour)

        area = cv2.contourArea(contour)
        if 800 < area < 2400:
            letter_regions.append((x, y, l, a))

    if len(letter_regions) != 5:
        continue
        # Desenhe retângulos ao redor dos contornos encontrados
    img_with_contours = img.copy()
    for rectangle in letter_regions:
        x, y, l, a = rectangle
        cv2.rectangle(img_with_contours, (x-2, y-2), (x+l+2, y+l+2), (0, 255, 0), 1)

    # Visualize a imagem com os contornos
    plt.imshow(cv2.cvtColor(img_with_contours, cv2.COLOR_BGR2RGB))
    plt.title('Contours on Original Image')
    plt.show()

    final_img = cv2.merge([img_thresh] * 3)
    i = 0
    for rectangle in letter_regions:
        x, y, l, a = rectangle
        img_letter = img_thresh[y-2:y+a+2, x-2:x+l+2]
        file_name = path.basename(file).replace(".png", f"letter{i}")
        i += 1
        cv2.imwrite(f'letters/{file_name}.png', img_letter)
        cv2.rectangle(final_img, (x-2, y-2), (x+l+2, y+l+2), (0, 255, 0), 1)
    file_name = path.basename(file)
    cv2.imwrite(f'identify/{file_name}', final_img)

    # Aguarde um tempo antes de fechar a janela
    cv2.waitKey(0)
    cv2.destroyAllWindows()

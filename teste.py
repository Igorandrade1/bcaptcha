import cv2
import numpy as np

MIN_CONTOUR_AREA = 300
MAX_CONTOUR_AREA = 2400
MAX_HORIZONTAL_LIMIT = 150
MIN_HORIZONTAL_LIMIT = 30
img = cv2.imread("img_for_testing/img_captcha_4592.png")
# img = cv2.imread("treat_imgs/img_captcha_0.png")
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

Contours, Hierarchy = cv2.findContours(img_removed_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Criando uma cópia da imagem original para desenhar os contornos sem alterar a original
contour_img = img.copy()
letter_regions = []
for i, contour in enumerate(Contours):
    area = cv2.contourArea(contour)
    if MIN_CONTOUR_AREA < area < MAX_CONTOUR_AREA:
        [X, Y, W, H] = cv2.boundingRect(contour)
        # Adicionar uma condição para verificar o limite horizontal
        if MIN_HORIZONTAL_LIMIT < W < MAX_HORIZONTAL_LIMIT:
            # Check if the contour has no parent (inner contour)
            if Hierarchy[0][i][3] == -1:
                letter_regions.append([X, Y, W, H])
                cv2.rectangle(contour_img, (X, Y), (X + W, Y + H), (0, 255, 0), 2)
for i, rectangle in enumerate(letter_regions):
    x, y, l, a = rectangle

    img_letter = img[y - 2:y + a + 10, x - 2:x + l + 2]
    #cv2.imshow('Contornos', img_letter)
    #cv2.waitKey(0)
    #cv2.imwrite('img_captcha_4577_letter1.png',img_letter)

    #cv2.destroyAllWindows()
    print()
cv2.imshow('Contornos', contour_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(letter_regions)

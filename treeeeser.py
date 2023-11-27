import cv2
import numpy as np
from os import path, makedirs

MIN_CONTOUR_AREA = 300
MAX_CONTOUR_AREA = 2400
MAX_HORIZONTAL_LIMIT = 150
MIN_HORIZONTAL_LIMIT = 30
img_ori = cv2.imread("bdcaptcha/img_captcha_0.png")
img = cv2.imread("treat_imgs/img_captcha_0.png")
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



cv2.imshow('contour_img', contour_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Carregar a segunda imagem
img2 = cv2.imread("bdcaptcha/img_captcha_6.png")




# Criar uma máscara inicial preenchida com zeros
mask = np.zeros_like(img2, dtype=np.uint8)

# Desenhar os contornos na máscara
for region in letter_regions:
    [X, Y, W, H] = region
    cv2.rectangle(mask, (X, Y), (X+W, Y+H), (255, 255, 255), -1)  # Preencher a região com branco

# Inverter a máscara (para ter branco nas áreas sem contornos)
inverse_mask = cv2.bitwise_not(mask)

# Aplicar um tratamento (conversão para tons de cinza) apenas nas áreas sem contornos
img_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Aplicar o filtro de mediana para reduzir ruído sal-e-pimenta
average_img = cv2.medianBlur(img_gray, 3)

# Aplicar o thresholding de Otsu
_, binary_img = cv2.threshold(average_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# # Aplicar erosão para reduzir ruídos maiores
kernel_erosion = np.ones((5, 5), np.uint8)
img_erodida = cv2.erode(binary_img, kernel_erosion, iterations=1)

black_and_white_img = cv2.bitwise_not(img_erodida)

# Combinação da imagem original com as áreas preservadas e a imagem tratada nas áreas sem contornos
result_img_with_treatment = cv2.bitwise_and(img2, mask) + cv2.bitwise_and(cv2.cvtColor(black_and_white_img, cv2.COLOR_GRAY2BGR), inverse_mask)



# Mostrar a imagem resultante
cv2.imshow('Imagem Resultante', result_img_with_treatment)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


result_img_with_treatment_gray_img = cv2.cvtColor(result_img_with_treatment, cv2.COLOR_BGR2GRAY)

# Iterar pelas regiões dos contornos
for region in letter_regions:
    [X, Y, W, H] = region

    # Iterar pelos pixels dentro da região
    for i in range(X, X + W):
        for j in range(Y, Y + H):
            # Acessar o valor do pixel em (i, j) na imagem result_img_with_treatment_gray_img
            pixel_value = result_img_with_treatment_gray_img[j, i]

            # Se o valor do pixel for maior que 200, pintar a área de preto
            if pixel_value > 200:
                result_img_with_treatment[j, i] = [0, 0, 0]  # BGR (preto)
            else:
                result_img_with_treatment[j, i] = [255, 255, 255]  # BGR (BRANCO)
            # Fazer algo com o valor do pixel (por exemplo, imprimir)
            print(f"Valor do pixel em ({i}, {j}): {pixel_value}")

# Mostrar a imagem resultante com a área destacada
# cv2.imshow('Imagem Resultante com Área Pintada de Preto', result_img_with_treatment)
# cv2.waitKey(0)
# cv2.destroyAllWindows()





# Aplicar limiar adaptativo
_, img_adaptive_thresh = cv2.threshold(result_img_with_treatment_gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Iterar pelas regiões dos contornos
for region in letter_regions:
    [X, Y, W, H] = region

    # Iterar pelos pixels dentro da região
    for i in range(X, X + W):
        for j in range(Y, Y + H):
            # Acessar o valor do pixel na imagem limiarizada
            pixel_value = img_adaptive_thresh[j, i]

            # Inverter as cores dentro da região delimitada pelos contornos
            if pixel_value == 0:
                img_adaptive_thresh[j, i] = 255  # Tornar pixels pretos em brancos
            else:
                img_adaptive_thresh[j, i] = 0  # Tornar pixels brancos em pretos

# Aplicar operação de fechamento para preencher falhas em pixels pretos
kernel_closing = np.ones((5, 5), np.uint8)
img_filled = cv2.morphologyEx(img_adaptive_thresh, cv2.MORPH_CLOSE, kernel_closing)

# ... (o resto do seu código)

# Aplicar operação de dilatação para suavizar as bordas
kernel_dilation = np.ones((3, 3), np.uint8)
img_smoothed = cv2.dilate(img_filled, kernel_dilation, iterations=1)

# ... (o resto do seu código)

# Mostrar a imagem resultante

# Mostrar a imagem resultante
cv2.imshow('ori', img_ori)
cv2.imshow('Imagem com Inversão de Cores e Preenchimento de Falhas', img_filled)
cv2.imshow('Imagem Original', result_img_with_treatment_gray_img)
cv2.imshow('Imagem com Limiar Adaptativo', img_adaptive_thresh)
cv2.imshow('Imagem Suavizada com Dilatação', img_smoothed)
cv2.waitKey(0)
cv2.destroyAllWindows()

print()

cv2.imwrite("img_for_testing/img_for_test.png", img_smoothed)
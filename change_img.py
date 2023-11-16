import cv2
import numpy as np

def apply_filters_to_img(path_img: str, path_save_output_img: str):
    img = cv2.imread(path_img, cv2.IMREAD_GRAYSCALE)

    # Aplique um desfoque para ajudar a conectar regiões próximas
    blurred_img = cv2.GaussianBlur(img, (5, 5), 0)

    # Aplique a binarização para criar uma máscara
    _, mask = cv2.threshold(blurred_img, 200, 255, cv2.THRESH_BINARY_INV)

    # Encontre contornos na máscara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Itere sobre os contornos e pinte de preto aqueles que são pequenos
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 80000:  # Ajuste o valor do limiar conforme necessário
            cv2.drawContours(img, [contour], -1, 0, thickness=cv2.FILLED)

    # Aplicar operação de abertura para remover ruídos brancos
    kernel_open = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_open)

    # Aplicar operação de fechamento para remover pequenos buracos pretos
    kernel_close = np.ones((5, 5), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel_close)

    # Aplicar operação de abertura novamente para remover ruídos brancos menores
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_open)

    # Inverter cores (branco para preto e vice-versa)
    img = cv2.bitwise_not(img)

    # Aplicar Unsharp Masking para mais nitidez
    blurred = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.addWeighted(img, 1.5, blurred, -0.5, 0)

    # Salve a imagem resultante
    cv2.imwrite(path_save_output_img, img)


apply_filters_to_img("test_methods/processed_img_3.png", "test_methods/processed_img_3_after_change_img.png")
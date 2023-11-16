import cv2
from PIL import Image
methods = [
    cv2.THRESH_BINARY,
    cv2.THRESH_BINARY_INV,
    cv2.THRESH_TRUNC,
    cv2.THRESH_TOZERO,
    cv2.THRESH_TOZERO_INV,
]

img = cv2.imread("bdcaptcha/telanova11.png")


# transformar a imagem em escala de cinza

img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

blurred_img = cv2.GaussianBlur(img_gray, (5, 5), 0)

# Aplique a binarização para tornar a imagem em preto e branco

_, img_binary = cv2.threshold(blurred_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)


i = 0
for method in methods:
    i += 1
    _, processed_img = cv2.threshold(img_binary, 127, 255, method or cv2.THRESH_OTSU)
    cv2.imwrite(f'test_methods/processed_img_{i}.png', processed_img)



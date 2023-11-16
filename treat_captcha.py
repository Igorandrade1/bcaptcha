import cv2
import numpy as np
import glob
from os import path
def treat_img(path_origin: str, destiny_path: str = "treat_imgs"):
    files = glob.glob(f"{path_origin}/*")

    for file in files:
        img = cv2.imread(file)

        # Converte a imagem para escala de cinza
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplica o filtro de mediana para reduzir ruído sal-e-pimenta
        average_img = cv2.medianBlur(img_gray, 3)

        # Aplica o thresholding de Otsu
        _, binary_img = cv2.threshold(average_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Aplica erosão para reduzir ruídos maiores
        kernel_erosion = np.ones((5, 5), np.uint8)
        img_erodida = cv2.erode(binary_img, kernel_erosion, iterations=1)

        # Aplica realce de nitidez usando um kernel Laplaciano
        kernel_laplaciano = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
        img_clear = cv2.filter2D(img_erodida, -1, kernel_laplaciano)
        file_name = path.basename(file)
        # Salva a imagem resultante
        cv2.imwrite(path.join(destiny_path, file_name), img_clear)


if __name__ == "__main__":
    treat_img("bdcaptcha")
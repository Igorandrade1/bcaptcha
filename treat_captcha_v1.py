import cv2
import numpy as np
import glob
from os import path


def paint_the_selected_areas_in_the_image(img: str, min_contour_area: int):
    blurred = cv2.blur(img, (5, 5), 0)
    img_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    contours, hierarchy = cv2.findContours(img_thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create a black image to draw the contours

    for contour in contours:
        if cv2.contourArea(contour) < min_contour_area:
            [X, Y, W, H] = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)

            # Calcular o momento para obter a orientação
            moments = cv2.moments(contour)
            if moments['m00'] != 0:
                cx = int(moments['m10'] / moments['m00'])
                cy = int(moments['m01'] / moments['m00'])
                theta = 0.5 * np.arctan2(2 * moments['mu11'], moments['mu20'] - moments['mu02'])

                # Filtrar contornos horizontais (ajuste o ângulo conforme necessário)
                if np.abs(theta) < np.pi / 3:
                    # Preencha os contornos com preto
                    cv2.fillPoly(img, [contour], (0, 0, 0))
                    cv2.rectangle(img, (X, Y), (X + W, Y + H), (0, 0, 255), 2)


min_contour_area = 700

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

        paint_the_selected_areas_in_the_image(img=img_clear, min_contour_area=min_contour_area)
        black_and_white_img = cv2.bitwise_not(img_clear)
        file_name = path.basename(file)
        # Salva a imagem resultante
        cv2.imwrite(path.join(destiny_path, file_name), black_and_white_img)


if __name__ == "__main__":
    treat_img("bdcaptcha")
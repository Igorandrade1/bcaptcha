from keras.models import load_model
from helpers import resize_to_fit
from imutils import paths
import numpy as np
import cv2
import pickle
from treat_captcha_v1 import treat_img
from treat_captcha_v2 import ImageProcessor
from os import path

path.join(path.dirname(__file__), "solve")


folder_treat_img_v1_and_final_img = path.join(path.dirname(__file__), "solve")
original_image_folder_name = "bdcaptcha"


def broken_captcha():
    # importar o modelo treinado e o tradutor
    with open("labels_model.dat", "rb") as translator_file:
        lb = pickle.load(translator_file)

    model = load_model("trained_model.hdf5")

    treat_img(path_origin=folder_treat_img_v1_and_final_img, destiny_path=folder_treat_img_v1_and_final_img)

    processor = ImageProcessor(
        treat_image_folder_name=folder_treat_img_v1_and_final_img,
        original_image_folder_name=original_image_folder_name
    )

    processor.process_file(full_path_to_save_final_file=folder_treat_img_v1_and_final_img)
    # usar o modelo para resolver o captcha

    files = list(paths.list_images("solve"))

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
        image_to_capture_the_letters = gray.copy()
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

        letter_regions = sorted(letter_regions, key=lambda x: x[0])
        # Desenhe retângulos ao redor dos contornos em letter_regions
        for (x, y, l, a) in letter_regions:
            cv2.rectangle(img, (x, y), (x + l, y + a), (0, 255, 0), 2)

            # Desenhe retângulos ao redor dos contornos encontrados
        img_with_contours = img.copy()

        final_img = cv2.merge([img_thresh] * 3)
        forecast = []
        i = 0
        for i, rectangle in enumerate(letter_regions):
            x, y, l, a = rectangle

            img_letter = image_to_capture_the_letters[y - 2:y + a + 10, x - 2:x + l + 2]

            # dar a letra para inteligencia artificial

            img_letter = resize_to_fit(img_letter, 20, 20)

            # tratamento para o keras funcionar (img com 4 dimensoes)
            img_letter = np.expand_dims(img_letter, axis=2)

            img_letter = np.expand_dims(img_letter, axis=0)

            letter_forecast = model.predict(img_letter)
            letter_forecast = lb.inverse_transform(letter_forecast)[0]
            forecast.append(letter_forecast)

            # desenhar letra prevista na imagem final
        forecast_text = "".join(forecast)

        print(forecast_text)
        # return forecast_text


if __name__ == "__main__":
    broken_captcha()
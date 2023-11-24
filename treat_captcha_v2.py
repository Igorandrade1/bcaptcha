import cv2
import numpy as np
from os import path, makedirs, listdir
from typing import Tuple, List, Any


class ImageProcessor:
    def __init__(self, treat_image_folder_name, original_image_folder_name):
        self.full_folder_to_save_the_processed_images = path.join(
            path.dirname(__file__),
            "treat_imgs_v2"
        )
        self.original_image_folder_name = original_image_folder_name
        self.full_folder_original_image = path.join(
            path.dirname(__file__),
            self.original_image_folder_name

        )
        self.treat_image_folder_name = treat_image_folder_name
        self.full_folder_treat_image = path.join(
            path.dirname(__file__),
            self.treat_image_folder_name

        )

        self.current_treat_image = cv2.imread(self.full_folder_treat_image)
        self.img = self.current_treat_image.copy()
        self.letter_regions = []

    def process_file(self):
        for file in listdir(self.full_folder_treat_image):
            file_name = path.basename(file)
            full_path_file_current_treat_image = path.join(self.full_folder_treat_image, file_name)
            full_path_file_current_original_image = path.join(self.full_folder_original_image, file_name)
            if path.isfile(full_path_file_current_treat_image):

                self.current_treat_image = cv2.imread(full_path_file_current_treat_image)
                self.current_treat_image = self.preprocess_image(img=self.current_treat_image)
                self.letter_regions = self.find_contours(
                    img=self.current_treat_image,
                    min_contour_area=300,
                    max_contour_area=2400,
                    max_horizontal_limit=150,
                    min_horizontal_limit=30,
                )
                current_original_image = cv2.imread(full_path_file_current_original_image)
                # Adicione aqui as ações que você deseja realizar para cada arquivo

                mask = np.zeros_like(current_original_image, dtype=np.uint8)

                for region in self.letter_regions:
                    [X, Y, W, H] = region
                    cv2.rectangle(mask, (X, Y), (X + W, Y + H), (255, 255, 255), -1)  # Preencher a região com branco

                # Inverter a máscara (para ter branco nas áreas sem contornos)
                inverse_mask = cv2.bitwise_not(mask)

                # Aplicar um tratamento (conversão para tons de cinza) apenas nas áreas sem contornos
                current_original_image_gray = cv2.cvtColor(current_original_image, cv2.COLOR_BGR2GRAY)
                # Aplicar o filtro de mediana para reduzir ruído sal-e-pimenta
                current_original_image_with_average_filter = cv2.medianBlur(current_original_image_gray, 3)

                # Aplicar o thresholding de Otsu
                _, current_original_image_binary = cv2.threshold(current_original_image_with_average_filter, 0, 255,
                                                                 cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # # Aplicar erosão para reduzir ruídos maiores
                kernel_erosion = np.ones((5, 5), np.uint8)
                current_original_image_eroded = cv2.erode(current_original_image_binary, kernel_erosion, iterations=1)

                current_original_image_black_and_white = cv2.bitwise_not(current_original_image_eroded)
                # Combinação da imagem original com as áreas preservadas e a imagem tratada nas áreas sem contornos
                original_image_result_with_treatment = cv2.bitwise_and(current_original_image, mask) + cv2.bitwise_and(
                    cv2.cvtColor(current_original_image_black_and_white, cv2.COLOR_GRAY2BGR), inverse_mask)

                result_original_image_with_treatment_gray = cv2.cvtColor(original_image_result_with_treatment,
                                                                         cv2.COLOR_BGR2GRAY)

                # Iterar pelas regiões dos contornos
                for region in self.letter_regions:
                    [X, Y, W, H] = region

                    # Iterar pelos pixels dentro da região
                    for i in range(X, X + W):
                        for j in range(Y, Y + H):
                            # Acessar o valor do pixel em (i, j) na imagem result_original_image_with_treatment_gray
                            pixel_value = result_original_image_with_treatment_gray[j, i]

                            # Se o valor do pixel for maior que 200, pintar a área de preto
                            if pixel_value > 200:
                                original_image_result_with_treatment[j, i] = [0, 0, 0]  # BGR (preto)
                            else:
                                original_image_result_with_treatment[j, i] = [255, 255, 255]  # BGR (BRANCO)

                # Aplicar limiar adaptativo
                _, original_image_with_adaptive_thresh = cv2.threshold(
                    result_original_image_with_treatment_gray, 0, 255,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Iterar pelas regiões dos contornos
                for region in self.letter_regions:
                    [X, Y, W, H] = region

                    # Iterar pelos pixels dentro da região
                    for i in range(X, X + W):
                        for j in range(Y, Y + H):
                            # Acessar o valor do pixel na imagem limiarizada
                            pixel_value = original_image_with_adaptive_thresh[j, i]

                            # Inverter as cores dentro da região delimitada pelos contornos
                            if pixel_value == 0:
                                original_image_with_adaptive_thresh[j, i] = 255  # Tornar pixels pretos em brancos
                            else:
                                original_image_with_adaptive_thresh[j, i] = 0  # Tornar pixels brancos em pretos

                # Aplicar operação de fechamento para preencher falhas em pixels pretos
                kernel_closing = np.ones((5, 5), np.uint8)
                original_image_with_filled = cv2.morphologyEx(original_image_with_adaptive_thresh, cv2.MORPH_CLOSE,
                                                              kernel_closing)

                kernel_dilation = np.ones((3, 3), np.uint8)
                original_image_with_smoothed = cv2.dilate(original_image_with_filled, kernel_dilation, iterations=1)

                cv2.imwrite(self.full_folder_to_save_the_processed_images, original_image_with_smoothed)

    @staticmethod
    def preprocess_image(img: np.ndarray) -> np.ndarray:
        """
            this function will to convert image to grayscale
            then it will Dilate to unite nearby regions
            and then apply Erosion to remove small connections
            finally Remove fine lines

        :param img: image already loaded using cv2 imread
        :return:
        """
        # convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.blur(gray, (5, 5), 0)
        img_thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
        #  then it will Dilate to unite nearby regions
        kernel_dilate = np.ones((3, 3), np.uint8)
        img_dilated = cv2.dilate(img_thresh, kernel_dilate, iterations=1)
        # apply Erosion to remove small connections
        kernel_erode = np.ones((3, 3), np.uint8)
        img_eroded = cv2.erode(img_dilated, kernel_erode, iterations=1)
        #  Remove fine lines
        kernel_line = np.ones((1, 5), np.uint8)
        img_removed_lines = cv2.morphologyEx(img_eroded, cv2.MORPH_OPEN, kernel_line)
        clear_img = img_removed_lines

        return clear_img

    @staticmethod
    def find_contours(
            img,
            min_contour_area: int,
            max_contour_area: int,
            max_horizontal_limit: int,
            min_horizontal_limit: int

    ) -> list[list[Any]]:
        """
            this function receive the image to calculate the contours and returns them
        :param min_horizontal_limit:
        :param max_horizontal_limit:
        :param max_contour_area:
        :param min_contour_area:
        :param img: np.ndarray img created using cv2 imread
        :return: Tuple[Tuple, np.ndarray]
        """
        # Implement contour finding logic here
        # ...
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contour_img = img.copy()
        letter_regions = []

        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if min_contour_area < area < max_contour_area:
                [X, Y, W, H] = cv2.boundingRect(contour)
                # Add a condition to check the horizontal limit
                if min_horizontal_limit < W < max_horizontal_limit:
                    # Check if the contour has no parent (inner contour)
                    if hierarchy[0][i][3] == -1:
                        letter_regions.append([X, Y, W, H])
                        cv2.rectangle(contour_img, (X, Y), (X + W, Y + H), (0, 255, 0), 2)

        return letter_regions

    def extract_letter_regions(self):

        # Implement logic to extract letter regions
        # ...
        ...

    def create_result_image(self):
        # Implement logic to create the result image
        ...

    def apply_post_processing(self):
        # Implement post-processing steps here
        ...

    def show_result(self):
        # Implement logic to display the result
        ...

    def save_result(self, output_path):
        cv2.imwrite(output_path, self.result_img)
        ...


if __name__ == "__main__":
    input_image_path = "treat_imgs/img_captcha_6.png"
    output_folder = "img_for_testing/"
    output_path = path.join(output_folder, "img_for_test.png")

    processor = ImageProcessor(input_image_path)

    processor.preprocess_image()
    processor.find_contours()
    processor.extract_letter_regions()
    processor.create_result_image()
    processor.apply_post_processing()
    processor.show_result()
    processor.save_result(output_path)

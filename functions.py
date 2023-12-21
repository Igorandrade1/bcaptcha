import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
import base64
from PIL import Image
import glob
from os import path

def iniciar_driver():
    # Iniciar o WebDriver do Selenium usando o Chrome
    return webdriver.Chrome()


def processar_imagem_captcha(driver, url, output_path):
    try:
        driver.get(url)

        # Obter a URL da imagem captcha
        url_da_imagem = driver.find_element(By.ID, 'captchaImg_N2').get_attribute('src')

        # Remova o prefixo 'data:image/png;base64,' para obter apenas os dados da imagem
        dados_imagem = url_da_imagem.split(',')[1]

        # Decodifique os dados base64
        imagem_decodificada = base64.b64decode(dados_imagem)

        # Salvar a imagem localmente
        with open(output_path, 'wb') as file:
            file.write(imagem_decodificada)

        # Aplicar o código de redimensionamento apenas para uma imagem específica
        files = glob.glob(output_path)

        for file in files:
            folder_to_save_img_too = path.join(path.dirname(__file__), 'bdcaptcha', file.split('/')[1])
            imagem_original = Image.open(file)

            # Redimensionar a imagem para 500x147 pixels usando o método de interpolação BICUBIC
            nova_resolucao = (500, 147)
            imagem_redimensionada = imagem_original.resize(nova_resolucao, resample=Image.BICUBIC)

            # Salvar a imagem redimensionada com qualidade ajustável (para o formato JPEG)
            # Experimente diferentes valores para quality entre 0 e 100
            imagem_redimensionada.save(file, quality=90)
            imagem_redimensionada.save(folder_to_save_img_too, quality=90)

            # Ou salvar em formato PNG (sem perdas)
            # imagem_redimensionada.save(file, format='PNG')

            # Fechar a imagem original
            imagem_original.close()

    except Exception as e:
        print(f"Erro: {e}")


def fill_captcha_field(driver, captcha_value):
    """
    Fill the captcha field with the provided value.

    :param driver: Selenium WebDriver instance.
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param captcha_value: The value to be entered in the captcha field.
    :type captcha_value: str
    """
    try:
        # Optional: Navigate to the page where the captcha field is located
        # url_page = 'your_url_here'
        # driver.get(url_page)

        # Find the input field by ID and enter the captcha value
        captcha_field = driver.find_element(By.ID, 'mainForm:txtCaptcha')
        captcha_field.send_keys(captcha_value)

        # Optionally, wait for the changes to take effect
        # driver.implicitly_wait(2)

    except Exception as e:
        print(f"Error: {e}")


def click_element_by_id(driver, element_id):
    """
    Clicks on the element based on its ID.

    :param driver: Selenium WebDriver instance.
    :type driver: selenium.webdriver.chrome.webdriver.WebDriver

    :param element_id: ID of the element to be clicked.
    :type element_id: str
    """
    try:
        # Find the element by ID and click on it
        element = driver.find_element(By.ID, element_id)
        element.click()

    except Exception as e:
        print(f"Error clicking on the element: {e}")
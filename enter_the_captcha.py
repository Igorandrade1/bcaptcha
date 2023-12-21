from solve_captcha import broken_captcha
from functions import processar_imagem_captcha, iniciar_driver, fill_captcha_field
from selenium.webdriver.remote.webdriver import WebDriver

# Exemplo de uso da função
# url_captcha = "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
# output_path_captcha = 'solve/img_captcha_to_resolve.png'
# driver = iniciar_driver()
#

# processar_imagem_captcha(driver=driver, url=url_captcha, output_path=output_path_captcha)
# captcha_already_solved = broken_captcha()


def solve_captcha(web_driver: WebDriver, url_captcha_page: str, output_path_save_captcha: str) -> str:
    """
    This function had the objective process captcha until it is resolved

    :type web_driver: WebDriver
    :type output_path_save_captcha: str     :type url_captcha: str

    :param web_driver: selenium webdriver already initialized
    :param url_captcha_page: url of page that the captcha image is
    :param output_path_save_captcha: Folder path and name file to image which will be downloaded to the page
    :return: str
    """
    captcha_solved = ''
    while len(captcha_solved) != 5:
        web_driver.refresh()
        processar_imagem_captcha(web_driver, url_captcha_page, output_path_save_captcha)
        captcha_solved = broken_captcha()

    # Aqui você pode adicionar lógica adicional após resolver os 5 captchas, se necessário.

    return captcha_solved


url_captcha = "https://consulta-crf.caixa.gov.br/consultacrf/pages/consultaEmpregador.jsf"
output_path_captcha = 'solve/img_captcha_to_resolve.png'
driver = iniciar_driver()

captcha_solved = solve_captcha(
    web_driver=driver,
    url_captcha_page=url_captcha,
    output_path_save_captcha=output_path_captcha
)

print()
fill_captcha_field(driver=driver, captcha_value=captcha_solved)
print(captcha_solved)



from PIL import Image
import glob

files = glob.glob("bdcaptcha/*")

for file in files:
    imagem_original = Image.open(file)

    # Redimensionar a imagem para 500x147 pixels usando o método de interpolação BICUBIC
    nova_resolucao = (500, 147)
    imagem_redimensionada = imagem_original.resize(nova_resolucao, resample=Image.BICUBIC)

    # Salvar a imagem redimensionada com qualidade ajustável (para o formato JPEG)
    # Experimente diferentes valores para quality entre 0 e 100
    imagem_redimensionada.save(file, quality=90)

    # Ou salvar em formato PNG (sem perdas)
    # imagem_redimensionada.save(file, format='PNG')

    # Fechar a imagem original
    imagem_original.close()



# imagem_original = Image.open(file)
#
# # Redimensionar a imagem para 500x147 pixels usando o método de interpolação BICUBIC
# nova_resolucao = (500, 147)
# imagem_redimensionada = imagem_original.resize(nova_resolucao, resample=Image.BICUBIC)
#
# # Salvar a imagem redimensionada com qualidade ajustável (para o formato JPEG)
# # Experimente diferentes valores para quality entre 0 e 100
# imagem_redimensionada.save(file, quality=90)
#
# # Ou salvar em formato PNG (sem perdas)
# # imagem_redimensionada.save(file, format='PNG')
#
# # Fechar a imagem original
# imagem_original.close()

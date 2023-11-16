from PIL import Image
import glob
# Caminho da imagem original


files = glob.glob("bdcaptcha/*")

for file in files:
    imagem_original = Image.open(file)

    # Redimensionar a imagem para 500x147 pixels
    nova_resolucao = (500, 147)
    imagem_redimensionada = imagem_original.resize(nova_resolucao)

    # Salvar a imagem redimensionada
    # caminho_imagem_redimensionada = "bdcaptcha/telanova0.png"
    imagem_redimensionada.save(file)

    # Fechar a imagem original
    imagem_original.close()




# caminho_imagem_original = "bdcaptcha/telanova0.png"
#
# # Abrir a imagem
# imagem_original = Image.open(caminho_imagem_original)
#
# # Redimensionar a imagem para 500x147 pixels
# nova_resolucao = (500, 147)
# imagem_redimensionada = imagem_original.resize(nova_resolucao)
#
# # Salvar a imagem redimensionada
# caminho_imagem_redimensionada = "bdcaptcha/telanova0.png"
# imagem_redimensionada.save(caminho_imagem_redimensionada)
#
# # Fechar a imagem original
# imagem_original.close()



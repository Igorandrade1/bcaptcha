# import cv2
#
# # Carregue a imagem em escala de cinza
# imagem_escala_de_cinza = cv2.imread('img_para_pegar_cor.png', cv2.IMREAD_GRAYSCALE)
#
# # Aplique a binarização para transformar em preto e branco
# _, imagem_binaria = cv2.threshold(imagem_escala_de_cinza, 127, 255, cv2.THRESH_BINARY)
#
#
# cv2.imshow('Nova Imagem com Recortes', imagem_binaria)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
#
# # Inverta as cores
# imagem_invertida = cv2.bitwise_not(imagem_binaria)
#
# cv2.imshow('Nova Imagem com Recortes', imagem_invertida)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
#
#
#
# # Salve a imagem invertida
# cv2.imwrite('imagem_invertida.jpg', imagem_invertida)
#
# # Salve a imagem binária
# cv2.imwrite('imagem_preto_e_branco.jpg', imagem_binaria)



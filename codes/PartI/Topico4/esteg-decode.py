import cv2
import sys
import numpy as np

# Leitura da imagem
image = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
if image is None:
    print('Imagem não carregada corretamente')

# Definição das dimensões da imagem
width = image.shape[0]
height = image.shape[1]
# Quantidade de bits a serem deslocados
nbits = 5

imagemEscondida = image.copy()

for i in range(width):
    for j in range(height):
        valImage = image[i,j]

        # Para obter a imagem escondida, deve-se deslocar a imagem original 5 bits para a esquerda. 
        # Assim, teremos os 3 bits escondidos nas posições mais significativas, e o restante preenchido com 0
        valImage[0] = valImage[0] << nbits
        valImage[1] = valImage[1] << nbits
        valImage[2] = valImage[2] << nbits

        # Atribuição destes bits para a imagem escondida
        imagemEscondida[i,j] = valImage

#cv2.imwrite("esteganografia.png", imagemEscondida)
cv2.imshow("image", imagemEscondida)
cv2.waitKey(0)
import cv2
import sys
import numpy as np

imagemPortadora = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
imagemEscondida = cv2.imread(sys.argv[2], cv2.IMREAD_COLOR)

if imagemPortadora is None or imagemEscondida is None:
    print('Imagens não carregaram corretamente')

width_p = imagemPortadora.shape[0]
height_p = imagemPortadora.shape[1]
width_e = imagemEscondida.shape[0]
height_e = imagemEscondida.shape[1]

print(imagemPortadora.shape)

if width_p != width_e or height_p != height_e:
    print('Imagens devem ter o mesmo tamanho')

imagemFinal = imagemPortadora.copy()

nbits = 3

for i in range(width_p):
    for j in range(height_p):
        valPortadora = imagemPortadora[i,j]
        valEscondida = imagemEscondida[i,j]
        valPortadora[0] = valPortadora[0] >> nbits << nbits
        valPortadora[1] = valPortadora[1] >> nbits << nbits
        valPortadora[2] = valPortadora[2] >> nbits << nbits
        valEscondida[0] = valEscondida[0] >> (8-nbits)
        valEscondida[1] = valEscondida[1] >> (8-nbits)
        valEscondida[2] = valEscondida[2] >> (8-nbits)
        
        # valFinal[0] = valPortadora[0] | valEscondida[0]
        # valFinal[1] = valPortadora[1] | valEscondida[1]
        # valFinal[2] = valPortadora[2] | valEscondida[2]

        valFinal = np.bitwise_or(valPortadora, valEscondida)
        imagemFinal[i,j] = valFinal

cv2.imwrite("esteganografia.png", imagemFinal)
cv2.imshow("image", imagemFinal)
cv2.waitKey(0)
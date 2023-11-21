import cv2
import numpy as np
import sys

# Carrega a imagem
image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)

if image is None:
    print(f"Erro ao carregar a imagem: {sys.argv[1]}")

# Elemento estruturante
str_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 11))

# Operação de abertura
abertura = cv2.morphologyEx(image, cv2.MORPH_OPEN, str_element)
result_image = abertura

# Exibe a imagem resultante
cv2.imshow("Morfologia", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()



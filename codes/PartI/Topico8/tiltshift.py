import cv2
import numpy as np

# Leitura da imagem inicial
image = cv2.imread('blend2.jpg')

# Criação de uma cópia da imagem
image_copy = np.copy(image)

# Criação de uma imagem borrada, aplicando filtro média 21x21
image_borrada = np.copy(image)
tamanho_filtro = 21
mask_media = np.ones((tamanho_filtro, tamanho_filtro), np.float32) / (tamanho_filtro * tamanho_filtro)
img_borrada_32f = image_borrada.astype(np.float32)
img_borrada_filtered = cv2.filter2D(img_borrada_32f, -1, mask_media, borderType=cv2.BORDER_CONSTANT)
img_borrada_result = img_borrada_filtered.astype(np.uint8)

altura, largura, canais = image.shape

# Imprima o tamanho da imagem
print(f"Altura: {altura} pixels")
print(f"Largura: {largura} pixels")

cv2.imshow("filtroespacial", img_borrada_result)
cv2.waitKey(0)
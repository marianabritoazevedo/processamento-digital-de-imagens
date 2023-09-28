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

# Defina as dimensões da imagem
altura = 256
largura = 256

# Crie uma matriz vazia para a imagem gradativa do preto para o branco na horizontal
grad_preto_branco = np.zeros((altura, largura, 3), dtype=np.uint8)

# Crie uma matriz vazia para a imagem gradativa do branco para o preto na horizontal
grad_branco_preto = np.zeros((altura, largura, 3), dtype=np.uint8)

# Defina os valores de l1 e l2 e d
l1 = 0.3
l2 = 0.7
d = 0.05

# Preencha as imagens gradativas usando a função α(x) na horizontal
for y in range(altura):
    for x in range(largura):
        # Calcule o valor de α(x) para o pixel atual na horizontal
        alpha = 0.5 * (np.tanh((y - l1) / d) - np.tanh((y - l2) / d))
        
        # Mapeie o valor de α(x) para o intervalo de 0 a 255
        valor_pixel = int(alpha * 255)
        
        # Preencha os pixels nas imagens gradativas na horizontal
        grad_preto_branco[y, x] = (valor_pixel, valor_pixel, valor_pixel)
        grad_branco_preto[y, x] = (255 - valor_pixel, 255 - valor_pixel, 255 - valor_pixel)

img1 = np.multiply(image_copy, grad_preto_branco) 
img2 = np.multiply(img_borrada_result, grad_branco_preto) 
img_final = cv2.add(img1, img2)

# Exiba as imagens (opcional)
cv2.imshow("Gradiente Preto para Branco (Horizontal)", grad_preto_branco)
cv2.imshow("Gradiente Branco para Preto (Horizontal)", grad_branco_preto)
cv2.imshow("Final", img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()


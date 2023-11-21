import cv2
import numpy as np
import random

# Definição dos parâmetros iniciais
raio = 3 # Raio dos pontos 
jitter = 4 # Espaçamento para os pontos 

image = cv2.imread("paisagem2.jpg") 
width = image.shape[1]
height = image.shape[0]

# Criação da matriz que irá armazenar os pontos. Inicialmente, todos
# são completamente brancos
points = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)

# Loop para detecção de bordas diversas vezes ao longo da imagem
for i in range(1, 200, 10):
    # Detecção de bordas com o algoritmo Canny
    border = cv2.Canny(image, i, 3*i)

    # Loop para desenhar os pontos nas bordas. Deve-se passar por toda a imagem
    for l in range(0, height):
        for c in range(0, width):
            # Se é um pixel branco, quer dizer que detectou uma borda
            if border[l, c] == 255:
                # Posição do ponto a partir de número aleatório dentro do intervalo de jitter
                x = int(l + random.randint(-jitter, jitter) + 1)
                y = int(c + random.randint(-jitter, jitter) + 1)
                x = max(0, min(x, height - 1))  # Garante que x está dentro dos limites
                y = max(0, min(y, width - 1))   # Garante que y está dentro dos limites
                # Definição de passo para ajuste da intensidade da cor
                passo = (random.randint(0, 1) / 10.0) + 1.0
                # Determinação da cor do ponto
                val = (
                    min(int(image[x, y, 0] * passo), 255),
                    min(int(image[x, y, 1] * passo), 255),
                    min(int(image[x, y, 2] * passo), 255),
                )
                # Desenho do ponto na imagem 
                cv2.circle(points, (y, x), raio, val, -1)

cv2.imshow("result.png", points)
cv2.waitKey()
cv2.imwrite("result.png", points)


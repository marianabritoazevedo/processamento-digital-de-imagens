import numpy as np
import cv2
import sys

# Parâmetros para o algoritmo kmeans
nClusters = 8
nRodadas = 1

# Verifica número de argumentos no comando
if len(sys.argv) != 3:
    print("Usage: python kmeans.py input_image output_image")
    sys.exit(0)

# Leitura da imagem de entrada
img = cv2.imread(sys.argv[1])

# Transforma a imagem em um array unidimensional de pontos de dados (samples) do tipo float
samples = img.reshape((-1, 3)).astype(np.float32)

# Critério de parada do algoritmo K-means
criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)

# Aplicação do algoritmo
_, labels, (centers) = cv2.kmeans(samples, nClusters, None, criterio, nRodadas, cv2.KMEANS_RANDOM_CENTERS)

# Converte os centros dos clusters para o tipo de dados uint8
centers = np.uint8(centers)

# Mapeia os rótulos de cluster de volta para os pixels na imagem
img_final = centers[labels.flatten()]
img_final = img_final.reshape(img.shape)

# Exibe e salva a imagem clusterizada
cv2.imshow("kmeans", img_final)
cv2.imwrite(sys.argv[2], img_final)
cv2.waitKey(0)
cv2.destroyAllWindows()

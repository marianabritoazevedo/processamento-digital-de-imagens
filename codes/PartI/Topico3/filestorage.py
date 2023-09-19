import cv2
import numpy as np
import math
import plotly.express as px
import plotly.io as pio

# Constantes do programa
SIDE = 256
PERIODOS = 4

# Armazenamento da imagem como png e como yml
img_png = cv2.FileStorage()
img_yml = cv2.FileStorage()

# Abre imagem YML e escreve apenas zeros, com o tipo float 32
img_yml.open("senoide.yml", cv2.FileStorage_WRITE)
image = np.zeros((SIDE, SIDE), dtype=np.float32)

# Imagem yml com valores da senóide
for i in range(SIDE):
    for j in range(SIDE):
        image[i, j] = 127 * math.sin(2 * math.pi * PERIODOS * j / SIDE) + 128

# Escreva a matriz de imagem no arquivo YAML
img_yml.write("yml_final", image)
img_yml.release()

# Normaliza a imagem inicialmente em yml e converte para o tipo int 8
image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
image = np.uint8(image)

# Abre a imagem PNG e salva a matriz resultante
img_png.open("senoide.png", cv2.FileStorage_WRITE)
img_png.write("mat", image)
img_png.release()

# Para verificar que funcionou corretamente, abre a imagem yml, normaliza e converte para mostrá-la
# Também salva os valores dos pixels da primeira linha da imagem YML e PNG
img_yml.open("senoide.yml", cv2.FileStorage_READ)
image = img_yml.getNode("yml_final").mat()
line_yml = image[0, :]
img_yml.release()

image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
image = np.uint8(image)
line_png = image[0, :]

# Mostra a imagem na tela
cv2.imshow("image", image)
cv2.waitKey(0)

# Pega valores da primeira linha de cada um dos tipos de imagem e traça um gráfico 
eixoy = line_yml - line_png
eixox = [x for x in range(0, 256)]

# Cria e salva gráfico gerado
fig = px.line(x=eixox, y=eixoy, title='Diferenças pixels YML x PNG', labels={'y': 'Diferença', 'x': 'Coluna do pixel da primeira linha'})
fig.update_layout(width=1200) 
pio.write_image(fig, 'diferencas_graph.png')

# Exibe o gráfico gerado
image = cv2.imread('diferencas_graph.png')
cv2.imshow('Gráfico das diferenças', image)
cv2.waitKey(0)



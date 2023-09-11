import cv2

# Carregar a imagem em escala de cinza
image = cv2.imread("bolhas.png", cv2.IMREAD_GRAYSCALE)

# Verifica se carregou corretamente a imagem
if image is None:
    print("Não foi possível carregar a imagem")
    exit()

# Definição da largura e altura da imagem. Ela é retornada com um array [altura, largura]
width = image.shape[1]
height = image.shape[0]
print(f"Tamanho da imagem: {width}x{height}")

# Inicializar variáveis
n_objects = 0

# Percorrer a imagem em busca de objetos
for i in range(height):
    for j in range(width):
        if image[i, j] == 255: # Encontrou uma bolha
            n_objects += 1 # Incrementa quantidade de bolhas
            cv2.floodFill(image, None, (j, i), n_objects) # Preenche com floodFill naquela imagem, ponto (j,i) com cor n_objects

print(f"A figura tem {n_objects} bolhas")
cv2.imshow("image", image)
#cv2.imwrite("labeling.png", image)
cv2.waitKey(0)

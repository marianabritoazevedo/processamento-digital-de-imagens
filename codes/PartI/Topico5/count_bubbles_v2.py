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

# Inicialmente, nenhuma bolha com buracos ou sem buracos
complete_bubbles = 0
holes_bubbles = 0
new_brackground = False

# Pintar o plano de fundo com uma nova cor. Será atribuída a cor 128
for i in range(width):
    for j in range(height):
        if image[i, j] == 0 and not new_brackground:
            cv2.floodFill(image, None, (j, i), 128)
            new_brackground = True
            break
        if new_brackground:
            break

cv2.imwrite('parte1-bolhas.png', image)

# Ao encontrar algo nas bordas, desconsiderar da contagem, pintar da cor do plano de fundo
for i in range(width):
    if image[i, 0] == 255 or image[i, 0] == 0:
        cv2.floodFill(image, None, (0, i), 128) # Retira bolhas do lado esquerdo
    if image[i, height-1] == 255 or image[i, height-1] == 0:
        cv2.floodFill(image, None, (height-1, i), 128) # Retira bolhas do lado direito

for j in range(height):
    if image[0, j] == 255 or image[0, j] == 0:
        cv2.floodFill(image, None, (j, 0), 128) # Retira bolhas do lado superior
    if image[width-1, j] == 255 or image[width-1, j] == 0:
        cv2.floodFill(image, None, (j, width-1), 128) # Retira bolhas do lado inferior

cv2.imwrite('parte2-bolhas.png', image)

# Procurando as bolhas COM buracos. Para isso, é preciso encontrar um buraco (cor 0) e na sua lateral esquerda, ser uma bolha (cor 255)
# Em seguida, pode-se pintar a bolha (cor 255) com a cor de fundo
for i in range(width):
    for j in range(height):
        if image[i, j] == 0 and image[i, j-1] == 255:
            holes_bubbles += 1
            cv2.floodFill(image, None, (j-1, i), 128)

print(f"Bolhas com buraco: {holes_bubbles}")
cv2.imwrite('parte3-bolhas.png', image)

# Procurando bolhas SEM buracos. Para isso, é preciso encontrar uma bolha completa (cor 255), e pintá-la com a cor do fundo
for i in range(width):
    for j in range(height):
        if image[i, j] == 255:
            complete_bubbles += 1
            cv2.floodFill(image, None, (j, i), 128)

print(f"Bolhas sem buraco: {complete_bubbles}")
cv2.imwrite('parte4-bolhas.png', image)

# Mostrar como ficou imagem final após o processamento completo
cv2.imshow("image", image)
cv2.waitKey(0)

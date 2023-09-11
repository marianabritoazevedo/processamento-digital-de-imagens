import cv2

image = cv2.imread('biel.png', cv2.IMREAD_GRAYSCALE)

if image is None:
    print('Imagem não foi carregada corretamente')

width = image.shape[0]
height = image.shape[1]

print(image.shape)

image_copy = image.copy()

mean_width = int(width/2)
mean_height = int(height/2)

# Substituindo os quadrantes
for i in range(mean_width):
    for j in range(mean_height):
        # Quadrante da região 1
        image[i,j] = image_copy[i+mean_width, j+mean_height]
        # Quadrante da região 4
        image[i+mean_width, j+mean_height] = image_copy[i,j]
        # Quadrante da região 2
        image[i, j+mean_height] = image_copy[i+mean_width,j]
        #Quadrante da região 3
        image[i+mean_width, j] = image_copy[i,j+mean_height]

cv2.imshow("image", image)
cv2.imwrite('troca-regioes.png', image)
cv2.waitKey(0)
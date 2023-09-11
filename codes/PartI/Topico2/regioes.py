import cv2

image = cv2.imread('biel.png', cv2.IMREAD_GRAYSCALE)

if image is None:
    print('Imagem não carregou corretamente')

x1, y1 = map(int, input('Digite as coordenadas do ponto P1 separadas por vírgula: ').split(','))
x2, y2 = map(int, input('Digite as coordenadas do ponto P2 separadas por vírgula: ').split(','))

for i in range(x1, x2+1):
    for j in range(y1, y2+1):
        val_grayscale = image[i,j]
        val_negative = 255 - val_grayscale
        image[i,j] = val_negative

cv2.imshow("image", image)
cv2.imwrite("negativo.png", image)
cv2.waitKey(0)

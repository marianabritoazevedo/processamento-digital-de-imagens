import cv2
import numpy as np

def filter(image):
    # Parâmetros do filtro homomórfico
    gamma_h = 0.3  # Parâmetro gamma para realce
    gamma_l = 1.5  # Parâmetro gamma para atenuação
    c = 1.0  # Parâmetro de corte

    # Dimensões da imagem para criação da máscara
    rows, cols, _ = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols, 2), np.float32)
    for i in range(rows):
        for j in range(cols):
            mask[i, j] = (gamma_h - gamma_l) * (1 - np.exp(-c * ((i - crow) ** 2 + (j - ccol) ** 2) / (ccol ** 2 + crow ** 2))) + gamma_l

    # Aplicação do filtro e retorno da nova imagem
    new_image = image * mask
    return new_image

# Carrega a imagem em escala de cinza
image = cv2.imread('teste-pdi.png', cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Erro ao abrir a imagem.")
else:
    # Considerando uma imagem com tamanho 2^n, calcula-se a transformada de Fourier
    float_image = np.float32(image)
    complex_image = cv2.dft(float_image, flags=cv2.DFT_COMPLEX_OUTPUT)
    # Deslocamento dos quadrantes para melhor visualização
    complex_image = np.fft.fftshift(complex_image)

    # Filtragem homomórfica
    new_image = filter(complex_image)

    # Aplicação da transformada inversa de fourier
    new_image = np.fft.ifftshift(new_image)
    imagem_filtrada = cv2.idft(new_image)
    imagem_filtrada = cv2.magnitude(imagem_filtrada[:, :, 0], imagem_filtrada[:, :, 1])

    # Organizando a imagem final
    imagem_filtrada = cv2.normalize(imagem_filtrada, None, 0, 255, cv2.NORM_MINMAX)
    imagem_filtrada = np.uint8(imagem_filtrada)

    # Visualização da imagem original e de seu espectro
    cv2.imshow("Imagem original", image)
    cv2.imshow('Imagem Filtrada', imagem_filtrada)
    cv2.imwrite('imagem-com-filtro.png', imagem_filtrada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

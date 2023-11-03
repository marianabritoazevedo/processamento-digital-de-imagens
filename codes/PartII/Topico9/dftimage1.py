import cv2
import numpy as np

# Carrega a imagem em escala de cinza
image = cv2.imread('senoide.png', cv2.IMREAD_GRAYSCALE)

if image is None:
    print("Erro ao abrir a imagem.")
else:
    # Como essa imagem já possui seu tamanho como uma potência de 2, 256x256, 
    # já podemos realizar o cálculo da transformada de Fourrier diretamente
    float_image = np.float32(image)
    complex_image = cv2.dft(float_image, flags=cv2.DFT_COMPLEX_OUTPUT)
    # Deslocamento dos quadrantes para melhor visualização
    complex_image = np.fft.fftshift(complex_image)

    # Cálculo do espectro de magnitude
    espectro_mag = cv2.magnitude(complex_image[:, :, 0], complex_image[:, :, 1])
    # Compressão de faixa dinâmica
    espectro_mag += 1.0
    espectro_mag = np.log(espectro_mag)
    # Normalização entre 0 e 1 para melhor exibição
    cv2.normalize(espectro_mag, espectro_mag, 0, 1, cv2.NORM_MINMAX)

    # Visualização da imagem original e de seu espectro
    cv2.imshow("Imagem original", image)
    cv2.imshow("Espectro de magnitude", espectro_mag)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

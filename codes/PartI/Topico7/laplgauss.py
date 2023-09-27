import cv2
import numpy as np

# Inicializa a captura de vídeo a partir da câmera padrão (0)
cap = cv2.VideoCapture(0)

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Câmera indisponível")
    exit()

# Define a largura e altura desejadas para o vídeo
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Exibe a largura e altura do vídeo
print("Largura =", width)
print("Altura =", height)

# Define uma janela para a imagem cinza, e outra para a imagem equalizada
cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
cv2.namedWindow('Laplaciano', cv2.WINDOW_NORMAL)
cv2.namedWindow('LaplGauss', cv2.WINDOW_NORMAL)

# Redefine o tamanho das janelas para a altura e largura que eu defini
cv2.resizeWindow('Original', width, height)
cv2.resizeWindow('Laplaciano', width, height)
cv2.resizeWindow('LaplGauss', width, height)

# Variáveis referentes aos filtros
gauss = [0.0625, 0.125,  0.0625, 0.125, 0.25,
            0.125,  0.0625, 0.125,  0.0625]
laplacian = [0, -1, 0, -1, 4, -1, 0, -1, 0]

mask_gauss = np.array(gauss).reshape(3, 3).astype(np.float32)
mask_laplacian = np.array(laplacian).reshape(3, 3).astype(np.float32)

while True:
    # Captura um quadro do vídeo
    ret, frame = cap.read()

    # Sai do loop se não houver mais quadros
    if not ret:
        break

    # Converte a imagem capturada para tons de cinza
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Cópia do tipo float para permitir a aplicação dos filtros
    frame_float = gray_frame.astype(np.float32)

    # Define filtro laplaciano
    laplacian_frame = cv2.filter2D(frame_float, -1, mask_laplacian, borderType=cv2.BORDER_CONSTANT)
    laplacian_frame = laplacian_frame.astype(np.uint8)

    # Define filtro laplaciano do gaussiano
    gauss_frame = cv2.filter2D(frame_float, -1, mask_gauss, borderType=cv2.BORDER_CONSTANT)
    gauss_laplace_frame = cv2.filter2D(gauss_frame, -1, mask_laplacian, borderType=cv2.BORDER_CONSTANT)
    gauss_laplace_frame = gauss_laplace_frame.astype(np.uint8)

    # Mostra a imagem em tons de cinza
    cv2.imshow('Original', gray_frame)
    cv2.imshow('Laplaciano', laplacian_frame)
    cv2.imshow('LaplGauss', gauss_laplace_frame)

    # Sai do loop se for pressionada a tecla ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
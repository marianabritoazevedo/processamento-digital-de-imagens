import cv2
import numpy as np

# Inicializa a captura de vídeo a partir da câmera padrão (0)
cap = cv2.VideoCapture(0)

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Câmera indisponível")
    exit()

# Define a largura e altura desejadas para o vídeo
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Exibe a largura e altura do vídeo
print("Largura =", width)
print("Altura =", height)

# Define uma janela para a imagem cinza, e outra para a imagem equalizada
cv2.namedWindow('Gray Image', cv2.WINDOW_NORMAL)
cv2.namedWindow('Equalized Image', cv2.WINDOW_NORMAL)

# Redefine o tamanho das janelas para a altura e largura que eu defini
cv2.resizeWindow("Gray Image", width, height)
cv2.resizeWindow("Equalized Image", width, height)

while True:
    # Captura um quadro do vídeo
    ret, frame = cap.read()

    # Sai do loop se não houver mais quadros
    if not ret:
        break

    # Converte a imagem capturada para tons de cinza
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Calcula o histograma
    # Para isso, recebe: lista de imagens para calcular histograma, o canal (o 0, já que são só tons de cinza), se vai usar alguma máscara, o tamanho do histograma e as dimensões (de 0 a 256)
    hist_gray = cv2.calcHist([gray_frame], [0], None, [256], [0, 256])

    # Calcula o histograma acumulado
    cumulative_hist = np.cumsum(hist_gray)

    # Normaliza o histograma acumulado
    cumulative_hist_normalized = (cumulative_hist / cumulative_hist[-1]) * 255

    # Aplica a equalização ao quadro em tons de cinza usando o histograma acumulado normalizado
    # Basicamente, ela aplica uma transformação para qual valor de pixel deve ser mapeada uma saída
    equalized_frame = cv2.LUT(gray_frame, cumulative_hist_normalized.astype(np.uint8))

    # Mostra a imagem em tons de cinza
    cv2.imshow('Gray Image', gray_frame)
    cv2.imshow('Equalized Image', equalized_frame)

    # Sai do loop se for pressionada a tecla ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()

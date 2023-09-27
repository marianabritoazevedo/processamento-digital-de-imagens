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

# Define o frame atual e o frame imediatamente antes dele
frame_x = None
frame_x_ant = None

# Variáveis para mostrar texto ao detectar movimento
texto = 'Movimento detectado!'
posicao_texto = (50, 50)
fonte = cv2.FONT_HERSHEY_SIMPLEX
escala = 1
cor = (255, 0, 0)  # Cor no formato BGR (verde no exemplo)
espessura = 2

while True:
    # Captura um quadro do vídeo
    ret, frame = cap.read()

    # Sai do loop se não houver mais quadros
    if not ret:
        break

    # Converte a imagem capturada para tons de cinza
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Atualiza o frame atual e o frame imediatamente antes dele
    frame_x_ant = frame_x
    frame_x = gray_frame

    # Se nenhum dos dois for nulo, calcula o histograma de cada 
    if frame_x is not None and frame_x_ant is not None:
        hist_x = cv2.calcHist([frame_x], [0], None, [256], [0, 256])
        hist_x_ant = cv2.calcHist([frame_x_ant], [0], None, [256], [0, 256])

        # Calcula a diferença (em módulo) de cada posição do histograma
        diff = np.abs(hist_x - hist_x_ant)

        # Verifica se é maior do que um limiar. Se for, houve movimento e mostra mensagem na tela
        print(np.sum(diff))
        if np.sum(diff) > 10000:
            cv2.putText(frame_x, texto, posicao_texto, fonte, escala, cor, espessura)


    # Mostra a imagem em tons de cinza
    cv2.imshow('Image', frame_x)

    # Sai do loop se for pressionada a tecla ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
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
texto_calibracao = 'Calibrando... Aguarde 4 segundos'
posicao_texto = (50, 80)
fonte = cv2.FONT_HERSHEY_SIMPLEX
escala = 1
cor = (0, 0, 255) 
cor_calibracao = (255, 0, 0)
espessura = 2

# Etapa 1: fazer calibração para ajustar o limiar
calibracao = True
cont = 0
list_calibracao = []
media_calibracao = 0

while calibracao:
    # Captura um quadro do vídeo
    ret, frame = cap.read()

    # Sai do loop se não houver mais quadros
    if not ret:
        break

    # Atualiza o frame atual e o frame imediatamente antes dele
    frame_x_ant = frame_x
    frame_x = frame

    # Se nenhum dos dois for nulo, calcula o histograma (para apenas um canal) de cada 
    if frame_x is not None and frame_x_ant is not None:

        red_frame_x = frame_x[:,:,2]
        red_frame_x_ant = frame_x_ant[:,:,2]

        hist_x = cv2.calcHist([red_frame_x], [0], None, [256], [0, 256])
        hist_x_ant = cv2.calcHist([red_frame_x_ant], [0], None, [256], [0, 256])

        # Calcula a diferença (em módulo) de cada posição do histograma
        diff = np.abs(hist_x - hist_x_ant)

        # Adiciona na lista de calibração
        list_calibracao.append(np.sum(diff))
        # Aumenta em 1 o contador
        cont += 1
        # Se já tiver feito isso com 100 quadros, calcula uma média e sai desse loop
        if cont == 100:
            media_calibracao = np.mean(list_calibracao)
            calibracao = False
    
    # Mostra a imagem dizendo que está sendo feita a calibração
    cv2.putText(frame_x, texto_calibracao, posicao_texto, fonte, escala, cor_calibracao, espessura)
    cv2.imshow('Image', frame_x)
    cv2.waitKey(1) 

# Depois, vai dizer se está em movimento ou não de acordo com a calibração feita
print(f' Lista de calibração: {list_calibracao}')
print(f' Valor da média: {media_calibracao}')
while True:
    # Captura um quadro do vídeo
    ret, frame = cap.read()

    # Sai do loop se não houver mais quadros
    if not ret:
        break

    # Atualiza o frame atual e o frame imediatamente antes dele
    frame_x_ant = frame_x
    frame_x = frame

    # Se nenhum dos dois for nulo, calcula o histograma (para apenas um canal) de cada 
    if frame_x is not None and frame_x_ant is not None:

        red_frame_x = frame_x[:,:,2]
        red_frame_x_ant = frame_x_ant[:,:,2]

        hist_x = cv2.calcHist([red_frame_x], [0], None, [256], [0, 256])
        hist_x_ant = cv2.calcHist([red_frame_x_ant], [0], None, [256], [0, 256])

        # Calcula a diferença (em módulo) de cada posição do histograma
        diff = np.abs(hist_x - hist_x_ant)

        # Verifica se é maior do que um limiar. Se for, houve movimento e mostra mensagem na tela
        print(np.sum(diff))
        if np.sum(diff) > media_calibracao:
            cv2.putText(frame_x, texto, posicao_texto, fonte, escala, cor, espessura)

    # Mostra a imagem em tons de cinza
    cv2.imshow('Image', frame_x)

    # Sai do loop se for pressionada a tecla ESC
    if cv2.waitKey(30) == 27:
        break

cap.release()
cv2.destroyAllWindows()
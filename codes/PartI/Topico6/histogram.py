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

# Número de bins para o histograma e faixa de valores
nbins = 64
range_ = [0, 255]

# Define se o histograma será uniforme e se será acumulado
uniform = True
accumulate = False

# Largura e altura do histograma
histw = nbins
histh = nbins // 2

while True:
    # Captura um quadro do vídeo
    ret, frame = cap.read()

    # Sai do loop se não houver mais quadros
    if not ret:
        break

    # Divide o quadro em canais de cores (R, G, B)
    planes = cv2.split(frame)

    # Calcula o histograma para cada canal de cor
    histR = cv2.calcHist([planes[0]], [0], None, [nbins], range_, accumulate=accumulate)
    histG = cv2.calcHist([planes[1]], [0], None, [nbins], range_, accumulate=accumulate)
    histB = cv2.calcHist([planes[2]], [0], None, [nbins], range_, accumulate=accumulate)

    # Normaliza os histogramas para o intervalo de exibição
    cv2.normalize(histR, histR, 0, histh, cv2.NORM_MINMAX)
    cv2.normalize(histG, histG, 0, histh, cv2.NORM_MINMAX)
    cv2.normalize(histB, histB, 0, histh, cv2.NORM_MINMAX)

    # Cria imagens vazias para exibir os histogramas
    histImgR = np.zeros((histh, histw, 3), dtype=np.uint8)
    histImgG = np.zeros((histh, histw, 3), dtype=np.uint8)
    histImgB = np.zeros((histh, histw, 3), dtype=np.uint8)

    # Desenha as linhas do histograma em cada imagem
    for i in range(1, nbins):
        cv2.line(histImgR, (i - 1, histh - int(histR[i - 1])), (i, histh - int(histR[i])), (0, 0, 255), 1, 8, 0)
        cv2.line(histImgG, (i - 1, histh - int(histG[i - 1])), (i, histh - int(histG[i])), (0, 255, 0), 1, 8, 0)
        cv2.line(histImgB, (i - 1, histh - int(histB[i - 1])), (i, histh - int(histB[i])), (255, 0, 0), 1, 8, 0)

    # Redimensiona os histogramas para terem as mesmas dimensões da região onde serão copiados
    histImgR = cv2.resize(histImgR, (nbins, histh))
    histImgG = cv2.resize(histImgG, (nbins, histh))
    histImgB = cv2.resize(histImgB, (nbins, histh))

    # Empilha as imagens dos histogramas em uma única imagem
    histImg = np.vstack((histImgR, histImgG, histImgB))

    # Adiciona a imagem do histograma à imagem original
    frame[0:3 * histh, 0:nbins] = histImg  # Ajusta a região da imagem onde o histograma será copiado

    # Exibe o vídeo com o histograma
    cv2.imshow("image", frame)

    # Sai do loop se a tecla 'Esc' for pressionada
    if cv2.waitKey(30) == 27:
        break

# Libera a câmera e fecha todas as janelas
cap.release()
cv2.destroyAllWindows()

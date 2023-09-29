import cv2
import numpy as np

# Função para aplicar o tiltshift em um frame, e depois, retornar o resultado desse frame
def apply_tiltshift(imagem, imagem_borrada):
    # Parâmetros da fórmula aplicados para o vídeo
    l1, l2, d, centro = -130, 130, 90, 400

    # Definição inicialmente de uma matriz apenas com zeros com a mesma dimensão da imagem original
    ponderada = np.zeros_like(imagem, dtype=np.float32)

    # Para a altura da imagem, aplicar a função de ponderação
    altura_imagem = imagem.shape[0]
    for i in range(altura_imagem):
        ponderacao = -0.5 * (np.tanh((i - centro + l1) / d) - np.tanh((i - centro + l2) / d))
        ponderada[i, :, :] = ponderacao

    # Calcular a ponderação inversa
    ponderada_negativa = 1.0 - ponderada
    # Multiplicação da imagem original com a ponderação
    res1 = cv2.multiply(imagem, ponderada)
    # Multiplicação da imagem borrada com a ponderação negativa
    res2 = cv2.multiply(imagem_borrada, ponderada_negativa)
    # Adição das duas imagens e transformação do tipo
    resultado = cv2.add(res1, res2).astype(np.uint8)

    return resultado

# Caminho para o vídeo original
caminho_video = 'video-pdi.mp4'

# Abre o vídeo original
cap = cv2.VideoCapture(caminho_video)

# Verifica se o vídeo foi aberto com sucesso
if not cap.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Obtém informações do vídeo original (largura, altura, taxa de frames, etc.)
largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
taxa_frames = cap.get(cv2.CAP_PROP_FPS)

# Define o codec e cria um objeto VideoWriter para escrever o novo vídeo
codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para formato MP4
novo_caminho_video = 'novo-video.mp4'
novo_video = cv2.VideoWriter(novo_caminho_video, codec, taxa_frames, (largura, altura))

# Contador de frames
contador_frames = 0

# Loop para ler frames do vídeo
while True:
    # Lê um frame do vídeo
    ret, frame = cap.read()

    # Verifica se o frame foi lido corretamente
    if not ret:
        break

    # A cada 3 frames, aplica o filtro tilt-shift
    if contador_frames % 3 == 0:
        # Aplica o filtro tilt-shift

        # Tamanho da matriz em que será aplicado o filtro média
        mask_media_tam = 15
        frame = frame.astype(np.float32)
        frame_borrado = cv2.filter2D(frame, -1, np.ones((mask_media_tam, mask_media_tam), np.float32) / (mask_media_tam ** 2))
        frame_modificado = apply_tiltshift(frame, frame_borrado)  # Aqui você pode modificar os parâmetros de tilt-shift conforme necessário

        # Escreve o frame modificado no novo vídeo
        for i in range(2):
            novo_video.write(frame_modificado)

    contador_frames += 1

# Libera o objeto de captura e o objeto de gravação
cap.release()
novo_video.release()

print(f'Novo vídeo salvo em: {novo_caminho_video}')

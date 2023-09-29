import cv2
import numpy as np

# Parâmetros da fórmula que poderão ser regulados
l1, l2, d, centro = -50, 50, 6, 100

# Tamanho da matriz em que será aplicado o filtro média
mask_media_tam = 15

# Valores iniciais dos sliders e seus limites
altura, decaimento, posicao = 0, 0, 0
altura_max, decaimento_max, posicao_max = 100, 100, 100

resultado = None

def apply_tiltshift(imagem, imagem_borrada):
    global l1, l2, d, centro, resultado

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
    print(f'l1={l1}, l2={l2}, d={d}, centro={centro}')

    cv2.imshow("Tiltshift", resultado)

# Verifica as mudanças nos parâmetros l1 e l2, implicando na mudança da altura
def on_trackbar_altura(val):
    global l1, l2
    # Obtem o valor do slider de altura
    altura_slider = cv2.getTrackbarPos("Altura", "Tiltshift")
    # Mapeia inversamente o valor do slider para l1 e l2 em um intervalo maior
    l1 = -altura_slider * 1.5
    l2 = altura_slider * 1.5
    apply_tiltshift(imagem, imagem_borrada)

# Verifica mudanças no parâmetro d, implicando em mudanças no borramento
def on_trackbar_decaimento(val):
    global d
    d = val
    apply_tiltshift(imagem, imagem_borrada)

# Verifica mudanças no parâmetro centro, implicando em mudanças no local em que
# a imagem não estará borrada
def on_trackbar_deslocamento(val):
    global centro
    centro = val * imagem.shape[0] / 100
    apply_tiltshift(imagem, imagem_borrada)

# Leitura da imagem original
imagem = cv2.imread("paisagem.jpg").astype(np.float32)
# Criação da imagem borrada
imagem_borrada = cv2.filter2D(imagem, -1, np.ones((mask_media_tam, mask_media_tam), np.float32) / (mask_media_tam ** 2))

# Criação da janela com os sliders para mudar os valores
cv2.namedWindow("Tiltshift", cv2.WINDOW_AUTOSIZE)
cv2.createTrackbar("Altura", "Tiltshift", altura, altura_max, on_trackbar_altura)
cv2.createTrackbar("Decaimento", "Tiltshift", decaimento, decaimento_max, on_trackbar_decaimento)
cv2.createTrackbar("Deslocamento", "Tiltshift", posicao, posicao_max, on_trackbar_deslocamento)

apply_tiltshift(imagem, imagem_borrada)

while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # 27 é o código da tecla ESC
        # Salva a imagem antes de fechar
        if resultado is not None:
            cv2.imwrite("resultado_tiltshift.jpg", resultado)
        break

cv2.destroyAllWindows()

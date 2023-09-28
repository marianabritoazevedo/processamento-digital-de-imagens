import cv2
import numpy as np

def on_trackbar_blend(val):
    global alfa
    alfa = val / alfa_slider_max
    cv2.addWeighted(image1, 1 - alfa, imageTop, alfa, 0.0, blended)
    cv2.imshow("addweighted", blended)

def on_trackbar_line(val):
    global imageTop
    imageTop = image2.copy()
    limit = val * 255 // top_slider_max
    if limit > 0:
        imageTop[0:limit, 0:256] = image2[0:limit, 0:256]
    on_trackbar_blend(alfa_slider)

# Inicialize as variáveis
alfa = 0.0
alfa_slider = 0
alfa_slider_max = 100

top_slider = 0
top_slider_max = 100

# Carregue as imagens
image1 = cv2.imread("blend1.jpg")
image2 = cv2.imread("blend2.jpg")
imageTop = image2.copy()

blended = np.zeros_like(image1)

# Crie a janela
cv2.namedWindow("addweighted")

# Crie os trackbars
cv2.createTrackbar("Alpha x {}".format(alfa_slider_max), "addweighted", alfa_slider, alfa_slider_max, on_trackbar_blend)
cv2.createTrackbar("Scanline x {}".format(top_slider_max), "addweighted", top_slider, top_slider_max, on_trackbar_line)

# Chame as funções iniciais
on_trackbar_blend(alfa_slider)
on_trackbar_line(top_slider)

cv2.waitKey(0)
cv2.destroyAllWindows()


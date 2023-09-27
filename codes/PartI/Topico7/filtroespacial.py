import cv2
import numpy as np

def printmask(m):
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            print(m[i, j], end=', ')
        print()

cap = cv2.VideoCapture(0)  # open the default camera
media = [0.1111, 0.1111, 0.1111, 0.1111, 0.1111,
            0.1111, 0.1111, 0.1111, 0.1111]
gauss = [0.0625, 0.125,  0.0625, 0.125, 0.25,
            0.125,  0.0625, 0.125,  0.0625]
horizontal = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
vertical = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
laplacian = [0, -1, 0, -1, 4, -1, 0, -1, 0]
boost = [0, -1, 0, -1, 5.2, -1, 0, -1, 0]

mask = np.array(media).reshape(3, 3).astype(np.float32)
result = None
width, height = 0, 0
absolut = 1

if not cap.isOpened():  # check if we succeeded
    print("Câmera indisponível")
    exit()

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print("largura =", width)
print("altura =", height)
print("fps =", cap.get(cv2.CAP_PROP_FPS))
print("format =", cap.get(cv2.CAP_PROP_FORMAT))

cv2.namedWindow("filtroespacial", cv2.WINDOW_NORMAL)
cv2.namedWindow("original", cv2.WINDOW_NORMAL)

# Redefine o tamanho das janelas para a altura e largura que eu defini
cv2.resizeWindow("filtroespacial", width, height)
cv2.resizeWindow("original", width, height)

absolut = 1  # calcs abs of the image

while True:
    ret, frame = cap.read()  # get a new frame from the camera
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    framegray = cv2.flip(framegray, 1)
    cv2.imshow("original", framegray)
    frame32f = framegray.astype(np.float32)
    frameFiltered = cv2.filter2D(frame32f, -1, mask, borderType=cv2.BORDER_CONSTANT)
    if absolut:
        frameFiltered = cv2.convertScaleAbs(frameFiltered)

    result = frameFiltered.astype(np.uint8)

    cv2.imshow("filtroespacial", result)

    key = cv2.waitKey(10)
    if key == 27:  # esc pressed!
        break
    elif key == ord('a'):
        absolut = not absolut
    elif key == ord('m'):
        mask = np.array(media).reshape(3, 3).astype(np.float32)
        printmask(mask)
    elif key == ord('g'):
        mask = np.array(gauss).reshape(3, 3).astype(np.float32)
        printmask(mask)
    elif key == ord('h'):
        mask = np.array(horizontal).reshape(3, 3).astype(np.float32)
        printmask(mask)
    elif key == ord('v'):
        mask = np.array(vertical).reshape(3, 3).astype(np.float32)
        printmask(mask)
    elif key == ord('l'):
        mask = np.array(laplacian).reshape(3, 3).astype(np.float32)
        printmask(mask)
    elif key == ord('b'):
        mask = np.array(boost).reshape(3, 3).astype(np.float32)

cap.release()
cv2.destroyAllWindows()

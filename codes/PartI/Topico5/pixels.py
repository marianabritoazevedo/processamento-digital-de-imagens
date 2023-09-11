import cv2
import numpy as np

def main():
    image = cv2.imread("bolhas.png", cv2.IMREAD_GRAYSCALE)
    
    if image is None:
        print("Não foi possível abrir a imagem bolhas.png")
        return

    cv2.namedWindow("janela", cv2.WINDOW_AUTOSIZE)

    for i in range(200, 210):
        for j in range(10, 200):
            image[i, j] = 0
    
    cv2.imshow("janela", image)
    cv2.waitKey()

    image = cv2.imread("bolhas.png")

    val = np.array([0, 0, 255], dtype=np.uint8)  # BGR format

    for i in range(200, 210):
        for j in range(10, 200):
            image[i, j] = val
    
    cv2.imshow("janela", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

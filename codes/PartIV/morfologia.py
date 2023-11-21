import cv2
import numpy as np
import sys

def main():
    if len(sys.argv) != 2:
        print("Uso: python script.py imagem")
        return

    # Carrega a imagem
    image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Erro ao carregar a imagem: {sys.argv[1]}")
        return

    # Elemento estruturante
    str_element = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Erosão
    erosao = cv2.erode(image, str_element)

    # Dilatação
    dilatacao = cv2.dilate(image, str_element)

    # Abertura
    abertura = cv2.morphologyEx(image, cv2.MORPH_OPEN, str_element)

    # Fechamento
    fechamento = cv2.morphologyEx(image, cv2.MORPH_CLOSE, str_element)

    # Abertura seguida de Fechamento
    abertfecha = cv2.morphologyEx(abertura, cv2.MORPH_CLOSE, str_element)

    # Concatenação horizontal das imagens resultantes
    result_image = np.concatenate((erosao, dilatacao, abertura, fechamento, abertfecha), axis=1)

    # Exibe a imagem resultante
    cv2.imshow("Morfologia", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

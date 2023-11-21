import streamlit as st
from PIL import Image

def page_u3_t11():
    st.title('Detecção de bordas com o algoritmo de Canny')
    st.markdown('''Este exercício tem como objetivo aplicar o algoritmo de Canny para gerar imagens artísticas com a técnica do pontilhismo.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando os programas [canny.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/canny.cpp) e [pontilhismo.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/pontilhismo.cpp),
    `cannypoints.cpp`. A ideia é usar as bordas produzidas pelo algoritmo de Canny para melhorar a qualidade da imagem pontilhista gerada.''')

    st.markdown('### Solução')
    st.markdown('''Utilizando os programas como base, inicialmente, são definidos os valores para o espaçamento entre os pontos, `jitter`, e o raio dos pontos. Com isso
    definido, realiza-se a leitura da imagem, e em seguida, cria-se uma matriz chamada `points` com o tamanho da imagem original e 3 canais de cores. Inicialmente, todos
    os pontos que estão sendo armazenados nesta matriz são brancos. ''')
    st.code('''
    import cv2
    import numpy as np
    import random

    # Definição dos parâmetros iniciais
    raio = 3 # Raio dos pontos 
    jitter = 4 # Espaçamento para os pontos 

    image = cv2.imread("paisagem2.jpg") 
    width = image.shape[1]
    height = image.shape[0]

    # Criação da matriz que irá armazenar os pontos. Inicialmente, todos
    # são completamente brancos
    points = np.full((height, width, 3), (255, 255, 255), dtype=np.uint8)
    ''')
    st.markdown('''Em seguida, é feito um loop mais externo, a fim de calcular várias vezes as bordas com o algoritmo de Canny, que conforme a sugestão da tarefa, terá
    os seus limiares aumentando gradativamente. Após detectar as bordas com `cv2.Canny()`, é feito um loop na imagem completa. O algoritmo de Canny, ao detectar uma borda,
    indica isto com o valor `255`. Logo, se uma borda for encontrada, será feito o seguinte procedimento:''')
    st.markdown('''
    - Encontrar a posição do ponto nos eixos x e y, levando em consideração o `jitter`;
    - Definir um passo, responsável por realizar o ajuste das cores;
    - Determinar propriamente a cor que será atribuída ao ponto;
    - Desenhar um ponto com `cv2.Circle()` com essas características.
    ''')

    st.code('''
    # Loop para detecção de bordas diversas vezes ao longo da imagem
    for i in range(1, 200, 10):
        # Detecção de bordas com o algoritmo Canny
        border = cv2.Canny(image, i, 3*i)

        # Loop para desenhar os pontos nas bordas. Deve-se passar por toda a imagem
        for l in range(0, height):
            for c in range(0, width):
                # Se é um pixel branco, quer dizer que detectou uma borda
                if border[l, c] == 255:
                    # Posição do ponto a partir de número aleatório dentro do intervalo de jitter
                    x = int(l + random.randint(-jitter, jitter) + 1)
                    y = int(c + random.randint(-jitter, jitter) + 1)
                    x = max(0, min(x, height - 1))  # Garante que x está dentro dos limites
                    y = max(0, min(y, width - 1))   # Garante que y está dentro dos limites
                    # Definição de passo para ajuste da intensidade da cor
                    passo = (random.randint(0, 1) / 10.0) + 1.0
                    # Determinação da cor do ponto
                    val = (
                        min(int(image[x, y, 0] * passo), 255),
                        min(int(image[x, y, 1] * passo), 255),
                        min(int(image[x, y, 2] * passo), 255),
                    )
                    # Desenho do ponto na imagem 
                    cv2.circle(points, (y, x), raio, val, -1)

    cv2.imshow("result.png", points)
    cv2.waitKey()
    cv2.imwrite("result.png", points)
    ''')
    st.markdown('''Abaixo, encontra-se a imagem original e a arte que foi gerada a partir dela:''')
    img1 = Image.open('./images/paisagem2.jpg')
    st.image(img1)
    img2 = Image.open('./images/pontilhismo.png')
    st.image(img2)
import streamlit as st
from PIL import Image

def page_u3_t12():
    st.title('Quantização vetorial com k-means')
    st.markdown('''Este exercício tem como objetivo experimentar o algoritmo k-means para clusterizar imagens.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [kmeans.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/kmeans.cpp) como exemplo, prepare um programa exemplo onde a 
    execução do código se dê usando o parâmetro `nRodadas=1`, e que os centros sejam iniciados de forma aleatória usando o parâmetro `KMEANS_RANDOM_CENTERS` ao invés de
    `KMEANS_PP_CENTERS`. Realize 10 rodadas diferentes do algoritmo e compare as imagens produzidas. Explique porque elas podem diferir tanto.''')

    st.markdown('### Solução')
    st.markdown('''O algoritmo K-means é um algoritmo iterativo que irá separar regiões ou pontos de uma figura com base em uma quantidade de `n` centros, em que a cada iteração,
    esses centros vão sendo recalculados de forma a obter a melhor clusterização possível. Neste exercício, o objetivo é encontrar 8 centros, que irão representar 8 cores 
    para a figura.''')
    st.markdown('''Assim, inicialmente, devem ser definidos os parâmetros do K-means, que neste caso, terá apenas uma rodada. Em seguida, é feita a leitura da imagem, e ela
    é convertida para o tipo `float`. Depois, é estabelecido um critério de parada e o algoritmo é rodado com a função `cv2.kmeans()`. Por fim, os rótulos de cada cluster
    encontrado são mapeados de volta para os pixels da imagem, e ao final, obtém-se a imagem final clusterizada.''')
    st.code('''
    import numpy as np
    import cv2
    import sys

    # Parâmetros para o algoritmo kmeans
    nClusters = 8
    nRodadas = 1

    # Verifica número de argumentos no comando
    if len(sys.argv) != 3:
        print("Usage: python kmeans.py input_image output_image")
        sys.exit(0)

    # Leitura da imagem de entrada
    img = cv2.imread(sys.argv[1])

    # Transforma a imagem em um array unidimensional de pontos de dados (samples) do tipo float
    samples = img.reshape((-1, 3)).astype(np.float32)

    # Critério de parada do algoritmo K-means
    criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001)

    # Aplicação do algoritmo
    _, labels, (centers) = cv2.kmeans(samples, nClusters, None, criterio, nRodadas, cv2.KMEANS_RANDOM_CENTERS)

    # Converte os centros dos clusters para o tipo de dados uint8
    centers = np.uint8(centers)

    # Mapeia os rótulos de cluster de volta para os pixels na imagem
    img_final = centers[labels.flatten()]
    img_final = img_final.reshape(img.shape)

    # Exibe e salva a imagem clusterizada
    cv2.imshow("kmeans", img_final)
    cv2.imwrite(sys.argv[2], img_final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ''')
    st.markdown('''Abaixo, encontra-se a imagem original e a imagem com o algoritmo K-means aplicado. Mesmo rodando o algoritmo 10 vezes, o resultado obtido sempre foi o
    mesmo, por isso está sendo ilustrada apenas uma imagem. Isso se deve à distribuição dos pixels da imagem: em algumas situações, devido a essa distribuição, mesmo com 
    os centros sendo implementados de forma aleatória, o k-means irá reproduzir o mesmo resultado.''')
    img1 = Image.open('./images/britto-kmeans.png')
    st.image(img1)
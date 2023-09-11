import streamlit as st
from PIL import Image

def page_u1_t2():
    st.title('Manipulando pixels em uma imagem')
    st.markdown('''Estes exercícios possuem como objetivo praticar algoritmos referentes à manipulação dos pixels de uma imagem.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [exemplos/pixels.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/pixels.cpp) como referência, implemente um programa 
    `regioes.cpp`. Esse programa deverá solicitar ao usuário as coordenadas de dois pontos $P_1$ e $P_2$  localizados dentro dos limites do tamanho da imagem e exibir
    o que lhe for fornecida. Entretanto, a região definida pelo retângulo de vértices opostos definidos pelos pontos $P_1$ e $P_2$ será exibida com o negativo da imagem na 
    região correspondente. O efeito é ilustrado na [Figura 4](https://agostinhobritojr.github.io/tutorial/pdi/#fig_regions)''')
    st.markdown('### Solução')
    st.markdown('Para resolver esta questão, antes de mais nada, deve-se realizar a leitura da imagem e solicitar as coordenadas dos pontos $P_1$ e $P_2$ ao usuário.')
    st.code('''
        import cv2

        image = cv2.imread('biel.png', cv2.IMREAD_GRAYSCALE)

        if image is None:
            print('Imagem não carregou corretamente')

        x1, y1 = map(int, input('Digite as coordenadas do ponto P1 separadas por vírgula: ').split(','))
        x2, y2 = map(int, input('Digite as coordenadas do ponto P2 separadas por vírgula: ').split(','))
    ''')
    st.markdown('''Em seguida, iremos percorrer cada pixel da imagem dentro das coordenadas definidas pelo usuário e implementar o negativo da imagem nesta região. Para isso,
    deve-se levar em consideração que o negativo de uma imagem, em uma imagem cinzenta, pode ser obtido a partir da seguinte fórmula:''')
    st.markdown('''$cor_{nova} = 255 - cor_{atual}$''')
    st.markdown('''Assim, esta implementação pode ser visualizada abaixo. É importante lembrar que no python, a expressão `range(x, y)` irá percorrer os pontos entre `x` e `y-1`,
    por isso é importante acrescentar o termo `+1` no loop para percorrer corretamente os pontos.''')
    st.code('''
    for i in range(x1, x2+1):
        for j in range(y1, y2+1):
            val_grayscale = image[i,j]
            val_negative = 255 - val_grayscale
            image[i,j] = val_negative
    ''')
    st.markdown('''Por fim, pode-se visualizar o resultado final da imagem e salvá-la.''')
    st.code('''
        cv2.imshow("image", image)
        cv2.imwrite("negativo.png", image)
        cv2.waitKey(0)
    ''')
    st.markdown('''Abaixo, segue o resultado obtido para o negativo de uma imagem com $P_1 = (50, 150)$ e $P_2 = (200, 200)$:''')
    img1 = Image.open('./images/negativo.png')
    st.image(img1)

    st.markdown('<hr>', unsafe_allow_html=True)

    # Segundo exercício
    st.markdown('## Exercício 2')
    st.markdown('''Utilizando o programa [exemplos/pixels.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/pixels.cpp) como referência, implemente um programa 
    `trocaregioes.cpp`. Seu programa deverá trocar os quadrantes em diagonal na imagem. Explore o uso da classe `Mat` e seus construtores para criar as regiões que serão trocadas. 
    O efeito é ilustrado na [Figura 5](https://agostinhobritojr.github.io/tutorial/pdi/#fig_trocaregioes)''')
    st.markdown('### Solução')
    st.markdown('Para resolver esta questão, utilizou-se a lógica de dividir a imagem em 4 regiões e realizar as suas trocas. A imagem abaixo ilustra a ideia seguida no código.')
    img2 = Image.open('./images/troca-regioes.png')
    st.image(img2)
    st.markdown('''Inicialmente, deve-se realizar a leitura da imagem e computar sua largura e altura. Também é importante calcular a metade da altura e da largura, visto que
    precisaremos destes valores para realizar corretamente a troca dos pixels em cada região. Para auxiliar nesta troca, é necessário realizar a cópia da imagem original. Estes
    passos podem ser observados no trecho de código abaixo.''')
    st.code('''
        import cv2

        image = cv2.imread('biel.png', cv2.IMREAD_GRAYSCALE)

        if image is None:
            print('Imagem não foi carregada corretamente')

        width = image.shape[0]
        height = image.shape[1]

        image_copy = image.copy()

        mean_width = int(width/2)
        mean_height = int(height/2)
    ''')
    st.markdown('''Em seguida, é feita efetivamente a troca das regiões, aplicando na imagem original as novas coordenadas a partir da cópia da imagem, e por fim, mostra-se a 
    imagem resultante na tela. Para isso, seguiu-se a segunte lógica para cada uma das regiões:''')
    st.markdown('''
    * __Região 1__: considerando as coordenadas desta região como $(x, y)$, devemos substitui-las por $(x+mean_{width}, y+mean_{height})$.
    * __Região 4__: considerando as coordenadas desta região como $(x+mean_{width}, y+mean_{height})$, devemos substitui-las por $(x, y)$.
    * __Região 2__: considerando as coordenadas desta região como $(x, y+mean_{height})$, devemos substitui-las por $(x+mean_{width}, y)$.
    * __Região 3__: considerando as coordenadas desta região como $(x+mean_{width}, y)$, devemos substitui-las por $(x, y+mean_{height})$.
    ''')
    st.code('''
        # Substituindo os quadrantes
        for i in range(mean_width):
            for j in range(mean_height):
                # Quadrante da região 1
                image[i,j] = image_copy[i+mean_width, j+mean_height]
                # Quadrante da região 4
                image[i+mean_width, j+mean_height] = image_copy[i,j]
                # Quadrante da região 2
                image[i, j+mean_height] = image_copy[i+mean_width,j]
                #Quadrante da região 3
                image[i+mean_width, j] = image_copy[i,j+mean_height]

        cv2.imshow("image", image)
        cv2.waitKey(0)
    ''')
    st.markdown('''Ao final, obteve-se a seguinte imagem:''')
    img3 = Image.open('./images/troca-regioe-result.png')
    st.image(img3)
    
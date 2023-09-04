import streamlit as st
from PIL import Image

def page_u1_t5():
    st.title('Preenchendo regiões')
    st.markdown('''Estes exercícios possuem como objetivo praticar algoritmos utilizados para realizar o preenchimento de regiões em imagens, como o `floodfill`, 
    bem como a rotulação de regiões da imagem, conhecimento como `labeling`.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Observando-se o programa [labeling.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/labeling.cpp) como exemplo, 
    é possível verificar que caso existam mais de 255 objetos na cena, o processo de rotulação poderá ficar comprometido. Identifique a situação em que isso 
    ocorre e proponha uma solução para este problema.''')
    st.markdown('### Solução')
    st.markdown('''Em geral, nos algoritmos de processamento digital de imagens, são utilizadas matrizes com variáveis do tipo `unsigned char`, com tamanho **1 byte**, para guardar
    informações de cores, por exemplo. Entretanto, uma variável deste tamanho só permite armazenar até 8 bits, ou seja, 256 possibilidades de valores. Dessa forma, considerando
    que uma cor será atribuída ao fundo da imagem, poderiam existir até 255 diferentes objetos para serem rotulados em uma imagem. ''')
    st.markdown('''Entretanto, em uma situação com mais de 255 objetos, o ideal seria utilizar uma outra estrutura para armazenar os valores referentes às cores. Por exemplo,
    poderia ser utilizada uma variável do tipo `short int` de tamanho **2 bytes** para conseguir armazenar uma maior quantidade de informações, e consequentemente, permitir a
    rotulação de mais de 255 objetos.''')
    st.markdown('<hr>', unsafe_allow_html=True)

    # Segundo exercício
    st.markdown('## Exercício 2')
    st.markdown('''Aprimore o algoritmo de contagem apresentado para identificar regiões com ou sem buracos internos que existam na cena. 
    Assuma que objetos com mais de um buraco podem existir. Inclua suporte no seu algoritmo para não contar bolhas que tocam as bordas da imagem. 
    Não se pode presumir, a priori, que elas tenham buracos ou não.''')
    st.markdown('### Solução')
    st.markdown('''Para realizar este exercício, será necessário seguir o passo a passo com as seguintes implementações: 

    1. Estrutura inicial do código (ler imagem, determinar dimensões)
    2. Mudança na cor de fundo
    3. Remoção de bolhas nas bordas
    4. Contagem de bolhas com buracos
    5. Contagem de bolhas sem buracos''')
    st.markdown('Antes de entrar na solução do problema, abaixo encontra-se a imagem que será utilizada para realizar a contagem de regiões com e sem buracos internos:')
    img1 = Image.open('./images/bolhas.png')
    st.image(img1)

    st.markdown('#### 1- Estrutura inicial do código')
    st.markdown('''Antes de realizar qualquer processamento, é necessário abrir corretamente a imagem, determinar sua largura e altura, bem como variáveis auxiliares. Essas
    variáveis são: `complete_bubbles` para indicar a quantidade de bolhas sem buracos, `holes_bubbles` para indicar a quantidade de bolhas com buracos, e `new_background` um
    booleano para identificar se o fundo já foi pintado com a nova cor.''')
    st.code('''
        import cv2

        # Carregar a imagem em escala de cinza
        image = cv2.imread("bolhas.png", cv2.IMREAD_GRAYSCALE)

        # Verifica se carregou corretamente a imagem
        if image is None:
            print("Não foi possível carregar a imagem")
            exit()

        # Definição da largura e altura da imagem. Ela é retornada com um array [altura, largura]
        width = image.shape[1]
        height = image.shape[0]
        print(f"Tamanho da imagem: {width}x{height}")

        # Inicialmente, nenhuma bolha com buracos ou sem buracos
        complete_bubbles = 0
        holes_bubbles = 0
        new_brackground = False
    ''')

    st.markdown('#### 2- Mudança de cor do fundo')
    st.markdown('''Para poder identificar corretamente as regiões em branco, tenham buracos ou não, é necessário pintar o fundo com uma cor diferente para ficar mais fácil de
    identificar as regiões com bolhas. Agora, será adotado que `0` será a cor para o interior das bolhas com buraco, `255` será a cor propriamente das bolhas e `128` será
    a nova cor de fundo. Para isso, ao identificar o primeiro pixel com cor `0`, será aplicado o algoritmo `floodfill` para preencher a região com a cor `128`.''')
    st.code('''
        # Pintar o plano de fundo com uma nova cor. Será atribuída a cor 128
        for i in range(width):
            for j in range(height):
                if image[i, j] == 0 and not new_brackground:
                    cv2.floodFill(image, None, (j, i), 128)
                    new_brackground = True
                    break
                if new_brackground:
                    break
    ''')
    st.markdown('Abaixo encontra-se o resultado de como ficou a imagem após realizada esta etapa:')
    img2 = Image.open('./images/parte1-bolhas.png')
    st.image(img2)

    st.markdown('#### 3- Remoção de bolhas nas bordas')
    st.markdown('''Bolhas nas bordas não irão ser levadas em consideração no algoritmo de contagem. Assim, deve-se percorrer os 4 cantos da imagem, com altura `0` ou `height-1`,
    bem como largura `0` ou `width-1`, e aplicar novamente o algoritmo `floodfill`. ''')
    st.code('''
        # Ao encontrar algo nas bordas, desconsiderar da contagem, pintar da cor do plano de fundo
        for i in range(width):
            if image[i, 0] == 255 or image[i, 0] == 0:
                cv2.floodFill(image, None, (0, i), 128) # Retira bolhas do lado esquerdo
            if image[i, height-1] == 255 or image[i, height-1] == 0:
                cv2.floodFill(image, None, (height-1, i), 128) # Retira bolhas do lado direito

        for j in range(height):
            if image[0, j] == 255 or image[0, j] == 0:
                cv2.floodFill(image, None, (j, 0), 128) # Retira bolhas do lado superior
            if image[width-1, j] == 255 or image[width-1, j] == 0:
                cv2.floodFill(image, None, (j, width-1), 128) # Retira bolhas do lado inferior
    ''')
    st.markdown('Abaixo encontra-se o resultado obtido após realizar este processamento:')
    img3 = Image.open('./images/parte2-bolhas.png')
    st.image(img3)

    st.markdown('#### 4- Contagem de bolhas com buracos')
    st.markdown('''As bolhas com buracos poderão ser identificadas da seguinte forma: ao percorrer a imagem, se for identificado um pixel com cor `0`, e o seu pixel imediatamente à
    direita possuir cor `255`, significa que uma bolha com buraco foi encontrada. Deve-se incrementar seu respectivo contador, e em seguida, aplicar o `floodfill` na região com
    cor `255`, para representar que esta bolha já foi contabilizada.''')
    st.code('''
        # Procurando as bolhas COM buracos. Para isso, é preciso encontrar um buraco (cor 0) e na sua lateral esquerda, ser uma bolha (cor 255)
        # Em seguida, pode-se pintar a bolha (cor 255) com a cor de fundo
        for i in range(width):
            for j in range(height):
                if image[i, j] == 0 and image[i, j-1] == 255:
                    holes_bubbles += 1
                    cv2.floodFill(image, None, (j-1, i), 128)

        print(f"Bolhas com buraco: {holes_bubbles}")
    ''')
    st.markdown('Abaixo encontra-se o resultado obtido após realizar este processamento:')
    img4 = Image.open('./images/parte3-bolhas.png')
    st.image(img4)

    st.markdown('#### 5- Contagem de bolhas sem buracos')
    st.markdown('''Por fim, deve-se percorrer a imagem novamente e identificar as bolhas sem buracos. Ao encontrar um pixel com cor `255`, obrigatoriamente teremos uma bolha sem
    buraco. Deve-se incrementar seu respectivo contador, e aplicar o `floodfill` neste pixel.''')
    st.code('''
        for i in range(width):
            for j in range(height):
                if image[i, j] == 255:
                    complete_bubbles += 1
                    cv2.floodFill(image, None, (j, i), 128)

        print(f"Bolhas sem buraco: {complete_bubbles}")
    ''')
    st.markdown('Abaixo encontra-se o resultado obtido após realizar este processamento:')
    img5 = Image.open('./images/parte4-bolhas.png')
    st.image(img5)
    st.markdown('Ao final, obteve-se que a seguinte saída:')
    st.code('''
        Bolhas com buracos: 7
        Bolhas sem buracos: 14
    ''')

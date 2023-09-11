import streamlit as st
from PIL import Image

def page_u1_t4():
    st.title('Decomposição de imagens em planos de bits')
    st.markdown('''Este exercício possue como objetivo realizar a decodificação de uma imagem escondida em outra imagem.''')

    st.markdown('## Exercício 1')
    st.markdown('''Usando o programa [esteg-encode.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/esteg-encode.cpp) como referência para esteganografia, escreva
    um programa que recupere a imagem codificada de uma imagem resultante de esteganografia. Lembre-se que os bits menos significativos dos pixels da imagem fornecida deverão 
    compor os bits mais significativos dos pixels da imagem recuperada. O programa deve receber como parâmetros de linha de comando o nome da imagem resultante da esteganografia. 
    Teste a sua implementação com a imagem da [Figura 14](https://agostinhobritojr.github.io/tutorial/pdi/#fig_desafio_esteganografia).''')
    st.markdown('### Solução')
    st.markdown('''Para resolver este problema e reproduzir a imagem que está escondida na imagem codificada, tornou-se necessário recuperar os bits da imagem escondida e 
    torná-los os mais significativos para gerar a nova imagem, levando em consideração os 3 canais de cores R, G e B. A ilustração abaixo explica o processo 
    realizado neste exercício:''')

    img1 = Image.open('./images/decodificacao.png')
    st.image(img1)

    st.markdown('''Considerando que 1 byte possui 8 bits, de forma que os 5 primeiros bits são da imagem codificada e os 3 últimos da imagem escondida, realizou-se o deslocamento 
    à esquerda bit a bit com um total de 5 bits para recuperar a imagem escondida. Ao fazer isso, agora os 3 primeiros bits serão os bits mais significativos da imagem escondida,
    e os 5 bits restantes serão preenchidos com `0`.''')
    st.markdown('''Dessa forma, deve-se inicialmente ler a imagem, definir sua largura a altura, bem como a quantidade de bits a serem deslocados. Também é importante realizar
    uma cópia da imagem original para podermos sobrescrevê-la e gerar a imagem escondida.''')
    st.code('''
    import cv2
    import sys
    import numpy as np

    # Leitura da imagem
    image = cv2.imread(sys.argv[1], cv2.IMREAD_COLOR)
    if image is None:
        print('Imagem não carregada corretamente')

    # Definição das dimensões da imagem
    width = image.shape[0]
    height = image.shape[1]
    # Quantidade de bits a serem deslocados
    nbits = 5

    imagemEscondida = image.copy()
    ''')

    st.markdown('''Em seguida, realiza-se o deslocamento de bits para cada pixel da imagem conforme explicado anteriormente, e em seguida, atribui-se o novo pixel à imagem 
    escondida. Por fim, pode-se visualizar a imagem resultante e salvá-la.''')
    st.code('''
    for i in range(width):
        for j in range(height):
            valImage = image[i,j]

            # Para obter a imagem escondida, deve-se deslocar a imagem original 5 bits para a esquerda. 
            # Assim, teremos os 3 bits escondidos nas posições mais significativas, e o restante preenchido com 0
            valImage[0] = valImage[0] << nbits
            valImage[1] = valImage[1] << nbits
            valImage[2] = valImage[2] << nbits

            # Atribuição destes bits para a imagem escondida
            imagemEscondida[i,j] = valImage

    cv2.imwrite("esteganografia.png", imagemEscondida)
    cv2.imshow("image", imagemEscondida)
    cv2.waitKey(0)
    ''')

    st.markdown('Abaixo, pode-se visualizar a imagem original e a imagem escondida obtida após a decodificação:')
    img2 = Image.open('./images/result-decode.png')
    st.image(img2)
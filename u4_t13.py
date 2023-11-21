import streamlit as st
from PIL import Image

def page_u4_t13():
    st.title('Filtragem de forma com morfologia matemática')
    st.markdown('''Este exercício tem como praticar técnicas de morfologia com imagens de dígitos.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Usando o programa [morfologia.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/morfologia.cpp) como referência, crie um programa que resolva o
    problema da pré-filtragem para o reconhecimento dos caracteres usando operações morfológicas. Cuidado para deixar o ponto decimal separado dos demais dígitos para evitar
    um reconhecimento errado do número do visor.''')

    st.markdown('### Solução')
    st.markdown('''Inicialmente, foram exploradas quatro operações morfológicas (erosão, dilatação, abertura e fechamento) com diferentes tamanhos para o elemento estruturante 
    a fim de encontrar qual seria a melhor solução para completar os dígitos corretamente. O maior desafio deste programa encontra-se para completar o dígito `0`, que possui uma
    parte em branco com a altura consideravelmente maior do que a largura.''')
    st.markdown('''Nesse sentido, a melhor solução obtida foi encontrada a partir da utilização da abertura com um elemento estruturante em forma de retângulo com dimensões
    (4, 11). Abaixo, encontra-se a implementação do código para completar os dígitos, em que há a leitura da imagem, definição do elemento estruturante, aplicação da abertura,
    e por fim, a exibição da imagem resultante.''')
    st.code('''
    import cv2
    import numpy as np
    import sys

    # Carrega a imagem
    image = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)

    if image is None:
        print(f"Erro ao carregar a imagem: {sys.argv[1]}")

    # Elemento estruturante
    str_element = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 11))

    # Operação de abertura
    abertura = cv2.morphologyEx(image, cv2.MORPH_OPEN, str_element)
    result_image = abertura

    # Exibe a imagem resultante
    cv2.imshow("Morfologia", result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ''')
    st.markdown('''A figura abaixo ilustra os resultados obtidos para as 5 figuras de dígitos fornecidas para teste:''')
    img1 = Image.open('./images/todos-digitos.png')
    st.image(img1)

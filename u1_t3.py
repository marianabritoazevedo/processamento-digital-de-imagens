import streamlit as st
from PIL import Image

def page_u1_t3():
    st.title('Serialização de dados em ponto flutuante via FileStorage')
    st.markdown('''Este exercício tem como objetivo praticar a manipulação de imagens PNG e YML.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [filestorage.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/filestorage.cpp) como base, crie um programa que gere 
    uma imagem de dimensões 256x256 pixels contendo uma senóide de 4 períodos com amplitude de 127 desenhada na horizontal, como aquela apresentada na 
    [Figura 6](https://agostinhobritojr.github.io/tutorial/pdi/#fig_filestorage). Grave a imagem no formato PNG e no formato YML. Compare os arquivos gerados, extraindo uma 
    linha de cada imagem gravada e comparando a diferença entre elas. Trace um gráfico da diferença calculada ao longo da linha correspondente extraída nas imagens. 
    O que você observa?''')
    st.markdown('### Solução')
    st.markdown('Para resolver esta questão, inicialmente, deve-se importar as bibliotecas necessárias e armazenar constantes com as dimensões da imagem e os períodos da senoide.')
    st.code('''
    import cv2
    import numpy as np
    import math
    import plotly.express as px
    import plotly.io as pio

    # Constantes do programa
    SIDE = 256
    PERIODOS = 4

    ''')
    st.markdown(''' Em seguida, são criadas as variáveis do tipo `FileStorage`, que permitem armazenar dados em arquivos com um formato mais genérico, tanto para imagem YML quanto
    para a imagme PNG. No próximo passo, será gerada a imagem YML. Para isso, iremos escrever na imagem apenas zeros (sendo uma variável do tipo float), e em seguida, para cada
    pixel, será calculado o seu valor com base na senóide determinada no problema. Por fim, esta imagem é escrita no arquivo `senoide.yml`. 
    ''')
    st.code('''
    # Armazenamento da imagem como png e como yml
    img_png = cv2.FileStorage()
    img_yml = cv2.FileStorage()

    # Abre imagem YML e escreve apenas zeros, com o tipo float
    img_yml.open("senoide.yml", cv2.FileStorage_WRITE)
    image = np.zeros((SIDE, SIDE), dtype=np.float32)

    # Imagem yml com valores da senóide
    for i in range(SIDE):
        for j in range(SIDE):
            image[i, j] = 127 * math.sin(2 * math.pi * PERIODOS * j / SIDE) + 128

    # Escreva a matriz de imagem no arquivo YAML
    img_yml.write("yml_final", image)
    img_yml.release()
    ''')
    st.markdown(''' Posteriormente, será gerada a imagem do tipo PNG. Esta imagem não suporta valores do tipo float, assim, é preciso normalizar a imagem anterior, aplicando 
    `cv2.NORM_MINMAX`, e em seguida, convertê-la para o tipo `uint8`. Logo em seguida, é possível escrevê-la em um arquivo denominado `senoide.png`.
    ''')
    st.code('''
    # Normaliza a imagem inicialmente em yml e converte para o tipo int 8
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    image = np.uint8(image)

    # Abre a imagem PNG e salva a matriz resultante
    img_png.open("senoide.png", cv2.FileStorage_WRITE)
    img_png.write("mat", image)
    img_png.release()
    ''')
    st.markdown('''Por fim, para verificar que a imagem foi gerada corretamente, abre-se a imagem YML, realiza-se novamente sua conversão, e a imagem PNG final é mostrada
    na tela. Nesta etapa, também são capturados os valores dos pixels da primeira linha de cada uma das imagens geradas.
    ''')
    st.code('''
    # Para verificar que funcionou corretamente, abre a imagem yml, normaliza e converte para mostrá-la
    # Também salva os valores dos pixels da primeira linha da imagem YML e PNG
    img_yml.open("senoide.yml", cv2.FileStorage_READ)
    image = img_yml.getNode("yml_final").mat()
    line_yml = image[0, :]
    img_yml.release()

    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX)
    image = np.uint8(image)
    line_png = image[0, :]

    # Mostra a imagem na tela
    cv2.imshow("image", image)
    cv2.waitKey(0)
    ''')
    st.markdown(''' A imagem PNG gerada pode ser visualizada abaixo:''')
    img1 = Image.open('./images/senoide-final.png')
    st.image(img1)

    st.markdown('''Para concluir o exercício, deve-se comparar os arquivos gerados, extraindo uma linha de cada imagem, e visualizando a diferença entre elas. O trecho de
    código abaixo ilustra um exemplo com alguns os 10 primeiros valores presentes na primeira linha da figura YML e da figura PNG, respectivamente:''')
    st.code('''
    data_yml = [128., 1.40448181e+02, 1.52776474e+02, 1.64866150e+02, 
       1.76600800e+02, 1.87867386e+02, 1.98557419e+02, 2.08567947e+02,
       2.17802567e+02, 2.26172333e+02, 2.33596634e+02]
    data_png = [127, 139, 152, 164, 176, 187, 198, 208, 217, 226]
    ''')
    st.markdown('''Tendo em vista tais valores, realiza-se o cálculo da diferença entre os valores dos pixels da imagem YML e da imagem PNG, e ao final, é exibido um gráfico com
    as diferenças.''')
    st.code('''
    # Pega valores da primeira linha de cada um dos tipos de imagem e traça um gráfico 
    eixoy = line_yml - line_png
    eixox = [x for x in range(0, 256)]

    # Cria e salva gráfico gerado
    fig = px.line(x=eixox, y=eixoy, title='Diferenças pixels YML x PNG', labels={'y': 'Diferença', 'x': 'Coluna do pixel da primeira linha'})
    fig.update_layout(width=1200) 
    pio.write_image(fig, 'diferencas_graph.png')

    # Exibe o gráfico gerado
    image = cv2.imread('diferencas_graph.png')
    cv2.imshow('Gráfico das diferenças', image)
    cv2.waitKey(0)
    ''')
    st.markdown('''Abaixo, pode-se visualizar o gráfico obtido. É possível perceber que, assim como para a imagem, o gráfico de diferenças possui um comportamento periódico,
    semelhante a uma senoide.''')
    img2 = Image.open('./images/diferencas_graph.png')
    st.image(img2)
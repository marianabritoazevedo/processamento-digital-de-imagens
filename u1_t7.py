import streamlit as st
from PIL import Image

def page_u1_t7():
    st.title('Filtragem no domínio espacial I')
    st.markdown('''Estes exercícios possuem como objetivo praticar a aplicação de filtros.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [filtroespacial.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/filtroespacial.cpp) como referência, implemente um 
    programa `laplgauss.cpp`. O programa deverá acrescentar mais uma funcionalidade ao exemplo fornecido, permitindo que seja calculado o laplaciano do gaussiano das 
    imagens capturadas. Compare o resultado desse filtro com a simples aplicação do filtro laplaciano.''')

    st.markdown('### Solução')
    st.markdown('''O primeiro passo é realizar os ajustes da câmera, verificando se ela foi aberta corretamente, e depois, definindo sua altura e largura, bem como 3 janelas: 
    uma com a imagem original, outra aplicando apenas o laplaciano, e última aplicando o laplaciano do gaussiano.''')
    st.code('''
        import cv2
        import numpy as np

        # Inicializa a captura de vídeo a partir da câmera padrão (0)
        cap = cv2.VideoCapture(0)

        # Verifica se a câmera foi aberta corretamente
        if not cap.isOpened():
            print("Câmera indisponível")
            exit()

        # Define a largura e altura desejadas para o vídeo
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Exibe a largura e altura do vídeo
        print("Largura =", width)
        print("Altura =", height)

        # Define uma janela para a imagem cinza, e outra para a imagem equalizada
        cv2.namedWindow('Original', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Laplaciano', cv2.WINDOW_NORMAL)
        cv2.namedWindow('LaplGauss', cv2.WINDOW_NORMAL)

        # Redefine o tamanho das janelas para a altura e largura que eu defini
        cv2.resizeWindow('Original', width, height)
        cv2.resizeWindow('Laplaciano', width, height)
        cv2.resizeWindow('LaplGauss', width, height)
    ''')

    st.markdown('''Em seguida, são definidas as máscaras com os valores dos filtros laplaciano e gaussiano. Vale ressaltar que estes dois filtros aplicados são os seguintes:''')
    img1 = Image.open('./images/filtros-masks.png')
    st.image(img1)
    st.code('''
        # Variáveis referentes aos filtros
        gauss = [0.0625, 0.125,  0.0625, 0.125, 0.25,
                    0.125,  0.0625, 0.125,  0.0625]
        laplacian = [0, -1, 0, -1, 4, -1, 0, -1, 0]

        mask_gauss = np.array(gauss).reshape(3, 3).astype(np.float32)
        mask_laplacian = np.array(laplacian).reshape(3, 3).astype(np.float32)
    ''')
    st.markdown('''Por fim, enquanto o programa estiver executando, ele irá aplicar os dois filtros utilizando a função `cv2.filter2D` do OpenCV. É válido ressaltar que, para
    a aplicação correta dos filtros, é necessário converter a imagem para o tipo `float`, aplicar a operação, e depois, convertê-la novamente para o seu formato original.
    Ao final, podem ser visualizadas todas as três imagens citadas.''')
    st.code('''
            while True:
                # Captura um quadro do vídeo
                ret, frame = cap.read()

                # Sai do loop se não houver mais quadros
                if not ret:
                    break

                # Converte a imagem capturada para tons de cinza
                gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Cópia do tipo float para permitir a aplicação dos filtros
                frame_float = gray_frame.astype(np.float32)

                # Define filtro laplaciano
                laplacian_frame = cv2.filter2D(frame_float, -1, mask_laplacian, borderType=cv2.BORDER_CONSTANT)
                laplacian_frame = laplacian_frame.astype(np.uint8)

                # Define filtro laplaciano do gaussiano
                gauss_frame = cv2.filter2D(frame_float, -1, mask_gauss, borderType=cv2.BORDER_CONSTANT)
                gauss_laplace_frame = cv2.filter2D(gauss_frame, -1, mask_laplacian, borderType=cv2.BORDER_CONSTANT)
                gauss_laplace_frame = gauss_laplace_frame.astype(np.uint8)

                # Mostra a imagem em tons de cinza
                cv2.imshow('Original', gray_frame)
                cv2.imshow('Laplaciano', laplacian_frame)
                cv2.imshow('LaplGauss', gauss_laplace_frame)

                # Sai do loop se for pressionada a tecla ESC
                if cv2.waitKey(30) == 27:
                    break

            cap.release()
            cv2.destroyAllWindows()
    ''')
    img2 = Image.open('./images/filtros.png')
    st.image(img2)
    st.markdown('''É válido ressaltar que apenas a aplicação do laplaciano, sem aplicar um filtro suavizante antes, pode resultar no aumento do ruído da imagem, visto
    que esse operador é sensível a variações em alta frequência na imagem.''')

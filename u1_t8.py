import streamlit as st
from PIL import Image

def page_u1_t8():
    st.title('Filtragem no domínio espacial II')
    st.markdown('''Estes exercícios possuem como objetivo praticar a aplicação de filtros, mais especificamente, o tiltshift.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [addweighted.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/addweighted.cpp) como referência, implemente 
    um programa `tiltshift.cpp`. Três ajustes deverão ser providos na tela da interface:''')
    st.markdown('''
    - Um ajuste para regular a altura da região central que entrará em foco;
    - Um ajuste para regular a força de decaimento da região borrada;
    - Um ajuste para regular a posição vertical do centro da região que entrará em foco. Finalizado o programa, a imagem produzida deverá ser salva em arquivo.
    ''')

    st.markdown('### Solução')
    st.markdown('''Antes de mais nada, é necessário entender o processo utilizado para gerar o efeito do tiltshift. Este processo se encontra ilustrado na figura abaixo:''')
    img1 = Image.open('./images/explicacao-tiltshift.png')
    st.image(img1)
    st.markdown('''Basicamente, a partir da imagem original, deve-se criar uma cópia da imagem e outra imagem com o filtro média aplicado para gerar o borramento. Em seguida, 
    é preciso gerar duas imagens com a equação abaixo, que vai variando entre os tons de cinza, sendo uma o inverso da outra.''')
    st.latex(r'''
    \alpha(x) = -0.5 (tanh(\frac{x - l_1}{d}) - tanh(\frac{x - l_2}{d}))
    ''')
    st.markdown('''Agora, em relação ao código, o primeiro passo consiste na definição dos parâmetros iniciais do tiltshift, bem como dos sliders para controlá-los.''')
    st.code('''
        # Parâmetros da fórmula que poderão ser regulados
        l1, l2, d, centro = -50, 50, 6, 100

        # Tamanho da matriz em que será aplicado o filtro média
        mask_media_tam = 15

        # Valores iniciais dos sliders e seus limites
        altura, decaimento, posicao = 0, 0, 0
        altura_max, decaimento_max, posicao_max = 100, 100, 100

        # Variável para armazenar o resultado final do tiltshift
        resultado = None
    ''')
    st.markdown('''Em seguida, cria-se a função `apply_tiltshift` para aplicar o processo descrito anteriormente à imagem:''')
    st.code('''
        def apply_tiltshift(imagem, imagem_borrada):
            global l1, l2, d, centro, resultado

            # Definição inicialmente de uma matriz apenas com zeros com a mesma dimensão da imagem original
            ponderada = np.zeros_like(imagem, dtype=np.float32)

            # Para a altura da imagem, aplicar a função de ponderação
            altura_imagem = imagem.shape[0]
            for i in range(altura_imagem):
                ponderacao = -0.5 * (np.tanh((i - centro + l1) / d) - np.tanh((i - centro + l2) / d))
                ponderada[i, :, :] = ponderacao

            # Calcular a ponderação inversa
            ponderada_negativa = 1.0 - ponderada
            # Multiplicação da imagem original com a ponderação
            res1 = cv2.multiply(imagem, ponderada)
            # Multiplicação da imagem borrada com a ponderação negativa
            res2 = cv2.multiply(imagem_borrada, ponderada_negativa)
            # Adição das duas imagens e transformação do tipo
            resultado = cv2.add(res1, res2).astype(np.uint8)
            print(f'l1={l1}, l2={l2}, d={d}, centro={centro}')

            cv2.imshow("Tiltshift", resultado)
    ''')
    st.markdown('''Também são criadas funções para auxiliarem a detecção de movimentação no slider, com o objetivo de atualizar corretamente os valores da altura, decaimento
    e deslocamento.''')
    st.code('''
        # Verifica as mudanças nos parâmetros l1 e l2, implicando na mudança da altura
        def on_trackbar_altura(val):
            global l1, l2
            # Obtem o valor do slider de altura
            altura_slider = cv2.getTrackbarPos("Altura", "Tiltshift")
            # Mapeia inversamente o valor do slider para l1 e l2 em um intervalo maior
            l1 = -altura_slider * 1.5
            l2 = altura_slider * 1.5
            apply_tiltshift(imagem, imagem_borrada)

        # Verifica mudanças no parâmetro d, implicando em mudanças no borramento
        def on_trackbar_decaimento(val):
            global d
            d = val
            apply_tiltshift(imagem, imagem_borrada)

        # Verifica mudanças no parâmetro centro, implicando em mudanças no local em que
        # a imagem não estará borrada
        def on_trackbar_deslocamento(val):
            global centro
            centro = val * imagem.shape[0] / 100
            apply_tiltshift(imagem, imagem_borrada)
    ''')
    st.markdown('''Por fim, cria-se a janela para exibir a imagem e seus respectivos sliders, e ao final, se o usuário clicar na tecla `ESC`, a imagem será salva em um arquivo
    chamado `resultado_tiltshift.jpg`''')
    st.code('''
        # Leitura da imagem original
        imagem = cv2.imread("paisagem.jpg").astype(np.float32)
        # Criação da imagem borrada
        imagem_borrada = cv2.filter2D(imagem, -1, np.ones((mask_media_tam, mask_media_tam), np.float32) / (mask_media_tam ** 2))

        # Criação da janela com os sliders para mudar os valores
        cv2.namedWindow("Tiltshift", cv2.WINDOW_AUTOSIZE)
        cv2.createTrackbar("Altura", "Tiltshift", altura, altura_max, on_trackbar_altura)
        cv2.createTrackbar("Decaimento", "Tiltshift", decaimento, decaimento_max, on_trackbar_decaimento)
        cv2.createTrackbar("Deslocamento", "Tiltshift", posicao, posicao_max, on_trackbar_deslocamento)

        apply_tiltshift(imagem, imagem_borrada)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # 27 é o código da tecla ESC
                # Salva a imagem antes de fechar
                if resultado is not None:
                    cv2.imwrite("resultado_tiltshift.jpg", resultado)
                break

        cv2.destroyAllWindows()
    ''')
    st.markdown('''Abaixo, observa-se o resultado final do programa com a imagem e seus sliders:''')
    img2 = Image.open('./images/simulador-tiltshift-imagem.png')
    st.image(img2)

    st.markdown('<hr>', unsafe_allow_html=True)

    # Segundo exercício
    st.markdown('## Exercício 2')
    st.markdown('''Utilizando o programa [addweighted.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/addweighted.cpp) como referência, implemente 
    um programa `tiltshiftvideo.cpp`. Tal programa deverá ser capaz de processar um arquivo de vídeo, produzir o efeito de tilt-shift nos quadros presentes e escrever 
    o resultado em outro arquivo de vídeo. A ideia é criar um efeito de miniaturização de cenas. Descarte quadros em uma taxa que julgar conveniente para evidenciar o 
    efeito de stop motion, comum em vídeos desse tipo.''')
    st.markdown('### Solução')
    st.markdown('''Basicamente, utilizou-se o mesmo código do exercício 1, realizando-se apenas algumas adaptações para o trabalho com o vídeo. Nesse sentido, inicialmente, 
    deve-se ler o vídeo e capturar sua altura e largura, bem como criar uma variável em que serão escritos os frames do novo vídeo. ''')
    st.code('''
        # Caminho para o vídeo original
        caminho_video = 'video-pdi.mp4'

        # Abre o vídeo original
        cap = cv2.VideoCapture(caminho_video)

        # Verifica se o vídeo foi aberto com sucesso
        if not cap.isOpened():
            print("Erro ao abrir o vídeo.")
            exit()

        # Obtém informações do vídeo original (largura, altura, taxa de frames, etc.)
        largura = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        altura = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        taxa_frames = cap.get(cv2.CAP_PROP_FPS)

        # Define o codec e cria um objeto VideoWriter para escrever o novo vídeo
        codec = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para formato MP4
        novo_caminho_video = 'novo-video.mp4'
        novo_video = cv2.VideoWriter(novo_caminho_video, codec, taxa_frames, (largura, altura))

        # Contador de frames
        contador_frames = 0
    ''')
    st.markdown('''Em seguida, realiza-se o seguinte processo: a cada três frames, um deles é capturado e aplicado o tiltshift com os valores dos parâmetros já definidos, e
    então, escreve-se esse frame de forma duplicada no novo arquivo de vídeo (isto é feito com o intuito de simular o stop motion). Por fim, o novo vídeo é salvo.''')
    st.code('''
        while True:
            # Lê um frame do vídeo
            ret, frame = cap.read()

            # Verifica se o frame foi lido corretamente
            if not ret:
                break

            # A cada 3 frames, aplica o filtro tilt-shift
            if contador_frames % 3 == 0:
                # Aplica o filtro tilt-shift

                # Tamanho da matriz em que será aplicado o filtro média
                mask_media_tam = 15
                frame = frame.astype(np.float32)
                frame_borrado = cv2.filter2D(frame, -1, np.ones((mask_media_tam, mask_media_tam), np.float32) / (mask_media_tam ** 2))
                frame_modificado = apply_tiltshift(frame, frame_borrado)  # Aqui você pode modificar os parâmetros de tilt-shift conforme necessário

                # Escreve o frame modificado no novo vídeo
                for i in range(2):
                    novo_video.write(frame_modificado)

            contador_frames += 1

        # Libera o objeto de captura e o objeto de gravação
        cap.release()
        novo_video.release()

    print(f'Novo vídeo salvo em: {novo_caminho_video}')
    ''')
    st.markdown('''O vídeo final após a aplicação do tiltshift pode ser conferido [aqui](https://drive.google.com/file/d/1MifX70_powq_0vcAJxIXc_1hrA-oWzkc/view?usp=sharing)! ''')
    
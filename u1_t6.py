import streamlit as st
from PIL import Image

def page_u1_t6():
    st.title('Manipulação de histogramas')
    st.markdown('''Estes exercícios possuem como objetivo praticar o algoritmo de equalização de histograma, realizando sua aplicação direta e também aplicando-o no contexto
    de detecção de movimento em filmagens.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [histogram.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/histogram.cpp) como referência, implemente um programa 
    `equalize.cpp`. Este deverá, para cada imagem capturada, realizar a equalização do histogram antes de exibir a imagem. Teste sua implementação apontando a câmera para 
    ambientes com iluminações variadas e observando o efeito gerado. Assuma que as imagens processadas serão em tons de cinza.''')

    st.markdown('### Solução')

    st.markdown('''Para implementar este programa, inicialmente, é necessário realizar as configurações no OpenCV para capturar a imagem da câmera desejada. Para isso, é
    preciso verificar se a câmera abriu corretamente, definir o tamanho da largura e altura da janela e atribuir nomes à cada uma das janelas.''')
    st.markdown('''⚠️ **Atenção**: neste código, utilizou-se o índice `0` para abrir a câmera, mas é possível que você precise utilizar um índice diferente a depender das configurações
    de vídeo e das câmeras de seu computador ou notebook''')
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
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Exibe a largura e altura do vídeo
        print("Largura =", width)
        print("Altura =", height)

        # Define uma janela para a imagem cinza, e outra para a imagem equalizada
        cv2.namedWindow('Gray Image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Equalized Image', cv2.WINDOW_NORMAL)

        # Redefine o tamanho das janelas para a altura e largura que eu defini
        cv2.resizeWindow("Gray Image", width, height)
        cv2.resizeWindow("Equalized Image", width, height)
    ''')

    st.markdown('''Em seguida, enquanto a câmera estiver ligada, é preciso transformar a imagem para tons de cinza, e em seguida, realizar a equalização do histograma. 
    Isso pode ser feito de duas maneiras: ''')
    st.markdown('''**1ª possibilidade**: aplicar diretamente a função `cv2.equalizeHist()` que já faz a equalização do histograma, e em seguida, mostrar a imagem original e
    sua imagem equalizada. Ao pressionar a tecla `ESC`, o programa será finalizado.''')
    st.code('''
        while True:
            # Captura um quadro do vídeo
            ret, frame = cap.read()

            # Sai do loop se não houver mais quadros
            if not ret:
                break

            # Converte a imagem capturada para tons de cinza
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Aplica diretamente a equalização de histograma
            equalized_frame = cv2.equalizeHist(gray_frame)

            # Mostra a imagem em tons de cinza
            cv2.imshow('Gray Image', gray_frame)
            cv2.imshow('Equalized Image', equalized_frame)

            # Sai do loop se for pressionada a tecla ESC
            if cv2.waitKey(30) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    ''')

    st.markdown('''**2ª possibilidade**: aplicar o passo a passo da equalização do histograma, que inclui: 

    (1) Cálculo do histograma original;
    (2) Cálculo do histograma acumulado;
    (3) Normalização do histograma acumulado; 
    (4) Aplicação da transformação na imagem original.  ''')
    st.markdown('''Da mesma forma que o programa anterior, ao final, serão exibidas as imagens original e sua imagem equalizada, e ao pressionar a tecla `ESC`, o programa 
    será finalizado.''')
    st.code('''
        while True:
            # Captura um quadro do vídeo
            ret, frame = cap.read()

            # Sai do loop se não houver mais quadros
            if not ret:
                break

            # Converte a imagem capturada para tons de cinza
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Calcula o histograma
            # Para isso, recebe: lista de imagens para calcular histograma, o canal (o 0, já que são só tons de cinza), 
            # se vai usar alguma máscara, o tamanho do histograma e as dimensões (de 0 a 256)
            hist_gray = cv2.calcHist([gray_frame], [0], None, [256], [0, 256])

            # Calcula o histograma acumulado
            cumulative_hist = np.cumsum(hist_gray)

            # Normaliza o histograma acumulado
            cumulative_hist_normalized = (cumulative_hist / cumulative_hist[-1]) * 255

            # Aplica a equalização ao quadro em tons de cinza usando o histograma acumulado normalizado
            # Basicamente, ela aplica uma transformação para qual valor de pixel deve ser mapeada uma saída
            equalized_frame = cv2.LUT(gray_frame, cumulative_hist_normalized.astype(np.uint8))

            # Mostra a imagem em tons de cinza
            cv2.imshow('Gray Image', gray_frame)
            cv2.imshow('Equalized Image', equalized_frame)

            # Sai do loop se for pressionada a tecla ESC
            if cv2.waitKey(30) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    ''')
    st.markdown('''Ao final, pode-se observar o seguinte resultado: ''')
    img1 = Image.open('./images/equalized-and-normal.png')
    st.image(img1)

    st.markdown('<hr>', unsafe_allow_html=True)

    # Segundo exercício
    st.markdown('## Exercício 2')
    st.markdown('''Utilizando o programa [histogram.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/histogram.cpp) como referência, implemente um programa 
    `motiondetector.cpp`. Este deverá continuamente calcular o histograma da imagem (apenas uma componente de cor é suficiente) e compará-lo com o último histograma 
    calculado. Quando a diferença entre estes ultrapassar um limiar pré-estabelecido, ative um alarme. Utilize uma função de comparação que julgar conveniente.''')

    st.markdown('### Solução')
    st.markdown('''Para implementar o detector de movimento, inicialmente, é necessário fazer as devidas configurações para a câmera, bem como definir as propriedades dos
    textos que irão aparecer na tela em situações de alarme. Também são definidas duas variáveis, `frame_x` e `frame_x_ant` para guardarem, respectivamente, os pixels do
    frame atual e do frame exatamente anterior a ele. Elas são inicializadas como variáveis nulas. ''')
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
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # Exibe a largura e altura do vídeo
        print("Largura =", width)
        print("Altura =", height)

        # Define o frame atual e o frame imediatamente antes dele
        frame_x = None
        frame_x_ant = None

        # Variáveis para mostrar texto ao detectar movimento
        texto = 'Movimento detectado!'
        texto_calibracao = 'Calibrando... Aguarde 4 segundos'
        posicao_texto = (50, 80)
        fonte = cv2.FONT_HERSHEY_SIMPLEX
        escala = 1
        cor = (0, 0, 255) 
        cor_calibracao = (255, 0, 0)
        espessura = 2
    ''')
    st.markdown('''Em seguida, é realizada uma calibração. Isso ocorre porque, a depender do ambiente em que é realizada a filmagem, o limiar para detectar se houve algum
    movimento ou não pode mudar consideravelmente. Dessa forma, durante 100 quadros, é aplicado o algoritmo de detecção de movimento para calcular um limiar médio a ser 
    implementado posteriormente.  ''')
    st.markdown('''Basicamente, a lógica de detecção de movimento ocorre da seguinte forma: escolhe-se apenas um dos canais de cores (neste caso, escolheu-se o canal vermelho)
    e é realizado o cálculo do histograma do frame atual e do frame anterior. Posteriormente, calcula-se a diferença entre os valores das posições de cada um dos histogramas, e
    aplica-se a função de módulo, de forma que haja apenas valores positivos. Por fim, estes valores resultantes são somados. Em uma situação ideal em que não há movimento, 
    espera-se que esta soma seja a menor possível, visto que, em um ambiente parado, a imagem tende a continuar a mesma, e consequentemente, os pixels tendem a permanecer os 
    mesmos em suas posições.''')
    st.markdown('''Nesse sentido, após fazer esse cálculo com 100 frames, obtém-se o valor médio para o limiar, que poderá ser aplicado de fato para detectar movimento.''')
    st.code('''
        # Etapa 1: fazer calibração para ajustar o limiar
        calibracao = True
        cont = 0
        list_calibracao = []
        media_calibracao = 0

        while calibracao:
            # Captura um quadro do vídeo
            ret, frame = cap.read()

            # Sai do loop se não houver mais quadros
            if not ret:
                break

            # Atualiza o frame atual e o frame imediatamente antes dele
            frame_x_ant = frame_x
            frame_x = frame

            # Se nenhum dos dois for nulo, calcula o histograma (para apenas um canal) de cada 
            if frame_x is not None and frame_x_ant is not None:

                red_frame_x = frame_x[:,:,2]
                red_frame_x_ant = frame_x_ant[:,:,2]

                # Calcula o histograma do canal vermelho de cada frame    
                hist_x = cv2.calcHist([red_frame_x], [0], None, [256], [0, 256])
                hist_x_ant = cv2.calcHist([red_frame_x_ant], [0], None, [256], [0, 256])

                # Calcula a diferença (em módulo) de cada posição do histograma
                diff = np.abs(hist_x - hist_x_ant)

                # Adiciona na lista de calibração a soma e incrementa o contador
                list_calibracao.append(np.sum(diff))
                cont += 1

                # Se já tiver feito isso com 100 quadros, calcula uma média e sai desse loop
                if cont == 100:
                    media_calibracao = np.mean(list_calibracao)
                    calibracao = False
            
            # Mostra a imagem dizendo que está sendo feita a calibração
            cv2.putText(frame_x, texto_calibracao, posicao_texto, fonte, escala, cor_calibracao, espessura)
            cv2.imshow('Image', frame_x)
            cv2.waitKey(1) 
    ''')
    st.markdown('''Por fim, é implementada a detecção de movimento de fato, levando em consideração o limiar estabelecido na etapa anterior e realizando o mesmo processo.''')
    st.code('''
        # Etapa 2: detecção de movimento
        while True:
            # Captura um quadro do vídeo
            ret, frame = cap.read()

            # Sai do loop se não houver mais quadros
            if not ret:
                break

            # Atualiza o frame atual e o frame imediatamente antes dele
            frame_x_ant = frame_x
            frame_x = frame

            # Se nenhum dos dois for nulo, calcula o histograma (para apenas um canal) de cada 
            if frame_x is not None and frame_x_ant is not None:

                red_frame_x = frame_x[:,:,2]
                red_frame_x_ant = frame_x_ant[:,:,2]

                # Calcula o histograma do canal vermelho de cada frame 
                hist_x = cv2.calcHist([red_frame_x], [0], None, [256], [0, 256])
                hist_x_ant = cv2.calcHist([red_frame_x_ant], [0], None, [256], [0, 256])

                # Calcula a diferença (em módulo) de cada posição do histograma
                diff = np.abs(hist_x - hist_x_ant)

                # Verifica se é maior do que um limiar. Se for, houve movimento e mostra mensagem na tela
                if np.sum(diff) > media_calibracao:
                    cv2.putText(frame_x, texto, posicao_texto, fonte, escala, cor, espessura)

            # Mostra a imagem em tons de cinza
            cv2.imshow('Image', frame_x)

            # Sai do loop se for pressionada a tecla ESC
            if cv2.waitKey(30) == 27:
                break

        cap.release()
        cv2.destroyAllWindows()
    ''')
    st.markdown('''Ao final, obteve-se o resultado apresentado abaixo. Inicialmente, a imagem está parada, realizando a calibração, e em seguida, passa-se uma mão em 
    movimento na frente da câmera, mostrando que ele capturou este movimento.''')
    img2 = Image.open('./images/calibrando.png')
    img3 = Image.open('./images/movimento.png')
    st.image(img2)
    st.image(img3)

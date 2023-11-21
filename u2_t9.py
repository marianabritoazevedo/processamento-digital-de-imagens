import streamlit as st
from PIL import Image

def page_u2_t9():
    st.title('Processando imagens no domínio da frequência')
    st.markdown('''Estes exercícios possuem como objetivo praticar técnicas de processamento de imagens no domínio da frequência.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando os programa [exemplos/dftimage.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/dftimage.cpp), calcule e apresente o espectro de 
    magnitude da imagem [Figura 7](https://agostinhobritojr.github.io/tutorial/pdi/#fig_senoide256png).''')

    st.markdown('### Solução')
    st.markdown('''Primeiramente, é necessário visualizar a imagem que iremos calcular o espectro de magnitude, encontrada abaixo:''')
    img1 = Image.open('./images/senoideok.png')
    st.image(img1)

    st.markdown('''Para realizar o cálculo do espectro de magnitude da imagem, é preciso seguir uma série de passos:''')
    st.markdown('''
    1) Deixar o tamanho da imagem processável. No algoritmo da transformada de fourier, é necessário que as imagens possuam tamanho 2^n. Caso elas não possuam este formato, deve-se
    fazer um padding da imagem com zeros para que seu tamanho seja processável;
    2) Transformar a imagem para ponto flutuante;
    3) Calcular a DFT da imagem;
    4) Deslocar os quadrantes, realizando suas trocas nas diagonais, para melhor visualização;
    5) Cálculo do espectro de magnitude.
    ''')
    st.markdown('''Nesse sentido, a célula de código abaixo realiza a leitura da imagem, e a implementação dos passos 1 ao 4. Como a imagem possui tamanho 256x256 pixels, não
    foi necessário realizar o procedimento de preenchimento com zeros. ''')
    st.code('''
        import cv2
        import numpy as np

        # Carrega a imagem em escala de cinza
        image = cv2.imread('senoide.png', cv2.IMREAD_GRAYSCALE)

        if image is None:
            print("Erro ao abrir a imagem.")
        else:
            # Como essa imagem já possui seu tamanho como uma potência de 2, 256x256, 
            # já podemos realizar o cálculo da transformada de Fourrier diretamente
            float_image = np.float32(image)
            complex_image = cv2.dft(float_image, flags=cv2.DFT_COMPLEX_OUTPUT)
            # Deslocamento dos quadrantes para melhor visualização
            complex_image = np.fft.fftshift(complex_image)
    ''')
    st.markdown('''Em seguida, é realizado o cálculo do espectro de magnitude. Para isso, deve-se utilizar a parte real e imaginária obtida pela DFT e aplicar o método
    `cv2.magnitude()`. Após isso, para visualizar o espectro, é necessário fazer sua compressão na faixa dinâmica, somando o valor `1` e aplicando-se o cálculo do logarítmo (soma-se
    1 justamente para evitar o cálculo de `log(0)`). Por fim, é feita uma normalização dos valores obtidos para a faixa entre `0` e `1`. ''')
    st.code('''
        # Cálculo do espectro de magnitude
        espectro_mag = cv2.magnitude(complex_image[:, :, 0], complex_image[:, :, 1])
        # Compressão de faixa dinâmica
        espectro_mag += 1.0
        espectro_mag = np.log(espectro_mag)
        # Normalização entre 0 e 1 para melhor exibição
        cv2.normalize(espectro_mag, espectro_mag, 0, 1, cv2.NORM_MINMAX)

        # Visualização da imagem original e de seu espectro
        cv2.imshow("Imagem original", image)
        cv2.imshow("Espectro de magnitude", espectro_mag)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    ''')
    st.markdown('''A imagem do espectro de magnitude obtida pode ser visualizada abaixo: ''')
    img2 = Image.open('./images/espectro1.png')
    st.image(img2)

    # Segundo exercício
    st.markdown('## Exercício 2')
    st.markdown('''Compare o espectro gerado para [Figura 7](https://agostinhobritojr.github.io/tutorial/pdi/#fig_senoide256png) com o valor teórico da transformada de
    Fourier da senóide''')

    st.markdown('### Solução')
    st.markdown('''Primeiramente, foi necessário gerar a senóide para cálculo dos valores teóricos com a seguinte fórmula:''')
    st.latex(r'''y = 127 \cdot sen(2 \cdot \pi \cdot 4 \cdot x) + 128''')
    st.markdown('''Onde `4` representa a quantidade de períodos da senóide, `127` representa a sua amplitude e `x` é um vetor de 256 pontos igualmente espaçados entre os
    valores `1` e `2π`. ''')
    st.markdown('''Após gerar o sinal, são calculados os valores teóricos da DFT para a senóide, e em seguida, as suas frequências correspondentes. Esse procedimento pode ser
    visto no trecho de código abaixo: ''')
    st.code('''
        import numpy as np
        import matplotlib.pyplot as plt

        tam = 256
        periodos = 4

        # Gerando a senoide semelhante à presente na imagem
        x = np.linspace(1, 2*np.pi, tam)
        y = 127 * np.sin(2 * np.pi * periodos * x) + 128

        # Cálculo da DFT para a senoide
        dft_resultado = np.fft.fft(y)

        # Frequências correspondentes à DFT
        frequencias = np.fft.fftfreq(len(y))
    ''')
    st.markdown('''Por fim, são gerados 2 gráficos, o primeiro ilustrando o sinal, e o segundo, o cálculo das suas frequências: ''')
    st.code('''
        # Plot do sinal e do cálculo da DFT
        plt.figure(figsize=(8, 6))
        plt.subplot(2, 1, 1)
        plt.plot(x, y)
        plt.title('Sinal da senoide')
        plt.xlabel('Frequência')
        plt.ylabel('Amplitude')

        plt.subplot(2, 1, 2)
        plt.stem(frequencias, np.abs(dft_resultado))
        plt.title('Parte Real da Transformada de Fourier')
        plt.xlabel('Frequência')
        plt.ylabel('Amplitude')

        plt.tight_layout()
        plt.show()
    ''')
    st.markdown('''Os gráficos obtidos podem ser visualizados a seguir:''')
    img3 = Image.open('./images/sinal-e-espectro.png')
    st.image(img3)
    st.markdown('''Com este resultado, pode-se concluir que, no exercício anterior, o espectro de magnitude apresentou um pequeno fator de erro. Os três pontos centrais,
    mais destacados no espectro de magnitude, são correspondetes aos pontos com maior amplitude no gráfico inferior. Entretanto, os pontos menos destacados são pequenos erros
    de cálculo, uma vez que não é possível visualizar estes pontos no gráfico gerado.''')

    # Terceiro exercício
    st.markdown('## Exercício 3')
    st.markdown('''Usando agora o [filestorage.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/filestorage.cpp) mostrado na Listagem 4 como referência, adapte
    o programa para ler a imagem em ponto flutuante armazenada no arquivo YAML equivalente''')
    st.markdown('### Solução')
    st.markdown('''Para fazer a adaptação, bastou mudar o modo de leitura da imagem no início do programa. Ao invés de abrir uma imagem `.png`, deve-se criar um arquivo 
    `cv2.FileStorage()`, e assim, realizar a leitura do arquivo `.yml`, capturando o seu conteúdo no nó `mat`. ''')
    st.code('''
        import cv2
        import numpy as np

        # Leitura da imagem yml
        img_yml = cv2.FileStorage()
        img_yml.open("senoide-256.yml", cv2.FileStorage_READ)
        image = img_yml.getNode("mat").mat()
        img_yml.release()
    ''')
    st.markdown('Com esta mudança do tipo de arquivo, obteve-se o resultado abaixo referente ao espectro de magnitude da imagem:')
    img4 = Image.open('./images/espectro2.png')
    st.image(img4)

    # Quarto exercício
    st.markdown('## Exercício 4')
    st.markdown('''Compare o novo espectro de magnitude gerado com o valor teórico da transformada de Fourier da senóide. O que mudou para que o espectro de magnitude gerado
    agora esteja mais próximo do valor teórico? Por que isso aconteceu?''')
    
    st.markdown('### Solução')
    st.markdown('''Como o arquivo `.yml` possui valores em ponto flutuante mais precisos, ao realizar o cálculo da transformada de Fourier, ele não apresentou erros como quando
    aplicado à imagem em `.png`, originamente em um formato `char`. Dessa forma, agora, obteve-se o espectro de magnitude correspondente ao valor teórico.''')




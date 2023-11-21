import streamlit as st
from PIL import Image

def page_u2_t10():
    st.title('Filtragem no domínio da frequência')
    st.markdown('''Estes exercícios possuem como objetivo praticar técnicas de filtragem de imagens no domínio da frequência, mais especificamente, o filtro homomórfico.''')

    # Primeiro exercício
    st.markdown('## Exercício 1')
    st.markdown('''Utilizando o programa [exemplos/dftfilter.cpp](https://agostinhobritojr.github.io/tutorial/pdi/exemplos/dftfilter.cpp), implemente o filtro homomórfico
    para melhorar imagens com iluminação irregular. Crie uma cena mal iluminada e ajuste os parâmetros do filtro homomórfico para corrigir a iluminação da melhor forma possível.
    Assuma que a imagem fornecida é em tons de cinza.''')

    st.markdown('### Solução')
    st.markdown('''Antes de partir para o programa, é importante verificar a fórmula referente ao filtro homomórfico, que encontra-se descrita abaixo:''')
    st.latex(r'''H(u, v) = (\gamma_H - \gamma_L )(1 - e^{-c(\frac{D^2(u, v)}{D_0^2})}) + \gamma_L''')
    st.markdown('''Os parâmetros γ que aparecem na equação são referentes aos ganhos para altas e baixas frequências, de forma que estes parâmetros irão controlar a atenuação
    e o contraste na figura. Também é possível ajustar nessa equação o parâmetro "c", que irá influenciar no corte do filtro.''')
    st.markdown('''Dessa forma, inicialmente, criou-se a função `filter`, que irá receber a imagem, aplicar o filtro homomórfico a ela com base na fórmula explicada anteriormente,
    e por fim, irá retornar a imagem com a filtragem aplicada.''')
    st.code('''
    def filter(image):
        # Parâmetros do filtro homomórfico
        gamma_h = 0.3  # Parâmetro gamma para realce
        gamma_l = 1.5  # Parâmetro gamma para atenuação
        c = 1.0  # Parâmetro de corte

        # Dimensões da imagem para criação da máscara
        rows, cols, _ = image.shape
        crow, ccol = rows // 2, cols // 2
        mask = np.zeros((rows, cols, 2), np.float32)
        for i in range(rows):
            for j in range(cols):
                mask[i, j] = (gamma_h - gamma_l) * (1 - np.exp(-c * ((i - crow) ** 2 + (j - ccol) ** 2) / (ccol ** 2 + crow ** 2))) + gamma_l

        # Aplicação do filtro e retorno da nova imagem
        new_image = image * mask
        return new_image
    ''')
    st.markdown('''Em seguida, é feita a leitura da imagem. Como esta filtragem é realizada no domínio da frequência, deve-se converter a imagem para o tipo `float` e 
    calcular a sua DFT, realizando-se em seguida a aplicação do filtro. Nesta situação, a imagem possui altura de largura com 2^n pixels de tamanho, não sendo necessário
    fazer nenhuma operação adicional de padding. ''')
    st.code('''
    # Carrega a imagem em escala de cinza
    image = cv2.imread('teste-pdi.png', cv2.IMREAD_GRAYSCALE)

    if image is None:
        print("Erro ao abrir a imagem.")
    else:
        # Considerando uma imagem com tamanho 2^n, calcula-se a transformada de Fourier
        float_image = np.float32(image)
        complex_image = cv2.dft(float_image, flags=cv2.DFT_COMPLEX_OUTPUT)
        # Deslocamento dos quadrantes para melhor visualização
        complex_image = np.fft.fftshift(complex_image)

        # Filtragem homomórfica
        new_image = filter(complex_image)
    ''')
    st.markdown('''Por fim, para visualizar o resultado obtido, é necessário calcular a transformada inversa de Fourier, fazendo a sua normalização e devidas conversões
    de tipos. Assim, ao final, mostra-se a imagem original e a imagem filtrada, e o programa é encerrado. ''')
    st.code('''
    # Aplicação da transformada inversa de fourier
    new_image = np.fft.ifftshift(new_image)
    imagem_filtrada = cv2.idft(new_image)
    imagem_filtrada = cv2.magnitude(imagem_filtrada[:, :, 0], imagem_filtrada[:, :, 1])

    # Organizando a imagem final
    imagem_filtrada = cv2.normalize(imagem_filtrada, None, 0, 255, cv2.NORM_MINMAX)
    imagem_filtrada = np.uint8(imagem_filtrada)

    # Visualização da imagem original e de seu espectro
    cv2.imshow("Imagem original", image)
    cv2.imshow('Imagem Filtrada', imagem_filtrada)
    cv2.imwrite('imagem-com-filtro.png', imagem_filtrada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    ''')
    st.markdown('''O resultado final obtido ao aplicar a filtragem homomórfica em uma imagem mal iluminada encontra-se abaixo:''')
    img1 = Image.open("./images/antes-e-depois-filtro-homomorfico.png")
    st.image(img1)
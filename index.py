import streamlit as st

from u1_t2 import page_u1_t2
from u1_t3 import page_u1_t3
from u1_t4 import page_u1_t4
from u1_t5 import page_u1_t5
from u1_t6 import page_u1_t6  
from u1_t7 import page_u1_t7
from u1_t8 import page_u1_t8
from u2_t9 import page_u2_t9
from u2_t10 import page_u2_t10
from u3_t11 import page_u3_t11
from u3_t12 import page_u3_t12
from u4_t13 import page_u4_t13

def page_inicio():
    st.title('Processamento Digital de Imagens')
    st.markdown('Olá! Eu me chamo Mariana Brito Azevedo, e sou estudante de Engenharia de Computação na Universidade Federal do Rio Grande do Norte (UFRN). Esta página contém os códigos desenvolvidos por mim na disciplina de Processamento Digital de Imagens (DCA0445) cursada na UFRN.')
    st.markdown(':point_left: Selecione no menu ao lado qual aplicação deseja visualizar!')
    st.markdown('Abaixo encontram-se os links para acessar meu github e perfil no LinkedIn caso tenha interesse em conhecer mais do meu trabalho!')
    st.markdown('[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/marianabritoazevedo)')
    st.markdown('[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mariana-brito-azevedo/)')

menu = ['Página inicial', 'Parte 1 - Tópico 2', 'Parte 1 - Tópico 3', 'Parte 1 - Tópico 4', 'Parte 1 - Tópico 5', 
        'Parte 1 - Tópico 6', 'Parte 1 - Tópico 7', 'Parte 1 - Tópico 8', 'Parte 2 - Tópico 9', 'Parte 2 - Tópico 10',
        'Parte 3 - Tópico 11', 'Parte 3 - Tópico 12', 'Parte 4 - Tópico 13']
menu_option = st.sidebar.selectbox('Menu', menu)

if menu_option == 'Página inicial':
    page_inicio()
elif menu_option == 'Parte 1 - Tópico 2':
    page_u1_t2()
elif menu_option == 'Parte 1 - Tópico 3':
    page_u1_t3()
elif menu_option == 'Parte 1 - Tópico 4':
    page_u1_t4()
elif menu_option == 'Parte 1 - Tópico 5':
    page_u1_t5()
elif menu_option == 'Parte 1 - Tópico 6':
    page_u1_t6()
elif menu_option == 'Parte 1 - Tópico 7':
    page_u1_t7()
elif menu_option == 'Parte 1 - Tópico 8':
    page_u1_t8()
elif menu_option == 'Parte 2 - Tópico 9':
    page_u2_t9()
elif menu_option == 'Parte 2 - Tópico 10':
    page_u2_t10()
elif menu_option == 'Parte 3 - Tópico 11':
    page_u3_t11()
elif menu_option == 'Parte 3 - Tópico 12':
    page_u3_t12()
elif menu_option == 'Parte 4 - Tópico 13':
    page_u4_t13()
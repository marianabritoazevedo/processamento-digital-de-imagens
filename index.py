import streamlit as st

from u1_t2 import page_u1_t2
from u1_t4 import page_u1_t4
from u1_t5 import page_u1_t5    

def page_inicio():
    st.title('Processamento Digital de Imagens')
    st.markdown('Olá! Eu me chamo Mariana Brito Azevedo, e sou estudante de Engenharia de Computação na Univesidade Federal do Rio Grande do Norte (UFRN). Esta página contém os códigos desenvolvidos por mim na disciplina de Processamento Digital de Imagens (DCA0445) cursada na UFRN.')
    st.markdown(':point_left: Selecione no menu ao lado qual aplicação deseja visualizar!')
    st.markdown('Abaixo encontram-se os links para acessar meu github e perfil no LinkedIn caso tenha interesse em conhecer mais do meu trabalho!')
    st.markdown('[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/marianabritoazevedo)')
    st.markdown('[![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mariana-brito-azevedo/)')

menu = ['Página inicial', 'Unidade 1 - Tópico 2', 'Unidade 1 - Tópico 4', 'Unidade 1 - Tópico 5']
menu_option = st.sidebar.selectbox('Menu', menu)

if menu_option == 'Página inicial':
    page_inicio()
elif menu_option == 'Unidade 1 - Tópico 2':
    page_u1_t2()
elif menu_option == 'Unidade 1 - Tópico 4':
    page_u1_t4()
elif menu_option == 'Unidade 1 - Tópico 5':
    page_u1_t5()
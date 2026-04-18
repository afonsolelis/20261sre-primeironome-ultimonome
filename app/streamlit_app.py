import streamlit as st

st.title('Streamlit Teste AWS EC2')
st.write('Este é um app de teste hospedado em EC2.')

if st.button('Clique aqui'):
    st.success('App ativo!')

import streamlit as st
from lotofacil_stats import (
    capturar_ultimos_resultados,
    analisar_frequencia,
    gerar_cartoes_otimizados
)

st.set_page_config(page_title="Analisador Lotofácil", layout="centered")

st.title("Analisador Inteligente - Lotofácil")

qtd_concursos = st.slider("Escolha quantos concursos deseja capturar:", min_value=50, max_value=250, value=100)
qtd_cartoes = st.slider("Quantos cartões deseja gerar?", 1, 20, 5)

concursos = capturar_ultimos_resultados(qtd=qtd_concursos)

if concursos:
    ultimo_num, ultima_data, ultima_dezenas = concursos[0]
    st.markdown("---")
    st.subheader(f"Último Concurso: {ultimo_num} ({ultima_data})")
    st.markdown(f"**Dezenas Sorteadas:** {', '.join(map(str, ultima_dezenas))}")
    st.markdown("---")

    st.subheader("Frequência das Dezenas")
    freq = analisar_frequencia(concursos)
    st.bar_chart(freq)

    st.subheader("Cartões Gerados com Base nas Mais Frequentes")
    cartoes = gerar_cartoes_otimizados(freq, qtd_cartoes)

    for i, cartao in enumerate(cartoes, start=1):
        st.markdown(f"**Cartão {i}:** {', '.join(map(str, cartao))}")

st.markdown("---")
st.markdown("<p style='text-align:center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

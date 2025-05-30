import streamlit as st
from lotofacil_stats import (
    capturar_ultimos_resultados,
    analisar_frequencia,
    gerar_cartoes_otimizados
)

st.set_page_config(page_title="Analisador Lotofácil", layout="centered")

st.markdown("<h1 style='text-align:center;'>Analisador Inteligente - Lotofácil</h1>", unsafe_allow_html=True)

qtd_concursos = st.slider("Escolha quantos concursos deseja capturar:", min_value=50, max_value=250, value=100)
concursos = capturar_ultimos_resultados(qtd=qtd_concursos)

if concursos:
    ultimo_num, ultima_data, ultima_dezenas = concursos[0]
    st.markdown(f"<h4 style='text-align:center;'>Último Concurso: {ultimo_num} ({ultima_data})</h4>", unsafe_allow_html=True)
    st.markdown(f"<h5 style='text-align:center;'>Dezenas Sorteadas: {', '.join(map(str, ultima_dezenas))}</h5>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>Estatísticas e Frequência</h2>", unsafe_allow_html=True)
    freq = analisar_frequencia(concursos)
    st.bar_chart(freq)

    st.markdown("<h2 style='text-align:center;'>Gerar Cartões Otimizados</h2>", unsafe_allow_html=True)
    qtd_cartoes = st.slider("Quantos cartões deseja gerar?", 1, 20, 5)
    cartoes = gerar_cartoes_otimizados(freq, qtd_cartoes)

    for i, cartao in enumerate(cartoes, start=1):
        st.markdown(f"<h4 style='text-align:center;'>Cartão {i}: {', '.join(map(str, cartao))}</h4>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<p style='text-align:center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

import streamlit as st
from lotofacil_stats import LotoFacilStats
import requests

# Sessão de estado
if "concursos" not in st.session_state:
    st.session_state.concursos = []

if "cartoes_gerados" not in st.session_state:
    st.session_state.cartoes_gerados = []

def capturar_ultimos_resultados(qtd=250):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"
    concursos = []

    try:
        resp = requests.get(url_base)
        if resp.status_code != 200:
            st.error("Erro ao buscar o último concurso.")
            return []

        dados = resp.json()
        ultimo = dados[0] if isinstance(dados, list) else dados
        numero_atual = int(ultimo.get("concurso"))
        data_concurso = ultimo.get("data")
        dezenas = sorted([int(d) for d in ultimo.get("dezenas")])
        concursos.append(dezenas)

        st.markdown(f"<h4 style='text-align: center;'>Último Concurso: {numero_atual} ({data_concurso})<br>Dezenas: {dezenas}</h4>", unsafe_allow_html=True)

        for i in range(1, qtd):
            concurso_numero = numero_atual - i
            resp = requests.get(f"{url_base}{concurso_numero}")
            if resp.status_code == 200:
                dados = resp.json()
                data = dados[0] if isinstance(dados, list) else dados
                dezenas = sorted([int(d) for d in data.get("dezenas")])
                concursos.append(dezenas)
            else:
                break
    except Exception as e:
        st.error(f"Erro ao acessar API: {e}")
    return concursos

def main():
    st.markdown("<h1 style='text-align: center;'>Análise e Geração de Cartões Lotofácil</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

    qtd_concursos = st.slider("Número de concursos para capturar", min_value=10, max_value=250, value=100)

    if st.button("📊 Capturar e Analisar"):
        with st.spinner("Capturando concursos..."):
            st.session_state.concursos = capturar_ultimos_resultados(qtd=qtd_concursos)
            st.session_state.cartoes_gerados = []  # limpa cartões gerados

    if st.session_state.concursos:
        stats = LotoFacilStats(st.session_state.concursos)

        st.subheader("📈 Estatísticas")
        st.write(f"Frequência dos números: {stats.frequencia_numeros()}")
        st.write(f"Soma média dos concursos: {stats.soma_media():.2f}")
        st.write(f"Pares/Ímpares: {stats.pares_impares_distribuicao()}")
        st.write(f"Números consecutivos: {stats.numeros_consecutivos():.2f}")
        st.write(f"Distribuição por grupos: {stats.grupos_distribuicao()}")
        quentes_frios = stats.numeros_quentes_frios()
        st.write(f"Números quentes: {quentes_frios['quentes']}")
        st.write(f"Números frios: {quentes_frios['frios']}")

        st.subheader("🧠 Geração de Cartões")
        n_cartoes = st.slider("Quantidade de cartões", 1, 20, 5)
        alvo = st.slider("Mínimo de acertos desejado (simulado)", 12, 15, 14)

        if st.button("🧪 Gerar Cartões"):
            st.session_state.cartoes_gerados = stats.gerar_cartoes_otimizados(n_cartoes, alvo)

        if st.session_state.cartoes_gerados:
            st.success(f"{len(st.session_state.cartoes_gerados)} cartões gerados:")
            for i, c in enumerate(st.session_state.cartoes_gerados, 1):
                st.write(f"Cartão {i}: {c}")
        else:
            st.warning("Nenhum cartão atingiu exatamente o alvo. Exibindo os melhores encontrados.")

        if st.button("✅ Conferir com Último Concurso"):
            ultimo = st.session_state.concursos[0]
            st.markdown("<h4 style='text-align: center;'>Conferência com o Último Concurso</h4>", unsafe_allow_html=True)
            for i, cartao in enumerate(st.session_state.cartoes_gerados, 1):
                acertos = len(set(cartao) & set(ultimo))
                st.write(f"Cartão {i}: {cartao} - **{acertos} acertos**")

    st.markdown("<hr><p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

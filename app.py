import streamlit as st
from lotofacil_stats import LotoFacilStats
import requests

# Sessão de estado para guardar concursos e cartões gerados
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

        st.markdown(
            f"<h4 style='text-align: center;'>Último Concurso: {numero_atual} ({data_concurso})<br>Dezenas: {dezenas}</h4>",
            unsafe_allow_html=True)

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

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Capturar e Analisar"):
            with st.spinner("Capturando concursos..."):
                st.session_state.concursos = capturar_ultimos_resultados(qtd=qtd_concursos)

    # Sliders sempre visíveis (fora do botão), conforme solicitado
    st.subheader("🎯 Parâmetros para Geração de Cartões")
    num_cartoes = st.slider("Número de cartões a gerar", 1, 20, 5, key="slider_gerar")
    alvo_minimo = st.slider("Alvo mínimo de acertos simulados", 12, 15, 14, key="slider_alvo")

    with col2:
        if st.button("🧠 Gerar Cartões"):
            if not st.session_state.concursos:
                st.warning("Capture os concursos antes de gerar cartões.")
            else:
                stats = LotoFacilStats(st.session_state.concursos)
                st.session_state.cartoes_gerados = stats.gerar_cartoes_otimizados(num_cartoes, alvo_minimo)

    with col3:
        if st.button("✅ Conferir Cartões"):
            if not st.session_state.cartoes_gerados or not st.session_state.concursos:
                st.warning("Gere os cartões primeiro.")
            else:
                ultimo = st.session_state.concursos[0]
                st.markdown("<h4 style='text-align: center;'>Conferência com Último Concurso</h4>", unsafe_allow_html=True)
                for i, cartao in enumerate(st.session_state.cartoes_gerados, 1):
                    acertos = len(set(cartao) & set(ultimo))
                    st.write(f"Cartão {i}: {cartao} - **{acertos} acertos**")

    # Exibir estatísticas se concursos foram capturados
    if st.session_state.concursos:
        stats = LotoFacilStats(st.session_state.concursos)
        st.subheader("📈 Estatísticas Gerais")
        st.write(f"Frequência dos números: {stats.frequencia_numeros()}")
        st.write(f"Soma média dos concursos: {stats.soma_media():.2f}")
        st.write(f"Média de pares/impares por concurso: {stats.pares_impares_distribuicao()}")
        st.write(f"Média de números consecutivos: {stats.numeros_consecutivos():.2f}")
        st.write(f"Distribuição média por grupos: {stats.grupos_distribuicao()}")
        quentes_frios = stats.numeros_quentes_frios()
        st.write(f"Números quentes: {quentes_frios['quentes']}")
        st.write(f"Números frios: {quentes_frios['frios']}")

    if st.session_state.cartoes_gerados:
        st.subheader("🧾 Cartões Gerados")
        for i, c in enumerate(st.session_state.cartoes_gerados, 1):
            st.write(f"Cartão {i}: {c}")

    st.markdown("<hr><p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

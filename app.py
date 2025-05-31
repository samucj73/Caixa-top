import streamlit as st
from lotofacil_stats import LotoFacilStats
import requests

# Sessão de estado
if "concursos" not in st.session_state:
    st.session_state.concursos = []

if "cartoes_gerados" not in st.session_state:
    st.session_state.cartoes_gerados = []

if "ultimo_concurso_info" not in st.session_state:
    st.session_state.ultimo_concurso_info = {}

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

        st.session_state.ultimo_concurso_info = {
            "numero": numero_atual,
            "data": data_concurso,
            "dezenas": dezenas
        }

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

# Interface
st.markdown("<h1 style='text-align: center;'>Análise e Geração de Cartões Lotofácil</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

# Aba lateral para captura
with st.sidebar:
    st.markdown("### 🔁 Captura de Concursos")
    qtd_concursos = st.slider("Qtd. de concursos a capturar", 10, 250, 100)
    if st.button("📥 Capturar Concursos"):
        with st.spinner("Capturando dados..."):
            st.session_state.concursos = capturar_ultimos_resultados(qtd=qtd_concursos)
        if st.session_state.concursos:
            st.success("Concursos capturados com sucesso!")

# Abas principais
abas = st.tabs(["📈 Estatísticas", "🧠 Gerar Cartões", "✅ Conferência"])

# Estatísticas
with abas[0]:
    if st.session_state.concursos:
        stats = LotoFacilStats(st.session_state.concursos)
        st.subheader("📊 Estatísticas Gerais")
        st.write(f"Frequência dos números: {stats.frequencia_numeros()}")
        st.write(f"Soma média dos concursos: {stats.soma_media():.2f}")
        st.write(f"Média de pares/impares: {stats.pares_impares_distribuicao()}")
        st.write(f"Média de consecutivos: {stats.numeros_consecutivos():.2f}")
        st.write(f"Distribuição por grupos: {stats.grupos_distribuicao()}")
        qf = stats.numeros_quentes_frios()
        st.write(f"Números quentes: {qf['quentes']}")
        st.write(f"Números frios: {qf['frios']}")
    else:
        st.warning("Capture os concursos para ver as estatísticas.")

# Geração de cartões
with abas[1]:
    if st.session_state.concursos:
        st.subheader("🎯 Geração de Cartões")
        n_cartoes = st.slider("Qtd. de cartões", 1, 20, 5)
        alvo = st.slider("Alvo mínimo de acertos", 12, 15, 14)

        if st.button("🚀 Gerar Cartões"):
            stats = LotoFacilStats(st.session_state.concursos)
            st.session_state.cartoes_gerados = stats.gerar_cartoes_otimizados(n_cartoes, alvo)

        if st.session_state.cartoes_gerados:
            st.success(f"{len(st.session_state.cartoes_gerados)} cartões gerados:")
            for i, c in enumerate(st.session_state.cartoes_gerados, 1):
                st.write(f"Cartão {i}: {c}")
    else:
        st.warning("Capture os concursos antes de gerar cartões.")

# Conferência
with abas[2]:
    st.subheader("📅 Último Concurso")
    if info := st.session_state.ultimo_concurso_info:
        st.markdown(f"<p style='text-align: center;'>Concurso {info['numero']} - {info['data']}<br>Dezenas: {info['dezenas']}</p>", unsafe_allow_html=True)
    else:
        st.info("Capture concursos para visualizar o último resultado.")

    if st.session_state.cartoes_gerados:
        if st.button("📋 Conferir Cartões com Último Concurso"):
            dezenas = set(st.session_state.ultimo_concurso_info["dezenas"])
            for i, c in enumerate(st.session_state.cartoes_gerados, 1):
                acertos = len(set(c) & dezenas)
                st.write(f"Cartão {i}: {c} - **{acertos} acertos**")
    else:
        st.info("Gere os cartões primeiro para fazer a conferência.")

st.markdown("<hr><p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

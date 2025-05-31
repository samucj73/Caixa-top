import streamlit as st
from lotofacil_stats import LotoFacilStats
from lotofacil_avancado import LotoFacilAvancado
import requests

st.set_page_config(page_title="Lotofácil Inteligente", layout="centered")

def capturar_ultimos_resultados(qtd=250):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"
    concursos = []

    try:
        resp = requests.get(url_base)
        if resp.status_code != 200:
            st.error("Erro ao buscar o último concurso.")
            return [], None

        dados = resp.json()
        ultimo = dados[0] if isinstance(dados, list) else dados

        numero_atual = int(ultimo.get("concurso"))
        data_concurso = ultimo.get("data")
        dezenas = sorted([int(d) for d in ultimo.get("dezenas")])
        concursos.append(dezenas)

        info_ultimo = {
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

        return concursos, info_ultimo

    except Exception as e:
        st.error(f"Erro ao acessar API: {e}")
        return [], None

# Inicializar sessão
if "concursos" not in st.session_state:
    st.session_state.concursos = []

if "cartoes_gerados" not in st.session_state:
    st.session_state.cartoes_gerados = []

if "info_ultimo_concurso" not in st.session_state:
    st.session_state.info_ultimo_concurso = None

st.markdown("<h1 style='text-align: center;'>Lotofácil Inteligente</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# Captura inicial de concursos
with st.expander("📥 Capturar Concursos"):
    qtd_concursos = st.slider("Quantidade de concursos para análise", 10, 250, 100)
    if st.button("🔄 Capturar Agora"):
        with st.spinner("Capturando concursos da Lotofácil..."):
            concursos, info = capturar_ultimos_resultados(qtd_concursos)
            if concursos:
                st.session_state.concursos = concursos
                st.session_state.info_ultimo_concurso = info
                st.success(f"{len(concursos)} concursos capturados com sucesso!")

# Verifica se os dados estão prontos
if not st.session_state.concursos:
    st.warning("Capture os concursos antes de utilizar as funcionalidades abaixo.")
else:
    abas = st.tabs(["📊 Estatísticas", "🧠 Gerar Cartões", "✅ Conferência", "📊 Análises Avançadas"])
    stats = LotoFacilStats(st.session_state.concursos)
    avancado = LotoFacilAvancado(st.session_state.concursos)

    # --- ABA 1: Estatísticas Gerais ---
    with abas[0]:
        st.subheader("📈 Estatísticas Gerais")
        st.write(f"Frequência dos números: {stats.frequencia_numeros()}")
        st.write(f"Soma média dos concursos: {stats.soma_media():.2f}")
        st.write(f"Média de pares/impares: {stats.pares_impares_distribuicao()}")
        st.write(f"Média de consecutivos: {stats.numeros_consecutivos():.2f}")
        st.write(f"Distribuição por grupos: {stats.grupos_distribuicao()}")
        quentes_frios = stats.numeros_quentes_frios()
        st.write(f"Números quentes: {quentes_frios['quentes']}")
        st.write(f"Números frios: {quentes_frios['frios']}")

    # --- ABA 2: Geração de Cartões ---
    with abas[1]:
        st.subheader("🧾 Geração de Cartões Otimizados")
        n_cartoes = st.slider("Quantidade de cartões", 1, 200, 5)
        alvo_acertos = st.slider("Alvo mínimo de acertos simulados",  11, 15, 14)
        if st.button("🚀 Gerar Cartões"):
            gerados = avancado.gerar_cartoes_com_avancado(num_cartoes=n_cartoes, alvo_min_acertos=alvo_acertos)
            if gerados:
                st.session_state.cartoes_gerados = gerados
                st.success(f"{len(gerados)} cartões gerados!")
            else:
                st.error("Nenhum cartão atingiu o desempenho mínimo.")

        if st.session_state.cartoes_gerados:
            st.subheader("Cartões Gerados")
            for i, c in enumerate(st.session_state.cartoes_gerados, 1):
                st.write(f"Cartão {i}: {c}")

    # --- ABA 3: Conferência ---
    with abas[2]:
        st.subheader("🎯 Conferência de Cartões")
        if st.session_state.info_ultimo_concurso:
            info = st.session_state.info_ultimo_concurso
            st.markdown(
                f"<h4 style='text-align: center;'>Último Concurso #{info['numero']} ({info['data']})<br>Dezenas: {info['dezenas']}</h4>",
                unsafe_allow_html=True
            )
        else:
            st.warning("Informações do último concurso indisponíveis.")

        if st.button("🔍 Conferir agora"):
            if not st.session_state.cartoes_gerados:
                st.info("Gere os cartões primeiro.")
            elif not st.session_state.info_ultimo_concurso:
                st.warning("Dados do último concurso não encontrados.")
            else:
                dezenas_ultimo = st.session_state.info_ultimo_concurso["dezenas"]
                for i, cartao in enumerate(st.session_state.cartoes_gerados, 1):
                    acertos = len(set(cartao) & set(dezenas_ultimo))
                    st.write(f"Cartão {i}: {cartao} - **{acertos} acertos**")

    # --- ABA 4: Estatísticas Avançadas ---
    with abas[3]:
        st.subheader("🔍 Estatísticas Avançadas")
        st.write(f"Média de números primos por concurso: {avancado.media_primos():.2f}")
        st.write(f"Média de múltiplos de 3 por concurso: {avancado.media_multiplos_3():.2f}")
        st.write(f"Distribuição de primos: {avancado.distribuicao_primos()}")
        st.write(f"Distribuição de múltiplos de 3: {avancado.distribuicao_multiplos_3()}")

st.markdown("<hr><p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

import streamlit as st
from lotofacil_stats import LotoFacilStats
import requests

# Sessão de estado para concursos e cartões
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

        st.session_state.numero_ultimo = numero_atual
        st.session_state.data_ultimo = data_concurso
        st.session_state.dezenas_ultimo = dezenas

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
    st.markdown("<h1 style='text-align: center;'>🔍 LotoFácil Inteligente</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

    aba = st.sidebar.radio("Escolha uma aba", ["🎯 Geração", "📈 Estatísticas", "✅ Conferência"])

    if aba == "🎯 Geração":
        qtd_concursos = st.slider("Quantidade de concursos para análise", 10, 250, 100)

        if st.button("📥 Capturar Concursos"):
            with st.spinner("Buscando concursos..."):
                concursos = capturar_ultimos_resultados(qtd=qtd_concursos)
                st.session_state.concursos = concursos
                st.success(f"{len(concursos)} concursos capturados com sucesso!")

        if st.session_state.concursos:
            st.markdown(f"🎯 <strong>Último Concurso:</strong> #{st.session_state.numero_ultimo} - {st.session_state.data_ultimo}<br><strong>Dezenas:</strong> {st.session_state.dezenas_ultimo}", unsafe_allow_html=True)
            
            n_cartoes = st.slider("Número de cartões a gerar", 1, 20, 5)
            alvo = st.slider("Mínimo de acertos simulados (alvo)", 12, 15, 14)

            if st.button("🚀 Gerar Cartões"):
                stats = LotoFacilStats(st.session_state.concursos)
                st.session_state.cartoes_gerados = stats.gerar_cartoes_otimizados(n_cartoes, alvo)

                if not st.session_state.cartoes_gerados:
                    st.warning("⚠️ Nenhum cartão atingiu o desempenho mínimo.")
                else:
                    st.success(f"{len(st.session_state.cartoes_gerados)} cartões gerados:")
                    for i, c in enumerate(st.session_state.cartoes_gerados, 1):
                        st.write(f"Cartão {i}: {c}")
        else:
            st.info("Clique em 'Capturar Concursos' para iniciar a análise.")

    elif aba == "📈 Estatísticas":
        if not st.session_state.concursos:
            st.warning("Capture os concursos antes de visualizar estatísticas.")
        else:
            stats = LotoFacilStats(st.session_state.concursos)
            st.subheader("📊 Estatísticas Gerais")
            st.write("📌 Frequência dos Números:", stats.frequencia_numeros())
            st.write("📌 Soma média dos concursos:", round(stats.soma_media(), 2))
            st.write("📌 Média de pares/impares:", stats.pares_impares_distribuicao())
            st.write("📌 Média de números consecutivos:", round(stats.numeros_consecutivos(), 2))
            st.write("📌 Distribuição por grupos:", stats.grupos_distribuicao())
            quente_frio = stats.numeros_quentes_frios()
            st.write("🔥 Números quentes:", quente_frio["quentes"])
            st.write("❄️ Números frios:", quente_frio["frios"])

    elif aba == "✅ Conferência":
        if not st.session_state.cartoes_gerados or not st.session_state.concursos:
            st.warning("Gere os cartões e capture concursos antes de conferir.")
        else:
            if st.button("📤 Conferir Cartões com o Último Concurso"):
                dezenas = st.session_state.dezenas_ultimo
                st.markdown(f"<strong>Último Concurso:</strong> #{st.session_state.numero_ultimo} - {st.session_state.data_ultimo}<br><strong>Dezenas:</strong> {dezenas}", unsafe_allow_html=True)
                st.write("---")
                for i, cartao in enumerate(st.session_state.cartoes_gerados, 1):
                    acertos = len(set(cartao) & set(dezenas))
                    st.write(f"Cartão {i}: {cartao} - **{acertos} acertos**")

    st.markdown("<hr><p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

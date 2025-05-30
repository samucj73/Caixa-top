import streamlit as st
from lotofacil_stats import LotoFacilStats
import requests

# Estilização centralizada
def titulo(texto):
    st.markdown(f"<h2 style='text-align: center; color: #4CAF50;'>{texto}</h2>", unsafe_allow_html=True)

def subtitulo(texto):
    st.markdown(f"<h4 style='text-align: center;'>{texto}</h4>", unsafe_allow_html=True)

def rodape(texto):
    st.markdown(f"<hr><p style='text-align: center; color: gray;'>{texto}</p>", unsafe_allow_html=True)

# Captura concursos via API
def capturar_ultimos_resultados(qtd=250):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"
    concursos = []

    try:
        resp = requests.get(url_base)
        if resp.status_code != 200:
            st.error("Erro ao buscar o último concurso.")
            return []

        dados = resp.json()
        if isinstance(dados, list):
            ultimo = dados[0]
        else:
            ultimo = dados

        numero_atual = int(ultimo.get("concurso"))
        dezenas_atuais = sorted([int(d) for d in ultimo.get("dezenas")])
        data_atual = ultimo.get("data")

        # Mostrar dados mais recentes centralizados
        st.markdown(f"""
            <div style="text-align: center;">
                <h3>Concurso mais recente: {numero_atual} — {data_atual}</h3>
                <p><strong>Dezenas sorteadas:</strong> {dezenas_atuais}</p>
            </div>
        """, unsafe_allow_html=True)

        concursos.append(dezenas_atuais)

        for i in range(1, qtd):
            concurso_numero = numero_atual - i
            resp = requests.get(f"{url_base}{concurso_numero}")
            if resp.status_code == 200:
                dados = resp.json()
                if isinstance(dados, list):
                    data = dados[0]
                else:
                    data = dados

                dezenas = sorted([int(d) for d in data.get("dezenas")])
                concursos.append(dezenas)
            else:
                break

    except Exception as e:
        st.error(f"Erro ao acessar API: {e}")

    return concursos

# Interface principal
def main():
    titulo("🔢 LotoFácil Inteligente")
    subtitulo("Análise Estatística e Geração de Cartões Otimizados")

    qtd_concursos = st.slider("Selecione a quantidade de concursos para análise:", 10, 250, 100)

    if st.button("🔍 Capturar concursos"):
        with st.spinner("Buscando concursos..."):
            concursos = capturar_ultimos_resultados(qtd=qtd_concursos)
            if concursos:
                st.session_state.concursos = concursos
                st.success("Concursos capturados com sucesso!")

    if "concursos" in st.session_state:
        stats = LotoFacilStats(st.session_state.concursos)

        titulo("📊 Estatísticas")
        st.write(f"**Frequência dos números:** {stats.frequencia_numeros()}")
        st.write(f"**Soma média dos concursos:** {stats.soma_media():.2f}")
        st.write(f"**Média de pares/ímpares:** {stats.pares_impares_distribuicao()}")
        st.write(f"**Média de números consecutivos:** {stats.numeros_consecutivos():.2f}")
        st.write(f"**Distribuição por grupos:** {stats.grupos_distribuicao()}")
        quentes_frios = stats.numeros_quentes_frios()
        st.write(f"**Números quentes:** {quentes_frios['quentes']}")
        st.write(f"**Números frios:** {quentes_frios['frios']}")

        st.markdown("---")
        titulo("🎯 Gerar Cartões Otimizados")
        n_cartoes = st.slider("Número de cartões a gerar", 1, 20, 5)
        alvo_acertos = st.slider("Alvo mínimo de acertos (12 a 15)", 12, 15, 14)

        if st.button("🎰 Gerar Cartões"):
            cartoes = stats.gerar_cartoes_otimizados(num_cartoes=n_cartoes, alvo_min_acertos=alvo_acertos)
            st.session_state.cartoes = cartoes

        if "cartoes" in st.session_state:
            subtitulo("🃏 Cartões Gerados")
            for i, c in enumerate(st.session_state.cartoes, 1):
                st.markdown(f"<p style='text-align: center;'><strong>Cartão {i}:</strong> {c}</p>", unsafe_allow_html=True)

    rodape("© 2025 SAMUCJ TECHNOLOGY")

if __name__ == "__main__":
    main()

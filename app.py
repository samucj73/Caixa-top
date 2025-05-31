import streamlit as st
from lotofacil_stats import LotoFacilStats
import requests

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
        data_concurso = ultimo.get("data")
        dezenas = sorted([int(d) for d in ultimo.get("dezenas")])
        concursos.append(dezenas)

        # Exibir dados do concurso mais recente
        st.markdown(f"<h4 style='text-align: center;'>Último Concurso: {numero_atual} ({data_concurso})<br>Dezenas: {dezenas}</h4>", unsafe_allow_html=True)

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
                st.warning(f"Concurso {concurso_numero} não encontrado ou erro na API.")
                break

    except Exception as e:
        st.error(f"Erro ao acessar API: {e}")

    return concursos

def main():
    st.markdown("<h1 style='text-align: center;'>Análise e Geração de Cartões Lotofácil</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

    qtd_concursos = st.slider("Número de concursos para capturar", min_value=10, max_value=250, value=100)

    if st.button("Capturar e Analisar"):
        with st.spinner("Capturando concursos..."):
            concursos = capturar_ultimos_resultados(qtd=qtd_concursos)

        if concursos:
            st.success(f"{len(concursos)} concursos capturados com sucesso!")
            stats = LotoFacilStats(concursos)

            st.subheader("Estatísticas Gerais")
            st.write(f"Frequência dos números: {stats.frequencia_numeros()}")
            st.write(f"Soma média dos concursos: {stats.soma_media():.2f}")
            st.write(f"Média de pares/impares por concurso: {stats.pares_impares_distribuicao()}")
            st.write(f"Média de números consecutivos: {stats.numeros_consecutivos():.2f}")
            st.write(f"Distribuição média por grupos (5 grupos de 5 números): {stats.grupos_distribuicao()}")
            quentes_frios = stats.numeros_quentes_frios()
            st.write(f"Números quentes (mais frequentes): {quentes_frios['quentes']}")
            st.write(f"Números frios (menos frequentes): {quentes_frios['frios']}")

            st.subheader("Geração de Cartões Otimizados")
            n_cartoes = st.slider("Número de cartões para gerar", 1, 20, 5)
            alvo_acertos = st.slider("Alvo mínimo de acertos simulados (12 a 15)", 12, 15, 14)

            cartoes = stats.gerar_cartoes_otimizados(num_cartoes=n_cartoes, alvo_min_acertos=alvo_acertos)

            if cartoes:
                st.success(f"{len(cartoes)} cartões gerados com base no desempenho médio!")
                for i, c in enumerate(cartoes, 1):
                    st.write(f"Cartão {i}: {c}")
            else:
                st.error("Nenhum cartão gerado atingiu o desempenho desejado.")

    st.markdown("<hr><p style='text-align: center;'>SAMUCJ TECHNOLOGY</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()

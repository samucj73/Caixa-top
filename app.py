
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
        dezenas_ult = sorted([int(d) for d in ultimo.get("dezenas")])
        data_ult = ultimo.get("data")

        concursos.append(dezenas_ult)

        for i in range(1, qtd):
            concurso_numero = numero_atual - i
            resp = requests.get(f"{url_base}{concurso_numero}")
            if resp.status_code == 200:
                dados = resp.json()
                data = dados[0] if isinstance(dados, list) else dados
                dezenas = sorted([int(d) for d in data.get("dezenas")])
                concursos.append(dezenas)
            else:
                st.warning(f"Concurso {concurso_numero} não encontrado ou erro na API.")
                break

    except Exception as e:
        st.error(f"Erro ao acessar API: {e}")

    return concursos, (numero_atual, data_ult, dezenas_ult)


def main():
    st.title("📊 Análise e Geração de Cartões Lotofácil")
    st.markdown("---")

    qtd_concursos = st.slider("🔢 Quantos concursos deseja analisar?", 10, 250, 100)
    if st.button("📥 Capturar e Analisar Concursos"):
        with st.spinner("Buscando concursos..."):
            concursos, dados_ultimo = capturar_ultimos_resultados(qtd_concursos)

        if concursos:
            numero, data, dezenas = dados_ultimo
            st.markdown(f"### 🟩 Último Concurso: Nº {numero} ({data})")
            st.write("Dezenas sorteadas:", dezenas)

            stats = LotoFacilStats(concursos)

            st.subheader("📈 Estatísticas")
            st.write("Frequência:", stats.frequencia_numeros())
            st.write("Soma média:", round(stats.soma_media(), 2))
            st.write("Distribuição pares/ímpares:", stats.pares_impares_distribuicao())
            st.write("Média de consecutivos:", round(stats.numeros_consecutivos(), 2))
            st.write("Distribuição por grupos:", stats.grupos_distribuicao())
            quentes_frios = stats.numeros_quentes_frios()
            st.write("🔴 Quentes:", quentes_frios["quentes"])
            st.write("🔵 Frios:", quentes_frios["frios"])

            st.subheader("🎯 Geração de Cartões Otimizados")
            n_cartoes = st.slider("Número de cartões", 1, 20, 5)
            alvo_acertos = st.slider("Alvo mínimo de acertos", 12, 15, 14)
            validar_desempenho = st.checkbox("✅ Validar desempenho nos últimos concursos", value=True)

            if st.button("🎰 Gerar Cartões"):
                cartoes = stats.gerar_cartoes_otimizados(
                    num_cartoes=n_cartoes,
                    alvo_min_acertos=alvo_acertos if validar_desempenho else None
                )
                st.success(f"{len(cartoes)} cartões gerados com sucesso:")
                for i, c in enumerate(cartoes, 1):
                    st.write(f"Cartão {i}: {sorted(c)}")

    st.markdown("---")
    st.markdown("© SAMUCJ TECHNOLOGY")


if __name__ == "__main__":
    main()

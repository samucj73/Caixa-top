import requests
import random
from collections import Counter

def capturar_ultimos_resultados(qtd=250):
    url_base = "https://loteriascaixa-api.herokuapp.com/api/lotofacil/"
    concursos = []
    try:
        resp = requests.get(url_base)
        if resp.status_code != 200:
            return []
        dados = resp.json()
        ultimo = dados[0] if isinstance(dados, list) else dados
        numero_atual = int(ultimo.get("concurso"))
        dezenas = sorted([int(d) for d in ultimo.get("dezenas")])
        data_concurso = ultimo.get("data")
        concursos.append((numero_atual, data_concurso, dezenas))
        for i in range(1, qtd):
            concurso_numero = numero_atual - i
            resp = requests.get(f"{url_base}{concurso_numero}")
            if resp.status_code == 200:
                dados = resp.json()
                data = dados[0] if isinstance(dados, list) else dados
                numero = int(data.get("concurso"))
                dezenas = sorted([int(d) for d in data.get("dezenas")])
                data_concurso = data.get("data")
                concursos.append((numero, data_concurso, dezenas))
            else:
                break
    except Exception as e:
        print("Erro:", e)
    return concursos

def analisar_frequencia(concursos):
    todas_dezenas = []
    for _, _, dezenas in concursos:
        todas_dezenas.extend(dezenas)
    contagem = Counter(todas_dezenas)
    freq_dict = {str(n): contagem.get(n, 0) for n in range(1, 26)}
    return freq_dict

def gerar_cartoes_otimizados(frequencias, qtd_cartoes=5):
    dezenas_ordenadas = sorted(frequencias.items(), key=lambda x: x[1], reverse=True)
    mais_frequentes = [int(dezena) for dezena, _ in dezenas_ordenadas[:20]]
    cartoes = []
    for _ in range(qtd_cartoes):
        cartao = sorted(random.sample(mais_frequentes, 15))
        cartoes.append(cartao)
    return cartoes

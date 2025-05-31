from collections import Counter
import random

class LotoFacilStats:
    def __init__(self, concursos):
        self.concursos = concursos
        self.numeros = list(range(1, 26))

    def frequencia_numeros(self):
        contador = Counter()
        for concurso in self.concursos:
            contador.update(concurso)
        return dict(sorted(contador.items()))

    def soma_media(self):
        somas = [sum(c) for c in self.concursos]
        return sum(somas) / len(somas) if somas else 0

    def pares_impares_distribuicao(self):
        pares = []
        impares = []
        for c in self.concursos:
            p = sum(1 for n in c if n % 2 == 0)
            pares.append(p)
            impares.append(15 - p)
        return {'pares': sum(pares)/len(pares), 'impares': sum(impares)/len(impares)}

    def numeros_consecutivos(self):
        consecutivos = []
        for c in self.concursos:
            count = sum(1 for i in range(14) if c[i] + 1 == c[i+1])
            consecutivos.append(count)
        return sum(consecutivos)/len(consecutivos) if consecutivos else 0

    def grupos_distribuicao(self):
        grupos = {1:[], 2:[], 3:[], 4:[], 5:[]}
        for c in self.concursos:
            g1 = sum(1 for n in c if 1 <= n <= 5)
            g2 = sum(1 for n in c if 6 <= n <= 10)
            g3 = sum(1 for n in c if 11 <= n <= 15)
            g4 = sum(1 for n in c if 16 <= n <= 20)
            g5 = sum(1 for n in c if 21 <= n <= 25)
            grupos[1].append(g1)
            grupos[2].append(g2)
            grupos[3].append(g3)
            grupos[4].append(g4)
            grupos[5].append(g5)
        return {k: sum(v)/len(v) for k,v in grupos.items()}

    def numeros_quentes_frios(self, top_n=10):
        freq = self.frequencia_numeros()
        ordenado = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        quentes = [num for num, _ in ordenado[:top_n]]
        frios = [num for num, _ in ordenado[-top_n:]]
        return {'quentes': quentes, 'frios': frios}

    def simular_acertos(self, cartao, ultimos=20):
        """Retorna a média de acertos de um cartão nos últimos 'ultimos' concursos"""
        ultimos_concursos = self.concursos[:ultimos]
        acertos = [len(set(cartao) & set(c)) for c in ultimos_concursos]
        return sum(acertos) / len(acertos)

    def gerar_cartoes_otimizados(self, num_cartoes=5, alvo_min_acertos=14):
        freq = self.frequencia_numeros()
        quentes = set(self.numeros_quentes_frios()['quentes'])
        frios = set(self.numeros_quentes_frios()['frios'])

        pares_impares = self.pares_impares_distribuicao()
        media_pares = round(pares_impares['pares'])
        media_impares = 15 - media_pares

        cartoes = []
        tentativas = 0
        max_tentativas = num_cartoes * 200

        while len(cartoes) < num_cartoes and tentativas < max_tentativas:
            tentativas += 1
            cartao = set()

            pares_quentes = [n for n in quentes if n % 2 == 0]
            impares_quentes = [n for n in quentes if n % 2 != 0]
            pares_frios = [n for n in frios if n % 2 == 0]
            impares_frios = [n for n in frios if n % 2 != 0]

            qtd_pares_quentes = media_pares // 2
            qtd_pares_frios = media_pares - qtd_pares_quentes
            qtd_impares_quentes = media_impares // 2
            qtd_impares_frios = media_impares - qtd_impares_quentes

            cartao.update(random.sample(pares_quentes, min(qtd_pares_quentes, len(pares_quentes))))
            cartao.update(random.sample(pares_frios, min(qtd_pares_frios, len(pares_frios))))
            cartao.update(random.sample(impares_quentes, min(qtd_impares_quentes, len(impares_quentes))))
            cartao.update(random.sample(impares_frios, min(qtd_impares_frios, len(impares_frios))))

            while len(cartao) < 15:
                cartao.add(random.choice(self.numeros))

            cartao = sorted(cartao)
            media_acertos = self.simular_acertos(cartao)

            if cartao not in cartoes and media_acertos >= alvo_min_acertos:
                cartoes.append(cartao)

        return cartoes

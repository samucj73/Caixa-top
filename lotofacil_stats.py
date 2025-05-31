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
        return sum(sum(c) for c in self.concursos) / len(self.concursos) if self.concursos else 0

    def pares_impares_distribuicao(self):
        pares = [sum(1 for n in c if n % 2 == 0) for c in self.concursos]
        impares = [15 - p for p in pares]
        return {'pares': sum(pares)/len(pares), 'impares': sum(impares)/len(impares)}

    def numeros_consecutivos(self):
        consecutivos = []
        for c in self.concursos:
            count = sum(1 for i in range(len(c)-1) if c[i]+1 == c[i+1])
            consecutivos.append(count)
        return sum(consecutivos)/len(consecutivos) if consecutivos else 0

    def grupos_distribuicao(self):
        grupos = {i: [] for i in range(1, 6)}
        for c in self.concursos:
            grupos[1].append(sum(1 for n in c if 1 <= n <= 5))
            grupos[2].append(sum(1 for n in c if 6 <= n <= 10))
            grupos[3].append(sum(1 for n in c if 11 <= n <= 15))
            grupos[4].append(sum(1 for n in c if 16 <= n <= 20))
            grupos[5].append(sum(1 for n in c if 21 <= n <= 25))
        return {k: sum(v)/len(v) for k, v in grupos.items()}

    def numeros_quentes_frios(self, top_n=10):
        freq = self.frequencia_numeros()
        ordenado = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return {
            'quentes': [num for num, _ in ordenado[:top_n]],
            'frios': [num for num, _ in ordenado[-top_n:]]
        }

    def gerar_cartoes_otimizados(self, num_cartoes=5, alvo_min_acertos=14):
        freq = self.frequencia_numeros()
        quentes = set(self.numeros_quentes_frios()['quentes'])
        frios = set(self.numeros_quentes_frios()['frios'])

        pares_impares = self.pares_impares_distribuicao()
        media_pares = round(pares_impares['pares'])
        media_impares = 15 - media_pares

        melhores_cartoes = []

        tentativas = 0
        max_tentativas = num_cartoes * 100

        while len(melhores_cartoes) < num_cartoes and tentativas < max_tentativas:
            tentativas += 1
            cartao = set()

            pares_quentes = [n for n in quentes if n % 2 == 0]
            impares_quentes = [n for n in quentes if n % 2 != 0]
            pares_frios = [n for n in frios if n % 2 == 0]
            impares_frios = [n for n in frios if n % 2 != 0]

            qtd_pq = media_pares // 2
            qtd_pf = media_pares - qtd_pq
            qtd_iq = media_impares // 2
            qtd_if = media_impares - qtd_iq

            cartao.update(random.sample(pares_quentes, min(qtd_pq, len(pares_quentes))))
            cartao.update(random.sample(pares_frios, min(qtd_pf, len(pares_frios))))
            cartao.update(random.sample(impares_quentes, min(qtd_iq, len(impares_quentes))))
            cartao.update(random.sample(impares_frios, min(qtd_if, len(impares_frios))))

            while len(cartao) < 15:
                cartao.add(random.choice(self.numeros))

            cartao = sorted(cartao)
            ultimo = self.concursos[0]
            acertos = len(set(cartao) & set(ultimo))

            if cartao not in melhores_cartoes:
                if acertos >= alvo_min_acertos:
                    melhores_cartoes.append(cartao)

        if not melhores_cartoes:
            # Relaxa a condição para retornar os melhores disponíveis
            candidatos = []
            while len(candidatos) < num_cartoes and tentativas < max_tentativas:
                cartao = sorted(random.sample(self.numeros, 15))
                acertos = len(set(cartao) & set(self.concursos[0]))
                candidatos.append((acertos, cartao))
                tentativas += 1
            candidatos.sort(reverse=True)
            return [c for _, c in candidatos[:num_cartoes]]

        return melhores_cartoes

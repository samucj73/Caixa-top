from collections import Counter
import random

class LotoFacilStats:
    def __init__(self, concursos):
        """
        concursos: lista de listas com 15 números cada
        """
        self.concursos = concursos
        self.numeros = list(range(1, 26))

    def frequencia_numeros(self):
        """Retorna dict número: frequência"""
        contador = Counter()
        for concurso in self.concursos:
            contador.update(concurso)
        return dict(sorted(contador.items()))

    def soma_media(self):
        """Média da soma dos números por concurso"""
        somas = [sum(c) for c in self.concursos]
        return sum(somas) / len(somas) if somas else 0

    def pares_impares_distribuicao(self):
        """Retorna média de pares e ímpares por concurso"""
        pares = []
        impares = []
        for c in self.concursos:
            p = sum(1 for n in c if n % 2 == 0)
            i = 15 - p
            pares.append(p)
            impares.append(i)
        return {'pares': sum(pares)/len(pares), 'impares': sum(impares)/len(impares)}

    def numeros_consecutivos(self):
        """Média de números consecutivos por concurso"""
        consecutivos = []
        for c in self.concursos:
            count = 0
            for i in range(len(c)-1):
                if c[i]+1 == c[i+1]:
                    count += 1
            consecutivos.append(count)
        return sum(consecutivos)/len(consecutivos) if consecutivos else 0

    def grupos_distribuicao(self):
        """Média de números por grupos: 1-5, 6-10, 11-15, 16-20, 21-25"""
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

    def gerar_cartoes_otimizados(self, num_cartoes=5, alvo_min_acertos=14):
        """
        Gera cartões baseados nas estatísticas.
        Simples: mistura números quentes e frios e tentativas aleatórias,
        priorizando pares/impares e grupos próximos das médias.
        """
        freq = self.frequencia_numeros()
        quentes = set(self.numeros_quentes_frios()['quentes'])
        frios = set(self.numeros_quentes_frios()['frios'])

        pares_impares = self.pares_impares_distribuicao()
        media_pares = round(pares_impares['pares'])
        media_impares = 15 - media_pares

        grupos_media = self.grupos_distribuicao()

        cartoes = []

        tentativas = 0
        max_tentativas = num_cartoes * 100

        while len(cartoes) < num_cartoes and tentativas < max_tentativas:
            tentativas += 1
            cartao = set()

            # Priorizar números quentes: pegar metade dos pares/impares de quentes
            pares_quentes = [n for n in quentes if n % 2 == 0]
            impares_quentes = [n for n in quentes if n % 2 != 0]

            pares_frios = [n for n in frios if n % 2 == 0]
            impares_frios = [n for n in frios if n % 2 != 0]

            # Adiciona pares quentes
            qtd_pares_quentes = media_pares // 2
            qtd_pares_frios = media_pares - qtd_pares_quentes

            # Adiciona ímpares quentes
            qtd_impares_quentes = media_impares // 2
            qtd_impares_frios = media_impares - qtd_impares_quentes

            cartao.update(random.sample(pares_quentes, min(qtd_pares_quentes, len(pares_quentes))))
            cartao.update(random.sample(pares_frios, min(qtd_pares_frios, len(pares_frios))))
            cartao.update(random.sample(impares_quentes, min(qtd_impares_quentes, len(impares_quentes))))
            cartao.update(random.sample(impares_frios, min(qtd_impares_frios, len(impares_frios))))

            # Ajusta para 15 números, completa com números aleatórios
            while len(cartao) < 15:
                n = random.choice(self.numeros)
                cartao.add(n)

            cartao = sorted(cartao)

            # TODO: Poderia validar acertos mínimos com concursos reais para garantir alvo_min_acertos

            if cartao not in cartoes:
                cartoes.append(cartao)

        return cartoes

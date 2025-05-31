import random
from collections import Counter

class LotoFacilAvancado:
    def __init__(self, concursos):
        self.concursos = concursos

    def primos(self):
        return [2, 3, 5, 7, 11, 13, 17, 19, 23]

    def multiplos_3(self):
        return [3, 6, 9, 12, 15, 18, 21, 24]

    def media_primos(self):
        total = sum(len([n for n in jogo if n in self.primos()]) for jogo in self.concursos)
        return total / len(self.concursos)

    def media_multiplos_3(self):
        total = sum(len([n for n in jogo if n in self.multiplos_3()]) for jogo in self.concursos)
        return total / len(self.concursos)

    def distribuicao_primos(self):
        contagem = Counter(len([n for n in jogo if n in self.primos()]) for jogo in self.concursos)
        return dict(sorted(contagem.items()))

    def distribuicao_multiplos_3(self):
        contagem = Counter(len([n for n in jogo if n in self.multiplos_3()]) for jogo in self.concursos)
        return dict(sorted(contagem.items()))

    def gerar_cartoes_com_avancado(self, num_cartoes=5, alvo_min_acertos=13):
        cartoes = []
        tentativas = 0
        max_tentativas = num_cartoes * 300  # tenta bastante para achar bons

        media_primos = round(self.media_primos())
        media_multiplos = round(self.media_multiplos_3())

        while len(cartoes) < num_cartoes and tentativas < max_tentativas:
            dezenas = sorted(random.sample(range(1, 26), 15))
            acertos_simulados = self.simular_desempenho(dezenas)

            if acertos_simulados >= alvo_min_acertos:
                qt_primos = len([d for d in dezenas if d in self.primos()])
                qt_multiplos = len([d for d in dezenas if d in self.multiplos_3()])

                if qt_primos == media_primos and qt_multiplos == media_multiplos:
                    cartoes.append(dezenas)

            tentativas += 1

        return cartoes

    def simular_desempenho(self, cartao):
        # Simula acertos do cartão nos últimos 20 concursos
        historico = self.concursos[:20]
        acertos = [len(set(cartao) & set(jogo)) for jogo in historico]
        return sum(acertos) / len(acertos) if acertos else 0

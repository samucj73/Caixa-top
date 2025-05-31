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
        def cartao_valido(cartao):
            # 1. Máx. 3 números consecutivos
            consecutivos = 1
            for i in range(1, len(cartao)):
                if cartao[i] == cartao[i-1] + 1:
                    consecutivos += 1
                    if consecutivos > 3:
                        return False
                else:
                    consecutivos = 1

            # 2. Máx. 8 dezenas repetidas do último concurso
            if self.concursos:
                ultimo = set(self.concursos[0])
                if len(set(cartao) & ultimo) > 8:
                    return False

            # 3. Limite de pares (mín. 3, máx. 12)
            pares = sum(1 for n in cartao if n % 2 == 0)
            if pares < 3 or pares > 12:
                return False

            # 4. Primos e múltiplos de 3 dentro da média ±1
            qt_primos = sum(1 for n in cartao if n in self.primos())
            qt_multiplos = sum(1 for n in cartao if n in self.multiplos_3())
            if not (media_primos - 1 <= qt_primos <= media_primos + 1):
                return False
            if not (media_multiplos - 1 <= qt_multiplos <= media_multiplos + 1):
                return False

            # 5. Evitar cartões já sorteados
            if cartao in self.concursos:
                return False

            # 6. Distribuição mínima por linha e coluna
            linhas = [0] * 5
            colunas = [0] * 5
            for n in cartao:
                linha = (n - 1) // 5
                coluna = (n - 1) % 5
                linhas[linha] += 1
                colunas[coluna] += 1
            if any(l < 2 for l in linhas) or any(c < 2 for c in colunas):
                return False

            return True

        cartoes_validos = []
        candidatos = []
        tentativas = 0
        max_tentativas = num_cartoes * 1500

        media_primos = round(self.media_primos())
        media_multiplos = round(self.media_multiplos_3())

        while len(cartoes_validos) < num_cartoes and tentativas < max_tentativas:
            dezenas = sorted(random.sample(range(1, 26), 15))
            if not cartao_valido(dezenas):
                tentativas += 1
                continue

            acertos_simulados = self.simular_desempenho(dezenas)

            candidatos.append((acertos_simulados, dezenas))
            if acertos_simulados >= alvo_min_acertos:
                cartoes_validos.append(dezenas)

            tentativas += 1

        if cartoes_validos:
            return cartoes_validos
        else:
            candidatos.sort(reverse=True)
            return [d for _, d in candidatos[:num_cartoes]]

    def simular_desempenho(self, cartao):
        # Simula acertos do cartão nos últimos 20 concursos
        historico = self.concursos[:20]
        acertos = [len(set(cartao) & set(jogo)) for jogo in historico]
        return sum(acertos) / len(acertos) if acertos else 0

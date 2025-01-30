
import cv2
from google.colab.patches import cv2_imshow
import numpy as np
import random

# classe do jogo de sorte
class Jogo1:
    def __init__(self, jogadores, baralho):
        self.__jogadores = jogadores
        self.__baralho = baralho

    def iniciar_jogo(self):
        num_cartas = int(input("Quantas cartas cada jogador deve receber?\n> "))
        print("\n")
        # o jogo inicia embaralhando o baralho
        self.__baralho.embaralhar()
        for jogador in self.__jogadores:
          # distribuindo a carta de cada um dos jogadores
            jogador.distribuir_mao(self.__baralho, num_cartas)
            print("Distribuindo as cartas... \n")
            jogador.exibir_cartas()
            jogador.contar_pontos()
            print(f"\n O jogador {jogador.obter_nome()} está com {jogador.obter_pontos()} pontos. \n")

    def vencedor(self):
        vencedor = None
        maior_pontos = 0
        for jogador in self.__jogadores:
            pontos = jogador.contar_pontos()
            # laço que compara a quantidade de pontos de cada um dos jogadores determina o vencedor
            if pontos > maior_pontos:
                vencedor = jogador
                maior_pontos = pontos
            elif pontos == maior_pontos:
              print(f"Ocorreu um empate entre o jogador {jogador.obter_nome()} e o jogador {vencedor.obter_nome()}")
        print(f" ☆ O vencedor é o jogador {vencedor.obter_nome()} ☆ ")

# classe do jogo 21
class Jogo2:
    def __init__(self, jogadores, baralho):
        self.__jogadores = jogadores
        self.__baralho = baralho

    def iniciar_jogo(self):
        self.__baralho.embaralhar()
        # inicia o jogo embaralhando o jogo
        for jogador in self.__jogadores:
          # distribui 2 cartas para cada um dos jogadores
            jogador.distribuir_mao(self.__baralho, 2)
            print("Cada jogador começará com duas cartas. \n")
            print("Distribuindo as cartas...")
            jogador.exibir_cartas()
            # faz o calculo dos pontos de cada um dos jogadores
            jogador.contar_pontos2()
            print(f"\n O jogador {jogador.obter_nome()} está com {jogador.obter_pontos()} pontos. \n")
        while True:
            for jogador in self.__jogadores:
                # laço para verificar se o jogador deseja puxar outra carta
                puxar = int(input(f"Jogador {jogador.obter_nome()} você deseja puxar uma carta? \n 0. Não \n 1. Sim\n> "))
                if puxar == 1:
                  # se o jogador digitar 1, puxa-se uma carta e atualiza as cartas e os pontos do mesmo
                    jogador.puxar_carta(self.__baralho)  # Corrigido: passa o baralho como parâmetro
                    jogador.exibir_cartas()
                    jogador.contar_pontos2()
                    print(f"\n O jogador {jogador.obter_nome()} está com {jogador.obter_pontos()} pontos. \n")
                elif puxar == 0:
                    print("\n Você não puxou uma carta \n")
                    continue
            # pergunta se mais jogadores querem puxar mais cartas
            sem_puxar = int(input("Mais algum jogador deseja puxar uma carta? \n 0. Não \n 1. Sim\n> "))
            if sem_puxar == 0:
                print("Calculando quem é o vencedor...")
                break

    def vencedor2(self):
        vencedor = None
        maior_pontos = 0
        for jogador in self.__jogadores:
            pontos = jogador.contar_pontos2()
            # laço que compara a quantidade de pontos de cada um dos jogadores com 21 e determina o vencedor
            if pontos > 21:
              print(f"O jogador {jogador.obter_nome()} está fora da rodada, pois ultrapassou 21 pontos.")
            elif pontos <= 21 and pontos > maior_pontos:
                vencedor = jogador
                maior_pontos = pontos
            elif pontos == maior_pontos:
              print(f"Ocorreu um empate entre o jogador {jogador.obter_nome()} e o jogador {vencedor.obter_nome()}")
        if vencedor:
            print(f" ☆ O vencedor é o jogador {vencedor.obter_nome()} com {maior_pontos} pontos! ☆ ")
        else:
            print("Nenhum jogador venceu, todos ultrapassaram 21 pontos.")


class Carta:
    def __init__(self, naipe, valor):
        self.__naipe = naipe
        self.__valor = valor

    def obter_naipe(self):
        return self.__naipe

    def obter_valor(self):
        return self.__valor

    def mostrar_carta(self):
        nomes = {1: "Ás", 11: "Valete", 12: "Dama", 13: "Rei"}
        valor = nomes.get(self.__valor, self.__valor)
        print(f"Carta: {valor} de {self.__naipe}")

    # método para aparecer as cartas
    def mostrar_imagem_carta(self, naipe, valor):
      # usando o opencv para mostrar/ escrevendo o caminho/ {naipe} e {valor} pegam os naipes e os valores de cada carta e, assim, direciona para a foto no drive
      caminho = f'/content/drive/My Drive/cartas/{naipe}/{valor}.png'
      # acessando a imagem no drive
      imagem = cv2.imread(caminho)


      if imagem is not None:
        cv2_imshow(imagem)

      else:
        print("Imagem não encontrada")

class Jogador:
    def __init__(self, nome):
        self.__nome = nome
        self.__mao = []
        self.__valores = []

    def distribuir_mao(self, baralho, num_cartas):
        self.__mao, self.__valores = baralho.distribuir(num_cartas)

    def exibir_cartas(self):
        print(f"\nCartas de {self.__nome} ------ \n")
        for carta in self.__mao:
            naipe = carta.obter_naipe()
            valor = carta.obter_valor()
            carta.mostrar_imagem_carta(naipe, valor)
            carta.mostrar_carta()


    # soma os valores das cartas
    def contar_pontos(self):
      self.__cont = 0
      for valor in  self.__valores:
        self.__cont += valor
      return self.__cont

    def contar_pontos2(self):
        self.__cont = 0
        for valor in self.__valores:
            # verifica cada um dos valores, se forem "especiais" (valete, rainha ou rei), muda para 10
            if valor in [11, 12, 13]:
                valor = 10
            # verifica cada um dos valores, se for "ás", muda para 11
            elif valor == 1:
                valor = 11
            self.__cont += valor
        return self.__cont

    def obter_pontos(self):
        return self.__cont

    def puxar_carta(self, baralho):
        if baralho:
            # atribuindo a ultima carta e retirando do baralho
            carta = baralho.pop()
            valor = carta.obter_valor()
            self.__valores.append(valor)
            self.__mao.append(carta)
        else:
            print("Não há mais cartas no baralho")

    def obter_nome(self):
        return self.__nome

class Baralho:
    def __init__(self, cartas):
        self.__baralho = cartas

    def embaralhar(self):
        random.shuffle(self.__baralho)

    def pop(self):
        # remove e retorna a ultima carta do baralho
        return self.__baralho.pop()

    def distribuir(self, num_cartas):
      self.__mao = []
      self.__valores = []
      for i in range(num_cartas):
        if self.__baralho:
          # atribuindo a ultima carta e retirando do baralho
          carta = self.__baralho.pop()
          valor = carta.obter_valor()
          self.__valores.append(valor)
          self.__mao.append(carta)
      return self.__mao, self.__valores

# Resto do código de menu e jogabilidade
print("Bem vindo ao Carteado!")

n = 0
while n < 1:
  print("Este é o nosso menu.")
  # opcoes do menu
  opcao = int(input("Selecione a opção que você deseja: \n 1.Regras do Jogo da Sorte \n 2. Regras do Jogo 21 \n 3. Inicie o Jogo da Sorte 1 \n 4. Inicie o Jogo 21 \n 5. Sair do menu \n> "))
  # regras do jogo 1
  if opcao == 1:
    print("Regras do jogo: \n - As cartas serão distribuídas igualmente para cada jogador \n - Ganha quem tiver a maior pontuação \n")
  elif opcao == 2:
  # regras do jogo 2
    print("Regras do jogo: \n - Serão distribuidas inicialmente 2 cartas para cada jogador \n - Ganha quem tiver a pontação mais próxima de 21 ganha \n - Cada jogador pode puxar uma carta se achar necessário \n - O valor de Às é 11 \n - O valor do Rei, da Rainha e do Valete é 10 \n")
  elif opcao == 3:
    m = 0
    # looping para o jogo 1
    while m < 1:
      print("\nO jogo começou!")
      num_jogadores = int(input("Quantos jogadores vão jogar? \n> "))
      jogadores = []
      for i in range(num_jogadores):
        # atribuindo op nome dos jogadores
        nome = input(f"Digite o nome do jogador {i + 1} \n> ")
        jogadores.append(Jogador(nome))
        # atribuindo as cartas
      cartas = [Carta("Paus", 1),Carta("Paus", 2),Carta("Paus", 3),Carta("Paus", 4),Carta("Paus", 5),Carta("Paus", 6),Carta("Paus", 7),Carta("Paus", 8), Carta("Paus", 9), Carta("Paus", 10),Carta("Paus", 11),Carta("Paus", 12),Carta("Paus", 13), Carta("Copas", 1),Carta("Copas", 2),Carta("Copas", 3),Carta("Copas", 4), Carta("Copas", 5),Carta("Copas", 6),Carta("Copas", 7), Carta("Copas", 8),Carta("Copas", 9),Carta("Copas", 10), Carta("Copas", 11),Carta("Copas", 12),Carta("Copas", 13), Carta("Espadas", 1),Carta("Espadas", 2),Carta("Espadas", 3),Carta("Espadas", 4),Carta("Espadas", 5),Carta("Espadas", 6),Carta("Espadas", 7),Carta("Espadas", 8),Carta("Espadas", 9),Carta("Espadas", 10),Carta("Espadas", 11),Carta("Espadas", 12),Carta("Espadas", 13),Carta("Ouros", 1), Carta("Ouros", 2),Carta("Ouros", 3),Carta("Ouros", 4),Carta("Ouros", 5),Carta("Ouros", 6),Carta("Ouros", 7),Carta("Ouros", 8),Carta("Ouros", 9),Carta("Ouros", 10),Carta("Ouros", 11),Carta("Ouros", 12),Carta("Ouros", 13)]
      # atribuindo o baralho
      baralho = Baralho(cartas)
      # inicializando o jogo
      jogo1 = Jogo1(jogadores, baralho)
      jogo1.iniciar_jogo()
      print("Calculando o vencedor...")
      jogo1.vencedor()
      # verificando se o jogador deseja outra jogada
      sair = int(input("\n Você deseja participar de outra rodada do jogo? \n 0.Não \n 1.Sim\n> "))
      if sair == 0:
        print("\n Você está saindo do jogo. Obrigada por participar! \n")
        break
      else:
        continue
  elif opcao == 4:
    m = 0
    # looping para o jogo 2
    while m < 1:
      print("\nO jogo começou!")
      num_jogadores = int(input("Quantos jogadores vão jogar? \n> "))
      jogadores = []
      for i in range(num_jogadores):
        # atribuindo op nome dos jogadores
        nome = input(f"Digite o nome do jogador {i + 1} \n> ")
        jogadores.append(Jogador(nome))
        # atribuindo as cartas
      cartas = [Carta("Paus", 1),Carta("Paus", 2),Carta("Paus", 3),Carta("Paus", 4),Carta("Paus", 5),Carta("Paus", 6),Carta("Paus", 7),Carta("Paus", 8), Carta("Paus", 9), Carta("Paus", 10),Carta("Paus", 11),Carta("Paus", 12),Carta("Paus", 13), Carta("Copas", 1),Carta("Copas", 2),Carta("Copas", 3),Carta("Copas", 4), Carta("Copas", 5),Carta("Copas", 6),Carta("Copas", 7), Carta("Copas", 8),Carta("Copas", 9),Carta("Copas", 10), Carta("Copas", 11),Carta("Copas", 12),Carta("Copas", 13), Carta("Espadas", 1),Carta("Espadas", 2),Carta("Espadas", 3),Carta("Espadas", 4),Carta("Espadas", 5),Carta("Espadas", 6),Carta("Espadas", 7),Carta("Espadas", 8),Carta("Espadas", 9),Carta("Espadas", 10),Carta("Espadas", 11),Carta("Espadas", 12),Carta("Espadas", 13),Carta("Ouros", 1), Carta("Ouros", 2),Carta("Ouros", 3),Carta("Ouros", 4),Carta("Ouros", 5),Carta("Ouros", 6),Carta("Ouros", 7),Carta("Ouros", 8),Carta("Ouros", 9),Carta("Ouros", 10),Carta("Ouros", 11),Carta("Ouros", 12),Carta("Ouros", 13)]
      # atribuindo o baralho
      baralho = Baralho(cartas)
      # inicializando o jogo
      jogo2 = Jogo2(jogadores, baralho)
      jogo2.iniciar_jogo()
      print("\n")
      jogo2.vencedor2()
      # verificando se o jogador deseja outra jogada
      sair = int(input("\n Você deseja participar de outra rodada do jogo? \n 0.Não \n 1.Sim \n> "))
      if sair == 0:
        print("\n Você está saindo do jogo. Obrigada por participar!")
        break
      else:
        continue
  # saindo do menu
  elif opcao == 5:
    print("\n Você está saindo do menu. Obrigada por jogar! \n")
    break

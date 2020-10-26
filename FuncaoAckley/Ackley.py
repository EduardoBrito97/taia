import random
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from collections import defaultdict

NUM_MAX_GERACOES = 100
NUM_POP = 100
PROB_MUTACAO = 0.4
PROB_RECOMB = 0.9
NUM_XS = 30
QTD_PAIS = 5

MET_USADO = 0

MELHOR_INDIVIDUO = []
FITNESS_MELHOR_INDIVIDUO = []
FITNESS_DESEJADO = 1

SOMA = []
MEDIA = []

NUM_AMOSTRAGEM = 1

MAPA_NUM_METODO = { 0:"PIORES INDIVIDUOS, CRUZAMENTO DISCRETO, MUTAÇÃO UNIFORME",
                    1:"PIORES INDIVIDUOS, CRUZAMENTO INTERMEDIÁRIO, MUTAÇÃO UNIFORME",
                    2:"THANOS, CRUZAMENTO DISCRETO, MUTAÇÃO UNIFORME",
                    3:"THANOS, CRUZAMENTO INTERMEDIÁRIO, MUTAÇÃO UNIFORME",
                    4:"PIORES INDIVIDUOS, CRUZAMENTO INTERMEDIÁRIO, MUTAÇÃO NÃO UNIFORME",
                    5:"THANOS, CRUZAMENTO INTERMEDIÁRIO, MUTAÇÃO NÃO UNIFORME"}

LIM_MAX = 1
LIM_MIN = -1

y=["PICDMU","PICIMU", "TCDMU", "TCIMU", "PICIMNU", "TCIMNU"]

def main():
  global MET_USADO

  mapaMetodoPassos = {}
  mapaMetodoMedias = {}
  mapaMetodoMediasMelhorIndividuo = {}
  mapaMetodoTempos = {}
  mapaMetodoSomas = {}

  for metodo in range(0, len(MAPA_NUM_METODO)):
    mapaMetodoPassos[metodo] = []
    mapaMetodoMedias[metodo] = []
    mapaMetodoMediasMelhorIndividuo[metodo] = []
    mapaMetodoTempos[metodo] = []
    mapaMetodoSomas[metodo] = []

  for i in range(0, NUM_AMOSTRAGEM):
    populacao = iniciarPopulacao()
    print(i)
    for metodo in range(0, len(MAPA_NUM_METODO)):
      MET_USADO = metodo
      populacaoUsada = populacao.copy()

      comeco = time.time()
      numPassosAgora = rodarPrograma(populacaoUsada)
      mapaMetodoTempos[metodo].append(time.time() - comeco)

      mapaMetodoPassos[metodo].append(numPassosAgora)

      mediaFitnessAgora = sum(MEDIA)/len(MEDIA)
      mapaMetodoMedias[metodo].append(mediaFitnessAgora)
      
      mediaFitnessMelhorIndividuoAgora = sum(FITNESS_MELHOR_INDIVIDUO)/len(FITNESS_MELHOR_INDIVIDUO)
      mapaMetodoMediasMelhorIndividuo[metodo].append(mediaFitnessMelhorIndividuoAgora)

      mediaSomaAgora = sum(SOMA)/len(SOMA)
      mapaMetodoSomas[metodo].append(mediaSomaAgora)

  x_mP=[]
  x_mF=[]
  x_mFM=[]
  x_mTE=[]
  x_mS=[]
  x_mP_Error=[]
  x_mF_Error=[]
  x_mFM_Error=[]
  x_mTE_Error=[]
  x_mS_Error=[]
  for metodo in MAPA_NUM_METODO:
    mediaPassos = sum(mapaMetodoPassos[metodo])/len(mapaMetodoPassos[metodo])
    mediaFitness = sum(mapaMetodoMedias[metodo])/len(mapaMetodoMedias[metodo])
    mediaFitnessMelhorIndividuo = sum( mapaMetodoMediasMelhorIndividuo[metodo])/len(mapaMetodoMediasMelhorIndividuo[metodo])
    mediaTempoExecucao = sum(mapaMetodoTempos[metodo])/len(mapaMetodoTempos[metodo])
    mediaSoma = sum(mapaMetodoSomas[metodo])/len(mapaMetodoSomas[metodo])
    x_mP.append(mediaPassos)
    x_mF.append(mediaFitness)
    x_mFM.append(mediaFitnessMelhorIndividuo)
    x_mTE.append(mediaTempoExecucao)
    x_mS.append(mediaSoma)
    x_mP_Error.append(desvioPadrao(mapaMetodoPassos[metodo]))
    x_mF_Error.append(desvioPadrao(mapaMetodoMedias[metodo]))
    x_mFM_Error.append(desvioPadrao(mapaMetodoMediasMelhorIndividuo[metodo]))
    x_mTE_Error.append(desvioPadrao(mapaMetodoTempos[metodo]))
    x_mS_Error.append(desvioPadrao(mapaMetodoSomas[metodo]))
    print('Quantidade de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaPassos))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoPassos[metodo])))
    print('Média de fitness para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaFitness))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoMedias[metodo])))
    print('Média de fitness melhores individuos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaFitnessMelhorIndividuo))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoMediasMelhorIndividuo[metodo])))
    print('Média tempo de execução para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaTempoExecucao) + ' segundos')
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoTempos[metodo])))
    print('Média de soma de fitness para ' + MAPA_NUM_METODO[metodo] + ': ' + str(mediaSoma))
    print('Desvio Padrão de passos para ' + MAPA_NUM_METODO[metodo] + ': ' + str(desvioPadrao(mapaMetodoSomas[metodo])))
    
    print('------------------------------------------------------------------------------------------------')

  plotGraficos(x_mP,x_mF,x_mFM,x_mTE,x_mS,x_mP_Error,x_mF_Error,x_mFM_Error,x_mTE_Error,x_mS_Error,y)

def desvioPadrao(elementos):
  mi = sum(elementos)/len(elementos)
  soma = 0
  for i in elementos:
    soma += abs(i - mi)**2
  return ((soma/len(elementos))**0.5)

def rodarPrograma(populacao):
  resetarVarGlobais()
  atualizaDados(populacao)
  numGeracoes = 1
  while (numGeracoes <= NUM_MAX_GERACOES 
          and FITNESS_MELHOR_INDIVIDUO[-1] < FITNESS_DESEJADO):
    populacao = realizarCruzamento(populacao)
    populacao = realizarMutacao(populacao)
    atualizaDados(populacao)
    numGeracoes += 1

  return numGeracoes

def resetarVarGlobais():
  global SOMA, FITNESS_MELHOR_INDIVIDUO, MEDIA, MELHOR_INDIVIDUO
  SOMA = []
  FITNESS_MELHOR_INDIVIDUO = []
  MEDIA = []
  MELHOR_INDIVIDUO = []

def iniciarPopulacao():
  populacao = []
  while (len(populacao) < NUM_POP):
    individuo = geraIndividuo()
    if (not individuo in populacao):
      populacao.append(individuo)

  return populacao

def geraIndividuo():
  individuo = []
  for _ in range(NUM_XS):
    individuo.append(random.uniform(LIM_MIN, LIM_MAX))
  return individuo

def atualizaDados(populacao):
  global SOMA, MEDIA, MELHOR_INDIVIDUO, FITNESS_MELHOR_INDIVIDUO
  SOMA.append(0)
  melhor_individuo = 0
  fitness_melhor_individuo = 0
  for individuo in populacao:
    fitness = calculaFitness(individuo)
    SOMA[-1] = SOMA[-1] + fitness
    if (fitness > fitness_melhor_individuo):
      fitness_melhor_individuo = fitness
      melhor_individuo = individuo

  MELHOR_INDIVIDUO.append(melhor_individuo)
  FITNESS_MELHOR_INDIVIDUO.append(fitness_melhor_individuo)
  MEDIA.append(SOMA[-1] / len(populacao))
  return

def funcaoAckley(individuo):
  somaXiQuadrado = 0
  somaCosXi = 0
  for xi in individuo:
    somaXiQuadrado += xi*xi
    somaCosXi = math.cos(math.pi * 2 * xi)
  
  exp1 = -0.2*math.sqrt(somaXiQuadrado/NUM_XS)
  primeiraExpressao = -20 * math.exp(exp1)

  exp2 = somaCosXi / NUM_XS
  segundaExpressao = -math.exp(exp2)

  return primeiraExpressao + segundaExpressao + 20 + math.exp(1)

def calculaFitness(individuo):
  return 1 / (1 + funcaoAckley(individuo))

def realizarCruzamento(populacao):
  chanceDaVez = random.randint(0,101)
  if (PROB_RECOMB * 100 < chanceDaVez):
    return populacao

  if MET_USADO == 0:
    pais = pegarMelhoresPais(populacao, 2)
    filhos = cruzamentoDiscreto(pais[0], pais[1], 2)
    
    pioresIndividuosIndices = pegarIndicesPioresIndividuos(populacao, 2)
    populacao[pioresIndividuosIndices[0]] = filhos[0]
    populacao[pioresIndividuosIndices[1]] = filhos[1]

  elif MET_USADO == 1:
    pais = pegarMelhoresPais(populacao, 2)
    filhos = cruzamentoIntermediario(pais[0], pais[1], 2)
    
    pioresIndividuosIndices = pegarIndicesPioresIndividuos(populacao, 2)
    populacao[pioresIndividuosIndices[0]] = filhos[0]
    populacao[pioresIndividuosIndices[1]] = filhos[1]
  
  elif MET_USADO == 2:
    pais = pegarPaisSuperSmashBros(populacao, len(populacao)/2) 
    indexPais = random.sample(range(0, len(pais)), len(pais))
    for i in range(0,len(indexPais),2):
      filhos = cruzamentoDiscreto(pais[indexPais[i]], pais[indexPais[i+1]], 2)
      populacao.append(filhos[0])
      populacao.append(filhos[1])

  elif MET_USADO == 3:
    pais = pegarPaisSuperSmashBros(populacao, len(populacao)/2) 
    indexPais = random.sample(range(0, len(pais)), len(pais))
    for i in range(0,len(indexPais),2):
      filhos = cruzamentoIntermediario(pais[indexPais[i]], pais[indexPais[i+1]], 2)
      populacao.append(filhos[0])
      populacao.append(filhos[1])

  return populacao

def pegarPaisSuperSmashBros(populacao, numPais): ###Combate entres os individuos pra saber quem vai ser o pai
  pais = []
  perdedores = []
  while len(pais)<numPais:
    indexCombatentes = random.sample(range(0, len(populacao)), 2)
    combatenteA = populacao[indexCombatentes[0]]
    combatenteB = populacao[indexCombatentes[1]]
    if calculaFitness(combatenteA) > calculaFitness(combatenteB): ###A gente salva os vencedores e mata os perdedores
      pais.append(combatenteA)
      perdedores.append(combatenteB)
      populacao.pop(indexCombatentes[1]) 
    else: 
      pais.append(combatenteB)
      perdedores.append(combatenteA)
      populacao.pop(indexCombatentes[0])
  return pais

def pegarMelhoresPais(populacao, numPais):
  posicaoPais = []
  for i in range(0, NUM_POP):
    posicaoPais.append(random.randint(0, NUM_POP-1))
  
  mapaFitnessIndividuo = {}
  fitnessPais = []
  for posicao in posicaoPais:
    individuo = populacao[posicao]
    fitness = calculaFitness(individuo)
    fitnessPais.append(fitness)
    mapaFitnessIndividuo[fitness] = individuo

  fitnessPais.sort(reverse=True)
  pais = []
  for i in range(0, numPais):
    pais.append(mapaFitnessIndividuo[fitnessPais[i]])

  return pais

def cruzamentoDiscreto(pai1, pai2, numFilhos):
  filhos = []
  for _ in range(numFilhos):
    filho = []
    for i in range(NUM_XS):
      filho.append((pai1[i] * 0.5) + (pai2[i] * 0.5))
    filhos.append(filho)

  return filhos

def cruzamentoIntermediario(pai1, pai2, numFilhos):
  filhos = []
  fitnessPai1 = calculaFitness(pai1)
  fitnessPai2 = calculaFitness(pai2)
  probPai1 = fitnessPai1 / (fitnessPai1 + fitnessPai2)
  probPai2 = fitnessPai2 / (fitnessPai1 + fitnessPai2)
  for _ in range(numFilhos):
    filho = []
    for i in range(NUM_XS):
      filho.append((pai1[i] * probPai1) + (pai2[i] * probPai2))
    filhos.append(filho)

  return filhos

def pegarIndicesPioresIndividuos(populacao, numIndividuos):
  fitnessPop = []
  mapaFitnessPosicao = {}
  i = 0
  for individuo in populacao:
    fitness = calculaFitness(individuo)
    fitnessPop.append(fitness)
    mapaFitnessPosicao[fitness] = i
    i += 1
  
  fitnessPop.sort()
  indicesPioresIndividuos = []
  for i in range(0, numIndividuos):
    fitness = fitnessPop[i]
    posicaoFitness = mapaFitnessPosicao[fitness]
    indicesPioresIndividuos.append(posicaoFitness)

  return indicesPioresIndividuos

def realizarMutacao(populacao):
  if MET_USADO <= 3:
    return mutacaoUniforme(populacao)
  else:
    return mutacaoNaoUniforme(populacao)

def mutacaoUniforme(populacao):
  novaPop = []
  for individuo in populacao:
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        novoX = random.uniform(LIM_MIN, LIM_MAX)

      novoIndividuo.append(novoX)
    novaPop.append(novoIndividuo)

  return novaPop

def mutacaoNaoUniforme(populacao):
  novaPop = []
  for individuo in populacao:
    desvPadr = desvioPadrao(individuo)
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        limInferior = (x - desvPadr) % 15
        limSuperior = (x + desvPadr) % 15
        novoX = random.uniform(limInferior, limSuperior)

      novoIndividuo.append(novoX)
    novaPop.append(novoIndividuo)

  return novaPop

def mutacaoGaussiana(populacao):
  novaPop = []
  mu = 0
  sigma = 0.5
  for individuo in populacao:
    dX = random.gauss(mu, sigma)
    novoIndividuo = []
    for x in individuo:
      novoX = x
      if (PROB_MUTACAO * 100 > random.randint(0, 101)):
        novoX = (x + dX) % 15
      novoIndividuo.append(novoX)
      
    novaPop.append(novoIndividuo)

  return novaPop

def plotGraficos(y_mP,y_mF,y_mFM,y_mTE,y_mS,y_mP_Error,y_mF_Error,y_mFM_Error,y_mTE_Error,y_mS_Error,x):
  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mP,yerr=y_mP_Error, color='green')
  plt.xlabel("Métodos")
  plt.ylabel("Quantidade de Passos")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mF,yerr=y_mF_Error, color='orange')
  plt.xlabel("Métodos")
  plt.ylabel("Média de fitness")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mFM,yerr=y_mFM_Error, color='blue')
  plt.xlabel("Métodos")
  plt.ylabel("Média de fitness melhores individuos ")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mTE,yerr=y_mTE_Error, color='red')
  plt.xlabel("Métodos")
  plt.ylabel("Média tempo de execução")
  plt.xticks(x_pos, x)
  plt.show()

  plt.style.use('ggplot')

  x_pos = [i for i, _ in enumerate(x)]

  plt.bar(x_pos, y_mS,yerr=y_mS_Error, color='purple')
  plt.xlabel("Métodos")
  plt.ylabel("Média de soma de fitness")
  plt.xticks(x_pos, x)
  plt.show()

main()
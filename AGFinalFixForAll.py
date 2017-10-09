# -*- coding: UTF-8 -*
"""
Universidade Federal de Mato-Grosso - Centro Universitário do Araguaia
Trabalho de Inteligência Artificial - Algoritmo Genético
Objetivo: Encontrar o Min e Max Global de Funções
Aluno: Vitor Rezende Campos
"""
import random
import math

print "Algoritmo Genético para encontrar Min Max Global de uma Função "
print "###############################################################"
print "Exercício 1:"
print "Determinar o MÁXIMO global da função: f(x) = x.sen.(10.pi.x)+1"
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
print "@@@@ PARÂMETROS PADRÕES"
print "População Inicial 	--> 	10"
print "Máximo de Gerações	-->	30"
print "Taxa de Crossover 	--> 	60%"
print "Taxa de Mutação		-->	5%"
print "###############################################################"
print "Exercício 2:"
print "Determinar o MÍNIMO global da função: f(x) = x2 - 3x + 4"
print "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
print "@@@@ PARÂMETROS PADRÕES"
print "População Inicial 	--> 	4"
print "Máximo de Gerações	-->	5"
print "Taxa de Crossover 	--> 	60%"
print "Taxa de Mutação		-->	1%"
print "###############################################################"
FLAG = int(raw_input ('Escolha o exercício a ser resolvido: '))
MAXIMIZE, MINIMIZE = (0,1)
GENETIC = ''

class Individuo (object):
  global FLAG
  tamanho = 22			# Tamanho da cadeia que representa o cromossomo
  alelos = (0,1)		# Valores que cada gene pode assumir
  if FLAG == 1:
    range = (-1.0, 2.0)		# Intervalo dos valores
    optimizacao = MAXIMIZE	# Tipo de optimização
  elif FLAG == 2:
    range = (-10.0, 10.0)
    optimizacao = MINIMIZE	# Tipo de optimização
  
  # Criação de um indivíduo
  def __init__ (self, cromossomo = None):
    # Aptidão do individuo
    self.score = None
    # Cromossomo formado pela combinação de genes
    self.cromossomo = cromossomo or self._criarCromossomo()
  
  # Cria um novo cromossomo
  def _criarCromossomo (self):
    return [random.choice (self.alelos) for gene in xrange (self.tamanho)]
  
  # Calcula a aptidao do Individuo
  def aptidao (self, otimo = None):
    #Decodificação do cromossomo
    dec = float ( int (GENETIC.join( map(str, self.cromossomo) ),2)) / float (pow(2,self.tamanho) - 1)
    x = self.range[0] + (self.range[1] - self.range[0]) * dec
    # Depois de decodificar o valor de x passa para a função
    if FLAG == 1:
      fx = x * math.sin (10.0 * math.pi * x) + 1.0
    elif FLAG == 2:
      fx = pow(x,2) - 3*x + 4
    self.score = fx
    
  # Cria novos filhos. Crossover de 2 Pontos
  def crossover (self, progenitores):
    return self._doispontos(progenitores)
  
  # Mutação do cromossomo
  def mutacao (self, gene):
    self._mutar(gene)
  
  #Inverte o alelo do gene para criar um novo individuo
  def _mutar (self, gene):
    self.cromossomo[gene] = int (not self.cromossomo[gene])
    
  #Cruzamento atraves de dois pontos de crossover
  def _doispontos (self, outro):
    esquerda, direita = self._pegarPivo()
    def progenitores (p0, p1):
      #Cria nova copia de p0
      cromossomo = p0.cromossomo[:]
      #Crossover
      cromossomo [esquerda:direita] = p1.cromossomo[esquerda:direita]
      filho = p0.__class__(cromossomo)
      filho.reparar (p0,p1)
      return filho
    return progenitores (self, outro), progenitores (outro, self)
  
  # Define onde vai ser o corte do crossover
  def _pegarPivo (self):
    esquerda = random.randrange (1, self.tamanho-2)
    direita = random.randrange (esquerda, self.tamanho-1)
    return esquerda, direita
  
  # Se necessario fixar duplicação
  def reparar (self, p0, p1):
    pass
  
  # Retorna a representação em forma de texto do objeto
  def __repr__ (self):
    dec = float ( int (GENETIC.join( map(str, self.cromossomo) ),2)) / float (pow(2,self.tamanho) - 1)
    x = self.range[0] + (self.range[1] - self.range[0]) * dec
    return '<Cromossomo do Indivíduo = "%s">\n <Função Aptidão = %s> # <Valor de X = %s>' % \
      (GENETIC.join(map(str,self.cromossomo)),self.score, x)
  
  # Compara aptidão de cada individuo
  def __cmp__ (self, outro):
    if self.optimizacao == MINIMIZE:
      return cmp (self.score, outro.score)
    else:
      return cmp (outro.score, self.score)
    
  # Criando replica
  def copiar (self):
    clone = self.__class__(self.cromossomo[:])
    clone.score = self.score
    return clone
  
  # Classe do ambiente populacional
  
class Ambiente (object):
  #Inicializa o ambiente com os parametros necessários
  #@param populacao: A população inicial de individuos
  #@param tamanho: Tamanho da população
  #@param maxgeracoes: O Máximo de gerações
  #@param taxa_crossover: A Taxa de crossover
  #@param taxa_mutacao: A Taxa de mutação
  #@param optimizacao: Tipo de optimização
  
  def __init__ (self, populacao = None, tamanho = 10, maxgeracoes = 100, taxa_crossover = 0.60, taxa_mutacao = 0.05, optimizacao = None):
    self.tamanho = tamanho
    self.optimizacao = optimizacao
    self.populacao = populacao or self._criaPopulacao()
    for individual in self.populacao:
      individual.aptidao (self.optimizacao)
      
    self.taxa_crossover = taxa_crossover
    self.taxa_mutacao = taxa_mutacao
    self.maxgeracoes = maxgeracoes
    self.geracao = 0
    self.imprime()
  
  # Cria população inicial
  def _criaPopulacao(self):
    return [Individuo() for individuo in xrange (self.tamanho)]
    
  def iniciar (self):
    while not self._solucao():
      self.gera()
  
  # Condições de parada do AG
  def _solucao (self):
    return (self.geracao > self.maxgeracoes) or (self.melhor.score == self.optimizacao)
  
  def gera (self):
    # Ordena os individuos baseado na sua aptidao
    self.populacao.sort()
    self._crossover()
    self.geracao += 1
    self.imprime()
    
  def _selecionar (self):
    return self._torneio()
  
  # Seleção por torneio
  def _torneio (self):
    competidores = []
    total_score = sum ([math.ceil(self.populacao[i].score) for i in xrange (self.tamanho)])
    for indice in xrange(self.tamanho):
      temp = [indice] * int((math.ceil(self.populacao[indice].score / total_score) * 100))
      competidores.extend (temp)
    return self.populacao[random.choice(competidores)]
  
  def _crossover (self):
    # Processo de Elitismo
    proxima_populacao = [self.melhor.copiar()]
    while len (proxima_populacao) < self.tamanho:
      progenitor1 = self._selecionar()
      if random.random() < self.taxa_crossover:
	progenitor2 = self._selecionar()
	descendente = progenitor1.crossover(progenitor2)
      else:
	#Faz uma copia do individuo
	descendente = [progenitor1.copiar()]
      for individuo in descendente:
	self._mutacao (individuo)
	individuo.aptidao (self.optimizacao)
	proxima_populacao.append (individuo)
    self.populacao = proxima_populacao[:self.tamanho]
    
  def _mutacao (self, individuo):
    for gene in xrange (individuo.tamanho):
      if random.random() < self.taxa_mutacao:
	individuo.mutacao(gene)
	
  def melhor():
    def fget(self):
      return self.populacao[0]
    return locals()
  melhor = property (**melhor())
  
  def imprime (self):
    print "-=-"*20
    print "Geração: " , self.geracao
    print "Melhor:  " , self.melhor
    
def menu ():
  global FLAG
  if FLAG == 1:
    sel = int (raw_input ('Deseja alterar parâmetros padrões? \nResponda: \n1) Sim \n0) Não\n'))
    if sel == 1:
      #Pegar aqui os parametros
      tam = int(raw_input ('População Inicial: '))
      maxgen = int(raw_input ('Número max de gerações: '))
      taxcross = float(raw_input ('Taxa de Crossover: (Ex: [0.50 = 50%] e [0.05 = 5%] ): '))
      taxmut = float(raw_input ('Taxa de Mutação: (Ex: [0.10 = 10%] e [0.01 = 1%] ): '))
      AG = Ambiente (tamanho=tam, maxgeracoes=maxgen-1, taxa_crossover=taxcross, taxa_mutacao=taxmut, optimizacao = 2.85026911722)
      AG.iniciar()
    elif sel == 0:
      AG = Ambiente (tamanho=10, maxgeracoes=29, taxa_crossover=0.60, taxa_mutacao=0.05, optimizacao = 2.85026911722)
      AG.iniciar()
    else:
      print "Opção Inválida!"
  elif FLAG == 2:
    sel = int (raw_input ('Deseja alterar parâmetros padrões?  \nResponda: \n1) Sim \n0) Não\n'))
    if sel == 1:
      #Pegar aqui os parametros
      tam = int(raw_input ('População Inicial: '))
      maxgen = int(raw_input ('Número max de gerações: '))
      taxcross = float(raw_input ('Taxa de Crossover: (Ex: [0.50 = 50%] e [0.05 = 5%] ): '))
      taxmut = float(raw_input ('Taxa de Mutação: (Ex: [0.10 = 10%] e [0.01 = 1%] ): '))
      AG = Ambiente (tamanho=tam, maxgeracoes=maxgen-1, taxa_crossover=taxcross, taxa_mutacao=taxmut, optimizacao = 1.75000000000)
      AG.iniciar()
    elif sel == 0:
      AG = Ambiente (tamanho=4, maxgeracoes=4, taxa_crossover=0.60, taxa_mutacao=0.01, optimizacao = 1.75000000000)
      AG.iniciar()
    else:
      print "Opção Inválida!"
    
  else:
    print "Opção Inválida!"
    
    
"""
 FUNÇÃO PRINCIPAL
"""
if __name__ == "__main__":
  menu ()
  
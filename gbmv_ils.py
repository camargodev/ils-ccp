import random
import time
import math
import sys

MAX_TENTATIVAS = 100
MAX_ITERACOES = 10000
INFERIOR = 0
SUPERIOR = 1
TAXA_PERTURBACAO = 0

class Grafo:

    def __init__(self):
        self.vertices = []
        self.arestas = dict()
        self.num_vertices = 0
        
    def adiciona_vertice(self, vertice):
        self.vertices.append(vertice)
        self.num_vertices += 1
        
    def adiciona_aresta(self, vert_origem, vert_destino, peso_aresta):
        self.arestas[vert_origem, vert_destino] = peso_aresta

    def valor_aresta(self, v_origem, v_destino):
        return self.arestas[v_origem, v_destino]

    def valor_vertice(self, indice):
        return int(self.vertices[indice])
        
    def get_num_vertices(self):
        return int(self.num_vertices)
        
    def get_arestas(self):
        return self.arestas
    
    def get_vertices(self):
        return self.vertices

class Grupo:

    def __init__(self, inferior, superior):
        self.limites = [inferior, superior]
        self.vertices = []
        self.valor_total_arestas = 0
        self.valor_total_vertices = 0
        
    def adiciona_vertice(self, vertice, arestas, valor_grupo):
        for vert in self.vertices:
            vert_min = min(vert, vertice)
            vert_max = max(vert, vertice)
            if (vert_min, vert_max) in arestas:
                self.valor_total_arestas += arestas[vert_min, vert_max]
        self.valor_total_vertices = valor_grupo
        self.vertices.append(vertice)
    
    def remove_vertice(self, vertice, arestas, vertices):
        for vert in self.vertices:
            vert_min = min(vert, vertice)
            vert_max = max(vert, vertice)
            if (vert_min, vert_max) in arestas:
                self.valor_total_arestas -= arestas[vert_min, vert_max]
        self.valor_total_vertices -= vertices[vertice]
        self.vertices.remove(vertice)
        
    def get_valor_arestas(self):
        return self.valor_total_arestas
        
    def get_valor_vertices(self):
        return self.valor_total_vertices
        
    def get_vertices(self):
        return self.vertices
    
    def get_limites(self):
        return self.limites

def criterio_de_parada(n):
    return n <= MAX_ITERACOES 
    
# def busca_completa(grupos, vertices, arestas):
    # grupos_solucao = copia_grupos(grupos, vertices, arestas)
    # for origem in grupos_solucao:
        # for vertice in origem.get_vertices():
            # for destino in grupos_solucao        
   
def nova_busca_local(grupos, vertices_arestas):
    
    
def busca_local(grupos, vertices, arestas):
    inicio_processo = time.time()
    grupos_vizinhos = [None]*len(vertices)
    pontuacao_maxima = calcula_pontuacao(grupos)
    indice_melhor_vizinho = -1
    estagnado = False
    while not estagnado:
        melhora = False
        for i in range(len(vertices)):
            grupos_vizinhos[i] = gera_nova_solucao(grupos, vertices, arestas)
            pontuacao_vizinho = calcula_pontuacao(grupos_vizinhos[i])
            if pontuacao_vizinho > pontuacao_maxima:
                melhora = True
                pontuacao_maxima = pontuacao_vizinho
                indice_melhor_vizinho = i
        estagnado = not melhora
    #print("BUSCA LOCAL DEMOROU: " + str(time.time() - inicio_processo))
    return grupos if indice_melhor_vizinho < 0 else grupos_vizinhos[indice_melhor_vizinho]

def gera_nova_solucao(grupos, vertices, arestas):
    inicio_processo = time.time()
    num_grupos = len(grupos)
    num_vertices = len(vertices)
    grupos_solucao = copia_grupos(grupos, vertices, arestas)
    solucao_valida = False
    while not solucao_valida:
        grupo_antigo_index = random.randint(0,num_grupos-1)
        grupo_antigo = grupos_solucao[grupo_antigo_index]
        vertices_grupo_antigo = grupo_antigo.get_vertices()
        vertice_random = random.randint(0,len(vertices_grupo_antigo)-1)
        vertice_random = vertices_grupo_antigo[vertice_random]
        grupo_novo_index = random.randint(0,num_grupos-1)
        while grupo_novo_index == grupo_antigo_index:
            grupo_novo_index = random.randint(0,num_grupos-1)
        grupo_novo = grupos_solucao[grupo_novo_index]
        if len(vertices_grupo_antigo) == 1:
            break
        valor_novo_grupo = grupo_novo.get_valor_vertices() + vertices[vertice_random]
        valor_antigo_grupo = grupo_antigo.get_valor_vertices() - vertices[vertice_random]
        if valor_antigo_grupo >= grupo_antigo.get_limites()[INFERIOR]:
            if valor_novo_grupo <= grupo_novo.get_limites()[SUPERIOR]:
                grupo_antigo.remove_vertice(vertice_random, arestas, vertices)
                grupo_novo.adiciona_vertice(vertice_random, arestas, valor_novo_grupo)
                grupos_solucao[grupo_antigo_index] = grupo_antigo
                grupos_solucao[grupo_novo_index] = grupo_novo
                solucao_valida = True
    #print("GERA NOVA DEMOROU: " + str(time.time() - inicio_processo))
    return grupos_solucao
        
def perturbacao(grupos, vertices, arestas):
    num_grupos = len(grupos)
    num_vertices = len(vertices)
    for i in range(math.floor(TAXA_PERTURBACAO*num_vertices)):
        grupos = gera_nova_solucao(grupos, vertices, arestas)             
    return grupos
    
def calcula_pontuacao(grupos):
    pontuacao = 0
    for grupo in grupos:
        pontuacao += grupo.get_valor_arestas()
    return pontuacao
    
def grupos_randomicos(vertices, grupos, arestas):
    num_grupos = len(grupos)
    num_vertices = len(vertices)
    grupos_validos = False
    tentativas = 0
    while not grupos_validos:
        tentativas += 1
        contador = 0
        grupos_auxiliar = copia_grupos(grupos, vertices, arestas)
        vertices_usados = []
        vertices_tentados = []
        valores_grupos = [0]*num_grupos
        distribuicao_valida = True
        complete = False
        for i in range(0, num_grupos):
            valor_grupo = 0
            while valor_grupo < grupos_auxiliar[i].get_limites()[INFERIOR]:
                vertice_random = random.randint(0,num_vertices-1)
                while vertice_random in vertices_tentados:
                    vertice_random = random.randint(0,num_vertices-1)
                valor_grupo += vertices[vertice_random]
                if valor_grupo <= grupos_auxiliar[i].get_limites()[SUPERIOR]:
                    grupos_auxiliar[i].adiciona_vertice(vertice_random, arestas, valor_grupo)
                    vertices_usados.append(vertice_random)
                    contador += 1
                else:
                    valor_grupo -= vertices[vertice_random]
                vertices_tentados.append(vertice_random)
                if len(vertices_tentados) == len(vertices) and len(vertices_usados) != len(vertices):
                    distribuicao_valida = False
                    break
                if len(vertices_usados) == len(vertices):
                    complete = True
            valores_grupos[i] = valor_grupo
            if not distribuicao_valida:
                break
        if distribuicao_valida and not complete:
            while len(vertices_usados) < num_vertices:
                grupo_random = random.randint(0, num_grupos-1)
                while not valores_grupos[grupo_random] < grupos_auxiliar[grupo_random].get_limites()[SUPERIOR]:
                    grupo_random = random.randint(0, num_grupos-1)
                vertice_random = random.randint(0,num_vertices-1)
                while vertice_random in vertices_tentados:
                    vertice_random = random.randint(0,num_vertices-1)
                novo_valor_grupo = valores_grupos[grupo_random] + vertices[vertice_random]
                if novo_valor_grupo <= grupos_auxiliar[grupo_random].get_limites()[SUPERIOR]:
                    grupos_auxiliar[grupo_random].adiciona_vertice(vertice_random, arestas, novo_valor_grupo)
                    vertices_usados.append(vertice_random)
                    valores_grupos[grupo_random] += vertices[vertice_random]
                    contador += 1
                vertices_tentados.append(vertice_random)
                if len(vertices_tentados) == len(vertices) and len(vertices_usados) != len(vertices):
                    distribuicao_valida = False
                    break
        grupos_validos = distribuicao_valida
        if tentativas == MAX_TENTATIVAS:
            exit("Arquivo inicial inválido")
    return grupos_auxiliar

def formata_linha(linha):
    return linha.replace(' \n','')
   
def processa_arquivo(arq_name):
    grafo = Grafo()
    with open(arq_name) as arq:
        linhas = arq.readlines()
    
    num_vertices, num_grupos = formata_linha(linhas[0]).split(' ')
    num_vertices, num_grupos = int(num_vertices), int(num_grupos)
    
    limites = formata_linha(linhas[1]).split(' ')
    grupos = []
    for i in range(num_grupos):
        grupos.append(Grupo(int(limites[2*i]), int(limites[2*i+1])))
    
    vertices = formata_linha(linhas[2]).split(' ')
    for vertice in vertices:
        if vertice.replace(' ','') != '':
            grafo.adiciona_vertice(int(vertice))
            
    for i in range(3, len(linhas)):
        linha = linhas[i]
        origem, destino, peso = formata_linha(linha).split(' ')
        grafo.adiciona_aresta(int(origem), int(destino), float(peso))
    
    return num_vertices, num_grupos, grupos, grafo
    
def mostra_grupo(grupo):
    print("Limites grupo: " + str(grupo.get_limites()))
    print("Valor vertices grupo: " + str(grupo.get_valor_vertices()))
    print("Vertices: " + str(grupo.get_vertices()))
    print("Valor arestas grupo: " + str(grupo.get_valor_arestas()) + str('\n'))
    
def copia_grupo(grupo, vertices, arestas):
    valor_grupo = 0
    limites = grupo.get_limites()[:]
    vertices_grupo = grupo.get_vertices()[:]
    novo_grupo = Grupo(limites[INFERIOR], limites[SUPERIOR])
    for vertice in vertices_grupo:
        valor_grupo += vertices[vertice]
        novo_grupo.adiciona_vertice(vertice, arestas, valor_grupo)
    return novo_grupo
    
def copia_grupos(grupos, vertices, arestas):
    num_grupos = len(grupos)
    novos_grupos = []
    for i in range(num_grupos):
        novo_grupo = copia_grupo(grupos[i], vertices, arestas)
        novos_grupos.append(novo_grupo)
    return novos_grupos
    
def ILS(grupos, vertices, arestas):
    n = 0
    n_total = 0
    grupos = busca_local(grupos, vertices, arestas)
    avaliacao_atual = calcula_pontuacao(grupos)
    while(criterio_de_parada(n)):
        n_total += 1
        novos_grupos = copia_grupos(grupos, vertices, arestas)
        novos_grupos = perturbacao(novos_grupos, vertices, arestas)
        novos_grupos = busca_local(novos_grupos, vertices, arestas)
        avaliacao_nova = calcula_pontuacao(novos_grupos)
        if avaliacao_nova > avaliacao_atual:
            avaliacao_atual = avaliacao_nova
            grupos = copia_grupos(novos_grupos, vertices, arestas)
            print('Iteracao ' + str(n_total) + ': ' + str(avaliacao_atual) + ' [estagnado há ' + str(n) + ' its.]')
            #print('TEMPO: ' + str(time.time() - inicio))
            n = 0
        else:
            n = n + 1   
    return grupos

def escreve_csv(arquivo, linha):
    with open(arquivo, 'w', newline='') as writeFile:
        writer = csv.writer(writeFile, delimiter=' ', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.write(linha)
    
def formata_resultado(grupos):
    string_grupos = '['
    for grupo in grupos:
        string_grupos += str(grupo.get_vertices()) + ','
    string_grupos += ']'
    string_grupos = string_grupos.replace(',]',']')
    return string_grupos
    
def gbmv_com_isl(instancia):
    num_vertices, num_grupos, grupos, grafo = processa_arquivo(instancia)
    grupos = grupos_randomicos(grafo.get_vertices(), grupos, grafo.get_arestas())
    for grupo in grupos:
        mostra_grupo(grupo)
    print("\nValor inicial: " + str(calcula_pontuacao(grupos)))
    grupos = ILS(grupos, grafo.get_vertices(), grafo.get_arestas())
    print(formata_resultado(grupos))
    print("\nValor final: " + str(calcula_pontuacao(grupos)))
   

inicio = time.time()
SEMENTE = int(inicio)
random.seed(SEMENTE)
TAXA_PERTURBACAO = float(sys.argv[2])
gbmv_com_isl(sys.argv[1])
print("SEMENTE: " + str(SEMENTE))
tempo_total = time.time() - inicio
print("TEMPO TOTAL: " + str(tempo_total))
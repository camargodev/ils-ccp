import random
import math
import sys
import time

PARADA = 10000
TAXA_PERTURBACAO = 0
MAX_TENTATIVAS = 10000
TEMPO_MAX = 10*60

num_vertices = 0
num_grupos = 0
vertices = []
arestas = dict()
inferiores = []
superiores = []

def formata_linha(linha):
    return linha.replace(' \n','')
   
def processa_arquivo(arq_name):
    
    with open(arq_name) as arq:
        linhas = arq.readlines()
    
    num_vertices, num_grupos = formata_linha(linhas[0]).split(' ')
    num_vertices, num_grupos = int(num_vertices), int(num_grupos)
    
    arestas = dict()
    vertices = [0 for x in range(num_vertices)]
    inferiores = [0 for x in range(num_grupos)]
    superiores = [0 for x in range(num_grupos)]
    
    limites = formata_linha(linhas[1]).split(' ')
    vertices_lidos = formata_linha(linhas[2]).split(' ')
    
    for i in range(num_grupos):
        inferiores[i] = int(limites[2*i])
        superiores[i] = int(limites[2*i+1])
    
    for i in range(num_vertices):
        if vertices_lidos[i].replace(' ','') != '':
            vertices[i] = int(vertices_lidos[i])
            
    for i in range(3, len(linhas)):
        linha = linhas[i]
        origem, destino, peso = formata_linha(linha).split(' ')
        origem, destino, peso = int(origem), int(destino), float(peso)
        arestas[origem, destino] = peso
     
    return num_vertices, num_grupos, vertices, arestas, inferiores, superiores
    
def distruibuicao_inicial():
    valido = False
    tentativas = 0
    while not valido:
        tentativas += 1
        grupos = [-1 for x in range(num_vertices)]
        valores = [-1 for x in range(num_grupos)]
        vertices_tentados = []
        vertices_usados = []
        distribuicao_invalida = False
        for grupo in range(num_grupos):
            valor_grupo = 0
            while valor_grupo < inferiores[grupo] and not distribuicao_invalida:
                vertice = random.randint(0, num_vertices-1)
                while vertice in vertices_tentados:
                    vertice = random.randint(0, num_vertices-1)
                if valor_grupo + vertices[vertice] <= superiores[grupo]:
                    valor_grupo += vertices[vertice]
                    vertices_usados.append(vertice)
                    grupos[vertice] = grupo
                    valores[grupo] = valor_grupo
                vertices_tentados.append(vertice)
                if len(vertices_tentados) == num_vertices and len(vertices_usados) != num_vertices:
                    distribuicao_invalida = True
        if not distribuicao_invalida:
            while len(vertices_tentados) < num_vertices:
                grupo = random.randint(0, num_grupos-1)
                while valores[grupo] == superiores[grupo]:
                    grupo = random.randint(0, num_grupos-1)
                vertice = random.randint(0, num_vertices-1)
                while vertice in vertices_tentados:
                    vertice = random.randint(0, num_vertices-1)
                if valores[grupo] + vertices[vertice] <= superiores[grupo]:
                    grupos[vertice] = grupo
                    valores[grupo] += vertices[vertice]
                    vertices_usados.append(vertice)
                vertices_tentados.append(vertice)
        if len(vertices_usados) == num_vertices:
            valido = True
        elif tentativas == MAX_TENTATIVAS:
            exit("Arquivo inicial inválido")
    return grupos, valores, calculo_arestas_iniciais(grupos)
    
def calculo_arestas_iniciais(grupos):
    pontuacoes = [0 for x in range(num_grupos)]
    for origem in range(num_vertices):
        for destino in range(origem+1, num_vertices):
            if grupos[origem] == grupos[destino]:
                pontuacoes[grupos[origem]] += arestas[(origem, destino)]
    return pontuacoes

def avaliacao(pontuacoes):
    pontuacao_total = 0
    for grupo in range(num_grupos):
        pontuacao_total += pontuacoes[grupo]
    return pontuacao_total

def move_vertice(grupos, vertice, destino, pontuacoes):
    origem = grupos[vertice]
    novo_valor_origem = pontuacoes[origem]
    novo_valor_destino = pontuacoes[destino]
    for v in range(0, vertice):
        aresta = arestas[v, vertice]
        if grupos[v] == origem:              
            novo_valor_origem -= aresta
        elif grupos[v] == destino:
            novo_valor_destino += aresta
    for v in range(vertice + 1, num_vertices):
        aresta = arestas[vertice, v]
        if grupos[v] == origem:              
            novo_valor_origem -= aresta
        elif grupos[v] == destino:
            novo_valor_destino += aresta
    return novo_valor_origem, novo_valor_destino
    
def perturbacao(grupos, valores, pontuacoes):
    num_perturbacoes = math.floor(float(TAXA_PERTURBACAO*num_vertices))
    novos_grupos = []
    novos_valores = []
    novas_pontuacoes = []
    for v in range(0, num_grupos):
        novos_grupos.append(grupos[v])
        novos_valores.append(valores[v])
        novas_pontuacoes.append(pontuacoes[v])
    for v in range(num_grupos, num_vertices):
        novos_grupos.append(grupos[v])
    for i in range(num_perturbacoes):
        vertice = random.randint(0, num_vertices-1)
        origem = novos_grupos[vertice] 
        destino = random.randint(0, num_grupos-1)       
        if destino == origem:
           break
        if not novos_valores[origem] - vertices[vertice] < inferiores[origem]:
            if not novos_valores[destino] + vertices[vertice] > superiores[destino]:
                pont_origem, pont_destino = move_vertice(novos_grupos, vertice, destino, novas_pontuacoes)
                novos_valores[origem] -= vertices[vertice]
                novos_valores[destino] += vertices[vertice]
                novos_grupos[vertice] = destino
                novas_pontuacoes[origem] = pont_origem
                novas_pontuacoes[destino] = pont_destino
                perturbacao_ok = True
    return novos_grupos, novos_valores, novas_pontuacoes
 
def busca_local_aleatoria(grupos_otimos, valores_otimos, pontuacoes_otimas, otimo):
    estagnado = 0
    while estagnado < 150:
        vertice = random.randint(0, num_vertices-1)
        origem = grupos_otimos[vertice]
        if not valores_otimos[origem] - vertices[vertice] < inferiores[origem]:
            destino = random.randint(0, num_grupos-1)
            if not valores_otimos[destino] + vertices[vertice] > superiores[destino]:
                pont_origem, pont_destino = move_vertice(grupos_otimos, vertice, destino, pontuacoes_otimas)
                pontuacao_total = otimo - pontuacoes_otimas[origem] + pont_origem - pontuacoes_otimas[destino] + pont_destino
                if pontuacao_total > otimo:
                    otimo = pontuacao_total
                    grupos_otimos[vertice] = destino
                    valores_otimos[origem] -= vertices[vertice]
                    valores_otimos[destino] += vertices[vertice]
                    pontuacoes_otimas[origem] = pont_origem
                    pontuacoes_otimas[destino] = pont_destino
                else:
                    estagnado += 1
    return grupos_otimos, valores_otimos, pontuacoes_otimas, otimo
    
def busca_local_completa(grupos, novos_valores, pontuacoes, otimo):
    estagnado = True
    for vertice in range(num_vertices):
        origem = grupos[vertice]
        novo_valor_origem = novos_valores[origem] - vertices[vertice]
        if not novo_valor_origem < inferiores[origem]:                
            for destino in range(0, origem):
                novo_valor_destino = novos_valores[destino] + vertices[vertice]
                if not novo_valor_destino > superiores[destino]:
                    pont_origem, pont_destino = move_vertice(grupos, vertice, destino, pontuacoes)
                    nova_pontuacao = otimo - pontuacoes[origem] + pont_origem - pontuacoes[destino]  + pont_destino
                    if nova_pontuacao > otimo:
                        grupos[vertice] = destino
                        novos_valores[origem] = novo_valor_origem
                        novos_valores[destino] = novo_valor_destino
                        pontuacoes[origem] = pont_origem
                        pontuacoes[destino] = pont_destino
                        return not estagnado, grupos, novos_valores, pontuacoes, nova_pontuacao
            for destino in range(origem+1, num_grupos):
                novo_valor_destino = novos_valores[destino] + vertices[vertice]
                if not novo_valor_destino > superiores[destino]:
                    pont_origem, pont_destino = move_vertice(grupos, vertice, destino, pontuacoes)
                    nova_pontuacao = otimo - pontuacoes[origem] + pont_origem - pontuacoes[destino]  + pont_destino
                    if nova_pontuacao > otimo:
                        grupos[vertice] = destino
                        novos_valores[origem] = novo_valor_origem
                        novos_valores[destino] = novo_valor_destino
                        pontuacoes[origem] = pont_origem
                        pontuacoes[destino] = pont_destino
                        return not estagnado, grupos, novos_valores, pontuacoes, nova_pontuacao
    final_completa = time.time()
    return estagnado, grupos, novos_valores, pontuacoes, otimo

def busca_local_mista(grupos, valores, pontuacoes, pontuacao_otima):
    estagnado = False
    while not estagnado:
        grupos, valores, pontuacoes, pontuacao_otima = busca_local_aleatoria(grupos, valores, pontuacoes, pontuacao_otima)
        estagnado, grupos, valores, pontuacoes, pontuacao_otima = busca_local_completa(grupos, valores, pontuacoes, pontuacao_otima)
    return grupos, valores, pontuacoes, pontuacao_otima
    
def configura_experimento(semente, taxa_perturbacao):
    global TAXA_PERTURBACAO
    random.seed(semente)
    TAXA_PERTURBACAO = float(taxa_perturbacao)
    
def ILS(arquivo, taxa_perturbacao, semente):
    global num_vertices, num_grupos, vertices, arestas, inferiores, superiores
    configura_experimento(semente, taxa_perturbacao)
    num_vertices, num_grupos, vertices, arestas, inferiores, superiores = processa_arquivo(arquivo)
    grupos, valores, pontuacoes = distruibuicao_inicial()
    pontuacao_otima = avaliacao(pontuacoes)
    print("PONTUAÇÃO INICIAL: " + str(pontuacao_otima))
    grupos_otimos, valores_otimos, pontuacoes_otimas, pontuacao_otima = busca_local_mista(grupos, valores, pontuacoes, pontuacao_otima)
    iteracoes_sem_melhorar = 0
    while iteracoes_sem_melhorar < PARADA:
        if (time.time() - inicio) >= TEMPO_MAX:
            break
        iteracoes_sem_melhorar += 1
        novos_grupos, novos_valores, novas_pontuacoes = perturbacao(grupos_otimos, valores_otimos, pontuacoes_otimas)
        novos_grupos, novos_valores, novas_pontuacoes, nova_pontuacao = busca_local_mista(novos_grupos, novos_valores, novas_pontuacoes, avaliacao(novas_pontuacoes))
        if nova_pontuacao > pontuacao_otima:
            #print("Nova pontuacao: " + str(nova_pontuacao))
            iteracoes_sem_melhorar = 0
            pontuacao_otima = nova_pontuacao
            grupos_otimos, valores_otimos, pontuacoes_otimas = novos_grupos, novos_valores, novas_pontuacoes
    return grupos_otimos, valores_otimos, pontuacoes_otimas
    
def main():
    grupos_otimos, valores_otimos, pontuacoes_otimas = ILS(sys.argv[1], sys.argv[2], sys.argv[3])
    print(grupos_otimos)
    print(avaliacao(pontuacoes_otimas))
    print("Semente: " + str(sys.argv[3]))
    final = time.time()
    print("Tempo total: " + str(final - inicio))
    
inicio = time.time()
main()
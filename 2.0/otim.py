import random
import math
import sys
import time

SEMENTE = 0
PARADA = 10000
TAXA_PERTURBACAO = 0
MAX_TENTATIVAS = 10000
TEMPO_MAX = 1*60*60

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
    novas_pontuacoes = copia_pontuacoes(pontuacoes)
    for v in range(num_vertices):
        if v != vertice:
            aresta = arestas[(min(v, vertice), max(v, vertice))]
            if grupos[v] == origem:              
                novas_pontuacoes[origem] -= aresta
            elif grupos[v] == destino:
                novas_pontuacoes[destino] += aresta
    return novas_pontuacoes

def copia_grupos(grupos):
    novos_grupos = []
    for grupo in grupos:
        novos_grupos.append(grupo)
    return novos_grupos

def copia_pontuacoes(pontuacoes):
    novas_pontuacoes = []
    for pontuacao in pontuacoes:
        novas_pontuacoes.append(pontuacao)
    return novas_pontuacoes

def copia_valores(valores):
    novos_valores = []
    for valor in valores:
        novos_valores.append(valor)
    return novos_valores
    
def perturbacao(grupos, valores, pontuacoes):
    novos_grupos = copia_grupos(grupos)
    num_perturbacoes = math.floor(float(TAXA_PERTURBACAO*num_vertices))
    novos_valores = copia_valores(valores)
    novas_pontuacoes = copia_pontuacoes(pontuacoes)
    for i in range(num_perturbacoes):
        perturbacao_ok = False
        destinos_tentados = []
        vertices_tentados = []
        while not perturbacao_ok:
            if len(vertices_tentados) == num_vertices:
                break
            if len(destinos_tentados) == num_grupos:
                break
            vertice = random.randint(0, num_vertices-1)
            if vertice not in vertices_tentados:
                vertices_tentados.append(vertice)
            origem = novos_grupos[vertice] 
            if not novos_valores[origem] - vertices[vertice] < inferiores[origem]:
                destino = random.randint(0, num_grupos-1)
                if destino not in destinos_tentados:
                    destinos_tentados.append(destino)
                while destino == origem:
                    destino = random.randint(0, num_grupos-1)
                    if destino not in destinos_tentados:
                        destinos_tentados.append(destino)
                if not novos_valores[destino] + vertices[vertice] > superiores[destino]:
                    novas_pontuacoes = move_vertice(novos_grupos, vertice, destino, novas_pontuacoes)
                    novos_valores[origem] -= vertices[vertice]
                    novos_valores[destino] += vertices[vertice]
                    novos_grupos[vertice] = destino
                    perturbacao_ok = True
    return novos_grupos, novos_valores, novas_pontuacoes
 
def busca_local_aleatoria(grupos, valores, pontuacoes):
    inicio_aleatoria = time.time()
    #print("\n\nRANDOM")
    #print("Começa com: " + str(grupos))
    iteracoes_sem_melhorar = 0
    otimo = avaliacao(pontuacoes)
    grupos_otimos = copia_grupos(grupos)
    valores_otimos = copia_valores(valores)
    pontuacoes_otimas = copia_pontuacoes(pontuacoes)
    while iteracoes_sem_melhorar < 1:
        iteracoes_sem_melhorar += 1
        for i in range(num_vertices):
            #print("\n  Tentativa: " + str(i))
            erro_origem = False
            erro_destino = False
            vertices_tentados = []
            destinos_tentados = []
            vertice = random.randint(0, num_vertices-1)
            origem = grupos_otimos[vertice]
            while valores_otimos[origem] - vertices[vertice] < inferiores[origem]:
                if len(vertices_tentados) == num_vertices:
                    erro_origem = True
                    break
                vertice = random.randint(0, num_vertices-1)
                origem = grupos_otimos[vertice]
                if vertice not in vertices_tentados:
                    vertices_tentados.append(vertice)
            #print("  Vertice: " + str(vertice))
            #print("  Origem:  " + str(origem))
            if not erro_origem:
                #print("  Origem VALIDA")
                destino = random.randint(0, num_grupos-1)
                while valores_otimos[destino] + vertices[vertice] > superiores[destino]:
                    if len(destinos_tentados) == num_grupos:
                        erro_destino = True
                        break
                    destino = random.randint(0, num_grupos-1)
                    if destino not in destinos_tentados:
                        destinos_tentados.append(destino)
                if not erro_destino and origem != destino:
                    #print("  Foi encontrado destino valido: " + str(destino))
                    novas_pontuacoes = move_vertice(grupos_otimos, vertice, destino, pontuacoes_otimas)
                    pontuacao_total = avaliacao(novas_pontuacoes)
                    if pontuacao_total > otimo:
                        iteracoes_sem_melhorar = 0
                        otimo = pontuacao_total
                        grupos_otimos[vertice] = destino
                        valores_otimos[origem] -= vertices[vertice]
                        valores_otimos[destino] += vertices[vertice]
                        pontuacoes_otimas = copia_pontuacoes(novas_pontuacoes)
                #else:
                    #print("  Nao ha destino valido")
    final_aleatoria = time.time()
    #print("DURAÇÃO ALEATORIA: " + str(final_aleatoria - inicio_aleatoria))
    return grupos_otimos, valores_otimos, pontuacoes_otimas, otimo
    
def busca_local_completa(grupos, valores, pontuacoes):
    inicio_completa = time.time()
    estagnado = True
    otimo = avaliacao(pontuacoes)
    novos_valores = copia_valores(valores)
    for vertice in range(num_vertices):
        origem = grupos[vertice]
        novo_valor_origem = valores[origem] - vertices[vertice]
        if not novo_valor_origem < inferiores[origem]:                
            for destino in range(num_grupos):
                novos_grupos = copia_grupos(grupos)
                if destino != origem:
                    novo_valor_destino = valores[destino] + vertices[vertice]
                    if not novo_valor_destino > superiores[destino]:
                        novos_grupos[vertice] = destino
                        novas_pontuacoes = move_vertice(grupos, vertice, destino, pontuacoes)
                        nova_pontuacao = avaliacao(novas_pontuacoes)
                        if nova_pontuacao > otimo:
                            novos_valores[origem] = novo_valor_origem
                            novos_valores[destino] = novo_valor_destino
                            return not estagnado, novos_grupos, novos_valores, novas_pontuacoes, nova_pontuacao
    final_completa = time.time()
    #print("DURAÇÃO COMPLETA: " + str(final_completa - inicio_completa))
    return estagnado, grupos, valores, pontuacoes, otimo

def busca_local_mista(grupos, valores, pontuacoes):
    #print("BUSCA LOCAL: " + str(grupos))
    estagnado = False
    grupos_otimos = copia_grupos(grupos)
    valores_otimos = copia_valores(valores)
    pontuacoes_otimas = copia_pontuacoes(pontuacoes)
    while not estagnado:
        #grupos_otimos, valores_otimos, pontuacoes_otimas, pontuacao_total = busca_local_aleatoria(grupos_otimos, valores_otimos, pontuacoes_otimas)
        #print("ALEATORIA: " + str(pontuacao_total) + " [" + str(grupos_otimos) + "]")
        estagnado, grupos_otimos, valores_otimos, pontuacoes_otimas, pontuacao_total = busca_local_completa(grupos_otimos, valores_otimos, pontuacoes_otimas)
        #print("COMPLETA: " + str(pontuacao_total) + " [" + str(grupos_otimos) + "]")
        #print("ESTAGNADO: " + str(estagnado))
    return grupos_otimos, valores_otimos, pontuacoes_otimas, pontuacao_total
    
def printa_solucao(msg, grupos, valores, pontuacoes):
    print("\n--- " + str(msg) + " ---")
    print("\nGrupos: " + str(grupos))
    print("Valores: " + str(valores))
    print("Pontuacoes: " + str(pontuacoes))

def configura_experimento(semente, taxa_perturbacao):
    global SEMENTE, TAXA_PERTURBACAO
    #SEMENTE = int(time.time())
    SEMENTE = semente
    random.seed(SEMENTE)
    TAXA_PERTURBACAO = float(taxa_perturbacao)
    
def ILS(arquivo, taxa_perturbacao, semente):
    global num_vertices, num_grupos, vertices, arestas, inferiores, superiores
    configura_experimento(semente, taxa_perturbacao)
    num_vertices, num_grupos, vertices, arestas, inferiores, superiores = processa_arquivo(arquivo)
    grupos, valores, pontuacoes = distruibuicao_inicial()
    print("SOLUÇÃO INICIAL: " + str(grupos))
    print("PONTUAÇÃO INICIAL: " + str(avaliacao(pontuacoes)))
    grupos_otimos, valores_otimos, pontuacoes_otimas, pontuacao_otima = busca_local_mista(grupos, valores, pontuacoes)
    iteracoes_sem_melhorar = 0
    novos_grupos = copia_grupos(grupos_otimos)
    while iteracoes_sem_melhorar < PARADA:
        #if time.time() - inicio >= TEMPO_MAX:
        #    break
        iteracoes_sem_melhorar += 1
        #print("RODADA " + str(iteracoes_sem_melhorar))
        #print("    COMEÇA EM: " + str(novos_grupos))
        novos_grupos, novos_valores, novas_pontuacoes = perturbacao(grupos_otimos, valores_otimos, pontuacoes_otimas)
        #print("    PÓS PERTURBAÇÃO: " + str(novos_grupos))
        novos_grupos, novos_valores, novas_pontuacoes, nova_pontuacao = busca_local_mista(novos_grupos, novos_valores, novas_pontuacoes)
        if nova_pontuacao > pontuacao_otima:
            print("MELHOROU! Nova pontuacao: " + str(nova_pontuacao))
            iteracoes_sem_melhorar = 0
            pontuacao_otima = nova_pontuacao
            grupos_otimos, valores_otimos, pontuacoes_otimas = novos_grupos, novos_valores, novas_pontuacoes
    return grupos_otimos, valores_otimos, pontuacoes_otimas
    
def main():
    grupos_otimos, valores_otimos, pontuacoes_otimas = ILS(sys.argv[1], sys.argv[2], sys.argv[3])
    print(grupos_otimos)
    print(avaliacao(pontuacoes_otimas))
    print("Semente: " + str(SEMENTE))
    final = time.time()
    print("Tempo total: " + str(final - inicio))
    
inicio = time.time()
main()
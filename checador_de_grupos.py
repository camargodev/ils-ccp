GRUPOS = [[59, 54, 113, 30, 28, 197, 221, 155, 78, 219, 35],[176, 79, 68, 212, 72, 107, 48, 184, 53, 106, 200, 7, 203],[179, 15, 124, 100, 225, 71, 16, 147, 193, 201, 132, 231, 25, 42, 185, 173, 130, 18, 94, 153],[64, 157, 51, 210, 39, 131, 135, 49, 175, 41, 180, 202, 102, 95, 233, 126, 148, 82, 133, 91],[144, 229, 146, 88, 213, 0, 6, 4, 58, 44, 80, 97, 46, 235, 33, 8, 143],[186, 171, 81, 84, 38, 14, 63, 160, 1, 55, 2, 10, 172, 215, 142, 121, 23],[45, 166, 150, 115, 21, 223, 40, 120, 151, 199, 206, 103, 57, 3, 66],[26, 98, 129, 161, 9, 190, 32, 232, 99, 149, 76, 187, 65, 75, 19, 169, 92, 177, 11, 194, 101, 119, 174, 207, 123, 167, 152, 86, 89, 154, 73, 12, 110, 118, 198, 183, 128, 34, 36, 108, 182, 74, 181, 134, 56, 60, 145, 90, 117, 111, 236, 218, 136, 239, 5, 170, 116, 163, 159, 140, 162, 85, 112, 214, 24, 141, 22, 211, 224, 158],[67, 27, 105, 43, 77, 168, 227, 230, 122, 222, 31, 96, 204, 156, 195, 192, 104, 137],[208, 69, 164, 228, 237, 20, 189, 165, 125, 47],[37, 93, 50, 220, 238, 217, 234, 188, 61, 216, 209, 87, 62, 127, 83, 52],[139, 13, 205, 196, 226, 191, 17, 138, 29, 109, 70, 178, 114]]

def calcula_pontuacao_grupo(vertices_grupo, arestas):
    pontuacao = 0
    for v1 in vertices_grupo:
        for v2 in vertices_grupo:
            if v1 < v2:
                #pv = min(v1,v2)
                #sv = max(v1,v2)
                pontuacao += arestas[v1,v2]
    return pontuacao
    
def formata_linha(linha):
    return linha.replace(' \n','')
    
def processa_arestas(arq_name):
    with open(arq_name) as arq:
        linhas = arq.readlines()
    
    arestas = dict()
            
    for i in range(3, len(linhas)):
        linha = linhas[i]
        origem, destino, peso = formata_linha(linha).split(' ')
        arestas[int(origem), int(destino)] = float(peso)
    return arestas
   
def checa():   
    arestas = processa_arestas('GBMV/gbmv240_01.ins')
    pontuacao_total = 0
    for grupo in GRUPOS:
        #print(grupo)
        pontuacao_total += calcula_pontuacao_grupo(grupo, arestas)
    print(pontuacao_total)
  
checa()  
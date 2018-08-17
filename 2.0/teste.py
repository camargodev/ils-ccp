import random
import math
import sys

strTotal = ""
v = random.randint(5, 15)
g = random.randint(math.floor(float(v/4 + 1)), math.floor(float(v/2)))

inferiores = []
superiores = []
for i in range(g):
    inf = random.randint(1, 3)
    sup = random.randint(inf+2, 20)
    inferiores.append(inf)
    superiores.append(sup)
    
verts = []
for i in range(v):
    verts.append(random.randint(1, 5))
    
arestas = []

for i in range(v-1):
    for j in range(i+1, v):
        arestas.append(str(i) + " " + str(j) + " " + str(random.randint(3, 5)))
        
        
print(str(v) + " " + str(g))
strTotal += str(v) + " " + str(g) + "\n"

strlim = ""
for i in range(g):
    strlim += str(inferiores[i]) + " "
    strlim += str(superiores[i]) + " "
print(strlim)
strTotal += strlim + "\n"

strver = ""
for i in range(v):
    strver += str(verts[i]) + " "
print(strver)
strTotal += strver + "\n"
for a in arestas:
    print(a)
    strTotal += a + "\n"
    
text_file = open("gbmv" + sys.argv[1] + ".ins", "w")
text_file.write(strTotal)
text_file.close()
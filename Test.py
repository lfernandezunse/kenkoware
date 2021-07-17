
'''
Filtro comun de control
'''

import random

lista = []

for _ in range(0,1500):
    if _ == 224:
        print()
    x = random.randint(0,1000)
    lista.append(int(x))
    _ += 1

print(lista.sort())
m = max(lista)
f = random.random()

print('Maximo: %d' %m)
print("Factor de tolerancia: %.2f " %f)

def dualidad(my_list):
    '''
    No se si sirve esta funcion porque los items de las bases de datos son tuplas, no enteros
    :param my_list:
    :return:
    '''
    x = list(dict.fromkeys(my_list))
    return x

def _ET(max, ft):
    return int(max + (max*ft))

print("\nExtremo de tolerancia: %d" %(_ET(m,f)))
print("Cantidad original: %d" %(len(lista)))
print(f"\nDualidad: {dualidad(lista)}")

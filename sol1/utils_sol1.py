
# Promedio
def calcular_promedio(lista):
    return round(sum(lista) / len(lista), 2) if lista else 0

# Mediana
def calcular_mediana(lista):
    if not lista:
        return 0
    lista_ordenada = merge_sort(lista)
    n = len(lista_ordenada)
    medio = n // 2
    if n % 2 == 0:
        return (lista_ordenada[medio - 1] + lista_ordenada[medio]) / 2
    else:
        return lista_ordenada[medio]

# Moda
def calcular_moda(lista):
    if not lista:
        return None
    frecuencias = {}
    for num in lista:
        frecuencias[num] = frecuencias.get(num, 0) + 1
    max_frecuencia = max(frecuencias.values())
    modas = [k for k, v in frecuencias.items() if v == max_frecuencia]
    return modas[0] if len(modas) == 1 else None  # Solo si hay moda única

# Extremismo = cantidad de opiniones extremas (1 o 5)
def calcular_extremismo(lista):
    return lista.count(1) + lista.count(5)

# Consenso = número de veces que la mayoría dio la misma opinión
def calcular_consenso(lista):
    if not lista:
        return 0
    frecuencias = {}
    for val in lista:
        frecuencias[val] = frecuencias.get(val, 0) + 1
    max_frecuencia = max(frecuencias.values())
    return max_frecuencia

# Merge Sort (para mediana)
def merge_sort(lista):
    if len(lista) <= 1:
        return lista
    medio = len(lista) // 2
    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])
    return merge(izquierda, derecha)

def merge(izq, der):
    resultado = []
    i = j = 0
    while i < len(izq) and j < len(der):
        if izq[i] <= der[j]:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])
    return resultado

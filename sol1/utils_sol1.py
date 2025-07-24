from estructuras_sol1 import encuestado, Pregunta, Tema, ABBTemas



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


def cargar_datos_test(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as f:
        lineas = [linea.strip() for linea in f if linea.strip()]

    encuestados = {}
    temas_abb = ABBTemas()
    i = 0

    # Leer encuestados
    while i < len(lineas) and not lineas[i].startswith('{'):
        partes = lineas[i].split(',')
        id_enc = i + 1
        nombre = partes[0].strip()
        experticia = int(partes[1].split(':')[1].strip())
        opinion = int(partes[2].split(':')[1].strip())
        encuestados[id_enc] = encuestado(id_enc, nombre, experticia, opinion)
        i += 1

   # Leer bloques de preguntas: cada bloque tiene 2 líneas
    preguntas_bloque = []
    while i < len(lineas):
        if lineas[i].startswith('{'):
            preguntas_bloque.append(lineas[i])
        i += 1

# Validar múltiplos de 2
if len(preguntas_bloque) % 2 != 0:
    raise ValueError("Bloques de preguntas mal formateados.")


    tema_contador = 1
    pregunta_contador = 1
    for t in range(0, len(preguntas_bloque), 2):
        nombre_tema = f"Tema {tema_contador}"
        tema = Tema(nombre_tema)

        for p in range(2):
            if t + p >= len(preguntas_bloque):
                break
            raw = preguntas_bloque[t + p]
            ids_enc = list(map(int, raw.strip('{} ').split(',')))
            encs = [encuestados[id_] for id_ in ids_enc]
            opiniones = [e.opinion for e in encs]
            experticias = [e.experticia for e in encs]

            id_pregunta = f"Pregunta{tema_contador}.{pregunta_contador}"
            pregunta_contador += 1

            pregunta = Pregunta(id_pregunta)
            pregunta.encuestados = sorted(encs, key=lambda e: (-e.opinion, -e.experticia))
            pregunta.promedio_opinion = calcular_promedio(opiniones)
            pregunta.promedio_experticia = calcular_promedio(experticias)
            pregunta.mediana = calcular_mediana(opiniones)
            pregunta.moda = calcular_moda(opiniones)
            pregunta.extremismo = round(calcular_extremismo(opiniones) / len(opiniones), 2)
            pregunta.consenso = round(calcular_consenso(opiniones) / len(opiniones), 2)

            tema.root_preguntas.insertar(pregunta)
            tema.total_encuestados += len(encs)

        # Calcular promedios del tema
        preguntas = tema.root_preguntas.recorrer_inorden()
        if preguntas:
            tema.promedio_opinion = calcular_promedio([p.promedio_opinion for p in preguntas])
            tema.promedio_experticia = calcular_promedio([p.promedio_experticia for p in preguntas])

        temas_abb.insertar(tema)
        tema_contador += 1
        pregunta_contador = 1  # reset por tema

    return temas_abb, encuestados


def generar_salida(temas_abb, encuestados, archivo_salida="output_generado.txt"):
    temas_ordenados = temas_abb.recorrer_inorden()
    lineas = []

    lineas.append("Resultados de la encuesta:\n")

    for tema in temas_ordenados:
        lineas.append(f"[{tema.promedio_opinion:.2f}] {tema.nombre}:")
        preguntas_ordenadas = tema.root_preguntas.recorrer_inorden()
        for pregunta in preguntas_ordenadas:
            ids = [str(e.id) for e in pregunta.encuestados]
            ids_str = ", ".join(ids)
            lineas.append(f" [{pregunta.promedio_opinion:.2f}] {pregunta.id_pregunta}: ({ids_str})")
        lineas.append("")

    # Lista de encuestados
    lineas.append("Lista de encuestados:")
    encs = sorted(encuestados.values(), key=lambda e: e.id)
    for e in encs:
        lineas.append(f" ({e.id}, Nombre:'{e.nombre}', Experticia:{e.experticia}, Opinión:{e.opinion})")
    lineas.append("")

    # Analíticas finales
    lineas.append("Resultados:")

    # Recolectar todas las preguntas
    todas_preguntas = []
    for tema in temas_ordenados:
        todas_preguntas.extend(tema.root_preguntas.recorrer_inorden())

    # Por cada métrica, obtener la pregunta deseada
    def menor_valor(lista):
        return min(lista) if lista else None

    def mayor_valor(lista):
        return max(lista) if lista else None

    def seleccionar_pregunta(preguntas, key_func, reverse=False):
        mejor = None
        for p in preguntas:
            val = key_func(p)
            if mejor is None or (val > key_func(mejor) if reverse else val < key_func(mejor)) or (val == key_func(mejor) and p.id_pregunta < mejor.id_pregunta):
                mejor = p
        return mejor

    lineas.append(f"  Pregunta con mayor promedio de opinion: [{seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_opinion, True).promedio_opinion:.2f}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_opinion, True).id_pregunta}")
    lineas.append(f"  Pregunta con menor promedio de opinion: [{seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_opinion).promedio_opinion:.2f}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_opinion).id_pregunta}")

    lineas.append(f"  Pregunta con mayor promedio de experticia: [{seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_experticia, True).promedio_experticia:.2f}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_experticia, True).id_pregunta}")
    lineas.append(f"  Pregunta con menor promedio de experticia: [{seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_experticia).promedio_experticia:.2f}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.promedio_experticia).id_pregunta}")

    lineas.append(f"  Pregunta con Mayor mediana de opinion: [{seleccionar_pregunta(todas_preguntas, lambda p: p.mediana, True).mediana}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.mediana, True).id_pregunta}")
    lineas.append(f"  Pregunta con menor mediana de opinion: [{seleccionar_pregunta(todas_preguntas, lambda p: p.mediana).mediana}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.mediana).id_pregunta}")

    lineas.append(f"  Pregunta con mayor moda de opinion: [{seleccionar_pregunta(todas_preguntas, lambda p: p.moda if p.moda is not None else -1, True).moda}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.moda if p.moda is not None else -1, True).id_pregunta}")
    lineas.append(f"  Pregunta con menor moda de opinion: [{seleccionar_pregunta(todas_preguntas, lambda p: p.moda if p.moda is not None else 999).moda}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.moda if p.moda is not None else 999).id_pregunta}")

    lineas.append(f"  Pregunta con mayor extremismo: [{seleccionar_pregunta(todas_preguntas, lambda p: p.extremismo, True).extremismo:.2f}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.extremismo, True).id_pregunta}")
    lineas.append(f"  Pregunta con mayor consenso: [{seleccionar_pregunta(todas_preguntas, lambda p: p.consenso, True).consenso:.2f}] Pregunta: {seleccionar_pregunta(todas_preguntas, lambda p: p.consenso, True).id_pregunta}")

    # Mostrar por consola
    for linea in lineas:
        print(linea)

    # Escribir en archivo
    with open(archivo_salida, "w", encoding="utf-8") as f:
        for linea in lineas:
            f.write(linea + "\n")
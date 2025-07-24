import time
from sol1.utils_sol1 import cargar_datos_test, generar_salida as salida_sol1
from sol2.utils_sol2 import cargar_datos_test as cargar_sol2, generar_salida as salida_sol2

def medir_tiempo_solucion_1(archivo):
    inicio = time.time()
    temas, encs = cargar_datos_test(archivo)
    salida_sol1(temas, encs, "salida_sol1.txt", imprimir=False)
    fin = time.time()
    return round(fin - inicio, 4)

def medir_tiempo_solucion_2(archivo):
    inicio = time.time()
    temas, encs = cargar_sol2(archivo)
    salida_sol2(temas, encs, "salida_sol2.txt", imprimir=False)
    fin = time.time()
    return round(fin - inicio, 4)

archivos_prueba = ["Test1.txt", "Test2.txt", "Test3.txt", "Test4.txt", "Test5.txt"]  # Tus archivos

print("Archivo\t\t| Tiempo S1 (s)\t| Tiempo S2 (s)")
print("-" * 40)
for archivo in archivos_prueba:
    t1 = medir_tiempo_solucion_1(archivo)
    t2 = medir_tiempo_solucion_2(archivo)
    print(f"{archivo}\t| {t1}\t\t| {t2}")

from sol1.utils_sol1 import cargar_datos_test, generar_salida

try:
    temas_abb, encuestados = cargar_datos_test("test2.txt")
    generar_salida(temas_abb, encuestados)
    print("Ejecución completa.")
except Exception as e:
    print(f"Ocurrió un error: {e}")

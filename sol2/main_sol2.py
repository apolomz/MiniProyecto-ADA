from utils_sol2 import cargar_datos_test, generar_salida

def main():
    lista_temas, encuestados = cargar_datos_test("Test1.txt")  # o ruta completa si estás probando el archivo
    generar_salida(lista_temas, encuestados)
    print("\n✅ Ejecución completa sin errores.")

if __name__ == "__main__":
    main()

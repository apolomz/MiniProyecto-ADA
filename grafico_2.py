import matplotlib.pyplot as plt

# Tamaños de entrada
tamanos = [40, 60, 80, 120, 160]

# Tiempos de ejecución en segundos
tiempos_s1 = [0.0008, 0.0006, 0.0009, 0.0018, 0.0027]
tiempos_s2 = [0.0006, 0.0005, 0.0008, 0.0012, 0.0021]

plt.figure(figsize=(10, 6))
plt.plot(tamanos, tiempos_s1, marker='o', label='Solución 1 (ABB)', color='blue')
plt.plot(tamanos, tiempos_s2, marker='s', label='Solución 2 (Listas)', color='green')
plt.xlabel('Tamaño de entrada (número de encuestados)')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Comparación de rendimiento entre Solución 1 y Solución 2')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico_comparativo.png')  # Esto guarda el gráfico
plt.show()

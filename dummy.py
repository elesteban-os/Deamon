
from multiprocessing import Process
import os
import sys

# Aumentar el límite de recursión
sys.setrecursionlimit(10**6)  

# Tarea intensiva de CPU que se ejecutará en múltiples procesos
def cpuTask():
    while True:
        factorial(1000)  # Tarea intensiva de CPU

def factorial(n):
	if n == 1:
		return 1
	else:
		return n * factorial(n - 1)

if __name__ == "__main__":
    # Obtener el número de núcleos de CPU disponibles
    num_cores = os.cpu_count()
    print(f"Número de núcleos de CPU disponibles: {num_cores}")
    
    processes = []
    for _ in range(num_cores):  # Crea procesos para consumir todos los núcleos disponibles
        p = Process(target=cpuTask)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
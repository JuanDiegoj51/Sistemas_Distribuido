# Tarea realzada por Juan Diego Jimenez
# Este codigo tiene como base el expuesto por la docente en clase y con la ayuda de la inteligencia 
# artificial y modificacion del codigo se logro lo siguiente: 
# Este codigo, simula el frontend, el backend y una database, el objetivo es que el front envie 18 solicitudes
# esta solicitud es un numero al azar del 1 al 10, enviado al backend el cual hayara el cuadrado, es decir, procesara
# la informacio y por ultimo, sera enviado a una database que publicara la informacion en la carpeta anexa al .py
# Para simular, se hacen 18 solicitudes las cuales seran distribuidas en 3 nodos backend que procesaran y publicaran la informacion


import queue
import threading
import time
import random

# Creación de las colas para la comunicación entre nodos
# Frontend -> Backend y Backend -> Base de Datos
frontend_to_backend_queue = queue.Queue()
backend_to_db_queue = queue.Queue()

# Simulación de nodos frontend que envían solicitudes al backend
def frontend(nodo_id, num_requests):
    # Cada nodo realizará `num_requests` solicitudes
    for i in range(num_requests):
        # Genera un número aleatorio entre 1 y 10
        number = random.randint(1, 10)
        print(f"Nodo {nodo_id}: Enviando {number} para calcular su cuadrado")
        # Envío del número al backend a través de la cola, junto con el ID del nodo
        frontend_to_backend_queue.put((nodo_id, number))
        # Simulación de tiempos de espera aleatorios entre las solicitudes
        time.sleep(random.uniform(0.1, 0.5))

    # Enviar una señal de finalización (None) para indicar que el nodo terminó sus solicitudes
    frontend_to_backend_queue.put((nodo_id, None))

# Simulación del backend que recibe solicitudes de varios nodos frontend y procesa los cálculos
def backend(num_nodos):
    finished_nodos = 0  # Contador de nodos que han terminado de enviar solicitudes
    while finished_nodos < num_nodos:
        # Obtener datos de la cola (nodo_id y número a procesar)
        nodo_id, number = frontend_to_backend_queue.get()
        if number is None:  # Verifica si el nodo ha enviado la señal de finalización
            finished_nodos += 1  # Incrementa el número de nodos que han terminado
            frontend_to_backend_queue.task_done()
            continue

        # Calcula el cuadrado del número recibido
        square = number ** 2
        print(f"Backend: Nodo {nodo_id} calculando el cuadrado de {number}: {square}")
        # Envía el resultado del cálculo a la base de datos a través de la cola
        backend_to_db_queue.put((nodo_id, number, square))
        frontend_to_backend_queue.task_done()

    # Cuando todos los nodos frontend han terminado, envía la señal de finalización al hilo de la base de datos
    backend_to_db_queue.put(None)

# Simulación de la base de datos que guarda los resultados en archivos
def database():
    while True:
        # Obtiene los datos del backend (nodo_id, número original, cuadrado)
        data = backend_to_db_queue.get()
        if data is None:  # Verifica si el backend ha enviado la señal de finalización
            backend_to_db_queue.task_done()
            break

        # Desempaqueta los datos recibidos
        nodo_id, number, square = data
        # Genera un nombre de archivo único para cada resultado
        output_file = f"nodo_{nodo_id}_resultado_{number}.txt"
        # Abre el archivo en modo de escritura y guarda los datos
        with open(output_file, "w") as file:
            file.write(f"Nodo: {nodo_id}\nNumero: {number}\nCuadrado: {square}\n")
        print(f"Database: Guardando {square} del Nodo {nodo_id} en el archivo {output_file}")
        backend_to_db_queue.task_done()

# Función principal para gestionar la creación y sincronización de los hilos
def main():
    num_nodos = 3  # Define el número de nodos frontend
    num_requests_per_nodo = 100 // num_nodos  # Calcula cuántas solicitudes hará cada nodo

    # Crear y arrancar los hilos frontend
    frontend_threads = []
    for nodo_id in range(1, num_nodos + 1):
        # Crear un hilo por cada nodo frontend, pasándole el ID del nodo y el número de solicitudes
        t = threading.Thread(target=frontend, args=(nodo_id, num_requests_per_nodo))
        frontend_threads.append(t)
        t.start()

    # Crear y arrancar el hilo del backend
    backend_thread = threading.Thread(target=backend, args=(num_nodos,))
    backend_thread.start()

    # Crear y arrancar el hilo de la base de datos
    database_thread = threading.Thread(target=database)
    database_thread.start()

    # Esperar a que todos los hilos frontend terminen su ejecución
    for t in frontend_threads:
        t.join()

    # Esperar a que el hilo del backend termine su ejecución
    backend_thread.join()

    # Esperar a que el hilo de la base de datos termine su ejecución
    database_thread.join()

    print("Todas las solicitudes han sido procesadas y guardadas.")

# Verificación para asegurarse de que el código se ejecuta cuando es llamado directamente
if __name__ == "__main__":
    main()
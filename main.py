
import notification
import startup
import time
import os

# Flujo del script
def main():
    # Agregar el script al inicio
    startup.add_to_startup(os.path.abspath(__file__))
    
    # Enviar una notificación de confirmación
    notification.notify("Only-Fans Daemon", "El daemon para los ventiladores se encuentra en ejecución.", app_icon="/home/kevin/Documents/GitHub/Deamon/of.png")

    # Hacer el resto de cosas en un bucle infinito que se tarde 5 segundos
    while True:
        notification.notify("Only-Fans Daemon", "Se hizo una consulta al estado de los sensores de temperatura.", app_icon="/home/kevin/Documents/GitHub/Deamon/of.png")
        time.sleep(10)


# Ejecutar el flujo principal
if __name__ == "__main__":
    main()

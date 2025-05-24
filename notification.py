
from plyer import notification

# Crear una notificación de sistema
def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name='My Application',
        timeout=5  # Duración de la notificación en segundos
    )

# Ejemplo de uso
if __name__ == "__main__":
    notify("Hola", "Esta es una notificación de prueba.")

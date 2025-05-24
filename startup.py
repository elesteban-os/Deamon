
import os
import notification

def add_to_startup():
    # Ruta del script actual
    script_path = os.path.abspath(__file__)

    # Ruta de la carpeta autostart para configurar que el script se ejecute al inicio
    autostart_dir = os.path.expanduser("~/.config/autostart")

    # Ruta del archivo .desktop donde se guardará la configuración para el inicio automático
    autostart_file = os.path.join(autostart_dir, "notification1.desktop")

    # Crear la carpeta autostart si no existe
    os.makedirs(autostart_dir, exist_ok=True)

    # Verificar si el archivo .desktop ya existe
    if os.path.exists(autostart_file):
        print("El archivo .desktop ya existe. El script ya está configurado para ejecutarse al inicio.")
        return

    # Crear el archivo .desktop para el inicio automático
    with open(autostart_file, "w") as desktop_file:
        desktop_file.write(f"""
[Desktop Entry]
Type=Application
Exec=python3 {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Notification Script
Comment=Ejecuta el script de notificación al inicio
""")
        
    print(f"El script se ha configurado para ejecutarse al inicio: {autostart_file}")


# Ejecutar la función para agregar el script al inicio
if __name__ == "__main__":
    add_to_startup()
    notification.notify("Startup Script", "El script de notificación se ha configurado para ejecutarse al inicio.")
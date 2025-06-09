# BloqueApp
Un pequeño gestor para bloquear aplicaciones durante determinados días de la semana. Ideal para estudiantes, freelance o adictos al Valorant.


# 🚀 ¿Qué hace?

  Te permite seleccionar hasta 10 aplicaciones (rutas .exe) que quieres bloquear.

  Para cada aplicación, puedes marcar en qué días debe bloquearse.

  Al iniciar el bloqueo, el sistema monitoriza constantemente los procesos.

  Si alguno de los procesos bloqueados se inicia en un día restringido, lo cierra automáticamente en menos de 10 segundos.

  Todo esto con una interfaz web simple, sin necesidad de modificar código.

# 📂 Estructura del proyecto

bloqueador-app/

├── AppBlockerPy.py      # Interfaz Flask para configurar

├── watcher.pyw          # Script que ejecuta el bloqueo en segundo plano

├── config.json          # Archivo donde se guarda la configuración

├── templates/
│   └── index.html       # Interfaz HTML

├── static/
│   └── style.css        # Estilos CSS

# 🧠 ¿Cómo funciona?

  Ejecutas AppBlockerPy.py
    Abre una interfaz web (localhost:5000) donde puedes seleccionar qué bloquear.

   Configuras la lista de bloqueos
    Escribes rutas a .exe y seleccionas los días de la semana.

  Guardas la configuración
    Se guarda automáticamente en config.json.

  Pulsas "Iniciar bloqueo"

        Se ejecuta watcher.pyw.

        Se cierra AppBlockerPy automáticamente.

        watcher.pyw comienza a vigilar los procesos activos.

  Si lanzas un proceso bloqueado...

        Se detecta.

        Se cierra automáticamente si coincide con un día bloqueado.

 # ✅ Requisitos

 Python 3.8+

 Paquetes estándar: flask, psutil
    Puedes instalarlos con:

    pip install flask psutil

# 🛠 Uso con .vbs (opcional)

Si quieres lanzar watcher.pyw sin que aparezca ninguna ventana, puedes usar un script .vbs.

Ejemplo lanzarWatcher.vbs:

    Set WshShell = CreateObject("WScript.Shell")
    WshShell.Run "pythonw.exe C:\ruta\a\watcher.pyw", 0

El 0 hace que no se muestre ninguna consola.

# 📌 Importante: cómo obtener el nombre correcto del ejecutable

Para que el bloqueo funcione correctamente, es fundamental usar el nombre exacto del proceso, no solo la ruta completa al archivo .exe.

🔧 Pasos para obtenerlo correctamente:

    Abre el programa que quieres bloquear (por ejemplo, Valorant).

    Presiona Ctrl + Shift + Esc para abrir el Administrador de tareas.

    Ve a la pestaña Detalles.

    Busca el nombre exacto del ejecutable (por ejemplo, VALORANT-Win64-Shipping.exe).

# 📌 Notas adicionales

    Si lanzas de nuevo AppBlockerPy, se cargará la última configuración.
    El watcher continúa funcionando en segundo plano mientras no cierres el proceso.
    Puedes compilar todo a .exe si lo deseas, pero no es obligatorio para usarlo.

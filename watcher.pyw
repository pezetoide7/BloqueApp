# watcher.py

import psutil
import time
import json
import os
import signal
from datetime import datetime
from pathlib import Path

# Ruta al JSON de configuración
CONFIG_PATH = Path(__file__).parent / 'config.json'

# Mapa de weekday() a letra usada en config.json
DAY_MAP = {
    0: 'L',  # Lunes
    1: 'M',  # Martes
    2: 'X',  # Miércoles
    3: 'J',  # Jueves
    4: 'V',  # Viernes
    5: 'S',  # Sábado
    6: 'D',  # Domingo
}

def cargar_config():
    """Lee y devuelve el JSON de config, o lista vacía si no existe."""
    if not CONFIG_PATH.exists():
        return []
    try:
        data = json.loads(CONFIG_PATH.read_text(encoding='utf-8'))
        return data.get('bloqueos', [])
    except Exception:
        return []

def cerrar_appblockerpy():
    """Cierra cualquier proceso que esté ejecutando AppBlockerPy.py."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        cmd = proc.info.get('cmdline') or []
        # Busca la referencia al script AppBlockerPy.py en la línea de comando
        if any('AppBlockerPy.py' in part for part in cmd):
            try:
                proc.send_signal(signal.SIGTERM)
            except Exception:
                pass

def monitorear():
    """Bucle principal: cada 5 s lee config y mata procesos bloqueados."""
    print("▶️ Iniciando watcher... (Ctrl+C para salir)")
    # Primero, cierra AppBlockerPy si sigue vivo
    cerrar_appblockerpy()

    while True:
        bloqueos = cargar_config()
        hoy = DAY_MAP[datetime.now().weekday()]
        # Para cada bloqueo configurado...
        for entry in bloqueos:
            ruta = entry.get('ruta', '')
            dias = entry.get('dias', [])
            # Solo actuamos si hoy está en los días de bloqueo
            if hoy not in dias:
                continue

            nombre = os.path.basename(ruta).lower()
            # Recorremos procesos
            for proc in psutil.process_iter(['pid', 'name']):
                nm = proc.info.get('name', '').lower()
                if nm == nombre:
                    try:
                        proc.kill()
                        print(f"⛔ {nombre} detenido.")
                    except Exception:
                        pass
        # Esperamos un rato antes de repetir (max 10 s hasta matar algo)
        time.sleep(5)


if __name__ == '__main__':
    monitorear()

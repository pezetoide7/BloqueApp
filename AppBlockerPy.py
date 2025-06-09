import json
import threading
import webbrowser
import subprocess
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# Inicializamos Flask
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)

CONFIG_PATH = Path(__file__).parent / 'config.json'

@app.route('/')
def index():
    # Leer config.json si existe
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
            bloqueos = data.get('bloqueos', [])
        except Exception:
            bloqueos = []
    else:
        bloqueos = []

    # Renderizar plantilla con bloqueos
    return render_template('index.html', bloqueos=bloqueos)

@app.route('/save_config', methods=['POST'])
def save_config():
    data = request.get_json()
    if not data or 'bloqueos' not in data:
        return jsonify({'status': 'error', 'message': 'Formato inválido'}), 400

    try:
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func:
        func()

@app.route('/start_watcher', methods=['POST'])
def start_watcher():
    try:
        watcher_path = Path(__file__).parent / 'watcher.pyw'
        subprocess.Popen([sys.executable, str(watcher_path)], shell=True)
        threading.Timer(1.0, shutdown_server).start()
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

def open_browser():
    webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(host='127.0.0.1', port=5000, debug=False)

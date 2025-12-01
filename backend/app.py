# VirtualLab/backend/app.py
from flask import Flask, render_template, jsonify, send_from_directory
import subprocess
import os
import requests
import json
import time

# --- GUACAMOLE CONFIGURATION ---
GUAC_URL = 'http://guacamole:8080/guacamole/api/'
API_USER = 'eegoy'
API_PASS = 'say4adm1nx!'

ACTIVE_SESSIONS = {}

def find_available_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 0))
    port = s.getsockname()[1]
    s.close
    return port

def get_guac_auth_token():
    """Authenticate with Guacamole API and retrieve an access token."""
    login_url = f"{GUAC_URL} tokens"
    payload = {
        'username': API_USER,
        'password': API_PASS
    }
    try:
        response = requests.post(login_url, data=payload)
        response.raise_for_status()
        return response.json()['authToken']
    except Exception as e:
        print(f"Error obtaining Guacamole API token: {e}")
        return None
    
def create_guac_connection(token, session_id, host_port):
    create_url = f"{GUAC_URL} sessions/data/json/connections?token={token}"
    
    connection_data = {
        "name": f"Session-{session_id}",
        "protocol": "vnc",
        "parameters": {
            "hostname": "host.docker.internal",
            "port": str(host_port),
            "password": "linuxvm1"
        }
    }
    try:
        response = requests.post(create_url, json=connection_data)
        response.raise_for_status()
        
        return response.json()['identifier']
    except Exception as e:
        print(f"Error creating Guacamole connection: {e}")
        return None

# --- PATH CONFIGURATION ---
DOCKER_COMPOSE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MODULE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')

app = Flask(
    __name__,
    template_folder='../frontend',
    static_folder='../frontend/src',
)

# --- ROUTES ---

@app.route('/')
def index():
    # Serves the main application shell
    return render_template('index.html')

@app.route('/landing_page.html')
def landing_page():
    return send_from_directory(MODULE_DIR, 'landing_page.html')

@app.route('/start_vm', methods=['POST'])
def start_vm_sessions():
    auth_token = get_guac_auth_token()
    if not auth_token:
        return jsonify({'status': 'error', 'message': 'API Authentication Failed.'}), 500
    
    session_id = os.urandom(8).hex()
    host_port = find_available_port()
    container_name = f"kali-session-{session_id}"
    
    try:
        command = [
            'docker', 'run', '-d',
            '--name', container_name,
            '-p', f'{host_port}:5900',
            '--rm',
            'kali-vnc:latest',
        ]
        subprocess.run(command, check=True, capture_output=True)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Failed to start VM. Error: {str(e)}'}), 500
    
    connection_id = create_guac_connection(auth_token, session_id, host_port)
    
    if not connection_id:
        subprocess.run(['docker', 'stop', container_name])
        return jsonify({'status': 'error', 'message': 'Failed to create Guacamole connection.'}), 500
    
    ACTIVE_SESSIONS[session_id] = {
        'container': container_name,
        'port': host_port,
        'connection_id': connection_id
    }
    
    return jsonify({
        'status': 'success',
        'connection_id': connection_id,
        'session_id': session_id
    }), 200
    
@app.route('/stop_vm', methods=['POST'])
def stop_vm_session():
    data = requests.json
    session_id = data.get('session_id')
    
    if session_id not in ACTIVE_SESSIONS:
        return jsonify({'status': 'error', 'message': 'Session not active.'}), 404

    session_info = ACTIVE_SESSIONS[session_id]
    auth_token = get_guac_auth_token()
    
    # 1. Delete Guacamole Connection
    if auth_token:
        conn_id = session_info['connection_id']
        delete_url = f"{GUAC_URL}session/data/json/connections/{conn_id}?token={auth_token}"
        try:
            requests.delete(delete_url).raise_for_status()
        except Exception as e:
            print(f"Error deleting Guacamole connection: {e}")

    # 2. Stop and Remove Docker Container
    try:
        subprocess.run(['docker', 'stop', session_info['container']], check=True)
        subprocess.run(['docker', 'rm', session_info['container']], check=True)
    except Exception as e:
        print(f"Error stopping Docker container: {e}")
        
    del ACTIVE_SESSIONS[session_id]
    return jsonify({'status': 'success', 'message': 'Session terminated.'}), 200
    
# Routes to serve specific HTML files (used in iframes)
@app.route('/learn_page.html')
def learn_page():
    return send_from_directory(MODULE_DIR, 'learn_page.html')

@app.route('/analisis_file.html')
def analisis_file():
    return send_from_directory(MODULE_DIR, 'analisis_file.html')

@app.route('/blank.html')
def blank():
    return send_from_directory(MODULE_DIR, 'blank.html')

@app.route('/file_analysis.html')
def file_analysis():
    return send_from_directory(MODULE_DIR, 'file_analysis.html')

@app.route('/metadata_investigation.html')
def metadata_investigation():
    return send_from_directory(MODULE_DIR, 'metadata_investigation.html')

@app.route('/digital_footprint.html')
def digital_footprint():
    return send_from_directory(MODULE_DIR, 'digital_footprint.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
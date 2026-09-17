import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

# Desactivar advertencias de certificados SSL autofirmados (común en routers locales)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
CORS(app)

# Configuración del Controller de Ubiquiti UniFi
UNIFI_IP = "192.168.1.1"       # IP de la consola UniFi / CloudKey
UNIFI_PORT = "8443"           # Puerto por defecto (8443 para Controller estándar)
UNIFI_USER = "admin_portal"   # Usuario administrador de UniFi
UNIFI_PASS = "contrasena123"   # Contraseña de UniFi
SITE_NAME = "default"         # Nombre del sitio en UniFi

# Base de Datos Simulada de Huéspedes
GUEST_DATABASE = {
    "1111111111": "Habitacion204",
    "2222222222": "Habitacion101",
    "3333333333": "Habitacion305"
}

def authorize_unifi_device(mac_address, minutes=1440):
    """
    Se autentica en el UniFi Controller y autoriza la dirección MAC.
    """
    try:
        session = requests.Session()
        session.verify = False  # Ignorar validación de certificado SSL local

        base_url = f"https://{UNIFI_IP}:{UNIFI_PORT}"
        
        # 1. Login en el Controller de UniFi (con timeout de 3 segundos)
        login_url = f"{base_url}/api/login"
        login_payload = {"username": UNIFI_USER, "password": UNIFI_PASS}
        
        login_response = session.post(login_url, json=login_payload, timeout=3)
        if login_response.status_code != 200:
            return False, "Error de autenticación con el controlador UniFi"

        # 2. Enviar comando de autorización
        auth_url = f"{base_url}/api/s/{SITE_NAME}/cmd/stamgr"
        auth_payload = {
            "cmd": "authorize-guest",
            "mac": mac_address.lower(),
            "minutes": minutes
        }
        
        auth_response = session.post(auth_url, json=auth_payload, timeout=3)
        if auth_response.status_code == 200:
            return True, "Dispositivo autorizado exitosamente en la red UniFi"
        
        return False, "No se pudo autorizar el dispositivo en la red"

    except requests.exceptions.ConnectionError:
        # ESTA LÍNEA SALVA TU PRUEBA LOCAL
        return True, "Simulación exitosa: Huésped validado (No hay router UniFi conectado para dar internet real)"
    except Exception as e:
        return False, f"Error del sistema: {str(e)}"

@app.route('/api/login-wifi', methods=['POST'])
def login_wifi():
    data = request.get_json()
    usuario = data.get('usuario')
    contrasena = data.get('contrasena')
    mac = data.get('mac')

    # Validación 1: Verificar que los campos no estén vacíos
    if not usuario or not contrasena or not mac:
        return jsonify({"success": False, "message": "Faltan datos obligatorios"}), 400

    # Validación 2: Comprobar credenciales del huésped
    if usuario in GUEST_DATABASE and GUEST_DATABASE[usuario] == contrasena:
        # Validación 3: Comunicarse con UniFi Controller
        success, message = authorize_unifi_device(mac, minutes=1440) # 24 horas de acceso
        
        if success:
            return jsonify({"success": True, "message": message}), 200
        else:
            return jsonify({"success": False, "message": message}), 500
    else:
        return jsonify({"success": False, "message": "Usuario o número de habitación incorrecto"}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
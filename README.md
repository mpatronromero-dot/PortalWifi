# PortalWifi 🏨🌐

Sistema de portal cautivo desarrollado para la gestión y autenticación de acceso a internet en redes de hostelería, integrado con hardware de red **Ubiquiti UniFi** y un backend en **Python/Flask**.

---

## 🚀 Características

* **Interfaz Personalizada:** Diseño web moderno adaptado con la identidad visual del hotel (HTML5 y CSS3).
* **Autenticación por Huésped:** Validación basada en el documento de identidad del usuario (usuario) y su número de habitación (contraseña).
* **Captura de Parámetros de Red:** Extracción automática de la dirección MAC del dispositivo cliente enviada por el controlador UniFi.
* **Backend Robusto:** API desarrollada en Flask encargada de procesar las credenciales y comunicarse con el controlador de red.
* **Autorización Automatizada:** Envío de órdenes a la API de UniFi para la liberación temporal del tráfico de internet.

---

## 🛠️ Tecnologías Utilizadas

* **Frontend:** HTML5, CSS3 (Diseño responsivo).
* **Backend:** Python, Framework Flask.
* **Librerías:** Requests (para consumo de API REST), Flask-CORS.
* **Redes / Infraestructura:** Ubiquiti UniFi Controller (API de gestión de invitados).

---

## ⚙️ Instrucciones de Instalación y Ejecución

Sigue estos pasos para levantar el entorno de desarrollo en tu equipo local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/PortalWifi.git](https://github.com/tu-usuario/PortalWifi.git)
   cd PortalWifi
   📐 Arquitectura del Flujo
El cliente se conecta a la red Wi-Fi del hotel y es redirigido automáticamente al portal cautivo.

El usuario introduce sus credenciales (ID y número de habitación).

El frontend envía los datos junto con la dirección MAC al servidor Flask.

El backend valida los datos y autoriza el dispositivo mediante la API del controlador UniFi.

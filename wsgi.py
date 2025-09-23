import os
from servidor_de_licencias.license_server import app
from api import app  # Asegúrate de que 'app' esté definido en api.py

# Gunicorn y otros servidores WSGI buscan la variable "application"
application = app

if __name__ == "__main__":
    # Usa el puerto de Railway si existe, o 5000 en local
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
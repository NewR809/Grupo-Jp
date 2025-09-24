import os
#from db import consultar_tabla, guardar_en_mysql
#from config import USERNAME, PASSWORD
#from api import app
from servidor_de_licencias.license_server import app

application = app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
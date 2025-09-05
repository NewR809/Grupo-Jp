import requests
import time
import random

# Configuración de conexión
API_URL = "https://mongodb-production-cac8.up.railway.app"  # Reemplaza con la IP pública o dominio
USERNAME = "powerbi"
PASSWORD = "secure123"
CLIENTE_ID = "cliente_001"  # Cambia este ID para cada máquina

def generar_dato():
    """Simula un dato que se va a enviar (puedes personalizarlo)."""
    temperatura = round(random.uniform(25.0, 30.0), 2)
    return f"Temperatura: {temperatura}°C"

def enviar_dato():
    """Envía el dato al servidor Flask."""
    payload = {
        "cliente_id": CLIENTE_ID,
        "dato": generar_dato()
    }

    try:
        response = requests.post(API_URL, json=payload, auth=(USERNAME, PASSWORD))
        if response.status_code == 200:
            print("✅ Dato enviado:", payload["dato"])
        else:
            print("❌ Error:", response.text)
    except Exception as e:
        print("❌ Excepción al enviar dato:", e)

if __name__ == "__main__":
    while True:
        enviar_dato()
        time.sleep(60)  # Espera 60 segundos antes de enviar el siguiente dato
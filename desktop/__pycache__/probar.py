import requests
import time

URL = "https://api-powerbi-xoh2.onrender.com/api/datos"
AUTH = ("powerbi", "secure123")  # usuario y contraseña de tu decorador

try:
    inicio = time.time()
    resp = requests.get(URL, auth=AUTH, timeout=30)  # timeout ampliado a 30s
    duracion = time.time() - inicio

    print(f"⏱️ Tiempo de respuesta: {duracion:.2f} segundos")
    print(f"📡 Código HTTP: {resp.status_code}")

    if resp.ok:
        print("✅ Respuesta JSON:")
        print(resp.json())
    else:
        print("❌ Error en la respuesta:", resp.text)

except requests.exceptions.Timeout:
    print("⚠️ La petición excedió el tiempo de espera (timeout).")
except requests.exceptions.RequestException as e:
    print("⚠️ Error de conexión:", e)
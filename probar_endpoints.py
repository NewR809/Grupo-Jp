import requests
from requests.auth import HTTPBasicAuth

# URL base de tu API en Render
BASE = "https://tu-api.onrender.com/api"   # 👈 cambia por tu URL real
AUTH = HTTPBasicAuth("powerbi", "secure123")

# Endpoints a probar
endpoints = ["", "consultar_gastos", "consultar_ingresos", "datos"]

for ep in endpoints:
    url = f"{BASE}/{ep}" if ep else BASE + "/"
    print(f"\n🔎 Probando {url}")
    try:
        r = requests.get(url, auth=AUTH, timeout=20)
        print("Código HTTP:", r.status_code)

        # Intentar parsear como JSON
        try:
            data = r.json()
            print("✅ JSON válido recibido:", data if len(str(data)) < 200 else "JSON grande...")
        except ValueError:
            print("❌ La respuesta no es JSON válido")
            print("Respuesta cruda:", r.text[:200])  # muestra primeros 200 caracteres

    except Exception as e:
        print("⚠️ Error de conexión:", e)
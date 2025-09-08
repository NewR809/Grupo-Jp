import requests

url = "http://127.0.0.1:5000/consultar_gastos"
response = requests.get(url, auth=("powerbi", "secure123"))

print("Código:", response.status_code)
print("Respuesta:", response.text)
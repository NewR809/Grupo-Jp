from flask import request, Response
from functools import wraps
from config import USERNAME, PASSWORD

def autenticar(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        auth = request.authorization
        if not auth or auth.username != USERNAME or auth.password != PASSWORD:
            return Response("Acceso denegado", 401, {"WWW-Authenticate": 'Basic realm="Acceso restringido"'})
        return f(*args, **kwargs)
    return decorador
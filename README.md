# Grupo-Jp  
Control de sucursales  

## 📌 API Financiera + Servidor de Licencias

Esta API permite **consultar e insertar datos de gastos e ingresos** desde una base de datos MySQL en Railway, además de **gestionar licencias** para el uso de la aplicación.  
Es compatible con **Power BI** y también expone un endpoint de **consultas filtradas** para el perfil administrador.

---

## 🔐 Endpoints con Autenticación Básica

**Credenciales requeridas**  
- **Usuario:** `powerbi`  
- **Contraseña:** `secure123`  

### `GET /consultar_gastos`  
Devuelve todos los **gastos registrados**.  

### `GET /consultar_ingresos`  
Devuelve todos los **ingresos registrados**.


### `POST /insertar_gasto`  
Inserta un nuevo gasto.  
**Campos requeridos (JSON body):**
```json
{
  "fecha": "2025-09-01",
  "categoria": "Servicios",
  "monto": 120,
  "descripcion": "Internet"
}



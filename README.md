# Grupo-Jp  
Control de sucursales  

## 📌 API Financiera para Power BI y Consultas

Esta API permite **consultar e insertar datos de gastos e ingresos** desde una base de datos MySQL en Railway.  
Es compatible con **Power BI** y también expone un endpoint de **consultas filtradas** para el perfil administrador.

---

## 🚀 Endpoints disponibles

### 🔹 Endpoints con autenticación básica
Usuario: `powerbi`  
Contraseña: `secure123`

- `GET /consultar_gastos` → Devuelve todos los gastos registrados.  
- `GET /consultar_ingresos` → Devuelve todos los ingresos registrados.  
- `POST /insertar_gasto` → Inserta un nuevo gasto.  
  - Campos requeridos: `fecha`, `categoria`, `monto`, `descripcion`  
- `POST /insertar_ingreso` → Inserta un nuevo ingreso.  
  - Campos requeridos: `fecha`, `fuente`, `monto`, `descripcion`  
- `GET /datos` → Devuelve un JSON con dos propiedades:  
  ```json
  {
    "Gastos": [...],
    "Ingresos": [...]
  }
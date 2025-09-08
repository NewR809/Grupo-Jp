from base_datos import guardar_en_mysql

# Datos de prueba
datos = ["2025-09-07", "Admin", 100.0, "Prueba", "Test desde app"]

guardar_en_mysql("gastos", datos)
print("✅ Datos enviados a MySQL")

guardar_en_mysql("Ingresos", datos)
print("✅ Datos enviados a MySQL")
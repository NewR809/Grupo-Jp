-- Tabla de Ingresos
#actualizacion de tablas
-- Tabla de gastos
CREATE TABLE IF NOT EXISTS gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id VARCHAR(100) NULL,
    dato VARCHAR(255) NULL,
    fecha DATE NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de ingresos
CREATE TABLE IF NOT EXISTS ingresos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id VARCHAR(100) NULL,
    dato VARCHAR(255) NULL,
    fecha DATE NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    descripcion TEXT
);

-- Tabla de auditoría de sesiones (opcional, para control de accesos)
CREATE TABLE IF NOT EXISTS log_sesiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL,
    accion VARCHAR(50) NOT NULL, -- login, logout, bloqueo, etc.
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
RENAME TABLE Gastos TO gastos;
RENAME TABLE Ingresos TO ingresos;
ALTER USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' BY 'tu_contraseña';

ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'TU_PASSWORD';
FLUSH PRIVILEGES;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTO-INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK(role IN ('visor','admin'))
);

-- Usuario inicial con rol "visor" (superusuario)
INSERT INTO usuarios (username, password, role)
VALUES ('visor', 'visorsecret', 'visor');

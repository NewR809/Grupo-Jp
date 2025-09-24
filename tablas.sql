-- ============================================
-- 📊 Tablas Financieras
-- ============================================

-- Tabla de Gastos
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

-- Tabla de Ingresos
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

-- ============================================
-- 🔑 Tabla de Licencias
-- ============================================

CREATE TABLE IF NOT EXISTS licencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    clave VARCHAR(100) UNIQUE NOT NULL,
    cliente VARCHAR(100) NOT NULL,
    activa BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================
-- 👤 Tabla de Usuarios (para roles)
-- ============================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('visor','admin') NOT NULL
);

-- Usuario inicial con rol "visor"
INSERT INTO usuarios (username, password, role)
VALUES ('visor', 'visorsecret', 'visor')
ON DUPLICATE KEY UPDATE username=username;

-- ============================================
-- 📜 Tabla de Auditoría de Sesiones
-- ============================================

CREATE TABLE IF NOT EXISTS log_sesiones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL,
    accion VARCHAR(50) NOT NULL, -- login, logout, bloqueo, etc.
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Tabla de Ingresos
CREATE TABLE IF NOT EXISTS Ingresos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id VARCHAR(100),
    dato TEXT,
    fecha DATE NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    categoria VARCHAR(150) NOT NULL,
    descripcion TEXT
);

-- Tabla de Gastos
CREATE TABLE IF NOT EXISTS Gastos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id VARCHAR(100),
    dato TEXT,
    fecha DATE NOT NULL,
    usuario VARCHAR(100) NOT NULL,
    monto DECIMAL(12,2) NOT NULL,
    categoria VARCHAR(150) NOT NULL,
    descripcion TEXT
);



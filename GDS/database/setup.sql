-- ================================================================
-- Script de creación de base de datos GDS
-- Sistema de Booking Engine centralizado
-- ================================================================

-- Crear base de datos
CREATE DATABASE IF NOT EXISTS principal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE principal_db;

-- ================================================================
-- Tabla de Usuarios
-- ================================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    dni VARCHAR(20) NOT NULL UNIQUE,
    fecha_nacimiento DATE NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_dni (dni)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- Tabla de Reservas
-- ================================================================
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    localizador_externo VARCHAR(100) NOT NULL,
    origen ENUM('WebService', 'Channel') NOT NULL,
    hotel_nombre VARCHAR(200) NOT NULL,
    habitacion_tipo VARCHAR(200) NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    num_huespedes INT NOT NULL DEFAULT 1,
    precio_total DECIMAL(10, 2) NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'completada') DEFAULT 'confirmada',
    datos_adicionales JSON NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    INDEX idx_usuario (usuario_id),
    INDEX idx_localizador (localizador_externo),
    INDEX idx_fecha_entrada (fecha_entrada),
    INDEX idx_estado (estado)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ================================================================
-- Datos de prueba (opcional)
-- ================================================================

-- Insertar un usuario de prueba (password: "test123" - debe ser hasheado en la aplicación)
-- La contraseña real debe ser hasheada con bcrypt en el backend
INSERT INTO usuarios (nombre, apellidos, email, dni, fecha_nacimiento, password) 
VALUES ('Usuario', 'de Prueba', 'test@example.com', '12345678A', '1990-01-01', '$2b$10$PLACEHOLDER')
ON DUPLICATE KEY UPDATE email=email;

-- ================================================================
-- Vistas útiles
-- ================================================================

-- Vista de reservas con información de usuario
CREATE OR REPLACE VIEW vista_reservas_completas AS
SELECT 
    r.id,
    r.localizador_externo,
    r.origen,
    r.hotel_nombre,
    r.habitacion_tipo,
    r.fecha_entrada,
    r.fecha_salida,
    r.num_huespedes,
    r.precio_total,
    r.estado,
    r.created_at,
    u.id as usuario_id,
    u.nombre,
    u.apellidos,
    u.email,
    DATEDIFF(r.fecha_salida, r.fecha_entrada) as num_noches
FROM reservas r
INNER JOIN usuarios u ON r.usuario_id = u.id;

-- ================================================================
-- Estadísticas y consultas útiles
-- ================================================================

-- Función para obtener estadísticas de reservas por usuario
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS obtener_estadisticas_usuario(IN user_id INT)
BEGIN
    SELECT 
        COUNT(*) as total_reservas,
        SUM(CASE WHEN estado = 'confirmada' THEN 1 ELSE 0 END) as reservas_confirmadas,
        SUM(CASE WHEN estado = 'cancelada' THEN 1 ELSE 0 END) as reservas_canceladas,
        SUM(CASE WHEN estado = 'completada' THEN 1 ELSE 0 END) as reservas_completadas,
        SUM(precio_total) as gasto_total,
        AVG(precio_total) as gasto_promedio
    FROM reservas
    WHERE usuario_id = user_id;
END //
DELIMITER ;

-- ================================================================
-- Permisos y seguridad
-- ================================================================

-- Dar permisos al usuario pms_user para la base de datos principal_db
GRANT ALL PRIVILEGES ON principal_db.* TO 'pms_user'@'localhost';
FLUSH PRIVILEGES;

-- ================================================================
-- Información del schema
-- ================================================================

SELECT 'Base de datos GDS creada exitosamente' as mensaje;
SELECT TABLE_NAME, TABLE_ROWS, CREATE_TIME 
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'principal_db' 
AND TABLE_TYPE = 'BASE TABLE';

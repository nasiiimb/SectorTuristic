-- Script para añadir el campo 'estado' a la tabla Reserva
-- Fecha: 2025-11-12

USE pms_database;

-- Añadir columna estado a la tabla Reserva
ALTER TABLE Reserva 
ADD COLUMN estado ENUM('Activa', 'Cancelada') NOT NULL DEFAULT 'Activa'
COMMENT 'Estado de la reserva: Activa o Cancelada';

-- Actualizar todas las reservas existentes como Activas
UPDATE Reserva SET estado = 'Activa' WHERE estado IS NULL;

-- Mostrar resultado
SELECT 'Campo estado añadido correctamente a la tabla Reserva' AS Resultado;

-- -----------------------------------------------------
-- Script para corregir datos mal codificados
-- Ejecutar después de fix_encoding.sql
-- -----------------------------------------------------

-- Establecer codificación UTF-8 para la sesión
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

-- Corregir datos en la tabla hotel
UPDATE hotel SET ubicacion = 'Paseo Marítimo, 10, Palma' WHERE idHotel = 1;

-- Corregir datos en la tabla tipohabitacion
UPDATE tipohabitacion SET categoria = 'Doble Estándar' WHERE idTipoHabitacion = 1;

SELECT 'Datos corregidos exitosamente' AS Mensaje;

-- Verificar los cambios
SELECT '=== HOTELES ===' AS '';
SELECT idHotel, nombre, ubicacion FROM hotel;

SELECT '=== TIPOS DE HABITACIÓN ===' AS '';
SELECT idTipoHabitacion, categoria FROM tipohabitacion;

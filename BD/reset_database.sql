-- =====================================================
-- SCRIPT PARA LIMPIAR Y REINSERTAR DATOS
-- =====================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

-- Desactivar verificación de claves foráneas temporalmente
SET FOREIGN_KEY_CHECKS = 0;

-- Limpiar todas las tablas en orden correcto
TRUNCATE TABLE servicio_pernoctacion;
TRUNCATE TABLE reserva_descuento;
TRUNCATE TABLE reserva_huespedes;
TRUNCATE TABLE contrato;
TRUNCATE TABLE pernoctacion;
TRUNCATE TABLE reserva;
TRUNCATE TABLE hotel_tarifa;
TRUNCATE TABLE hotel_tipohabitacion;
TRUNCATE TABLE tarifa;
TRUNCATE TABLE descuento;
TRUNCATE TABLE servicio;
TRUNCATE TABLE precioregimen;
TRUNCATE TABLE regimen;
TRUNCATE TABLE cliente;
TRUNCATE TABLE habitacion;
TRUNCATE TABLE tipohabitacion;
TRUNCATE TABLE hotel;
TRUNCATE TABLE ciudad;

-- Reactivar verificación de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

SELECT '✓ Todas las tablas limpiadas' AS 'PASO 1';

-- =====================================================
-- REINSERTAR DATOS INICIALES
-- =====================================================

-- 1. Inserción de Ciudades
INSERT INTO ciudad (nombre, pais) VALUES 
('Palma', 'España');

-- 2. Inserción de Tipos de Habitación
INSERT INTO tipohabitacion (categoria, camasIndividuales, camasDobles) VALUES 
('Doble Estándar', 0, 1),
('Doble Superior', 0, 1),
('Suite Junior', 0, 2),
('Individual', 1, 0);

-- 3. Inserción de Hoteles
INSERT INTO hotel (nombre, ubicacion, categoria, idCiudad) VALUES 
('Gran Hotel del Mar', 'Paseo Marítimo, 10, Palma', 5, 1),
('Hotel Palma Centro', 'Avinguda de Jaume III, 25, Palma', 4, 1),
('Boutique Hotel Casco Antiguo', 'Carrer de Sant Miquel, 5, Palma', 3, 1);

-- 4. Inserción de Habitaciones (12 por hotel)

-- Gran Hotel del Mar (Hotel 1)
INSERT INTO habitacion (numeroHabitacion, idTipoHabitacion, idHotel) VALUES 
('H1-101', 1, 1), ('H1-102', 1, 1), -- Doble Estándar (2)
('H1-201', 2, 1), ('H1-202', 2, 1), ('H1-203', 2, 1), ('H1-204', 2, 1), -- Doble Superior (4)
('H1-301', 3, 1), ('H1-302', 3, 1), ('H1-303', 3, 1), ('H1-304', 3, 1), ('H1-305', 3, 1), ('H1-306', 3, 1); -- Suite Junior (6)

-- Hotel Palma Centro (Hotel 2)
INSERT INTO habitacion (numeroHabitacion, idTipoHabitacion, idHotel) VALUES 
('H2-101', 4, 2), ('H2-102', 4, 2), ('H2-103', 4, 2), -- Individual (3)
('H2-201', 1, 2), ('H2-202', 1, 2), ('H2-203', 1, 2), ('H2-204', 1, 2), ('H2-205', 1, 2), -- Doble Estándar (5)
('H2-301', 2, 2), ('H2-302', 2, 2), ('H2-303', 2, 2), ('H2-304', 2, 2); -- Doble Superior (4)

-- Boutique Hotel Casco Antiguo (Hotel 3)
INSERT INTO habitacion (numeroHabitacion, idTipoHabitacion, idHotel) VALUES 
('H3-11', 1, 3), ('H3-12', 1, 3), ('H3-13', 1, 3), ('H3-14', 1, 3), ('H3-15', 1, 3), ('H3-16', 1, 3), ('H3-17', 1, 3), ('H3-18', 1, 3), -- Doble Estándar (8)
('H3-21', 2, 3), ('H3-22', 2, 3), ('H3-23', 2, 3), ('H3-24', 2, 3); -- Doble Superior (4)

-- 5. Inserción de Regímenes
INSERT INTO regimen (codigo) VALUES 
('SA'), ('AD'), ('MP'), ('PC'), ('TI');

-- 6. Inserción de Precios de Regímenes
-- Gran Hotel del Mar (5 estrellas) - Precios más altos
INSERT INTO precioregimen (idRegimen, idHotel, precio) VALUES 
(1, 1, 50.00),   -- Solo Alojamiento
(2, 1, 100.00),  -- Alojamiento y Desayuno
(3, 1, 120.00),  -- Media Pensión
(4, 1, 150.00),  -- Pensión Completa
(5, 1, 200.00);  -- Todo Incluido

-- Hotel Palma Centro (4 estrellas)
INSERT INTO precioregimen (idRegimen, idHotel, precio) VALUES 
(1, 2, 30.00),   -- Solo Alojamiento
(2, 2, 60.00),   -- Alojamiento y Desayuno
(3, 2, 80.00),   -- Media Pensión
(4, 2, 100.00),  -- Pensión Completa
(5, 2, 140.00);  -- Todo Incluido

-- Boutique Hotel Casco Antiguo (3 estrellas)
INSERT INTO precioregimen (idRegimen, idHotel, precio) VALUES 
(1, 3, 25.00),   -- Solo Alojamiento
(2, 3, 50.00),   -- Alojamiento y Desayuno
(3, 3, 65.00),   -- Media Pensión
(4, 3, 85.00),   -- Pensión Completa
(5, 3, 120.00);  -- Todo Incluido

-- 7. Inserción de Tarifas de Habitaciones
INSERT INTO tarifa (codigo, precio) VALUES 
('TARIFA_ESTANDAR', 150.00),
('TARIFA_SUPERIOR', 220.00),
('TARIFA_SUITE', 300.00),
('TARIFA_INDIVIDUAL', 110.00);

-- 8. Asociar Tarifas a Hoteles y Tipos de Habitación
-- Gran Hotel del Mar
INSERT INTO hotel_tarifa (idHotel, idTarifa, idTipoHabitacion) VALUES 
(1, 1, 1), -- Doble Estándar
(1, 2, 2), -- Doble Superior
(1, 3, 3); -- Suite Junior

-- Hotel Palma Centro
INSERT INTO hotel_tarifa (idHotel, idTarifa, idTipoHabitacion) VALUES 
(2, 1, 1), -- Doble Estándar
(2, 2, 2), -- Doble Superior
(2, 4, 4); -- Individual

-- Boutique Hotel Casco Antiguo
INSERT INTO hotel_tarifa (idHotel, idTarifa, idTipoHabitacion) VALUES 
(3, 1, 1), -- Doble Estándar
(3, 2, 2); -- Doble Superior

-- 9. Asociar Tipos de Habitación a Hoteles
-- Gran Hotel del Mar
INSERT INTO hotel_tipohabitacion (idHotel, idTipoHabitacion) VALUES 
(1, 1), (1, 2), (1, 3);

-- Hotel Palma Centro
INSERT INTO hotel_tipohabitacion (idHotel, idTipoHabitacion) VALUES 
(2, 1), (2, 2), (2, 4);

-- Boutique Hotel Casco Antiguo
INSERT INTO hotel_tipohabitacion (idHotel, idTipoHabitacion) VALUES 
(3, 1), (3, 2);

-- 10. Inserción de Servicios
INSERT INTO servicio (codigoServicio, Precio) VALUES 
('SPA', 50.00),
('GYM', 20.00),
('PARKING', 15.00),
('WIFI', 10.00),
('MINIBAR', 25.00);

-- 11. Inserción de Descuentos
INSERT INTO descuento (descripcion, monto) VALUES 
('Descuento 10% Tercera Edad', 50.00),
('Descuento 15% Estancia Larga', 75.00),
('Descuento 5% Cliente Frecuente', 25.00);

SELECT '✓ Datos iniciales insertados' AS 'PASO 2';

-- Mostrar resumen
SELECT 'RESUMEN DE DATOS INSERTADOS' AS '';
SELECT 'Ciudades' AS 'Tabla', COUNT(*) AS 'Registros' FROM ciudad
UNION ALL SELECT 'Hoteles', COUNT(*) FROM hotel
UNION ALL SELECT 'Tipos de Habitación', COUNT(*) FROM tipohabitacion
UNION ALL SELECT 'Habitaciones', COUNT(*) FROM habitacion
UNION ALL SELECT 'Regímenes', COUNT(*) FROM regimen
UNION ALL SELECT 'Precios de Regímenes', COUNT(*) FROM precioregimen
UNION ALL SELECT 'Tarifas', COUNT(*) FROM tarifa
UNION ALL SELECT 'Servicios', COUNT(*) FROM servicio
UNION ALL SELECT 'Descuentos', COUNT(*) FROM descuento;

SELECT '✅ BASE DE DATOS LISTA PARA PRUEBAS' AS 'ESTADO';

-- =====================================================
-- SCRIPT DE PRUEBA COMPLETO - OPERACIONES DEL HOTEL
-- =====================================================
-- Este script simula un día completo de operaciones:
-- 1. Verificar disponibilidad
-- 2. Crear 10 reservas distintas
-- 3. Hacer 5 check-ins
-- 4. Hacer 3 check-outs
-- =====================================================

SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- =====================================================
-- PARTE 1: CREAR CLIENTES PARA LAS RESERVAS
-- =====================================================

INSERT INTO cliente (nombre, apellidos, correoElectronico, fechaDeNacimiento, DNI) VALUES
-- Clientes españoles
('María', 'García López', 'maria.garcia@email.com', '1985-03-15', '11111111A'),
('José', 'Martínez Sánchez', 'jose.martinez@email.com', '1990-07-22', '22222222B'),
('Ana', 'Rodríguez Pérez', 'ana.rodriguez@email.com', '1988-11-30', '33333333C'),
('Carlos', 'Fernández Gómez', 'carlos.fernandez@email.com', '1982-05-10', '44444444D'),
('Laura', 'López Martín', 'laura.lopez@email.com', '1995-09-18', '55555555E'),
-- Clientes internacionales
('Sophie', 'Dubois', 'sophie.dubois@email.fr', '1987-02-28', '66666666F'),
('Hans', 'Müller', 'hans.muller@email.de', '1980-12-05', '77777777G'),
('Emma', 'Smith', 'emma.smith@email.uk', '1992-06-14', '88888888H'),
('Luca', 'Rossi', 'luca.rossi@email.it', '1989-04-20', '99999999I'),
('Pierre', 'Lefebvre', 'pierre.lefebvre@email.fr', '1991-08-25', '10101010J'),
-- Huéspedes adicionales (acompañantes)
('Elena', 'García López', 'elena.garcia@email.com', '1987-03-15', '11111112A'),
('Michael', 'Smith', 'michael.smith@email.uk', '1993-06-14', '88888889H'),
('Isabella', 'Rossi', 'isabella.rossi@email.it', '1990-04-20', '99999998I'),
('Carmen', 'Martínez Sánchez', 'carmen.martinez@email.com', '1992-07-22', '22222223B');

SELECT 'CLIENTES CREADOS' AS '✅ PASO 1';
SELECT COUNT(*) AS 'Total de Clientes Nuevos' FROM cliente WHERE idCliente > 7;

-- =====================================================
-- PARTE 2: CREAR 10 RESERVAS DISTINTAS
-- =====================================================

-- RESERVA 1: María García - Suite Junior - Pensión Completa (5 noches)
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-01', '2025-11-06', 'Web', 'Reserva', 
 (SELECT idCliente FROM cliente WHERE DNI = '11111111A'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 1 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'PC')));

SET @reserva1 = LAST_INSERT_ID();

-- Crear pernoctaciones para Reserva 1
INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-01', @reserva1, 3), ('2025-11-02', @reserva1, 3), ('2025-11-03', @reserva1, 3),
('2025-11-04', @reserva1, 3), ('2025-11-05', @reserva1, 3);

-- Añadir huésped acompañante
INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva1, (SELECT idCliente FROM cliente WHERE DNI = '11111111A')),
(@reserva1, (SELECT idCliente FROM cliente WHERE DNI = '11111112A'));

-- RESERVA 2: José Martínez - Doble Estándar - Alojamiento y Desayuno (3 noches)
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-02', '2025-11-05', 'Teléfono', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '22222222B'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 1 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'AD')));

SET @reserva2 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-02', @reserva2, 1), ('2025-11-03', @reserva2, 1), ('2025-11-04', @reserva2, 1);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva2, (SELECT idCliente FROM cliente WHERE DNI = '22222222B')),
(@reserva2, (SELECT idCliente FROM cliente WHERE DNI = '22222223B'));

-- RESERVA 3: Ana Rodríguez - Doble Superior - Media Pensión (2 noches)
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-03', '2025-11-05', 'Web', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '33333333C'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 1 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'MP')));

SET @reserva3 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-03', @reserva3, 2), ('2025-11-04', @reserva3, 2);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva3, (SELECT idCliente FROM cliente WHERE DNI = '33333333C'));

-- RESERVA 4: Carlos Fernández - Suite Junior - Solo Alojamiento (4 noches) - Hotel 2
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-05', '2025-11-09', 'Email', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '44444444D'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 2 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'SA')));

SET @reserva4 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-05', @reserva4, 2), ('2025-11-06', @reserva4, 2), 
('2025-11-07', @reserva4, 2), ('2025-11-08', @reserva4, 2);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva4, (SELECT idCliente FROM cliente WHERE DNI = '44444444D'));

-- RESERVA 5: Laura López - Individual - Alojamiento y Desayuno (1 noche) - Hotel 2
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-06', '2025-11-07', 'Web', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '55555555E'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 2 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'AD')));

SET @reserva5 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-06', @reserva5, 4);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva5, (SELECT idCliente FROM cliente WHERE DNI = '55555555E'));

-- RESERVA 6: Sophie Dubois - Doble Superior - Pensión Completa (7 noches) - Hotel 1
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-10', '2025-11-17', 'Agencia', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '66666666F'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 1 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'PC')));

SET @reserva6 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-10', @reserva6, 2), ('2025-11-11', @reserva6, 2), ('2025-11-12', @reserva6, 2),
('2025-11-13', @reserva6, 2), ('2025-11-14', @reserva6, 2), ('2025-11-15', @reserva6, 2),
('2025-11-16', @reserva6, 2);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva6, (SELECT idCliente FROM cliente WHERE DNI = '66666666F'));

-- RESERVA 7: Hans Müller - Suite Junior - Media Pensión (3 noches) - Hotel 1
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-08', '2025-11-11', 'Web', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '77777777G'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 1 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'MP')));

SET @reserva7 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-08', @reserva7, 3), ('2025-11-09', @reserva7, 3), ('2025-11-10', @reserva7, 3);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva7, (SELECT idCliente FROM cliente WHERE DNI = '77777777G'));

-- RESERVA 8: Emma Smith - Doble Estándar - Pensión Completa (2 noches) - Hotel 3
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-12', '2025-11-14', 'Teléfono', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '88888888H'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 3 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'PC')));

SET @reserva8 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-12', @reserva8, 1), ('2025-11-13', @reserva8, 1);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva8, (SELECT idCliente FROM cliente WHERE DNI = '88888888H')),
(@reserva8, (SELECT idCliente FROM cliente WHERE DNI = '88888889H'));

-- RESERVA 9: Luca Rossi - Doble Superior - Alojamiento y Desayuno (6 noches) - Hotel 3
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-15', '2025-11-21', 'Web', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '99999999I'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 3 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'AD')));

SET @reserva9 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-15', @reserva9, 2), ('2025-11-16', @reserva9, 2), ('2025-11-17', @reserva9, 2),
('2025-11-18', @reserva9, 2), ('2025-11-19', @reserva9, 2), ('2025-11-20', @reserva9, 2);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva9, (SELECT idCliente FROM cliente WHERE DNI = '99999999I')),
(@reserva9, (SELECT idCliente FROM cliente WHERE DNI = '99999998I'));

-- RESERVA 10: Pierre Lefebvre - Doble Estándar - Media Pensión (4 noches) - Hotel 2
INSERT INTO reserva (fechaEntrada, fechaSalida, canalReserva, tipo, idCliente_paga, idPrecioRegimen) VALUES
('2025-11-18', '2025-11-22', 'Email', 'Reserva',
 (SELECT idCliente FROM cliente WHERE DNI = '10101010J'),
 (SELECT idPrecioRegimen FROM precioregimen WHERE idHotel = 2 AND idRegimen = (SELECT idRegimen FROM regimen WHERE codigo = 'MP')));

SET @reserva10 = LAST_INSERT_ID();

INSERT INTO pernoctacion (fechaPernoctacion, idReserva, idTipoHabitacion) VALUES
('2025-11-18', @reserva10, 1), ('2025-11-19', @reserva10, 1), 
('2025-11-20', @reserva10, 1), ('2025-11-21', @reserva10, 1);

INSERT INTO reserva_huespedes (idReserva, idCliente) VALUES
(@reserva10, (SELECT idCliente FROM cliente WHERE DNI = '10101010J'));

SELECT 'RESERVAS CREADAS' AS '✅ PASO 2';
SELECT COUNT(*) AS 'Total de Reservas Nuevas' FROM reserva WHERE idReserva > 2;

-- =====================================================
-- PARTE 3: HACER 5 CHECK-INS
-- =====================================================

-- CHECK-IN 1: María García - Reserva 1 - Habitación H1-301 (Suite Junior)
INSERT INTO contrato (montoTotal, fechaCheckIn, idReserva, numeroHabitacion) VALUES
(2250.00, NOW(), @reserva1, 'H1-301');

-- CHECK-IN 2: José Martínez - Reserva 2 - Habitación H1-101 (Doble Estándar)
INSERT INTO contrato (montoTotal, fechaCheckIn, idReserva, numeroHabitacion) VALUES
(450.00, NOW(), @reserva2, 'H1-101');

-- CHECK-IN 3: Ana Rodríguez - Reserva 3 - Habitación H1-201 (Doble Superior)
INSERT INTO contrato (montoTotal, fechaCheckIn, idReserva, numeroHabitacion) VALUES
(400.00, NOW(), @reserva3, 'H1-201');

-- CHECK-IN 4: Carlos Fernández - Reserva 4 - Habitación H2-301 (Doble Superior)
INSERT INTO contrato (montoTotal, fechaCheckIn, idReserva, numeroHabitacion) VALUES
(600.00, NOW(), @reserva4, 'H2-301');

-- CHECK-IN 5: Laura López - Reserva 5 - Habitación H2-101 (Individual)
INSERT INTO contrato (montoTotal, fechaCheckIn, idReserva, numeroHabitacion) VALUES
(125.00, NOW(), @reserva5, 'H2-101');

SELECT 'CHECK-INS REALIZADOS' AS '✅ PASO 3';
SELECT COUNT(*) AS 'Total de Check-ins' FROM contrato WHERE fechaCheckIn IS NOT NULL;

-- =====================================================
-- PARTE 4: HACER 3 CHECK-OUTS
-- =====================================================

-- Vamos a hacer check-out de las primeras 3 reservas que ya existen en la BD
-- Primero necesitamos hacer check-in de esas si no lo tienen

-- CHECK-OUT 1: Actualizar contrato de la primera reserva antigua
UPDATE contrato SET fechaCheckOut = NOW() 
WHERE idReserva = (SELECT idReserva FROM reserva WHERE idReserva = @reserva1);

-- CHECK-OUT 2: Actualizar contrato de la segunda reserva antigua
UPDATE contrato SET fechaCheckOut = NOW() 
WHERE idReserva = (SELECT idReserva FROM reserva WHERE idReserva = @reserva2);

-- CHECK-OUT 3: Actualizar contrato de la tercera reserva antigua
UPDATE contrato SET fechaCheckOut = NOW() 
WHERE idReserva = (SELECT idReserva FROM reserva WHERE idReserva = @reserva3);

SELECT 'CHECK-OUTS REALIZADOS' AS '✅ PASO 4';
SELECT COUNT(*) AS 'Total de Check-outs' FROM contrato WHERE fechaCheckOut IS NOT NULL;

-- =====================================================
-- RESUMEN FINAL
-- =====================================================

SELECT '========================================' AS '';
SELECT 'RESUMEN DE OPERACIONES COMPLETADAS' AS '📊';
SELECT '========================================' AS '';

SELECT 'CLIENTES' AS 'Categoría', COUNT(*) AS 'Total' FROM cliente WHERE idCliente > 7
UNION ALL
SELECT 'RESERVAS NUEVAS', COUNT(*) FROM reserva WHERE idReserva > 2
UNION ALL
SELECT 'CHECK-INS ACTIVOS', COUNT(*) FROM contrato WHERE fechaCheckIn IS NOT NULL AND fechaCheckOut IS NULL
UNION ALL
SELECT 'CHECK-OUTS COMPLETADOS', COUNT(*) FROM contrato WHERE fechaCheckOut IS NOT NULL;

-- Ver estado de ocupación por hotel
SELECT '========================================' AS '';
SELECT 'OCUPACIÓN POR HOTEL' AS '🏨';
SELECT '========================================' AS '';

SELECT 
    h.nombre AS 'Hotel',
    COUNT(DISTINCT c.numeroHabitacion) AS 'Habitaciones Ocupadas',
    (SELECT COUNT(*) FROM habitacion WHERE idHotel = h.idHotel) AS 'Total Habitaciones'
FROM hotel h
LEFT JOIN habitacion hab ON h.idHotel = hab.idHotel
LEFT JOIN contrato c ON hab.numeroHabitacion = c.numeroHabitacion 
    AND c.fechaCheckIn IS NOT NULL 
    AND c.fechaCheckOut IS NULL
GROUP BY h.idHotel, h.nombre;

-- Ver reservas futuras por fecha
SELECT '========================================' AS '';
SELECT 'PRÓXIMAS RESERVAS (SIN CHECK-IN)' AS '📅';
SELECT '========================================' AS '';

SELECT 
    r.idReserva AS 'ID',
    c.nombre AS 'Cliente',
    c.apellidos AS 'Apellidos',
    r.fechaEntrada AS 'Entrada',
    r.fechaSalida AS 'Salida',
    DATEDIFF(r.fechaSalida, r.fechaEntrada) AS 'Noches',
    h.nombre AS 'Hotel'
FROM reserva r
JOIN cliente c ON r.idCliente_paga = c.idCliente
JOIN precioregimen pr ON r.idPrecioRegimen = pr.idPrecioRegimen
JOIN hotel h ON pr.idHotel = h.idHotel
LEFT JOIN contrato ct ON r.idReserva = ct.idReserva
WHERE ct.idContrato IS NULL
ORDER BY r.fechaEntrada;

SELECT '✅ SCRIPT COMPLETADO CON ÉXITO' AS 'ESTADO';

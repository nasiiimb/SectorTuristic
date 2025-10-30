-- -----------------------------------------------------
-- SCRIPT COMPLETO DE INSERCIÓN DE DATOS INICIALES
-- -----------------------------------------------------

-- Establecer codificación UTF-8 para la sesión
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

-- 1. Inserción de Ciudades
INSERT INTO Ciudad (nombre, pais) VALUES 
('Palma', 'España');

-- -----------------------------------------------------

-- 2. Inserción de Tipos de Habitación
INSERT INTO TipoHabitacion (categoria, camasIndividuales, camasDobles) VALUES 
('Doble Estándar', 0, 1),
('Doble Superior', 0, 1),
('Suite Junior', 0, 2),
('Individual', 1, 0);

-- -----------------------------------------------------

-- 3. Inserción de Hoteles
-- Asumimos que los IDs serán 1, 2 y 3. Todos están en Palma (idCiudad = 1).
INSERT INTO Hotel (nombre, ubicacion, categoria, idCiudad) VALUES 
('Gran Hotel del Mar', 'Paseo Marítimo, 10, Palma', 5, 1),
('Hotel Palma Centro', 'Avinguda de Jaume III, 25, Palma', 4, 1),
('Boutique Hotel Casco Antiguo', 'Carrer de Sant Miquel, 5, Palma', 3, 1);

-- -----------------------------------------------------

-- 4. Inserción de 12 Habitaciones Físicas por Hotel

-- Habitaciones para el 'Gran Hotel del Mar' (idHotel = 1)
INSERT INTO Habitacion (numeroHabitacion, idTipoHabitacion, idHotel) VALUES 
('H1-101', 1, 1), ('H1-102', 1, 1), -- Doble Estándar (2)
('H1-201', 2, 1), ('H1-202', 2, 1), ('H1-203', 2, 1), ('H1-204', 2, 1), -- Doble Superior (4)
('H1-301', 3, 1), ('H1-302', 3, 1), ('H1-303', 3, 1), ('H1-304', 3, 1), ('H1-305', 3, 1), ('H1-306', 3, 1); -- Suite Junior (6)

-- Habitaciones para el 'Hotel Palma Centro' (idHotel = 2)
INSERT INTO Habitacion (numeroHabitacion, idTipoHabitacion, idHotel) VALUES 
('H2-101', 4, 2), ('H2-102', 4, 2), ('H2-103', 4, 2), -- Individual (3)
('H2-201', 1, 2), ('H2-202', 1, 2), ('H2-203', 1, 2), ('H2-204', 1, 2), ('H2-205', 1, 2), -- Doble Estándar (5)
('H2-301', 2, 2), ('H2-302', 2, 2), ('H2-303', 2, 2), ('H2-304', 2, 2); -- Doble Superior (4)

-- Habitaciones para el 'Boutique Hotel Casco Antiguo' (idHotel = 3)
INSERT INTO Habitacion (numeroHabitacion, idTipoHabitacion, idHotel) VALUES 
('H3-11', 1, 3), ('H3-12', 1, 3), ('H3-13', 1, 3), ('H3-14', 1, 3), ('H3-15', 1, 3), ('H3-16', 1, 3), ('H3-17', 1, 3), ('H3-18', 1, 3), -- Doble Estándar (8)
('H3-21', 2, 3), ('H3-22', 2, 3), ('H3-23', 2, 3), ('H3-24', 2, 3); -- Doble Superior (4)

-- -----------------------------------------------------

-- 5. Inserción de Regímenes (planes de alimentación)
INSERT INTO Regimen (codigo) VALUES 
('SA'),  -- Solo Alojamiento
('AD'),  -- Alojamiento y Desayuno
('MP'),  -- Media Pensión
('PC'),  -- Pensión Completa
('TI');  -- Todo Incluido

-- -----------------------------------------------------

-- 6. Inserción de Tarifas (precios base por tipo de habitación)
INSERT INTO Tarifa (codigo, precio) VALUES 
('TARIFA_IND_2024', 80.00),     -- Tarifa 1: Individual
('TARIFA_DBL_EST_2024', 120.00), -- Tarifa 2: Doble Estándar
('TARIFA_DBL_SUP_2024', 150.00), -- Tarifa 3: Doble Superior
('TARIFA_SUITE_2024', 220.00);   -- Tarifa 4: Suite Junior

-- -----------------------------------------------------

-- 7. Asociación Hotel-Tarifa por tipo de habitación
-- Gran Hotel del Mar (idHotel = 1)
INSERT INTO Hotel_Tarifa (idHotel, idTipoHabitacion, idTarifa) VALUES 
(1, 1, 2),  -- Doble Estándar: 120€
(1, 2, 3),  -- Doble Superior: 150€
(1, 3, 4);  -- Suite Junior: 220€

-- Hotel Palma Centro (idHotel = 2)
INSERT INTO Hotel_Tarifa (idHotel, idTipoHabitacion, idTarifa) VALUES 
(2, 4, 1),  -- Individual: 80€
(2, 1, 2),  -- Doble Estándar: 120€
(2, 2, 3);  -- Doble Superior: 150€

-- Boutique Hotel Casco Antiguo (idHotel = 3)
INSERT INTO Hotel_Tarifa (idHotel, idTipoHabitacion, idTarifa) VALUES 
(3, 1, 2),  -- Doble Estándar: 120€
(3, 2, 3);  -- Doble Superior: 150€

-- -----------------------------------------------------

-- 8. Inserción de Precios de Regímenes por Hotel
-- Gran Hotel del Mar (idHotel = 1)
INSERT INTO PrecioRegimen (precio, idHotel, idRegimen) VALUES 
(0.00, 1, 1),    -- SA (Solo Alojamiento): 0€
(15.00, 1, 2),   -- AD (Alojamiento + Desayuno): 15€
(35.00, 1, 3),   -- MP (Media Pensión): 35€
(55.00, 1, 4),   -- PC (Pensión Completa): 55€
(80.00, 1, 5);   -- TI (Todo Incluido): 80€

-- Hotel Palma Centro (idHotel = 2)
INSERT INTO PrecioRegimen (precio, idHotel, idRegimen) VALUES 
(0.00, 2, 1),    -- SA: 0€
(12.00, 2, 2),   -- AD: 12€
(30.00, 2, 3),   -- MP: 30€
(50.00, 2, 4),   -- PC: 50€
(70.00, 2, 5);   -- TI: 70€

-- Boutique Hotel Casco Antiguo (idHotel = 3)
INSERT INTO PrecioRegimen (precio, idHotel, idRegimen) VALUES 
(0.00, 3, 1),    -- SA: 0€
(10.00, 3, 2),   -- AD: 10€
(25.00, 3, 3),   -- MP: 25€
(45.00, 3, 4),   -- PC: 45€
(65.00, 3, 5);   -- TI: 65€

-- -----------------------------------------------------

-- 9. Inserción de Servicios adicionales
INSERT INTO Servicio (codigoServicio, Precio) VALUES 
('SPA', 35.00),
('MASAJE', 50.00),
('GYM', 10.00),
('MINIBAR', 15.00),
('PARKING', 12.00),
('LATECHK', 25.00);

-- -----------------------------------------------------

-- 10. Inserción de Clientes de ejemplo
INSERT INTO Cliente (nombre, apellidos, correoElectronico, DNI, fechaDeNacimiento) VALUES 
('Ana', 'García López', 'ana.garcia@email.com', '12345678A', '1985-03-15'),
('Carlos', 'Martínez Ruiz', 'carlos.martinez@email.com', '23456789B', '1990-07-22'),
('Elena', 'Fernández Sanz', 'elena.fernandez@email.com', '34567890C', '1988-11-30'),
('David', 'López Pérez', 'david.lopez@email.com', '45678901D', '1992-05-10'),
('María', 'Sánchez Torres', 'maria.sanchez@email.com', '56789012E', '1987-09-18');

-- -----------------------------------------------------
-- Script de inserción finalizado.
-- -----------------------------------------------------
-- -----------------------------------------------------
-- SCRIPT COMPLETO DE INSERCIÓN DE DATOS INICIALES
-- -----------------------------------------------------

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
-- Script de inserción finalizado.
-- -----------------------------------------------------
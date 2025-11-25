-- -----------------------------------------------------
-- Script de Creación de Base de Datos para PMS
-- Versión: 2.3 (Corregida - UTF8)
-- -----------------------------------------------------

-- Establecer codificación UTF-8 para la sesión
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;

-- Se eliminan las tablas si ya existen para permitir una nueva creación desde cero.
DROP TABLE IF EXISTS Servicio_Pernoctacion;
DROP TABLE IF EXISTS Reserva_Descuento;
DROP TABLE IF EXISTS Reserva_Huespedes;
DROP TABLE IF EXISTS PagoEfectivo;
DROP TABLE IF EXISTS PagoTarjeta;
DROP TABLE IF EXISTS TipoPago;
DROP TABLE IF EXISTS Contrato;
DROP TABLE IF EXISTS Pernoctacion;
DROP TABLE IF EXISTS Reserva;
DROP TABLE IF EXISTS Hotel_Tarifa;
DROP TABLE IF EXISTS Hotel_TipoHabitacion;
DROP TABLE IF EXISTS Tarifa;
DROP TABLE IF EXISTS Descuento;
DROP TABLE IF EXISTS Servicio;
DROP TABLE IF EXISTS PrecioRegimen;
DROP TABLE IF EXISTS Regimen;
DROP TABLE IF EXISTS Cliente;
DROP TABLE IF EXISTS Habitacion;
DROP TABLE IF EXISTS TipoHabitacion;
DROP TABLE IF EXISTS Hotel;
DROP TABLE IF EXISTS Ciudad;


-- -----------------------------------------------------
-- Entidades de Configuración y Catálogos
-- -----------------------------------------------------

-- Tabla para Ciudades (MOVIDA PARA CORREGIR ORDEN DE CREACIÓN)
CREATE TABLE Ciudad (
  idCiudad INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  pais VARCHAR(100) NOT NULL
);

-- Tabla para almacenar los hoteles
CREATE TABLE Hotel (
  idHotel INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  ubicacion VARCHAR(255) NOT NULL,
  categoria INT NOT NULL COMMENT 'Ej: 3, 4, 5 estrellas',
  idCiudad INT NOT NULL,
  FOREIGN KEY (idCiudad) REFERENCES Ciudad(idCiudad) ON DELETE RESTRICT
);

-- Tabla para los tipos de habitación (Doble, Individual, Suite, etc.)
CREATE TABLE TipoHabitacion (
  idTipoHabitacion INT AUTO_INCREMENT PRIMARY KEY,
  categoria VARCHAR(50) NOT NULL UNIQUE,
  camasIndividuales INT DEFAULT 0,
  camasDobles INT DEFAULT 0,
  foto_url VARCHAR(500) DEFAULT NULL COMMENT 'URL de la foto de la habitación'
);

-- Tabla para las habitaciones físicas del hotel
CREATE TABLE Habitacion (
  numeroHabitacion VARCHAR(10) PRIMARY KEY,
  idTipoHabitacion INT NOT NULL,
  idHotel INT NOT NULL,
  FOREIGN KEY (idTipoHabitacion) REFERENCES TipoHabitacion(idTipoHabitacion) ON DELETE RESTRICT,
  FOREIGN KEY (idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE
);

-- Tabla para los regímenes de alojamiento (Solo Alojamiento, Media Pensión, etc.)
CREATE TABLE Regimen (
  idRegimen INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(10) NOT NULL UNIQUE
);

-- Tabla para almacenar los precios de los regímenes, asociados a un hotel
CREATE TABLE PrecioRegimen (
    idPrecioRegimen INT AUTO_INCREMENT PRIMARY KEY,
    idRegimen INT NOT NULL,
    idHotel INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (idRegimen) REFERENCES Regimen(idRegimen) ON DELETE CASCADE,
    FOREIGN KEY (idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE
);

-- Tabla para los servicios adicionales que ofrece el hotel
CREATE TABLE Servicio (
  codigoServicio VARCHAR(10) PRIMARY KEY,
  Precio DECIMAL(10, 2) NOT NULL
);

-- Tabla para las tarifas de las habitaciones
CREATE TABLE Tarifa (
  idTarifa INT AUTO_INCREMENT PRIMARY KEY,
  codigo VARCHAR(50) NOT NULL COMMENT 'Ej: TARIFA_ALTA_2025',
  precio DECIMAL(10, 2) NOT NULL
);

-- Tabla para los descuentos aplicables
CREATE TABLE Descuento (
  idDescuento INT AUTO_INCREMENT PRIMARY KEY,
  descripcion VARCHAR(255) NOT NULL,
  monto DECIMAL(10, 2) NOT NULL
);


-- -----------------------------------------------------
-- Entidades Principales y de Transacción
-- -----------------------------------------------------

-- Tabla para los clientes
CREATE TABLE Cliente (
  idCliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellidos VARCHAR(150) NOT NULL,
  correoElectronico VARCHAR(255) NOT NULL UNIQUE,
  fechaDeNacimiento DATE,
  DNI VARCHAR(20) NOT NULL UNIQUE,
  email VARCHAR(255) UNIQUE COMMENT 'Email para login',
  password VARCHAR(255) COMMENT 'Password hasheado para autenticación'
);

-- Tabla para las reservas
CREATE TABLE Reserva (
  idReserva INT AUTO_INCREMENT PRIMARY KEY,
  fechaEntrada DATE NOT NULL,
  fechaSalida DATE NOT NULL,
  canalReserva VARCHAR(50),
  tipo ENUM('Reserva', 'Walkin') NOT NULL,
  idCliente_paga INT NOT NULL,
  idPrecioRegimen INT NOT NULL,
  FOREIGN KEY (idCliente_paga) REFERENCES Cliente(idCliente) ON DELETE RESTRICT,
  FOREIGN KEY (idPrecioRegimen) REFERENCES PrecioRegimen(idPrecioRegimen) ON DELETE RESTRICT
);

-- Tabla para las pernoctaciones (noches) de una reserva
CREATE TABLE Pernoctacion (
  idPernoctacion INT AUTO_INCREMENT PRIMARY KEY,
  fechaPernoctacion DATE NOT NULL,
  idReserva INT NOT NULL,
  idTipoHabitacion INT NOT NULL,
  FOREIGN KEY (idReserva) REFERENCES Reserva(idReserva) ON DELETE CASCADE,
  FOREIGN KEY (idTipoHabitacion) REFERENCES TipoHabitacion(idTipoHabitacion) ON DELETE RESTRICT
);

-- Tabla para los contratos, que materializan una reserva
CREATE TABLE Contrato (
  idContrato INT AUTO_INCREMENT PRIMARY KEY,
  montoTotal DECIMAL(10, 2) NOT NULL,
  fechaCheckIn DATETIME NULL,
  fechaCheckOut DATETIME NULL,
  idReserva INT NOT NULL UNIQUE,
  numeroHabitacion VARCHAR(10) NOT NULL,
  FOREIGN KEY (idReserva) REFERENCES Reserva(idReserva) ON DELETE RESTRICT,
  FOREIGN KEY (numeroHabitacion) REFERENCES Habitacion(numeroHabitacion) ON DELETE RESTRICT
);

-- -----------------------------------------------------
-- Tablas de Pago (Estrategia: Tabla por Clase)
-- -----------------------------------------------------

-- Tabla padre para los pagos (MODIFICADA: Sin cláusula CHECK)
CREATE TABLE TipoPago (
  idTipoPago INT AUTO_INCREMENT PRIMARY KEY,
  montoPagado DECIMAL(10, 2) NOT NULL,
  idReserva INT NULL COMMENT 'Se rellena si es un prepago',
  idContrato INT NULL COMMENT 'Se rellena si el pago es en el hotel',
  FOREIGN KEY (idReserva) REFERENCES Reserva(idReserva) ON DELETE SET NULL,
  FOREIGN KEY (idContrato) REFERENCES Contrato(idContrato) ON DELETE SET NULL
);

-- Tabla hija para pagos en efectivo
CREATE TABLE PagoEfectivo (
  idTipoPago INT PRIMARY KEY,
  cambio DECIMAL(10, 2) DEFAULT 0.00,
  FOREIGN KEY (idTipoPago) REFERENCES TipoPago(idTipoPago) ON DELETE CASCADE
);

-- Tabla hija para pagos con tarjeta
CREATE TABLE PagoTarjeta (
  idTipoPago INT PRIMARY KEY,
  numeroTarjeta VARCHAR(20) NOT NULL,
  fechaExpiracion DATE NOT NULL,
  nombre_titular VARCHAR(150) NOT NULL,
  idCliente INT NOT NULL,
  FOREIGN KEY (idTipoPago) REFERENCES TipoPago(idTipoPago) ON DELETE CASCADE,
  FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente) ON DELETE RESTRICT
);


-- -----------------------------------------------------
-- Tablas Asociativas (Relaciones N:M)
-- -----------------------------------------------------

CREATE TABLE Hotel_TipoHabitacion (
  idHotel INT NOT NULL,
  idTipoHabitacion INT NOT NULL,
  PRIMARY KEY (idHotel, idTipoHabitacion),
  FOREIGN KEY (idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE,
  FOREIGN KEY (idTipoHabitacion) REFERENCES TipoHabitacion(idTipoHabitacion) ON DELETE CASCADE
);

CREATE TABLE Hotel_Tarifa (
  idHotel INT NOT NULL,
  idTarifa INT NOT NULL,
  idTipoHabitacion INT NOT NULL,
  PRIMARY KEY (idHotel, idTarifa, idTipoHabitacion),
  FOREIGN KEY (idHotel) REFERENCES Hotel(idHotel) ON DELETE CASCADE,
  FOREIGN KEY (idTarifa) REFERENCES Tarifa(idTarifa) ON DELETE CASCADE,
  FOREIGN KEY (idTipoHabitacion) REFERENCES TipoHabitacion(idTipoHabitacion) ON DELETE CASCADE
);

CREATE TABLE Reserva_Huespedes (
  idReserva INT NOT NULL,
  idCliente INT NOT NULL,
  PRIMARY KEY (idReserva, idCliente),
  FOREIGN KEY (idReserva) REFERENCES Reserva(idReserva) ON DELETE CASCADE,
  FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente) ON DELETE CASCADE
);

CREATE TABLE Reserva_Descuento (
  idReserva INT NOT NULL,
  idDescuento INT NOT NULL,
  PRIMARY KEY (idReserva, idDescuento),
  FOREIGN KEY (idReserva) REFERENCES Reserva(idReserva) ON DELETE CASCADE,
  FOREIGN KEY (idDescuento) REFERENCES Descuento(idDescuento) ON DELETE RESTRICT
);

CREATE TABLE Servicio_Pernoctacion (
  idPernoctacion INT NOT NULL,
  codigoServicio VARCHAR(10) NOT NULL,
  PRIMARY KEY (idPernoctacion, codigoServicio),
  FOREIGN KEY (idPernoctacion) REFERENCES Pernoctacion(idPernoctacion) ON DELETE CASCADE,
  FOREIGN KEY (codigoServicio) REFERENCES Servicio(codigoServicio) ON DELETE CASCADE
);

-- -----------------------------------------------------
-- Triggers para validar la tabla TipoPago
-- -----------------------------------------------------

-- Trigger para validar ANTES de insertar un nuevo pago
DELIMITER $$
CREATE TRIGGER before_tipopago_insert
BEFORE INSERT ON TipoPago
FOR EACH ROW
BEGIN
    IF (NEW.idReserva IS NOT NULL AND NEW.idContrato IS NOT NULL) OR (NEW.idReserva IS NULL AND NEW.idContrato IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un pago debe estar asociado a una reserva O a un contrato, pero no a ambos o a ninguno.';
    END IF;
END$$
DELIMITER ;

-- Trigger para validar ANTES de actualizar un pago existente
DELIMITER $$
CREATE TRIGGER before_tipopago_update
BEFORE UPDATE ON TipoPago
FOR EACH ROW
BEGIN
    IF (NEW.idReserva IS NOT NULL AND NEW.idContrato IS NOT NULL) OR (NEW.idReserva IS NULL AND NEW.idContrato IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un pago debe estar asociado a una reserva O a un contrato, pero no a ambos o a ninguno.';
    END IF;
END$$
DELIMITER ;
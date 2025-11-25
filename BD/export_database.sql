/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.0.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: PMS54870695D
-- ------------------------------------------------------
-- Server version	12.0.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `ciudad`
--

DROP TABLE IF EXISTS `ciudad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciudad` (
  `idCiudad` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `pais` varchar(100) NOT NULL,
  PRIMARY KEY (`idCiudad`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciudad`
--

LOCK TABLES `ciudad` WRITE;
/*!40000 ALTER TABLE `ciudad` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `ciudad` VALUES
(1,'Palma','Espa├▒a');
/*!40000 ALTER TABLE `ciudad` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idCliente` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(150) NOT NULL,
  `correoElectronico` varchar(255) NOT NULL,
  `fechaDeNacimiento` date DEFAULT NULL,
  `DNI` varchar(20) NOT NULL,
  PRIMARY KEY (`idCliente`),
  UNIQUE KEY `correoElectronico` (`correoElectronico`),
  UNIQUE KEY `DNI` (`DNI`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `cliente` VALUES
(1,'Ana','Garc├¡a L├│pez','ana.garcia@email.com','1985-03-15','12345678A'),
(2,'Carlos','Mart├¡nez Ruiz','carlos.martinez@email.com','1990-07-22','23456789B'),
(3,'Elena','Fern├índez Sanz','elena.fernandez@email.com','1988-11-30','34567890C'),
(4,'David','L├│pez P├®rez','david.lopez@email.com','1992-05-10','45678901D'),
(5,'Mar├¡a','S├ínchez Torres','maria.sanchez@email.com','1987-09-18','56789012E');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `contrato`
--

DROP TABLE IF EXISTS `contrato`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `contrato` (
  `idContrato` int(11) NOT NULL AUTO_INCREMENT,
  `montoTotal` decimal(10,2) NOT NULL,
  `fechaCheckIn` datetime DEFAULT NULL,
  `fechaCheckOut` datetime DEFAULT NULL,
  `idReserva` int(11) NOT NULL,
  `numeroHabitacion` varchar(10) NOT NULL,
  PRIMARY KEY (`idContrato`),
  UNIQUE KEY `idReserva` (`idReserva`),
  KEY `numeroHabitacion` (`numeroHabitacion`),
  CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`),
  CONSTRAINT `contrato_ibfk_2` FOREIGN KEY (`numeroHabitacion`) REFERENCES `habitacion` (`numeroHabitacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contrato`
--

LOCK TABLES `contrato` WRITE;
/*!40000 ALTER TABLE `contrato` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `contrato` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `descuento`
--

DROP TABLE IF EXISTS `descuento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `descuento` (
  `idDescuento` int(11) NOT NULL AUTO_INCREMENT,
  `descripcion` varchar(255) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idDescuento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `descuento`
--

LOCK TABLES `descuento` WRITE;
/*!40000 ALTER TABLE `descuento` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `descuento` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `habitacion`
--

DROP TABLE IF EXISTS `habitacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `habitacion` (
  `numeroHabitacion` varchar(10) NOT NULL,
  `idTipoHabitacion` int(11) NOT NULL,
  `idHotel` int(11) NOT NULL,
  PRIMARY KEY (`numeroHabitacion`),
  KEY `idTipoHabitacion` (`idTipoHabitacion`),
  KEY `idHotel` (`idHotel`),
  CONSTRAINT `habitacion_ibfk_1` FOREIGN KEY (`idTipoHabitacion`) REFERENCES `tipohabitacion` (`idTipoHabitacion`),
  CONSTRAINT `habitacion_ibfk_2` FOREIGN KEY (`idHotel`) REFERENCES `hotel` (`idHotel`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `habitacion`
--

LOCK TABLES `habitacion` WRITE;
/*!40000 ALTER TABLE `habitacion` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `habitacion` VALUES
('H1-101',1,1),
('H1-102',1,1),
('H1-201',2,1),
('H1-202',2,1),
('H1-203',2,1),
('H1-204',2,1),
('H1-301',3,1),
('H1-302',3,1),
('H1-303',3,1),
('H1-304',3,1),
('H1-305',3,1),
('H1-306',3,1),
('H2-101',4,2),
('H2-102',4,2),
('H2-103',4,2),
('H2-201',1,2),
('H2-202',1,2),
('H2-203',1,2),
('H2-204',1,2),
('H2-205',1,2),
('H2-301',2,2),
('H2-302',2,2),
('H2-303',2,2),
('H2-304',2,2),
('H3-11',1,3),
('H3-12',1,3),
('H3-13',1,3),
('H3-14',1,3),
('H3-15',1,3),
('H3-16',1,3),
('H3-17',1,3),
('H3-18',1,3),
('H3-21',2,3),
('H3-22',2,3),
('H3-23',2,3),
('H3-24',2,3);
/*!40000 ALTER TABLE `habitacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `hotel`
--

DROP TABLE IF EXISTS `hotel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel` (
  `idHotel` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `ubicacion` varchar(255) NOT NULL,
  `categoria` int(11) NOT NULL COMMENT 'Ej: 3, 4, 5 estrellas',
  `idCiudad` int(11) NOT NULL,
  PRIMARY KEY (`idHotel`),
  KEY `idCiudad` (`idCiudad`),
  CONSTRAINT `hotel_ibfk_1` FOREIGN KEY (`idCiudad`) REFERENCES `ciudad` (`idCiudad`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel`
--

LOCK TABLES `hotel` WRITE;
/*!40000 ALTER TABLE `hotel` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `hotel` VALUES
(1,'Gran Hotel del Mar','Paseo Mar├¡timo, 10, Palma',5,1),
(2,'Hotel Palma Centro','Avinguda de Jaume III, 25, Palma',4,1),
(3,'Boutique Hotel Casco Antiguo','Carrer de Sant Miquel, 5, Palma',3,1);
/*!40000 ALTER TABLE `hotel` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `hotel_tarifa`
--

DROP TABLE IF EXISTS `hotel_tarifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_tarifa` (
  `idHotel` int(11) NOT NULL,
  `idTarifa` int(11) NOT NULL,
  `idTipoHabitacion` int(11) NOT NULL,
  PRIMARY KEY (`idHotel`,`idTarifa`,`idTipoHabitacion`),
  KEY `idTarifa` (`idTarifa`),
  KEY `idTipoHabitacion` (`idTipoHabitacion`),
  CONSTRAINT `hotel_tarifa_ibfk_1` FOREIGN KEY (`idHotel`) REFERENCES `hotel` (`idHotel`) ON DELETE CASCADE,
  CONSTRAINT `hotel_tarifa_ibfk_2` FOREIGN KEY (`idTarifa`) REFERENCES `tarifa` (`idTarifa`) ON DELETE CASCADE,
  CONSTRAINT `hotel_tarifa_ibfk_3` FOREIGN KEY (`idTipoHabitacion`) REFERENCES `tipohabitacion` (`idTipoHabitacion`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_tarifa`
--

LOCK TABLES `hotel_tarifa` WRITE;
/*!40000 ALTER TABLE `hotel_tarifa` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `hotel_tarifa` VALUES
(2,1,4),
(1,2,1),
(2,2,1),
(3,2,1),
(1,3,2),
(2,3,2),
(3,3,2),
(1,4,3);
/*!40000 ALTER TABLE `hotel_tarifa` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `hotel_tipohabitacion`
--

DROP TABLE IF EXISTS `hotel_tipohabitacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hotel_tipohabitacion` (
  `idHotel` int(11) NOT NULL,
  `idTipoHabitacion` int(11) NOT NULL,
  PRIMARY KEY (`idHotel`,`idTipoHabitacion`),
  KEY `idTipoHabitacion` (`idTipoHabitacion`),
  CONSTRAINT `hotel_tipohabitacion_ibfk_1` FOREIGN KEY (`idHotel`) REFERENCES `hotel` (`idHotel`) ON DELETE CASCADE,
  CONSTRAINT `hotel_tipohabitacion_ibfk_2` FOREIGN KEY (`idTipoHabitacion`) REFERENCES `tipohabitacion` (`idTipoHabitacion`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hotel_tipohabitacion`
--

LOCK TABLES `hotel_tipohabitacion` WRITE;
/*!40000 ALTER TABLE `hotel_tipohabitacion` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `hotel_tipohabitacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pagoefectivo`
--

DROP TABLE IF EXISTS `pagoefectivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagoefectivo` (
  `idTipoPago` int(11) NOT NULL,
  `cambio` decimal(10,2) DEFAULT 0.00,
  PRIMARY KEY (`idTipoPago`),
  CONSTRAINT `pagoefectivo_ibfk_1` FOREIGN KEY (`idTipoPago`) REFERENCES `tipopago` (`idTipoPago`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagoefectivo`
--

LOCK TABLES `pagoefectivo` WRITE;
/*!40000 ALTER TABLE `pagoefectivo` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `pagoefectivo` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pagotarjeta`
--

DROP TABLE IF EXISTS `pagotarjeta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagotarjeta` (
  `idTipoPago` int(11) NOT NULL,
  `numeroTarjeta` varchar(20) NOT NULL,
  `fechaExpiracion` date NOT NULL,
  `nombre_titular` varchar(150) NOT NULL,
  `idCliente` int(11) NOT NULL,
  PRIMARY KEY (`idTipoPago`),
  KEY `idCliente` (`idCliente`),
  CONSTRAINT `pagotarjeta_ibfk_1` FOREIGN KEY (`idTipoPago`) REFERENCES `tipopago` (`idTipoPago`) ON DELETE CASCADE,
  CONSTRAINT `pagotarjeta_ibfk_2` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagotarjeta`
--

LOCK TABLES `pagotarjeta` WRITE;
/*!40000 ALTER TABLE `pagotarjeta` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `pagotarjeta` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `pernoctacion`
--

DROP TABLE IF EXISTS `pernoctacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pernoctacion` (
  `idPernoctacion` int(11) NOT NULL AUTO_INCREMENT,
  `fechaPernoctacion` date NOT NULL,
  `idReserva` int(11) NOT NULL,
  `idTipoHabitacion` int(11) NOT NULL,
  PRIMARY KEY (`idPernoctacion`),
  KEY `idReserva` (`idReserva`),
  KEY `idTipoHabitacion` (`idTipoHabitacion`),
  CONSTRAINT `pernoctacion_ibfk_1` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE CASCADE,
  CONSTRAINT `pernoctacion_ibfk_2` FOREIGN KEY (`idTipoHabitacion`) REFERENCES `tipohabitacion` (`idTipoHabitacion`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pernoctacion`
--

LOCK TABLES `pernoctacion` WRITE;
/*!40000 ALTER TABLE `pernoctacion` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `pernoctacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `precioregimen`
--

DROP TABLE IF EXISTS `precioregimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `precioregimen` (
  `idPrecioRegimen` int(11) NOT NULL AUTO_INCREMENT,
  `idRegimen` int(11) NOT NULL,
  `idHotel` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idPrecioRegimen`),
  KEY `idRegimen` (`idRegimen`),
  KEY `idHotel` (`idHotel`),
  CONSTRAINT `precioregimen_ibfk_1` FOREIGN KEY (`idRegimen`) REFERENCES `regimen` (`idRegimen`) ON DELETE CASCADE,
  CONSTRAINT `precioregimen_ibfk_2` FOREIGN KEY (`idHotel`) REFERENCES `hotel` (`idHotel`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `precioregimen`
--

LOCK TABLES `precioregimen` WRITE;
/*!40000 ALTER TABLE `precioregimen` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `precioregimen` VALUES
(1,1,1,0.00),
(2,2,1,15.00),
(3,3,1,35.00),
(4,4,1,55.00),
(5,5,1,80.00),
(6,1,2,0.00),
(7,2,2,12.00),
(8,3,2,30.00),
(9,4,2,50.00),
(10,5,2,70.00),
(11,1,3,0.00),
(12,2,3,10.00),
(13,3,3,25.00),
(14,4,3,45.00),
(15,5,3,65.00);
/*!40000 ALTER TABLE `precioregimen` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `regimen`
--

DROP TABLE IF EXISTS `regimen`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `regimen` (
  `idRegimen` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(10) NOT NULL,
  PRIMARY KEY (`idRegimen`),
  UNIQUE KEY `codigo` (`codigo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `regimen`
--

LOCK TABLES `regimen` WRITE;
/*!40000 ALTER TABLE `regimen` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `regimen` VALUES
(2,'AD'),
(3,'MP'),
(4,'PC'),
(1,'SA'),
(5,'TI');
/*!40000 ALTER TABLE `regimen` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `idReserva` int(11) NOT NULL AUTO_INCREMENT,
  `fechaEntrada` date NOT NULL,
  `fechaSalida` date NOT NULL,
  `canalReserva` varchar(50) DEFAULT NULL,
  `tipo` enum('Reserva','Walkin') NOT NULL,
  `idCliente_paga` int(11) NOT NULL,
  `idPrecioRegimen` int(11) NOT NULL,
  PRIMARY KEY (`idReserva`),
  KEY `idCliente_paga` (`idCliente_paga`),
  KEY `idPrecioRegimen` (`idPrecioRegimen`),
  CONSTRAINT `reserva_ibfk_1` FOREIGN KEY (`idCliente_paga`) REFERENCES `cliente` (`idCliente`),
  CONSTRAINT `reserva_ibfk_2` FOREIGN KEY (`idPrecioRegimen`) REFERENCES `precioregimen` (`idPrecioRegimen`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reserva_descuento`
--

DROP TABLE IF EXISTS `reserva_descuento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_descuento` (
  `idReserva` int(11) NOT NULL,
  `idDescuento` int(11) NOT NULL,
  PRIMARY KEY (`idReserva`,`idDescuento`),
  KEY `idDescuento` (`idDescuento`),
  CONSTRAINT `reserva_descuento_ibfk_1` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE CASCADE,
  CONSTRAINT `reserva_descuento_ibfk_2` FOREIGN KEY (`idDescuento`) REFERENCES `descuento` (`idDescuento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_descuento`
--

LOCK TABLES `reserva_descuento` WRITE;
/*!40000 ALTER TABLE `reserva_descuento` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `reserva_descuento` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `reserva_huespedes`
--

DROP TABLE IF EXISTS `reserva_huespedes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva_huespedes` (
  `idReserva` int(11) NOT NULL,
  `idCliente` int(11) NOT NULL,
  PRIMARY KEY (`idReserva`,`idCliente`),
  KEY `idCliente` (`idCliente`),
  CONSTRAINT `reserva_huespedes_ibfk_1` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE CASCADE,
  CONSTRAINT `reserva_huespedes_ibfk_2` FOREIGN KEY (`idCliente`) REFERENCES `cliente` (`idCliente`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva_huespedes`
--

LOCK TABLES `reserva_huespedes` WRITE;
/*!40000 ALTER TABLE `reserva_huespedes` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `reserva_huespedes` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `servicio`
--

DROP TABLE IF EXISTS `servicio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio` (
  `codigoServicio` varchar(10) NOT NULL,
  `Precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`codigoServicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio`
--

LOCK TABLES `servicio` WRITE;
/*!40000 ALTER TABLE `servicio` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `servicio` VALUES
('GYM',10.00),
('LATECHK',25.00),
('MASAJE',50.00),
('MINIBAR',15.00),
('PARKING',12.00),
('SPA',35.00);
/*!40000 ALTER TABLE `servicio` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `servicio_pernoctacion`
--

DROP TABLE IF EXISTS `servicio_pernoctacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicio_pernoctacion` (
  `idPernoctacion` int(11) NOT NULL,
  `codigoServicio` varchar(10) NOT NULL,
  PRIMARY KEY (`idPernoctacion`,`codigoServicio`),
  KEY `codigoServicio` (`codigoServicio`),
  CONSTRAINT `servicio_pernoctacion_ibfk_1` FOREIGN KEY (`idPernoctacion`) REFERENCES `pernoctacion` (`idPernoctacion`) ON DELETE CASCADE,
  CONSTRAINT `servicio_pernoctacion_ibfk_2` FOREIGN KEY (`codigoServicio`) REFERENCES `servicio` (`codigoServicio`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicio_pernoctacion`
--

LOCK TABLES `servicio_pernoctacion` WRITE;
/*!40000 ALTER TABLE `servicio_pernoctacion` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `servicio_pernoctacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tarifa`
--

DROP TABLE IF EXISTS `tarifa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tarifa` (
  `idTarifa` int(11) NOT NULL AUTO_INCREMENT,
  `codigo` varchar(50) NOT NULL COMMENT 'Ej: TARIFA_ALTA_2025',
  `precio` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idTarifa`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tarifa`
--

LOCK TABLES `tarifa` WRITE;
/*!40000 ALTER TABLE `tarifa` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tarifa` VALUES
(1,'TARIFA_IND_2024',80.00),
(2,'TARIFA_DBL_EST_2024',120.00),
(3,'TARIFA_DBL_SUP_2024',150.00),
(4,'TARIFA_SUITE_2024',220.00);
/*!40000 ALTER TABLE `tarifa` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tipohabitacion`
--

DROP TABLE IF EXISTS `tipohabitacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipohabitacion` (
  `idTipoHabitacion` int(11) NOT NULL AUTO_INCREMENT,
  `categoria` varchar(50) NOT NULL,
  `camasIndividuales` int(11) DEFAULT 0,
  `camasDobles` int(11) DEFAULT 0,
  PRIMARY KEY (`idTipoHabitacion`),
  UNIQUE KEY `categoria` (`categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipohabitacion`
--

LOCK TABLES `tipohabitacion` WRITE;
/*!40000 ALTER TABLE `tipohabitacion` DISABLE KEYS */;
set autocommit=0;
INSERT INTO `tipohabitacion` VALUES
(1,'Doble Est├índar',0,1),
(2,'Doble Superior',0,1),
(3,'Suite Junior',0,2),
(4,'Individual',1,0);
/*!40000 ALTER TABLE `tipohabitacion` ENABLE KEYS */;
UNLOCK TABLES;
commit;

--
-- Table structure for table `tipopago`
--

DROP TABLE IF EXISTS `tipopago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `tipopago` (
  `idTipoPago` int(11) NOT NULL AUTO_INCREMENT,
  `montoPagado` decimal(10,2) NOT NULL,
  `idReserva` int(11) DEFAULT NULL COMMENT 'Se rellena si es un prepago',
  `idContrato` int(11) DEFAULT NULL COMMENT 'Se rellena si el pago es en el hotel',
  PRIMARY KEY (`idTipoPago`),
  KEY `idReserva` (`idReserva`),
  KEY `idContrato` (`idContrato`),
  CONSTRAINT `tipopago_ibfk_1` FOREIGN KEY (`idReserva`) REFERENCES `reserva` (`idReserva`) ON DELETE SET NULL,
  CONSTRAINT `tipopago_ibfk_2` FOREIGN KEY (`idContrato`) REFERENCES `contrato` (`idContrato`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tipopago`
--

LOCK TABLES `tipopago` WRITE;
/*!40000 ALTER TABLE `tipopago` DISABLE KEYS */;
set autocommit=0;
/*!40000 ALTER TABLE `tipopago` ENABLE KEYS */;
UNLOCK TABLES;
commit;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER before_tipopago_insert
BEFORE INSERT ON TipoPago
FOR EACH ROW
BEGIN
    IF (NEW.idReserva IS NOT NULL AND NEW.idContrato IS NOT NULL) OR (NEW.idReserva IS NULL AND NEW.idContrato IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un pago debe estar asociado a una reserva O a un contrato, pero no a ambos o a ninguno.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER before_tipopago_update
BEFORE UPDATE ON TipoPago
FOR EACH ROW
BEGIN
    IF (NEW.idReserva IS NOT NULL AND NEW.idContrato IS NOT NULL) OR (NEW.idReserva IS NULL AND NEW.idContrato IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Un pago debe estar asociado a una reserva O a un contrato, pero no a ambos o a ninguno.';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping routines for database 'PMS54870695D'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2025-11-14 23:09:34

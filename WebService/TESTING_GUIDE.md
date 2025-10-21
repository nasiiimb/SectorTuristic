# 🧪 Guía de Pruebas - Sistema de Gestión Hotelera con Prisma

Esta guía te ayudará a probar todos los endpoints implementados paso a paso. El sistema utiliza **identificadores naturales** (nombres, DNI, códigos) en lugar de IDs internos.

## 📋 **Pre-requisitos**

Asegúrate de que:
1. El servidor esté corriendo: `npm run dev`
2. La base de datos esté inicializada con: `cd BD && crear_bd.bat`
3. Tengas una herramienta para hacer peticiones HTTP:
   - **Navegador** (para peticiones GET)
   - **Postman**, **Thunder Client** o **Insomnia** (para todas las peticiones)
   - **PowerShell** con `Invoke-WebRequest` o `curl`

---

## 🏨 **Datos de Prueba Disponibles**

### 📌 **Flujo de Reserva y Check-in**

**1. Crear Cliente (opcional DNI y fecha nacimiento)**
```json
{
  "nombre": "Juan",
  "apellidos": "Pérez",
  "correoElectronico": "juan@email.com"
  // DNI y fechaDeNacimiento son OPCIONALES
}
```

**2. Crear Reserva**
- Solo requiere identificar al cliente que paga (por DNI o email)
- **NO** se especifican huéspedes en este paso

**3. Check-in (aquí se añaden los huéspedes)**
- Se especifican los DNIs de todos los huéspedes
- Si algún cliente no tiene DNI, debe actualizarse antes: `PUT /api/clientes/:id`

---

### Hoteles:
- **Gran Hotel Miramar** - 5 estrellas, Palma, Mallorca, España
- **Hotel Mediterráneo** - 4 estrellas, Palma, Mallorca, España  
- **Hostal Sa Plaça** - 3 estrellas, Palma, Mallorca, España

### Clientes:
- **Juan Pérez** - DNI: 12345678A
- **María García** - DNI: 87654321B
- **Pedro López** - DNI: 11223344C

### Tipos de Habitación:
- Individual
- Doble Estándar
- Doble Superior
- Suite Junior

### Sistema de Tarifas:
- 5★: Individual (120€), Doble Estándar (150€), Doble Superior (200€), Suite (300€)
- 4★: Individual (90€), Doble Estándar (110€), Doble Superior (150€), Suite (220€)
- 3★: Individual (60€), Doble Estándar (75€), Doble Superior (100€), Suite (150€)

---

## 🧪 **Pruebas por Categoría**

### 1️⃣ **Disponibilidad de Habitaciones** 🔍

**⚠️ IMPORTANTE**: Este endpoint cuenta las **reservas activas** (pernoctaciones) para calcular disponibilidad real.

#### Buscar por nombre de hotel
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Respuesta esperada:**
```json
{
  "hotel": {
    "nombre": "Gran Hotel Miramar",
    "ubicacion": "Paseo Marítimo 33",
    "categoria": "5 estrellas",
    "ciudad": "Palma",
    "pais": "España"
  },
  "tiposDisponibles": [
    {
      "idTipoHabitacion": 2,
      "categoria": "Doble Estándar",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "150",
      "codigoTarifa": "TARIFA_5E_DBL_STD",
      "disponibles": 4,
      "totalHabitaciones": 4,
      "reservasActuales": 0
    },
    {
      "categoria": "Doble Superior",
      "precioPorNoche": "200",
      "disponibles": 4,
      "totalHabitaciones": 4,
      "reservasActuales": 0
    },
    {
      "categoria": "Suite Junior",
      "precioPorNoche": "300",
      "disponibles": 2,
      "totalHabitaciones": 2,
      "reservasActuales": 0
    }
  ],
  "totalTiposDisponibles": 3
}
```

#### Buscar por ciudad
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&ciudad=Palma
```

#### Buscar por país
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&pais=España
```

**Pruebas de Error:**
```http
# Sin fechas (debe dar error 400)
GET http://localhost:3000/api/disponibilidad?hotel=Gran

# Sin filtro de ubicación (debe dar error 400)
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05

# Fechas inválidas (debe dar error 400)
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-05&fechaSalida=2025-12-01&hotel=Gran

# Hotel inexistente (debe dar error 404)
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=HotelInexistente
```

---

### 2️⃣ **Crear Reserva con Validación de Disponibilidad** 📝

**⚠️ IMPORTANTE**: Al crear una reserva, se generan automáticamente:
- Registros de **Pernoctación** (uno por cada noche)
- Estos se cuentan en la disponibilidad para **prevenir overbooking**
- **Los huéspedes se especifican en el check-in**, no en la reserva
- **NO se requieren datos de pago** (el profesor indicó que no hace falta)

#### Crear una reserva válida (usando identificadores naturales)
```http
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "12345678A"
}
```

**Respuesta esperada (201 Created):**
```json
{
  "idReserva": 1,
  "fechaEntrada": "2025-12-01T00:00:00.000Z",
  "fechaSalida": "2025-12-05T00:00:00.000Z",
  "hotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "clientePaga": "Juan Pérez (12345678A)",
  "pernoctaciones": 4,
  "mensaje": "Reserva creada exitosamente"
}
```

#### Verificar que la disponibilidad se actualiza
```http
# Después de crear la reserva, consulta disponibilidad otra vez
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Deberías ver:**
```json
{
  "tiposDisponibles": [
    {
      "categoria": "Doble Superior",
      "disponibles": 3,        // ⬇️ Decrementó de 4 a 3
      "totalHabitaciones": 4,
      "reservasActuales": 1    // ⬆️ Incrementó de 0 a 1
    }
  ]
}
```

**Pruebas de Error:**

```http
# Sin parámetros requeridos (debe dar error 400)
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01"
}
```

```http
# Fechas inválidas (debe dar error 400)
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-05",
  "fechaSalida": "2025-12-01",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "12345678A"
}
```

```http
# Cliente inexistente (debe dar error 404)
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "99999999Z"
}
```

```http
# Sin disponibilidad (debe dar error 409 - Conflict)
# Primero crea 4 reservas de "Doble Superior" para llenar todas las habitaciones
# Luego intenta crear una quinta reserva
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "12345678A"
}
```

---

### 2.5️⃣ **Buscar Reservas por Cliente** 🔍

**⚠️ ÚTIL PARA EL PMS**: Buscar reservas por nombre/apellido del cliente.

#### Buscar por nombre
```http
GET http://localhost:3000/api/reservas/buscar/cliente?nombre=Juan
```

#### Buscar por apellido
```http
GET http://localhost:3000/api/reservas/buscar/cliente?apellido=Pérez
```

#### Buscar por nombre y apellido
```http
GET http://localhost:3000/api/reservas/buscar/cliente?nombre=Juan&apellido=Pérez
```

**Respuesta esperada (200 OK):**
```json
{
  "reservas": [
    {
      "idReserva": 1,
      "fechaEntrada": "2025-12-01T00:00:00.000Z",
      "fechaSalida": "2025-12-05T00:00:00.000Z",
      "clientePaga": {
        "nombre": "Juan",
        "apellidos": "Pérez",
        "DNI": "12345678A"
      },
      "precioRegimen": {
        "hotel": {
          "nombre": "Gran Hotel Miramar"
        }
      },
      "contrato": {
        "numeroHabitacion": "201"
      }
    }
  ],
  "total": 1,
  "filtros": {
    "nombre": "Juan",
    "apellido": "Pérez"
  }
}
```

**Pruebas de Error:**
```http
# Sin parámetros (debe dar error 400)
GET http://localhost:3000/api/reservas/buscar/cliente
```

**Nota**: Solo se pueden modificar ciertos campos. Las fechas y tipo de habitación requieren cancelar y crear nueva reserva.

```http
PUT http://localhost:3000/api/reservas/1
Content-Type: application/json

{
  "regimen": "Pensión Completa"
}
```

**Pruebas de Error:**

```http
# Modificar reserva inexistente (debe dar error 404)
PUT http://localhost:3000/api/reservas/99999
Content-Type: application/json

{
  "regimen": "Pensión Completa"
}
```

```http
# Modificar después de check-in (puede dar error 409 según lógica de negocio)
# Primero haz check-in, luego intenta modificar
PUT http://localhost:3000/api/reservas/1
Content-Type: application/json

{
  "regimen": "Pensión Completa"
}
```

---

### 4️⃣ **Check-in** 🔑

**⚠️ IMPORTANTE**: 
- El check-in asigna una **habitación física específica** (ej: habitación 101)
- Crea un **Contrato** vinculando la reserva con la habitación física
- **AQUÍ se especifican los huéspedes** (DNIs de quienes se alojan)
- **AQUÍ se completan los datos de los clientes** si no tenían DNI previamente
- Antes del check-in, asegúrate de que todos los clientes tengan su DNI registrado: `PUT /api/clientes/:id`
- **NO afecta la disponibilidad** (ya se contó en la reserva con las pernoctaciones)

#### Hacer check-in exitoso (usando nombre de hotel + número de habitación + huéspedes)
```http
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "101",
  "dniCliente": "12345678A",
  "dniHuespedes": ["12345678A", "87654321B"]
}
```

**Respuesta esperada (201 Created):**
```json
{
  "idContrato": 1,
  "numeroHabitacion": "101",
  "hotel": "Gran Hotel Miramar",
  "cliente": "Juan Pérez (12345678A)",
  "huespedes": [
    "Juan Pérez (12345678A)",
    "María García (87654321B)"
  ],
  "fechaEntrada": "2025-12-01T00:00:00.000Z",
  "fechaSalida": "2025-12-05T00:00:00.000Z",
  "estado": "Activo",
  "mensaje": "Check-in realizado exitosamente"
}
```

**Pruebas de Error:**

```http
# Sin datos requeridos (debe dar error 400)
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar"
}
```

```http
# Cliente sin reserva activa (debe dar error 404)
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "101",
  "dniCliente": "11223344C"
}
```

```http
# Check-in duplicado (debe dar error 409)
# Primero haz check-in exitoso, luego repite la misma petición
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "101",
  "dniCliente": "12345678A"
}
```

```http
# Habitación inexistente (debe dar error 404)
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "999",
  "dniCliente": "12345678A"
}
```

```http
# Tipo de habitación incorrecto (debe dar error 400)
# Reserva es para "Doble Superior" pero habitación 101 es "Individual"
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "101",
  "dniCliente": "12345678A"
}
```

---

### 5️⃣ **Check-out** 🚪

**⚠️ IMPORTANTE**: 
- El check-out cierra el contrato y marca la salida
- **NO afecta la disponibilidad** (las pernoctaciones ya están cerradas)
- Libera la habitación física para nuevas asignaciones

#### Hacer check-out (usando nombre de hotel + número de habitación)
```http
POST http://localhost:3000/api/checkout
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "101"
}
```

**Respuesta esperada (200 OK):**
```json
{
  "idContrato": 1,
  "numeroHabitacion": "101",
  "hotel": "Gran Hotel Miramar",
  "cliente": "Juan Pérez (12345678A)",
  "fechaEntrada": "2025-12-01T00:00:00.000Z",
  "fechaSalida": "2025-12-05T00:00:00.000Z",
  "fechaSalidaReal": "2025-12-05T10:30:00.000Z",
  "estado": "Finalizado",
  "mensaje": "Check-out realizado exitosamente"
}
```

**Pruebas de Error:**

```http
# Contrato inexistente (debe dar error 404)
POST http://localhost:3000/api/checkout
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "999"
}
```

```http
# Check-out sin check-in previo (debe dar error 404)
POST http://localhost:3000/api/checkout
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "102"
}
```

```http
# Check-out duplicado (debe dar error 409)
# Haz checkout exitoso, luego repite la petición
POST http://localhost:3000/api/checkout
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "101"
}
```

---

### 6️⃣ **Servicios Adicionales** 🍽️

#### Obtener todos los servicios disponibles
```http
GET http://localhost:3000/api/servicios
```

**Respuesta esperada:**
```json
{
  "servicios": [
    {
      "idServicio": 1,
      "nombre": "Spa y Masajes",
      "codigo": "SPA",
      "precio": "50.00"
    },
    {
      "nombre": "Alquiler de Bicicletas",
      "codigo": "BIKE",
      "precio": "15.00"
    }
  ],
  "total": 5
}
```

#### Añadir servicio a reserva (usando DNI del cliente)
```http
POST http://localhost:3000/api/servicios/agregar
Content-Type: application/json

{
  "dniCliente": "12345678A",
  "codigoServicio": "SPA",
  "fecha": "2025-12-02"
}
```

**Respuesta esperada:**
```json
{
  "idServicioContratado": 1,
  "servicio": "Spa y Masajes",
  "fecha": "2025-12-02T00:00:00.000Z",
  "precio": "50.00",
  "cliente": "Juan Pérez (12345678A)",
  "mensaje": "Servicio añadido exitosamente"
}
```

**Pruebas de Error:**

```http
# Sin datos requeridos (debe dar error 400)
POST http://localhost:3000/api/servicios/agregar
Content-Type: application/json

{
  "dniCliente": "12345678A"
}
```

```http
# Cliente sin reserva activa (debe dar error 404)
POST http://localhost:3000/api/servicios/agregar
Content-Type: application/json

{
  "dniCliente": "11223344C",
  "codigoServicio": "SPA",
  "fecha": "2025-12-02"
}
```

```http
# Servicio inexistente (debe dar error 404)
POST http://localhost:3000/api/servicios/agregar
Content-Type: application/json

{
  "dniCliente": "12345678A",
  "codigoServicio": "INEXISTENTE",
  "fecha": "2025-12-02"
}
```

```http
# Fecha fuera del rango de la reserva (debe dar error 400)
POST http://localhost:3000/api/servicios/agregar
Content-Type: application/json

{
  "dniCliente": "12345678A",
  "codigoServicio": "SPA",
  "fecha": "2025-12-10"
}
```

---

### 7️⃣ **Tipos de Habitación por Hotel** 🛏️

#### Obtener tipos de habitación de un hotel (con precios)
```http
GET http://localhost:3000/api/hoteles/tipos?hotel=Gran
```

**Respuesta esperada:**
```json
{
  "hotel": "Gran Hotel Miramar",
  "categoria": "5 estrellas",
  "tiposHabitacion": [
    {
      "idTipoHabitacion": 1,
      "categoria": "Individual",
      "camasIndividuales": 1,
      "camasDobles": 0,
      "precioBase": "120",
      "codigoTarifa": "TARIFA_5E_IND",
      "cantidad": 5
    },
    {
      "categoria": "Doble Estándar",
      "precioBase": "150",
      "codigoTarifa": "TARIFA_5E_DBL_STD",
      "cantidad": 4
    },
    {
      "categoria": "Doble Superior",
      "precioBase": "200",
      "codigoTarifa": "TARIFA_5E_DBL_SUP",
      "cantidad": 4
    },
    {
      "categoria": "Suite Junior",
      "precioBase": "300",
      "codigoTarifa": "TARIFA_5E_SUITE",
      "cantidad": 2
    }
  ],
  "totalTipos": 4
}
```

**Pruebas de Error:**

```http
# Hotel inexistente (debe dar error 404)
GET http://localhost:3000/api/hoteles/tipos?hotel=HotelInexistente
```

---

### 8️⃣ **Cancelar Reserva** ❌

**⚠️ IMPORTANTE**: 
- La cancelación **elimina las pernoctaciones**
- Esto **libera la disponibilidad** automáticamente
- No se puede cancelar si ya se hizo check-in

#### Cancelar reserva (usando ID de reserva)
```http
DELETE http://localhost:3000/api/reservas/1
```

**Respuesta esperada (200 OK):**
```json
{
  "idReserva": 1,
  "hotel": "Gran Hotel Miramar",
  "cliente": "Juan Pérez (12345678A)",
  "fechaEntrada": "2025-12-01T00:00:00.000Z",
  "fechaSalida": "2025-12-05T00:00:00.000Z",
  "pernoctacionesEliminadas": 4,
  "mensaje": "Reserva cancelada exitosamente"
}
```

#### Verificar que la disponibilidad se restaura
```http
# Después de cancelar, consulta disponibilidad
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Deberías ver:**
```json
{
  "tiposDisponibles": [
    {
      "categoria": "Doble Superior",
      "disponibles": 4,        // ⬆️ Incrementó de 3 a 4
      "totalHabitaciones": 4,
      "reservasActuales": 0    // ⬇️ Decrementó de 1 a 0
    }
  ]
}
```

**Pruebas de Error:**

```http
# Cancelar reserva inexistente (debe dar error 404)
DELETE http://localhost:3000/api/reservas/99999
```

```http
# Cancelar reserva con check-in hecho (debe dar error 409)
# Primero crea reserva, haz check-in, luego intenta cancelar
DELETE http://localhost:3000/api/reservas/1
```

---

## 🎯 **Flujo de Prueba Completo - Caso Real**

Sigue este orden para probar todo el sistema de principio a fin:

### **Escenario**: Juan Pérez reserva una habitación en el Gran Hotel Miramar

---

### **Paso 1**: Verificar datos iniciales
```http
GET http://localhost:3000/api/hoteles
GET http://localhost:3000/api/servicios
```

---

### **Paso 2**: Buscar disponibilidad (Juan busca hotel en Palma)
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Resultado esperado**: Ver habitaciones disponibles con precios:
- Doble Superior: 200€/noche, 4 disponibles ✅

---

### **Paso 3**: Crear reserva (Juan reserva una Doble Superior)
```http
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "12345678A"
}
```

**Resultado**: Reserva ID 1 creada, 4 pernoctaciones generadas
**Nota**: Los huéspedes se especificarán en el check-in

---

### **Paso 4**: Verificar que la disponibilidad se actualizó
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Resultado esperado**: 
- Doble Superior: 3 disponibles ⬇️ (decrementó de 4)
- reservasActuales: 1 ⬆️ (incrementó de 0)

---

### **Paso 5**: Intentar overbooking (crear 4 reservas más)
```http
# Repite esta petición 4 veces para crear reservas 2, 3, 4
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Desayuno",
  "dniClientePaga": "87654321B"
}
```

**Después de la 3ª reserva**: `disponibles: 0` ✅

**En la 4ª reserva**: ❌ Error 409 - "No hay disponibilidad"

---

### **Paso 6**: Juan llega al hotel - Check-in (especificando huéspedes)
```http
POST http://localhost:3000/api/checkin
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "201",
  "dniCliente": "12345678A",
  "dniHuespedes": ["12345678A", "87654321B"]
}
```

**Resultado**: Contrato ID 1 creado, habitación 201 asignada, huéspedes registrados

---

### **Paso 7**: Juan solicita servicio de spa
```http
POST http://localhost:3000/api/servicios/agregar
Content-Type: application/json

{
  "dniCliente": "12345678A",
  "codigoServicio": "SPA",
  "fecha": "2025-12-02"
}
```

**Resultado**: Servicio SPA (50€) añadido para el 2 de diciembre

---

### **Paso 8**: Juan termina su estancia - Check-out
```http
POST http://localhost:3000/api/checkout
Content-Type: application/json

{
  "nombreHotel": "Gran Hotel Miramar",
  "numeroHabitacion": "201"
}
```

**Resultado**: Contrato finalizado, habitación 201 liberada

---

### **Paso 9**: Verificar disponibilidad post check-out
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Resultado esperado**: 
- Doble Superior: **SIGUE en 0 disponibles** ✅
- reservasActuales: **SIGUE en 4** ✅
- **¿Por qué?** Porque las pernoctaciones siguen activas (la reserva no se canceló)

---

## 🧬 **Entendiendo la Arquitectura del Sistema**

### **Conceptos Clave:**

#### 1. **Reserva → Pernoctación** (Fase de Booking)
- Cuando se crea una **Reserva**, se generan automáticamente registros de **Pernoctación**
- Cada pernoctación representa una noche reservada de un tipo de habitación
- **ESTO ES LO QUE CUENTA PARA LA DISPONIBILIDAD** ✅
- Ejemplo: Reserva del 1 al 5 de diciembre = 4 pernoctaciones (1, 2, 3, 4 de diciembre)

#### 2. **Reserva → Contrato → Habitación Física** (Fase de Check-in)
- El **Contrato** se crea en el check-in
- Asigna una habitación física específica (ej: habitación 201)
- **NO afecta la disponibilidad** (ya se contó en la reserva)

#### 3. **¿Por qué esta arquitectura?**
```
INCORRECTO ❌: Contar contratos para disponibilidad
→ Problema: Permite overbooking antes del check-in

CORRECTO ✅: Contar pernoctaciones para disponibilidad
→ Previene overbooking desde el momento de la reserva
```

---

## 📊 **Verificación con Prisma Studio**

Abre Prisma Studio para ver los cambios en tiempo real:

```bash
npm run prisma:studio
```

Luego visita: `http://localhost:5555`

**Tablas clave para verificar:**
- **Pernoctacion**: Ver cuántas noches están reservadas por tipo
- **Habitacion**: Ver habitaciones físicas por hotel
- **Contrato**: Ver check-ins activos
- **Tarifa** y **Hotel_Tarifa**: Ver matriz de precios

---

## ✅ **Checklist de Pruebas Completo**

### **Disponibilidad y Tarifas** 💰
- [ ] Búsqueda de disponibilidad por hotel (con precios)
- [ ] Búsqueda de disponibilidad por ciudad
- [ ] Búsqueda de disponibilidad por país
- [ ] Verificar que precios cambian según categoría de hotel
- [ ] Verificar que campos `disponibles`, `totalHabitaciones`, `reservasActuales` son correctos

### **Reservas** 📝
- [ ] Crear reserva con disponibilidad ✅
- [ ] Verificar que disponibilidad decrementa después de reservar
- [ ] Crear reserva sin disponibilidad (error 409 - Conflict)
- [ ] Crear reserva con DNI inexistente (error 404)
- [ ] Crear reserva con fechas inválidas (error 400)
- [ ] Modificar reserva antes de check-in
- [ ] Intentar modificar después de check-in (según lógica de negocio)

### **Check-in / Check-out** 🔑
- [ ] Check-in exitoso (asigna habitación física)
- [ ] Verificar que disponibilidad NO cambia después de check-in ✅
- [ ] Check-in con tipo de habitación incorrecto (error 400)
- [ ] Check-in duplicado (error 409)
- [ ] Check-out exitoso
- [ ] Check-out duplicado (error 409)

### **Servicios Adicionales** 🍽️
- [ ] Obtener lista de servicios
- [ ] Añadir servicio a reserva activa
- [ ] Añadir servicio fuera del rango de fechas (error 400)
- [ ] Añadir servicio con código inexistente (error 404)

### **Pruebas de Integridad** 🧪
- [ ] Cancelar reserva (debe liberar disponibilidad) ✅
- [ ] Intentar cancelar después de check-in (error 409)
- [ ] Obtener tipos de habitación con precios por hotel
- [ ] Prueba de overbooking: Llenar todas las habitaciones de un tipo

### **Prueba End-to-End Completa** 🎯
- [ ] Flujo completo: Búsqueda → Reserva → Check-in → Servicios → Check-out

---

## 🐛 **Debugging y Troubleshooting**

### **Si encuentras errores:**

1. **Revisa la consola del servidor** 
   ```bash
   npm run dev
   ```
   Los errores de Prisma se muestran con consultas SQL

2. **Verifica los datos en Prisma Studio**
   ```bash
   npm run prisma:studio
   ```
   Visita: `http://localhost:5555`

3. **Comprueba el formato de datos**
   - Fechas: `YYYY-MM-DD` (ej: `2025-12-01`)
   - DNIs: String con letra (ej: `"12345678A"`)
   - Nombres: Coincidencia parcial con LIKE (ej: `"Gran"` encuentra `"Gran Hotel Miramar"`)

4. **Verifica la base de datos**
   ```bash
   cd BD
   crear_bd.bat
   ```

5. **Revisa los logs de Prisma**
   Las consultas se muestran en la consola con `prisma:query`

---

## 📈 **Pruebas de Rendimiento**

### **Optimización de Queries:**

El sistema usa **agregación con `groupBy`** en lugar de N+1 queries:

```typescript
// ❌ ANTES (20+ queries)
for (const reserva of reservas) {
  for (const pernoctacion of reserva.pernoctaciones) {
    await prisma.habitacion.findFirst(...); // Query por pernoctación
  }
}

// ✅ AHORA (7-8 queries)
const pernoctacionesPorTipo = await prisma.pernoctacion.groupBy({
  by: ['idTipoHabitacion'],
  _count: { idPernoctacion: true }
});
```

**Queries por petición de disponibilidad**: ~7-8 queries
- 1 query: Buscar hotel
- 1 query: Contar habitaciones por tipo (groupBy)
- 1 query: Contar pernoctaciones por tipo (groupBy)
- 3-4 queries: Buscar tarifas para cada tipo
- 1 query: Buscar detalles de tarifas

---

## 🎉 **¡Sistema Completo y Optimizado!**

✅ Prisma ORM integrado  
✅ API con identificadores naturales (sin IDs expuestos)  
✅ Sistema de tarifas dinámico (12 tarifas)  
✅ Lógica de disponibilidad correcta (cuenta pernoctaciones)  
✅ Prevención de overbooking  
✅ Optimizado para producción (groupBy, no N+1 queries)  

**Documentación adicional:**
- `RESUMEN_IMPLEMENTACION.md`: Resumen técnico completo
- `CORRECCION_DISPONIBILIDAD.md`: Explicación de la lógica de disponibilidad
- `TARIFAS_INFO.md`: Detalles del sistema de tarifas

# 📋 Documentación Completa de Endpoints - API Sector Turístico con Prisma

**Sistema de Gestión Hotelera (PMS) - Property Management System**

---

## 🏨 **Gestión de Hoteles**

### GET /api/hoteles
Devuelve una lista de todos los hoteles gestionados por el sistema.

**Respuesta 200 OK:**
```json
[
  {
    "idHotel": 1,
    "nombre": "Gran Hotel Miramar",
    "ubicacion": "Paseo Marítimo 33",
    "categoria": "5 estrellas",
    "idCiudad": 1,
    "ciudad": {
      "idCiudad": 1,
      "nombre": "Palma",
      "pais": "España"
    }
  }
]
```

### GET /api/hoteles/:id
Devuelve un hotel específico con sus relaciones.

**Parámetros:**
- `id` (path param): ID del hotel

**Respuesta 200 OK:**
```json
{
  "idHotel": 1,
  "nombre": "Gran Hotel Miramar",
  "ubicacion": "Paseo Marítimo 33",
  "categoria": "5 estrellas",
  "ciudad": {
    "nombre": "Palma",
    "pais": "España"
  },
  "habitaciones": [
    {
      "numeroHabitacion": "101",
      "tipoHabitacion": {
        "categoria": "Doble Superior"
      }
    }
  ]
}
```

### GET /api/hoteles/:id/tiposHabitacion
Devuelve los tipos de habitación disponibles en un hotel específico.

**Parámetros:**
- `id` (path param): ID del hotel

**Respuesta 200 OK:**
```json
[
  {
    "idTipoHabitacion": 3,
    "categoria": "Doble Superior",
    "camasIndividuales": 0,
    "camasDobles": 1,
    "cantidadHabitaciones": 4
  }
]
```

### POST /api/hoteles
Crea un nuevo hotel.

**Request Body:**
```json
{
  "nombre": "Hotel Nuevo",
  "ubicacion": "Calle Principal 1",
  "categoria": "4 estrellas",
  "idCiudad": 1
}
```

### PUT /api/hoteles/:id
Actualiza un hotel existente.

### DELETE /api/hoteles/:id
Elimina un hotel.

---

## 🔍 **Gestión de Disponibilidad y Búsqueda**

### GET /api/disponibilidad
Busca tipos de habitación disponibles con **precios incluidos**. Cuenta las **pernoctaciones** (reservas activas) para calcular disponibilidad real y prevenir overbooking.

**⚠️ IMPORTANTE:** 
- Calcula disponibilidad contando **pernoctaciones** (reservas), no contratos (check-ins)
- Incluye **precios dinámicos** basados en el sistema de tarifas
- Previene **overbooking** desde el momento de la reserva

**Query Params:**
- `fechaEntrada` (requerido): Fecha de entrada en formato YYYY-MM-DD
- `fechaSalida` (requerido): Fecha de salida en formato YYYY-MM-DD
- `hotel` (opcional): Nombre del hotel (búsqueda con LIKE, parcial)
- `ciudad` (opcional): Nombre de la ciudad
- `pais` (opcional): Nombre del país

**Nota:** Se debe usar al menos un filtro de ubicación (hotel, ciudad o pais).

**Ejemplo de petición:**
```http
GET /api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Respuesta 200 OK (búsqueda por hotel):**
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
      "codigoTarifa": "TARIFA_5E_DBL_SUP",
      "disponibles": 3,
      "totalHabitaciones": 4,
      "reservasActuales": 1
    }
  ],
  "totalTiposDisponibles": 2
}
```

**Respuesta 200 OK (búsqueda por ciudad/país):**
```json
{
  "hoteles": [
    {
      "idHotel": 1,
      "nombre": "Gran Hotel Miramar",
      "ubicacion": "Paseo Marítimo 33",
      "categoria": "5 estrellas",
      "ciudad": "Palma",
      "pais": "España",
      "tiposDisponibles": [
        {
          "categoria": "Doble Superior",
          "precioPorNoche": "200",
          "disponibles": 3
        }
      ]
    }
  ],
  "totalHoteles": 3
}
```

**Errores:**
- `400 Bad Request`: Faltan parámetros requeridos o fechas inválidas
- `404 Not Found`: Hotel no encontrado

---

## 📅 **Gestión de Reservas**

### GET /api/reservas/buscar/cliente
Busca reservas por nombre y/o apellido del cliente que paga. Útil para el PMS.

**Query Params:**
- `nombre` (opcional): Nombre del cliente (búsqueda parcial, case-insensitive)
- `apellido` (opcional): Apellido del cliente (búsqueda parcial, case-insensitive)

**Nota:** Al menos uno de los dos parámetros debe proporcionarse.

**Ejemplo de petición:**
```http
GET /api/reservas/buscar/cliente?nombre=Juan
GET /api/reservas/buscar/cliente?apellido=Pérez
GET /api/reservas/buscar/cliente?nombre=Juan&apellido=Pérez
```

**Respuesta 200 OK:**
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
        "regimen": {
          "nombre": "Media Pensión"
        },
        "hotel": {
          "nombre": "Gran Hotel Miramar"
        }
      },
      "contrato": {
        "numeroHabitacion": "201",
        "fechaCheckIn": "2025-12-01T10:00:00.000Z"
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

**Errores:**
- `400 Bad Request`: No se proporcionó nombre ni apellido

### POST /api/reservas
Crea una nueva reserva usando **identificadores naturales** (nombres, no IDs internos). 

**⚠️ IMPORTANTE:**
- Genera automáticamente **pernoctaciones** (una por cada noche)
- Las pernoctaciones se cuentan en disponibilidad para **prevenir overbooking**
- **NO** requiere especificar huéspedes (se especifican en el check-in)
- Valida disponibilidad antes de crear la reserva
- El cliente que paga puede identificarse por **DNI** (si ya lo tiene) o **email** (si no tiene DNI aún)

**Request Body:**
```json
{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "12345678A"  // O usar "emailClientePaga" si no tiene DNI
}
```

**Campos requeridos:**
- `fechaEntrada` (string, formato: YYYY-MM-DD)
- `fechaSalida` (string, formato: YYYY-MM-DD)
- `nombreHotel` (string): Nombre del hotel
- `tipoHabitacion` (string): Categoría de la habitación
- `regimen` (string): Código del régimen
- `dniClientePaga` **O** `emailClientePaga`: Identificador del cliente que paga

**Respuesta 201 Created:**
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

**Errores:**
- `400 Bad Request`: Faltan parámetros o fechas inválidas
- `404 Not Found`: Hotel, tipo habitación, régimen o cliente no encontrado
- `409 Conflict`: No hay disponibilidad para las fechas solicitadas

### GET /api/reservas
Obtiene todas las reservas del sistema.

**Respuesta 200 OK:**
```json
[
  {
    "idReserva": 1,
    "fechaEntrada": "2025-12-01T00:00:00.000Z",
    "fechaSalida": "2025-12-05T00:00:00.000Z",
    "clientePaga": {
      "nombre": "Juan",
      "apellidos": "Pérez",
      "DNI": "12345678A"
    },
    "pernoctaciones": [...]
  }
]
```

### GET /api/reservas/:id
Obtiene los detalles completos de una reserva específica.

**Parámetros:**
- `id` (path param): ID de la reserva

**Respuesta 200 OK:**
```json
{
  "idReserva": 1,
  "fechaEntrada": "2025-12-01T00:00:00.000Z",
  "fechaSalida": "2025-12-05T00:00:00.000Z",
  "clientePaga": {
    "nombre": "Juan",
    "apellidos": "Pérez"
  },
  "precioRegimen": {
    "regimen": {
      "nombre": "Media Pensión"
    }
  },
  "pernoctaciones": [...],
  "contrato": null
}
```

**Errores:**
- `404 Not Found`: Reserva no encontrada

### PUT /api/reservas/:id
Modifica los datos de una reserva existente.

**Parámetros:**
- `id` (path param): ID de la reserva

**Request Body (campos opcionales):**
```json
{
  "regimen": "Pensión Completa"
}
```

**Nota:** Para cambiar fechas o tipo de habitación, es recomendable cancelar y crear una nueva reserva.

**Respuesta 200 OK:**
```json
{
  "idReserva": 1,
  "mensaje": "Reserva actualizada exitosamente"
}
```

**Errores:**
- `404 Not Found`: Reserva no encontrada
- `409 Conflict`: Ya se hizo check-in (modificación no permitida)

### DELETE /api/reservas/:id
Cancela una reserva y **elimina las pernoctaciones**, liberando la disponibilidad.

**⚠️ IMPORTANTE:** Al cancelar, la disponibilidad se restaura automáticamente.

**Parámetros:**
- `id` (path param): ID de la reserva

**Respuesta 200 OK:**
```json
{
  "idReserva": 1,
  "hotel": "Gran Hotel Miramar",
  "cliente": "Juan Pérez (12345678A)",
  "pernoctacionesEliminadas": 4,
  "mensaje": "Reserva cancelada exitosamente"
}
```

**Errores:**
- `404 Not Found`: Reserva no encontrada
- `409 Conflict`: Ya se ha hecho check-in (no se puede cancelar)

---

## 🏠 **Proceso de Estancia (Check-in / Check-out)**

### POST /api/reservas/:id/checkin
Realiza el check-in, creando un **Contrato** y asignando una **habitación física específica**.

**⚠️ IMPORTANTE:**
- Asigna una habitación física (ej: habitación 201)
- **AQUÍ se especifican los huéspedes** que se alojan (incluyendo sus DNIs)
- **AQUÍ se completa la información de los clientes** (DNI y fecha de nacimiento si no los tenían)
- Crea el vínculo Reserva → Contrato → Habitación física
- **NO afecta la disponibilidad** (ya se contó en la reserva con las pernoctaciones)

**Parámetros:**
- `id` (path param): ID de la reserva

**Request Body:**
```json
{
  "numeroHabitacion": "201",
  "dniHuespedes": ["12345678A", "87654321B"]
}
```

**Nota:** 
- El array `dniHuespedes` debe incluir los **DNIs** de todas las personas que se alojarán
- Los clientes deben existir en la base de datos con sus DNIs antes del check-in
- Si un cliente no tiene DNI, debe actualizarse antes: `PUT /api/clientes/:id`

**Respuesta 201 Created:**
```json
{
  "idContrato": 1,
  "numeroHabitacion": "201",
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

**Errores:**
- `400 Bad Request`: Falta numeroHabitacion, tipo de habitación incorrecto, o datos inválidos
- `404 Not Found`: Reserva, habitación o algún huésped no encontrado
- `409 Conflict`: Ya se ha hecho check-in o la habitación está ocupada

### POST /api/contratos/:idContrato/checkout
Realiza el check-out de un huésped, finalizando el contrato.

**⚠️ IMPORTANTE:**
- Cierra el contrato y marca la fecha de salida
- **NO afecta la disponibilidad** (las pernoctaciones ya están cerradas)
- Libera la habitación física para nuevas asignaciones

**Parámetros:**
- `idContrato` (path param): ID del contrato

**Respuesta 200 OK:**
```json
{
  "idContrato": 1,
  "numeroHabitacion": "201",
  "hotel": "Gran Hotel Miramar",
  "cliente": "Juan Pérez (12345678A)",
  "fechaEntrada": "2025-12-01T00:00:00.000Z",
  "fechaSalida": "2025-12-05T00:00:00.000Z",
  "fechaSalidaReal": "2025-12-05T11:00:00.000Z",
  "estado": "Finalizado",
  "mensaje": "Check-out realizado exitosamente"
}
```

**Errores:**
- `404 Not Found`: Contrato no encontrado
- `409 Conflict`: Ya se ha hecho check-out previamente

---

## 🛎️ **Gestión de Servicios Adicionales**

### GET /api/servicios
Devuelve la lista de todos los servicios adicionales que se pueden contratar.

**Respuesta 200 OK:**
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
      "idServicio": 2,
      "nombre": "Alquiler de Bicicletas",
      "codigo": "BIKE",
      "precio": "15.00"
    }
  ],
  "total": 5
}
```

### GET /api/servicios/:codigo
Obtiene un servicio específico por su código.

**Parámetros:**
- `codigo` (path param): Código del servicio (ej: "SPA", "BIKE")

**Respuesta 200 OK:**
```json
{
  "idServicio": 1,
  "nombre": "Spa y Masajes",
  "codigo": "SPA",
  "precio": "50.00"
}
```

### POST /api/pernoctaciones/:idPernoctacion/servicios
Añade un servicio consumido a una noche específica de la estancia.

**Parámetros:**
- `idPernoctacion` (path param): ID de la pernoctación

**Request Body:**
```json
{
  "codigoServicio": "SPA"
}
```

**Respuesta 201 Created:**
```json
{
  "idServicioContratado": 1,
  "servicio": "Spa y Masajes",
  "fecha": "2025-12-02T00:00:00.000Z",
  "precio": "50.00",
  "pernoctacion": 1,
  "mensaje": "Servicio añadido exitosamente"
}
```

**Errores:**
- `400 Bad Request`: Falta codigoServicio
- `404 Not Found`: Pernoctación o servicio no encontrado
- `409 Conflict`: El servicio ya está asociado a la pernoctación

---

## 👥 **Gestión de Clientes**

### GET /api/clientes
Obtiene todos los clientes del sistema.

**Respuesta 200 OK:**
```json
[
  {
    "idCliente": 1,
    "nombre": "Juan",
    "apellidos": "Pérez",
    "correoElectronico": "juan@email.com",
    "DNI": "12345678A",
    "fechaDeNacimiento": "1990-05-15T00:00:00.000Z"
  }
]
```

### GET /api/clientes/:id
Obtiene un cliente específico con sus reservas.

**Parámetros:**
- `id` (path param): ID del cliente

**Respuesta 200 OK:**
```json
{
  "idCliente": 1,
  "nombre": "Juan",
  "apellidos": "Pérez",
  "DNI": "12345678A",
  "reservas": [
    {
      "idReserva": 1,
      "fechaEntrada": "2025-12-01T00:00:00.000Z",
      "fechaSalida": "2025-12-05T00:00:00.000Z"
    }
  ]
}
```

### POST /api/clientes
Crea un nuevo cliente.

**⚠️ IMPORTANTE**: Al crear una reserva, solo se requiere información básica del cliente (nombre, apellidos, email). El DNI y fecha de nacimiento son **opcionales** y se añaden durante el **check-in** junto con los huéspedes adicionales.

**Request Body:**
```json
{
  "nombre": "María",
  "apellidos": "López Sánchez",
  "correoElectronico": "maria@email.com",
  "fechaDeNacimiento": "1985-03-20",  // OPCIONAL
  "DNI": "87654321B"                   // OPCIONAL
}
```

**Campos obligatorios:**
- `nombre` (string): Nombre del cliente
- `apellidos` (string): Apellidos del cliente
- `correoElectronico` (string): Email del cliente (único)

**Campos opcionales:**
- `fechaDeNacimiento` (string, formato: YYYY-MM-DD): Fecha de nacimiento
- `DNI` (string): Documento de identidad

### PUT /api/clientes/:id
Actualiza un cliente existente.

**Request Body (campos opcionales):**
```json
{
  "correoElectronico": "nuevo@email.com"
}
```

---

## 🌍 **Recursos de Soporte (Catálogos)**

### GET /api/ciudades
Obtiene todas las ciudades del sistema.

**Respuesta 200 OK:**
```json
[
  {
    "idCiudad": 1,
    "nombre": "Palma",
    "pais": "España"
  }
]
```

### GET /api/ciudades/:id
Obtiene una ciudad específica con sus hoteles.

### POST /api/ciudades
Crea una nueva ciudad.

**Request Body:**
```json
{
  "nombre": "Barcelona",
  "pais": "España"
}
```

---

## 🛏️ **Tipos de Habitación**

### GET /api/tipos-habitacion
Obtiene todos los tipos de habitación del sistema.

**Respuesta 200 OK:**
```json
[
  {
    "idTipoHabitacion": 1,
    "categoria": "Individual",
    "camasIndividuales": 1,
    "camasDobles": 0
  },
  {
    "idTipoHabitacion": 2,
    "categoria": "Doble Estándar",
    "camasIndividuales": 0,
    "camasDobles": 1
  }
]
```

---

## 🍽️ **Regímenes**

### GET /api/regimenes
Obtiene todos los regímenes alimenticios disponibles.

**Respuesta 200 OK:**
```json
[
  {
    "idRegimen": 1,
    "nombre": "Solo Alojamiento"
  },
  {
    "idRegimen": 2,
    "nombre": "Desayuno"
  },
  {
    "idRegimen": 3,
    "nombre": "Media Pensión"
  },
  {
    "idRegimen": 4,
    "nombre": "Pensión Completa"
  }
]
```

### GET /api/regimenes/:codigo
Obtiene un régimen específico con sus precios por hotel.

**Parámetros:**
- `codigo` (path param): Código del régimen

---

## 🔧 **Health Check**

### GET /health
Verifica que el servidor está funcionando correctamente.

**Respuesta 200 OK:**
```json
{
  "status": "OK",
  "message": "API funcionando correctamente",
  "endpoints": {
    "catalogs": {
      "hoteles": "/api/hoteles",
      "ciudades": "/api/ciudades",
      "tiposHabitacion": "/api/tipos-habitacion",
      "regimenes": "/api/regimenes",
      "servicios": "/api/servicios"
    },
    "operations": {
      "disponibilidad": "/api/disponibilidad?fechaEntrada=YYYY-MM-DD&fechaSalida=YYYY-MM-DD&hotel=NombreHotel",
      "crearReserva": "POST /api/reservas",
      "checkin": "POST /api/reservas/:idReserva/checkin",
      "checkout": "POST /api/contratos/:idContrato/checkout",
      "anadirServicio": "POST /api/pernoctaciones/:idPernoctacion/servicios"
    }
  }
}
```

---

## 📝 **Códigos de Estado HTTP**

| Código | Significado | Uso |
|--------|-------------|-----|
| 200 OK | Operación exitosa | Consultas, actualizaciones, check-out |
| 201 Created | Recurso creado exitosamente | Crear reserva, check-in, añadir servicio |
| 400 Bad Request | Parámetros inválidos o faltantes | Faltan campos requeridos, formato incorrecto |
| 404 Not Found | Recurso no encontrado | Hotel, cliente, reserva inexistente |
| 409 Conflict | Conflicto con el estado actual | Sin disponibilidad, check-in duplicado |
| 500 Internal Server Error | Error del servidor | Error en base de datos, error inesperado |

---

## 🎯 **Flujo Completo - Ejemplo de Caso de Uso Real**

### **Escenario**: Juan Pérez reserva una habitación en el Gran Hotel Miramar

#### 1. Buscar disponibilidad con precios
```http
GET /api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Respuesta**: Ver habitaciones disponibles (Doble Superior: 200€/noche, 4 disponibles)

---

#### 2. Crear reserva (solo quien paga)
```http
POST /api/reservas
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

**Resultado**: Reserva creada, 4 pernoctaciones generadas, disponibilidad decrementada

---

#### 3. Verificar que la disponibilidad se actualizó
```http
GET /api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Resultado**: Doble Superior ahora muestra 3 disponibles (antes: 4)

---

#### 4. Hacer check-in (especificando huéspedes)
```http
POST /api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201",
  "dniHuespedes": ["12345678A", "87654321B"]
}
```

**Resultado**: Contrato creado, habitación 201 asignada, huéspedes registrados

---

#### 5. Añadir servicio (spa)
```http
POST /api/pernoctaciones/1/servicios
Content-Type: application/json

{
  "codigoServicio": "SPA"
}
```

**Resultado**: Servicio SPA (50€) añadido a la primera noche

---

#### 6. Hacer check-out
```http
POST /api/contratos/1/checkout
```

**Resultado**: Contrato finalizado, habitación 201 liberada

---

## 🧬 **Arquitectura del Sistema**

### **Conceptos Clave:**

**Reserva → Pernoctación** (Fase de Booking)
- Cuando se crea una Reserva, se generan pernoctaciones automáticamente
- Cada pernoctación = una noche reservada
- **Esto es lo que cuenta para disponibilidad** ✅

**Reserva → Contrato → Habitación** (Fase de Check-in)
- El Contrato se crea en el check-in
- Asigna habitación física específica
- **NO afecta disponibilidad** (ya se contó en la reserva)

### **Sistema de Tarifas:**
- Precios dinámicos según categoría de hotel y tipo de habitación
- 5★: Individual (120€), Doble Estándar (150€), Doble Superior (200€), Suite (300€)
- 4★: Individual (90€), Doble Estándar (110€), Doble Superior (150€), Suite (220€)
- 3★: Individual (60€), Doble Estándar (75€), Doble Superior (100€), Suite (150€)

---

## 📚 **Documentación Adicional**

- `TESTING_GUIDE.md`: Guía completa de pruebas con ejemplos
- `RESUMEN_IMPLEMENTACION.md`: Resumen técnico completo
- `CORRECCION_DISPONIBILIDAD.md`: Explicación de la lógica de disponibilidad
- `TARIFAS_INFO.md`: Detalles del sistema de tarifas

---

¡API completamente funcional con Prisma ORM! 🎉

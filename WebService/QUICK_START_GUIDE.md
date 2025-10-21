# 🏨 Guía Rápida de Uso - API Sector Turístico

## 🎯 Introducción

Esta API te permite gestionar reservas de hoteles **SIN necesidad de conocer IDs internos**. Puedes trabajar con nombres de hoteles, tipos de habitación, códigos de régimen y datos de clientes de forma natural.

---

## 📋 Paso 1: Conocer los Catálogos Disponibles

Antes de crear una reserva, consulta los catálogos para conocer qué opciones están disponibles:

### 🏨 Ver hoteles disponibles
```http
GET http://localhost:3000/api/hoteles
```

**Respuesta:**
```json
[
  {
    "idHotel": 1,
    "nombre": "Hotel Paraíso",
    "ubicacion": "Playa de Palma",
    "categoria": 5,
    "ciudad": {
      "nombre": "Palma",
      "pais": "España"
    }
  }
]
```

### 🛏️ Ver tipos de habitación disponibles
```http
GET http://localhost:3000/api/tipos-habitacion
```

**Respuesta:**
```json
[
  {
    "categoria": "Doble Superior",
    "camasIndividuales": 0,
    "camasDobles": 1,
    "disponibleEn": [
      {
        "hotel": "Hotel Paraíso",
        "ciudad": "Palma",
        "cantidad": 15
      }
    ]
  }
]
```

### 🍽️ Ver regímenes disponibles
```http
GET http://localhost:3000/api/regimenes
```

**Respuesta:**
```json
[
  {
    "codigo": "SA",
    "disponibleEn": [
      {
        "hotel": "Hotel Paraíso",
        "ciudad": "Palma",
        "precio": 80.00
      }
    ]
  },
  {
    "codigo": "AD",
    "disponibleEn": [
      {
        "hotel": "Hotel Paraíso",
        "ciudad": "Palma",
        "precio": 120.00
      }
    ]
  }
]
```

### 🛎️ Ver servicios adicionales
```http
GET http://localhost:3000/api/servicios
```

**Respuesta:**
```json
[
  {
    "codigoServicio": "SPA",
    "Precio": 50.00
  },
  {
    "codigoServicio": "MINIBAR",
    "Precio": 25.00
  }
]
```

---

## 📋 Paso 2: Buscar Disponibilidad

### Buscar por nombre de hotel
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Paraíso
```

**Respuesta:**
```json
{
  "hotel": {
    "nombre": "Gran Hotel del Mar",
    "ubicacion": "Paseo Marítimo, 10, Palma",
    "categoria": 5,
    "ciudad": "Palma",
    "pais": "España"
  },
  "tiposDisponibles": [
    {
      "idTipoHabitacion": 1,
      "categoria": "Doble Estándar",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "150.00",
      "codigoTarifa": "TARIFA_5E_DBL_STD"
    },
    {
      "idTipoHabitacion": 2,
      "categoria": "Doble Superior",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "200.00",
      "codigoTarifa": "TARIFA_5E_DBL_SUP"
    },
    {
      "idTipoHabitacion": 3,
      "categoria": "Suite Junior",
      "camasIndividuales": 0,
      "camasDobles": 2,
      "precioPorNoche": "300.00",
      "codigoTarifa": "TARIFA_5E_SUITE"
    }
  ],
  "totalHabitacionesDisponibles": 12
}
```

**📊 Nota sobre precios:** Los precios se ajustan según:
- 🌟 **Categoría del hotel**: Hoteles 5★ > 4★ > 3★
- 🛏️ **Tipo de habitación**: Suite > Superior > Estándar > Individual

### Buscar por ciudad
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&ciudad=Palma
```

### Buscar por país
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&pais=España
```

---

## 📋 Paso 3: Crear una Reserva

**NO necesitas conocer IDs**, simplemente proporciona los datos del cliente y los nombres de hotel/tipo de habitación:

```http
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "tipo": "Reserva",
  "canalReserva": "Web",
  "hotel": "Hotel Paraíso",
  "tipoHabitacion": "Doble Superior",
  "regimen": "AD",
  "clientePaga": {
    "nombre": "María",
    "apellidos": "García López",
    "correoElectronico": "maria.garcia@email.com",
    "DNI": "12345678A",
    "fechaDeNacimiento": "1985-05-20"
  },
  "huespedes": [
    {
      "nombre": "María",
      "apellidos": "García López",
      "correoElectronico": "maria.garcia@email.com",
      "DNI": "12345678A"
    },
    {
      "nombre": "Juan",
      "apellidos": "Pérez Martínez",
      "correoElectronico": "juan.perez@email.com",
      "DNI": "87654321B",
      "fechaDeNacimiento": "1980-03-15"
    }
  ]
}
```

**Lo que hace el sistema automáticamente:**
- ✅ Busca el hotel por nombre
- ✅ Busca el tipo de habitación por nombre
- ✅ Busca el régimen por código
- ✅ Crea el cliente si no existe (usando el DNI como identificador único)
- ✅ Crea los huéspedes si no existen
- ✅ Valida la disponibilidad
- ✅ Crea las pernoctaciones automáticamente
- ✅ Devuelve la reserva completa con todos los IDs generados

**Respuesta exitosa:**
```json
{
  "message": "Reserva creada exitosamente",
  "reserva": {
    "idReserva": 1,
    "fechaEntrada": "2025-12-01T00:00:00.000Z",
    "fechaSalida": "2025-12-05T00:00:00.000Z",
    "tipo": "Reserva",
    "clientePaga": {
      "idCliente": 1,
      "nombre": "María",
      "apellidos": "García López",
      "DNI": "12345678A"
    },
    "precioRegimen": {
      "precio": 120.00,
      "hotel": {
        "nombre": "Hotel Paraíso"
      },
      "regimen": {
        "codigo": "AD"
      }
    },
    "pernoctaciones": [
      {
        "idPernoctacion": 1,
        "fechaPernoctacion": "2025-12-01T00:00:00.000Z",
        "tipoHabitacion": {
          "categoria": "Doble Superior"
        }
      }
      // ... más pernoctaciones
    ]
  },
  "clienteCreado": "El cliente fue registrado en el sistema"
}
```

---

## 📋 Paso 4: Hacer Check-in

Usa el `idReserva` que obtuviste al crear la reserva:

```http
POST http://localhost:3000/api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201"
}
```

**Respuesta:**
```json
{
  "message": "Check-in realizado exitosamente",
  "contrato": {
    "idContrato": 1,
    "montoTotal": 480.00,
    "fechaCheckIn": "2025-12-01T10:30:00.000Z",
    "numeroHabitacion": "201"
  }
}
```

---

## 📋 Paso 5: Añadir Servicios

Usa el `idPernoctacion` de la reserva y el `codigoServicio`:

```http
POST http://localhost:3000/api/pernoctaciones/1/servicios
Content-Type: application/json

{
  "codigoServicio": "SPA"
}
```

---

## 📋 Paso 6: Hacer Check-out

Usa el `idContrato` que obtuviste en el check-in:

```http
POST http://localhost:3000/api/contratos/1/checkout
```

---

## 🎯 Ventajas de esta Aproximación

### ✅ No necesitas conocer IDs
- **Antes:** Tenías que saber que el cliente con ID 5 se llama María
- **Ahora:** Solo proporcionas el DNI y nombre de María

### ✅ Creación automática
- Si el cliente no existe, se crea automáticamente
- Si los huéspedes no existen, se crean automáticamente

### ✅ Búsqueda flexible
- Puedes buscar hoteles por nombre parcial: "Paraíso" encuentra "Hotel Paraíso"
- Puedes buscar ciudades y países

### ✅ Validación robusta
- El sistema verifica que el hotel exista
- Valida que el tipo de habitación esté disponible en ese hotel
- Verifica que el régimen se ofrezca en ese hotel
- Valida disponibilidad de fechas

---

## 💡 Ejemplos de Casos de Uso Reales

### Caso 1: Reserva para familia
```json
{
  "fechaEntrada": "2025-12-20",
  "fechaSalida": "2025-12-27",
  "tipo": "Reserva",
  "canalReserva": "Telefono",
  "hotel": "Hotel Paraíso",
  "tipoHabitacion": "Suite Familiar",
  "regimen": "PC",
  "clientePaga": {
    "nombre": "Pedro",
    "apellidos": "Sánchez Ruiz",
    "correoElectronico": "pedro@email.com",
    "DNI": "11111111A"
  },
  "huespedes": [
    {
      "nombre": "Pedro",
      "apellidos": "Sánchez Ruiz",
      "correoElectronico": "pedro@email.com",
      "DNI": "11111111A"
    },
    {
      "nombre": "Ana",
      "apellidos": "Martín García",
      "correoElectronico": "ana@email.com",
      "DNI": "22222222B"
    },
    {
      "nombre": "Lucas",
      "apellidos": "Sánchez Martín",
      "correoElectronico": "lucas@email.com",
      "DNI": "33333333C",
      "fechaDeNacimiento": "2015-08-10"
    }
  ]
}
```

### Caso 2: Reserva walk-in (llegada sin reserva previa)
```json
{
  "fechaEntrada": "2025-11-15",
  "fechaSalida": "2025-11-17",
  "tipo": "Walkin",
  "hotel": "Hotel Paraíso",
  "tipoHabitacion": "Individual",
  "regimen": "SA",
  "clientePaga": {
    "nombre": "Laura",
    "apellidos": "Fernández Costa",
    "correoElectronico": "laura@email.com",
    "DNI": "44444444D"
  },
  "huespedes": [
    {
      "nombre": "Laura",
      "apellidos": "Fernández Costa",
      "correoElectronico": "laura@email.com",
      "DNI": "44444444D"
    }
  ]
}
```

---

## 🔍 Endpoints de Consulta Rápida

```http
# Ver todos los hoteles con sus ciudades
GET http://localhost:3000/api/hoteles

# Ver todas las ciudades
GET http://localhost:3000/api/ciudades

# Ver todos los tipos de habitación
GET http://localhost:3000/api/tipos-habitacion

# Ver todos los regímenes
GET http://localhost:3000/api/regimenes

# Ver todos los servicios
GET http://localhost:3000/api/servicios

# Ver todas las reservas
GET http://localhost:3000/api/reservas

# Ver una reserva específica
GET http://localhost:3000/api/reservas/1
```

---

## ❓ Preguntas Frecuentes

### ¿Qué pasa si el cliente ya existe?
El sistema lo busca por DNI y usa los datos existentes. No crea duplicados.

### ¿Qué pasa si escribo mal el nombre del hotel?
Recibirás un error 404 indicando que no se encontró el hotel.

### ¿Puedo buscar hoteles por parte del nombre?
Sí, "Paraíso" encontrará "Hotel Paraíso Beach & Spa".

### ¿Qué datos son obligatorios del cliente?
- nombre
- apellidos
- correoElectronico
- DNI

La fecha de nacimiento es opcional.

---

## 🎊 ¡Listo para usar!

Tu API está diseñada para ser **intuitiva y fácil de usar** sin necesidad de conocer IDs internos. ¡Empieza a hacer reservas!

**Servidor:** http://localhost:3000
**Health Check:** http://localhost:3000/health

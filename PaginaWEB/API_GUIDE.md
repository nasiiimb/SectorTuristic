# API Guide - WebService PMS

Guía completa de todos los endpoints disponibles en la API del Sistema de Gestión Hotelera.

## URL Base

```
http://localhost:3000/api
```

---

## Tabla de Contenidos

1. [Hoteles](#hoteles)
2. [Ciudades](#ciudades)
3. [Tipos de Habitación](#tipos-de-habitación)
4. [Regímenes](#regímenes)
5. [Servicios](#servicios)
6. [Clientes](#clientes)
7. [Reservas](#reservas)
8. [Disponibilidad](#disponibilidad)
9. [Contratos (Check-in/Check-out)](#contratos-check-incheck-out)
10. [Pernoctaciones](#pernoctaciones)

---

## Hoteles

### Listar todos los hoteles

```http
GET /hoteles
```

**Respuesta:**
```json
[
  {
    "idHotel": 1,
    "nombre": "Hotel Paraíso",
    "ubicacion": "Playa de Palma",
    "categoria": 5,
    "idCiudad": 1,
    "ciudad": {
      "idCiudad": 1,
      "nombre": "Palma",
      "pais": "España"
    }
  }
]
```

---

### Obtener hotel por ID

```http
GET /hoteles/:id
```

**Parámetros:**
- `id` (número) - ID del hotel

**Ejemplo:**
```http
GET /hoteles/1
```

**Respuesta:**
```json
{
  "idHotel": 1,
  "nombre": "Hotel Paraíso",
  "ubicacion": "Playa de Palma",
  "categoria": 5,
  "idCiudad": 1,
  "ciudad": {
    "idCiudad": 1,
    "nombre": "Palma",
    "pais": "España"
  },
  "habitaciones": [
    {
      "numeroHabitacion": "101",
      "idTipoHabitacion": 1,
      "tipoHabitacion": {
        "categoria": "Doble",
        "camasIndividuales": 0,
        "camasDobles": 1
      }
    }
  ],
  "preciosRegimen": [
    {
      "idPrecioRegimen": 1,
      "precio": 100.00,
      "regimen": {
        "codigo": "AD",
        "descripcion": "Alojamiento y Desayuno"
      }
    }
  ]
}
```

**Errores:**
- `404` - Hotel no encontrado

---

### Obtener tipos de habitación de un hotel

```http
GET /hoteles/:id/tiposHabitacion
```

**Parámetros:**
- `id` (número) - ID del hotel

**Ejemplo:**
```http
GET /hoteles/1/tiposHabitacion
```

**Respuesta:**
```json
[
  {
    "idTipoHabitacion": 1,
    "categoria": "Doble",
    "camasIndividuales": 0,
    "camasDobles": 1,
    "habitaciones": [
      {
        "numeroHabitacion": "101",
        "idHotel": 1
      }
    ],
    "cantidadHabitaciones": 5
  }
]
```

---

### Crear hotel

```http
POST /hoteles
```

**Body:**
```json
{
  "nombre": "Hotel Nuevo",
  "ubicacion": "Centro de la ciudad",
  "categoria": 4,
  "idCiudad": 1
}
```

**Respuesta:** `201 Created`
```json
{
  "idHotel": 4,
  "nombre": "Hotel Nuevo",
  "ubicacion": "Centro de la ciudad",
  "categoria": 4,
  "idCiudad": 1,
  "ciudad": {
    "nombre": "Palma",
    "pais": "España"
  }
}
```

**Errores:**
- `400` - Datos inválidos
- `409` - Conflicto (nombre duplicado)

---

### Actualizar hotel

```http
PUT /hoteles/:id
```

**Parámetros:**
- `id` (número) - ID del hotel

**Body:**
```json
{
  "nombre": "Hotel Actualizado",
  "ubicacion": "Nueva ubicación",
  "categoria": 5,
  "idCiudad": 1
}
```

**Respuesta:** `200 OK`

**Errores:**
- `404` - Hotel no encontrado

---

### Eliminar hotel

```http
DELETE /hoteles/:id
```

**Parámetros:**
- `id` (número) - ID del hotel

**Respuesta:** `200 OK`
```json
{
  "message": "Hotel eliminado correctamente"
}
```

**Errores:**
- `404` - Hotel no encontrado

---

## Ciudades

### Listar todas las ciudades

```http
GET /ciudades
```

**Respuesta:**
```json
[
  {
    "idCiudad": 1,
    "nombre": "Palma",
    "pais": "España"
  }
]
```

---

### Obtener ciudad por ID

```http
GET /ciudades/:id
```

**Respuesta:**
```json
{
  "idCiudad": 1,
  "nombre": "Palma",
  "pais": "España",
  "hoteles": [
    {
      "idHotel": 1,
      "nombre": "Hotel Paraíso",
      "categoria": 5
    }
  ]
}
```

---

### Crear ciudad

```http
POST /ciudades
```

**Body:**
```json
{
  "nombre": "Barcelona",
  "pais": "España"
}
```

**Respuesta:** `201 Created`

---

## Tipos de Habitación

### Listar todos los tipos

```http
GET /tiposHabitacion
```

**Respuesta:**
```json
[
  {
    "idTipoHabitacion": 1,
    "categoria": "Doble",
    "camasIndividuales": 0,
    "camasDobles": 1
  },
  {
    "idTipoHabitacion": 2,
    "categoria": "Individual",
    "camasIndividuales": 1,
    "camasDobles": 0
  }
]
```

---

### Obtener tipo por ID

```http
GET /tiposHabitacion/:id
```

**Respuesta:**
```json
{
  "idTipoHabitacion": 1,
  "categoria": "Doble",
  "camasIndividuales": 0,
  "camasDobles": 1,
  "habitaciones": [
    {
      "numeroHabitacion": "101",
      "idHotel": 1
    }
  ]
}
```

---

## Regímenes

### Listar todos los regímenes

```http
GET /regimenes
```

**Respuesta:**
```json
[
  {
    "idRegimen": 1,
    "codigo": "AD"
  },
  {
    "idRegimen": 2,
    "codigo": "MP"
  },
  {
    "idRegimen": 3,
    "codigo": "PC"
  }
]
```

**Códigos de Régimen:**
- `AD` - Alojamiento y Desayuno
- `MP` - Media Pensión
- `PC` - Pensión Completa
- `TI` - Todo Incluido
- `SA` - Solo Alojamiento

---

### Obtener régimen por ID

```http
GET /regimenes/:id
```

**Respuesta:**
```json
{
  "idRegimen": 1,
  "codigo": "AD",
  "preciosRegimen": [
    {
      "idPrecioRegimen": 1,
      "precio": 100.00,
      "hotel": {
        "nombre": "Hotel Paraíso"
      }
    }
  ]
}
```

---

## Servicios

### Listar todos los servicios

```http
GET /servicios
```

**Respuesta:**
```json
[
  {
    "codigoServicio": "SPA",
    "Precio": 50.00
  },
  {
    "codigoServicio": "WIFI",
    "Precio": 0.00
  }
]
```

---

### Obtener servicio por código

```http
GET /servicios/:codigo
```

**Ejemplo:**
```http
GET /servicios/SPA
```

**Respuesta:**
```json
{
  "codigoServicio": "SPA",
  "Precio": 50.00
}
```

---

## Clientes

### Listar todos los clientes

```http
GET /clientes
```

**Respuesta:**
```json
[
  {
    "idCliente": 1,
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "correoElectronico": "juan.perez@example.com",
    "fechaDeNacimiento": "1985-03-15",
    "DNI": "12345678A"
  }
]
```

---

### Obtener cliente por ID

```http
GET /clientes/:id
```

**Respuesta:**
```json
{
  "idCliente": 1,
  "nombre": "Juan",
  "apellidos": "Pérez García",
  "correoElectronico": "juan.perez@example.com",
  "fechaDeNacimiento": "1985-03-15",
  "DNI": "12345678A",
  "reservasPagadas": [
    {
      "idReserva": 1,
      "fechaEntrada": "2024-12-01",
      "fechaSalida": "2024-12-05"
    }
  ]
}
```

---

### Crear cliente

```http
POST /clientes
```

**Body:**
```json
{
  "nombre": "María",
  "apellidos": "García López",
  "correoElectronico": "maria.garcia@example.com",
  "DNI": "87654321B",
  "fechaDeNacimiento": "1990-07-20"
}
```

**Respuesta:** `201 Created`

**Errores:**
- `409` - Email o DNI duplicado

---

### Actualizar cliente

```http
PUT /clientes/:id
```

**Body:**
```json
{
  "nombre": "María Carmen",
  "apellidos": "García López",
  "correoElectronico": "maria.carmen@example.com"
}
```

**Respuesta:** `200 OK`

---

## Reservas

### Listar todas las reservas

```http
GET /reservas
```

**Query Parameters (opcionales):**
- `idHotel` - Filtrar por hotel
- `fechaEntrada` - Filtrar por fecha de entrada
- `fechaSalida` - Filtrar por fecha de salida
- `idCliente` - Filtrar por cliente

**Ejemplo:**
```http
GET /reservas?idHotel=1&fechaEntrada=2024-12-01
```

**Respuesta:**
```json
[
  {
    "idReserva": 1,
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "canalReserva": "Web",
    "tipo": "Reserva",
    "clientePaga": {
      "nombre": "Juan",
      "apellidos": "Pérez García",
      "correoElectronico": "juan.perez@example.com"
    }
  }
]
```

---

### Obtener reserva por ID

```http
GET /reservas/:id
```

**Respuesta:**
```json
{
  "idReserva": 1,
  "fechaEntrada": "2024-12-01",
  "fechaSalida": "2024-12-05",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "idCliente_paga": 1,
  "idPrecioRegimen": 1,
  "clientePaga": {
    "idCliente": 1,
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "correoElectronico": "juan.perez@example.com"
  },
  "precioRegimen": {
    "precio": 100.00,
    "regimen": {
      "codigo": "AD"
    },
    "hotel": {
      "nombre": "Hotel Paraíso"
    }
  },
  "pernoctaciones": [
    {
      "idPernoctacion": 1,
      "fechaPernoctacion": "2024-12-01",
      "tipoHabitacion": {
        "categoria": "Doble"
      }
    }
  ],
  "reservaHuespedes": [
    {
      "cliente": {
        "nombre": "Juan",
        "apellidos": "Pérez García"
      }
    }
  ]
}
```

---

### Crear reserva

```http
POST /reservas
```

**Body:**
```json
{
  "fechaEntrada": "2024-12-01",
  "fechaSalida": "2024-12-05",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "idPrecioRegimen": 1,
  "cliente": {
    "nombre": "María",
    "apellidos": "García López",
    "correoElectronico": "maria.garcia@example.com",
    "DNI": "12345678A",
    "fechaDeNacimiento": "1990-05-15"
  },
  "huespedes": [
    {
      "nombre": "María",
      "apellidos": "García López",
      "correoElectronico": "maria.garcia@example.com",
      "DNI": "12345678A"
    }
  ],
  "pernoctaciones": [
    {
      "fechaPernoctacion": "2024-12-01",
      "idTipoHabitacion": 1
    },
    {
      "fechaPernoctacion": "2024-12-02",
      "idTipoHabitacion": 1
    },
    {
      "fechaPernoctacion": "2024-12-03",
      "idTipoHabitacion": 1
    },
    {
      "fechaPernoctacion": "2024-12-04",
      "idTipoHabitacion": 1
    }
  ]
}
```

**Notas importantes:**
- Si el cliente ya existe (por DNI), se actualiza su información
- `tipo` debe ser `"Reserva"` o `"Walkin"`
- Las fechas deben estar en formato `YYYY-MM-DD`
- Debe haber una pernoctación por cada noche (fechaSalida - fechaEntrada)

**Respuesta:** `201 Created`
```json
{
  "idReserva": 10,
  "fechaEntrada": "2024-12-01T00:00:00.000Z",
  "fechaSalida": "2024-12-05T00:00:00.000Z",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "idCliente_paga": 6,
  "idPrecioRegimen": 1,
  "clientePaga": {
    "idCliente": 6,
    "nombre": "María",
    "apellidos": "García López"
  },
  "pernoctaciones": [...]
}
```

**Errores:**
- `400` - Datos inválidos (fechas, tipo, etc.)
- `404` - Precio de régimen no encontrado
- `409` - Conflicto con datos del cliente

---

### Cancelar reserva

```http
DELETE /reservas/:id
```

**Respuesta:** `200 OK`
```json
{
  "message": "Reserva cancelada correctamente"
}
```

**Errores:**
- `404` - Reserva no encontrada
- `400` - No se puede cancelar (ya tiene check-in)

---

## Disponibilidad

### Consultar disponibilidad por ciudad

```http
GET /disponibilidad
```

**Query Parameters:**
- `fechaEntrada` - Fecha de entrada (YYYY-MM-DD) **[Obligatorio]**
- `fechaSalida` - Fecha de salida (YYYY-MM-DD) **[Obligatorio]**
- `ciudad` - Nombre de la ciudad **[Al menos uno obligatorio]**
- `hotel` - Nombre del hotel **[Al menos uno obligatorio]**
- `pais` - Nombre del país **[Al menos uno obligatorio]**

**Nota**: Debes proporcionar al menos un filtro de ubicación (`ciudad`, `hotel` o `pais`).

**Ejemplo por ciudad:**
```http
GET /disponibilidad?fechaEntrada=2024-12-01&fechaSalida=2024-12-05&ciudad=Palma
```

**Ejemplo por hotel:**
```http
GET /disponibilidad?fechaEntrada=2024-12-01&fechaSalida=2024-12-05&hotel=Paraíso
```

**Respuesta (búsqueda por ciudad):**
```json
[
  {
    "idHotel": 1,
    "nombre": "Hotel Paraíso",
    "ubicacion": "Playa de Palma",
    "categoria": 5,
    "ciudad": {
      "idCiudad": 1,
      "nombre": "Palma",
      "pais": "España"
    },
    "tiposDisponibles": [
      {
        "idTipoHabitacion": 1,
        "categoria": "Doble",
        "camasIndividuales": 0,
        "camasDobles": 1,
        "foto_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=600",
        "precioPorNoche": 100.00,
        "codigoTarifa": "ESTANDAR",
        "disponibles": 5,
        "totalHabitaciones": 8,
        "reservasActuales": 3
      },
      {
        "idTipoHabitacion": 2,
        "categoria": "Suite",
        "camasIndividuales": 0,
        "camasDobles": 1,
        "foto_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600",
        "precioPorNoche": 200.00,
        "codigoTarifa": "PREMIUM",
        "disponibles": 2,
        "totalHabitaciones": 4,
        "reservasActuales": 2
      }
    ],
    "totalTiposDisponibles": 2
  },
  {
    "idHotel": 2,
    "nombre": "Hotel Marina",
    "ubicacion": "Puerto de Palma",
    "categoria": 4,
    "ciudad": {
      "idCiudad": 1,
      "nombre": "Palma",
      "pais": "España"
    },
    "tiposDisponibles": [
      {
        "idTipoHabitacion": 1,
        "categoria": "Doble",
        "camasIndividuales": 0,
        "camasDobles": 1,
        "precioPorNoche": 90.00,
        "codigoTarifa": "ESTANDAR",
        "disponibles": 10,
        "totalHabitaciones": 12,
        "reservasActuales": 2
      }
    ],
    "totalTiposDisponibles": 1
  }
]
```

**Respuesta (búsqueda por hotel específico):**
```json
{
  "hotel": {
    "nombre": "Hotel Paraíso",
    "ubicacion": "Playa de Palma",
    "categoria": 5,
    "ciudad": "Palma",
    "pais": "España"
  },
  "tiposDisponibles": [
    {
      "idTipoHabitacion": 1,
      "categoria": "Doble",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "foto_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=600",
      "precioPorNoche": 100.00,
      "codigoTarifa": "ESTANDAR",
      "disponibles": 5,
      "totalHabitaciones": 8,
      "reservasActuales": 3
    }
  ],
  "totalTiposDisponibles": 1
}
```

**Caso sin disponibilidad:**
```json
[]
```
(Array vacío cuando se busca por ciudad/país y no hay hoteles con disponibilidad)

**Errores:**
- `400` - Parámetros faltantes o fechas inválidas
- `404` - Hotel o ciudad no encontrada

---

## Contratos (Check-in/Check-out)

### Listar todos los contratos

```http
GET /contratos
```

**Respuesta:**
```json
[
  {
    "idContrato": 1,
    "montoTotal": 400.00,
    "fechaCheckIn": "2024-10-30T10:00:00.000Z",
    "fechaCheckOut": null,
    "numeroHabitacion": "101",
    "reserva": {
      "idReserva": 1,
      "clientePaga": {
        "nombre": "Juan",
        "apellidos": "Pérez"
      }
    }
  }
]
```

---

### Obtener contrato por ID

```http
GET /contratos/:id
```

**Respuesta:**
```json
{
  "idContrato": 1,
  "montoTotal": 400.00,
  "fechaCheckIn": "2024-10-30T10:00:00.000Z",
  "fechaCheckOut": null,
  "idReserva": 1,
  "numeroHabitacion": "101",
  "reserva": {
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "clientePaga": {
      "nombre": "Juan",
      "apellidos": "Pérez García"
    }
  },
  "habitacion": {
    "numeroHabitacion": "101",
    "tipoHabitacion": {
      "categoria": "Doble"
    }
  }
}
```

---

### Crear contrato (Check-in)

```http
POST /contratos
```

**Body:**
```json
{
  "idReserva": 1,
  "numeroHabitacion": "101",
  "montoTotal": 400.00
}
```

**Respuesta:** `201 Created`
```json
{
  "idContrato": 5,
  "montoTotal": 400,
  "fechaCheckIn": "2024-10-30T12:45:30.123Z",
  "fechaCheckOut": null,
  "idReserva": 1,
  "numeroHabitacion": "101",
  "reserva": {
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "clientePaga": {
      "nombre": "Juan",
      "apellidos": "Pérez García"
    }
  }
}
```

**Errores:**
- `404` - Reserva o habitación no encontrada
- `409` - La reserva ya tiene un contrato activo
- `400` - Habitación no disponible

---

### Hacer Check-out

```http
PUT /contratos/:id/checkout
```

**Parámetros:**
- `id` (número) - ID del contrato

**Ejemplo:**
```http
PUT /contratos/5/checkout
```

**Respuesta:** `200 OK`
```json
{
  "message": "Check-out realizado exitosamente",
  "contrato": {
    "idContrato": 5,
    "montoTotal": 400,
    "fechaCheckIn": "2024-10-30T12:45:30.123Z",
    "fechaCheckOut": "2024-10-30T13:00:15.456Z",
    "idReserva": 1,
    "numeroHabitacion": "101"
  }
}
```

**Errores:**
- `404` - Contrato no encontrado
- `400` - Check-out ya realizado

---

## Pernoctaciones

### Obtener pernoctación por ID

```http
GET /pernoctaciones/:id
```

**Respuesta:**
```json
{
  "idPernoctacion": 1,
  "fechaPernoctacion": "2024-12-01",
  "idReserva": 1,
  "idTipoHabitacion": 1,
  "reserva": {
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05"
  },
  "tipoHabitacion": {
    "categoria": "Doble"
  },
  "servicioPernoctacion": [
    {
      "servicio": {
        "codigoServicio": "SPA",
        "Precio": 50.00
      }
    }
  ]
}
```

---

## Códigos de Estado HTTP

| Código | Significado |
|--------|-------------|
| `200` | OK - Solicitud exitosa |
| `201` | Created - Recurso creado exitosamente |
| `400` | Bad Request - Datos inválidos o parámetros faltantes |
| `404` | Not Found - Recurso no encontrado |
| `409` | Conflict - Conflicto con datos existentes (duplicados) |
| `500` | Internal Server Error - Error del servidor |

---

## Formato de Respuestas de Error

Todos los errores retornan un JSON con el siguiente formato:

```json
{
  "error": "Nombre del error",
  "message": "Descripción del error",
  "details": {}
}
```

**Ejemplos:**

### Error 404
```json
{
  "error": "No encontrado",
  "message": "Hotel no encontrado"
}
```

### Error 400
```json
{
  "error": "Error de validación",
  "message": "Los datos proporcionados no son válidos",
  "details": "Fecha de salida debe ser posterior a fecha de entrada"
}
```

### Error 409
```json
{
  "error": "Conflicto",
  "message": "Ya existe un registro con esos datos únicos",
  "details": {
    "target": ["correoElectronico"]
  }
}
```

---

## Casos de Uso Completos

### Flujo 1: Buscar y Reservar

1. **Buscar hoteles**
   ```http
   GET /hoteles
   ```

2. **Ver disponibilidad**
   ```http
   GET /disponibilidad?fechaEntrada=2024-12-01&fechaSalida=2024-12-05&idHotel=1&idTipoHabitacion=1
   ```

3. **Crear reserva**
   ```http
   POST /reservas
   ```

### Flujo 2: Check-in y Check-out

4. **Hacer check-in**
   ```http
   POST /contratos
   ```

5. **Hacer check-out**
   ```http
   PUT /contratos/5/checkout
   ```

### Flujo 3: Consultar información

6. **Ver detalles de reserva**
   ```http
   GET /reservas/10
   ```

7. **Ver contrato**
   ```http
   GET /contratos/5
   ```

---

## Notas Importantes

- Todas las fechas deben estar en formato ISO: `YYYY-MM-DD`
- Los campos de dinero usan decimales con 2 posiciones
- El tipo de reserva debe ser exactamente `"Reserva"` o `"Walkin"`
- Los códigos de régimen son strings: `"AD"`, `"MP"`, `"PC"`, `"TI"`, `"SA"`
- Si un cliente existe (por DNI), sus datos se actualizan automáticamente

---

## Ver También

- `README.md` - Descripción general del proyecto
- `COMO_EJECUTAR.md` - Cómo iniciar el servidor
- `PRISMA.md` - Documentación de Prisma ORM
- `POSTMAN_DEMO.md` - Ejemplos para testing con Postman

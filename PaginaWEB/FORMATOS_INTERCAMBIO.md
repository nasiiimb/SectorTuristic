# Formatos de Intercambio de Datos (XML/JSON)

## Índice
1. [JSON - API REST](#json---api-rest)
2. [Colecciones Postman](#colecciones-postman)
3. [Estructuras de Datos Principales](#estructuras-de-datos-principales)
4. [Esquemas de Respuesta](#esquemas-de-respuesta)
5. [Ejemplos Completos](#ejemplos-completos)

---

## JSON - API REST

### Descripción General
El sistema utiliza **JSON** como formato de intercambio de datos entre el frontend (Vue.js) y el backend (Node.js + Express). Todas las API endpoints devuelven respuestas en JSON con estructura estándar.

### Ubicación de Documentación
- **Documentación API**: `WebService/API_GUIDE.md`
- **Colección Postman**: `WebService/PMS_Demo.postman_collection.json`
- **Base de Datos Schema**: `WebService/prisma/schema.prisma`

### Endpoints Principales

#### 1. Disponibilidad
**Ruta**: `GET /api/disponibilidad`

**Propósito**: Consultar habitaciones disponibles en un rango de fechas y ciudad

**Parámetros Query**:
```json
{
  "fechaEntrada": "YYYY-MM-DD",
  "fechaSalida": "YYYY-MM-DD",
  "ciudad": "nombre_ciudad"
}
```

**Respuesta Exitosa** (200 OK):
```json
{
  "success": true,
  "data": {
    "ciudad": "Palma",
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "hoteles": [
      {
        "idHotel": 1,
        "nombre": "Gran Hotel del Mar",
        "categoria": 5,
        "ubicacion": "Paseo Marítimo, 10, Palma",
        "tiposHabitacion": [
          {
            "idTipoHabitacion": 2,
            "categoria": "Doble Estándar",
            "disponibles": 5,
            "precio": 150.00,
            "foto_url": "https://images.unsplash.com/..."
          }
        ]
      }
    ]
  }
}
```

---

#### 2. Crear Reserva
**Ruta**: `POST /api/reservas`

**Propósito**: Crear una nueva reserva en el sistema

**Body JSON**:
```json
{
  "fechaEntrada": "2024-12-01",
  "fechaSalida": "2024-12-05",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "hotel": "Gran Hotel del Mar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "AD",
  "clientePaga": {
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
  ]
}
```

**Respuesta Exitosa** (201 Created):
```json
{
  "success": true,
  "message": "Reserva creada exitosamente",
  "data": {
    "idReserva": 42,
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "cliente": {
      "idCliente": 15,
      "nombre": "María",
      "correoElectronico": "maria.garcia@example.com"
    },
    "montoTotal": 600.00,
    "regimen": "AD",
    "canalReserva": "Web"
  }
}
```

**Respuesta Error** (400 Bad Request):
```json
{
  "success": false,
  "error": "Descripción del error",
  "details": "Información adicional sobre qué validación falló"
}
```

---

#### 3. Consultar Regímenes
**Ruta**: `GET /api/regimenes`

**Propósito**: Obtener lista de regímenes disponibles (Solo Alojamiento, Media Pensión, etc.)

**Respuesta Exitosa** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "idRegimen": 1,
      "codigo": "SA",
      "descripcion": "Solo Alojamiento"
    },
    {
      "idRegimen": 2,
      "codigo": "AD",
      "descripcion": "Alojamiento y Desayuno"
    },
    {
      "idRegimen": 3,
      "codigo": "MP",
      "descripcion": "Media Pensión"
    },
    {
      "idRegimen": 4,
      "codigo": "PC",
      "descripcion": "Pensión Completa"
    },
    {
      "idRegimen": 5,
      "codigo": "TI",
      "descripcion": "Todo Incluido"
    }
  ]
}
```

---

#### 4. Consultar Hoteles por Ciudad
**Ruta**: `GET /api/hoteles`

**Parámetros Query**:
```json
{
  "ciudad": "Palma",
  "incluyeHabitaciones": "true"
}
```

**Respuesta Exitosa** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "idHotel": 1,
      "nombre": "Gran Hotel del Mar",
      "ubicacion": "Paseo Marítimo, 10, Palma",
      "categoria": 5,
      "ciudad": "Palma",
      "tiposHabitacion": [
        {
          "idTipoHabitacion": 2,
          "categoria": "Doble Estándar",
          "camasIndividuales": 0,
          "camasDobles": 1,
          "foto_url": "https://images.unsplash.com/..."
        }
      ]
    }
  ]
}
```

---

#### 5. Consultar Tipos de Habitación
**Ruta**: `GET /api/tipos-habitacion`

**Respuesta Exitosa** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "idTipoHabitacion": 1,
      "categoria": "Individual",
      "camasIndividuales": 1,
      "camasDobles": 0,
      "foto_url": "https://images.pexels.com/..."
    },
    {
      "idTipoHabitacion": 2,
      "categoria": "Doble Estándar",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "foto_url": "https://images.unsplash.com/..."
    }
  ]
}
```

---

#### 6. Consultar Ciudades
**Ruta**: `GET /api/ciudades`

**Respuesta Exitosa** (200 OK):
```json
{
  "success": true,
  "data": [
    {
      "idCiudad": 1,
      "nombre": "Palma",
      "pais": "España"
    }
  ]
}
```

---

## Colecciones Postman

### Ubicación
`WebService/PMS_Demo.postman_collection.json`

### Importar en Postman

1. Abre Postman
2. Clic en **Collections** → **Import**
3. Selecciona el archivo `PMS_Demo.postman_collection.json`
4. La colección se cargará con todos los endpoints pre-configurados

### Endpoints Incluidos

| # | Nombre | Método | Ruta |
|---|--------|--------|------|
| 1 | Consultar Disponibilidad por Ciudad | GET | `/api/disponibilidad` |
| 2 | Crear Reserva | POST | `/api/reservas` |
| 3 | Obtener Regímenes | GET | `/api/regimenes` |
| 4 | Obtener Hoteles | GET | `/api/hoteles` |
| 5 | Obtener Tipos de Habitación | GET | `/api/tipos-habitacion` |
| 6 | Obtener Ciudades | GET | `/api/ciudades` |

---

## Estructuras de Datos Principales

### Cliente
Representa una persona que hace una reserva o se hospeda.

```json
{
  "idCliente": 15,
  "nombre": "María",
  "apellidos": "García López",
  "correoElectronico": "maria.garcia@example.com",
  "DNI": "12345678A",
  "fechaDeNacimiento": "1990-05-15",
  "email": "maria.garcia@example.com",
  "password": "hasheado_seguro"
}
```

**Campos Requeridos**: nombre, apellidos, correoElectronico, DNI
**Campos Opcionales**: email, password, fechaDeNacimiento

### Reserva
Representa una reserva de habitación(es) para una estancia.

```json
{
  "idReserva": 42,
  "fechaEntrada": "2024-12-01",
  "fechaSalida": "2024-12-05",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "idCliente_paga": 15,
  "idPrecioRegimen": 7,
  "montoTotal": 600.00,
  "huespedes": [
    { "idCliente": 15 }
  ]
}
```

**Tipos de Reserva**: "Reserva", "Walkin"
**Canales**: "Web", "Telefónico", "Canal Manager", etc.

### Hotel
Representa un hotel del sistema.

```json
{
  "idHotel": 1,
  "nombre": "Gran Hotel del Mar",
  "ubicacion": "Paseo Marítimo, 10, Palma",
  "categoria": 5,
  "idCiudad": 1,
  "tiposHabitacion": [2, 3, 4]
}
```

### Habitación (Room Type)
Categoría de habitación (no es una habitación física específica).

```json
{
  "idTipoHabitacion": 2,
  "categoria": "Doble Estándar",
  "camasIndividuales": 0,
  "camasDobles": 1,
  "foto_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32"
}
```

### Régimen
Plan de alojamiento con servicios incluidos.

```json
{
  "idRegimen": 2,
  "codigo": "AD",
  "descripcion": "Alojamiento y Desayuno"
}
```

**Códigos Estándar**:
- `SA`: Solo Alojamiento
- `AD`: Alojamiento y Desayuno
- `MP`: Media Pensión
- `PC`: Pensión Completa
- `TI`: Todo Incluido

### Precio Régimen
Precio de un régimen específico en un hotel.

```json
{
  "idPrecioRegimen": 7,
  "idRegimen": 2,
  "idHotel": 1,
  "precio": 100.00
}
```

---

## Esquemas de Respuesta

### Respuesta Exitosa Estándar

```json
{
  "success": true,
  "data": {},
  "message": "Descripción de lo que se hizo"
}
```

### Respuesta Error Estándar

```json
{
  "success": false,
  "error": "Error principal",
  "details": "Detalles adicionales",
  "statusCode": 400
}
```

### Códigos HTTP Utilizados

| Código | Significado | Ejemplo |
|--------|-------------|---------|
| 200 | OK - Consulta exitosa | GET /api/hoteles |
| 201 | Created - Recurso creado | POST /api/reservas |
| 400 | Bad Request - Error de validación | Parámetros inválidos |
| 404 | Not Found - Recurso no encontrado | Hotel no existe |
| 500 | Server Error - Error del servidor | Excepción no controlada |

---

## Ejemplos Completos

### Flujo Completo: Disponibilidad → Reserva

#### Paso 1: Consultar Disponibilidad

**Petición**:
```bash
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2024-12-01&fechaSalida=2024-12-05&ciudad=Palma
```

**Respuesta**:
```json
{
  "success": true,
  "data": {
    "ciudad": "Palma",
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "hoteles": [
      {
        "idHotel": 1,
        "nombre": "Gran Hotel del Mar",
        "categoria": 5,
        "tiposHabitacion": [
          {
            "idTipoHabitacion": 2,
            "categoria": "Doble Estándar",
            "disponibles": 5,
            "precio": 100.00
          },
          {
            "idTipoHabitacion": 3,
            "categoria": "Doble Superior",
            "disponibles": 3,
            "precio": 120.00
          }
        ]
      },
      {
        "idHotel": 2,
        "nombre": "Hotel Palma Centro",
        "categoria": 4,
        "tiposHabitacion": [
          {
            "idTipoHabitacion": 1,
            "categoria": "Individual",
            "disponibles": 8,
            "precio": 60.00
          }
        ]
      }
    ]
  }
}
```

#### Paso 2: Crear Reserva

**Petición**:
```bash
POST http://localhost:3000/api/reservas
Content-Type: application/json
```

**Body**:
```json
{
  "fechaEntrada": "2024-12-01",
  "fechaSalida": "2024-12-05",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "hotel": "Gran Hotel del Mar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "AD",
  "clientePaga": {
    "nombre": "Carlos",
    "apellidos": "Rodríguez Martínez",
    "correoElectronico": "carlos.rodriguez@example.com",
    "DNI": "87654321B",
    "fechaDeNacimiento": "1985-03-20"
  },
  "huespedes": [
    {
      "nombre": "Carlos",
      "apellidos": "Rodríguez Martínez",
      "correoElectronico": "carlos.rodriguez@example.com",
      "DNI": "87654321B"
    },
    {
      "nombre": "Ana",
      "apellidos": "Rodríguez Martínez",
      "correoElectronico": "ana.rodriguez@example.com",
      "DNI": "87654321C"
    }
  ]
}
```

**Respuesta**:
```json
{
  "success": true,
  "message": "Reserva creada exitosamente",
  "data": {
    "idReserva": 42,
    "idCliente": 16,
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "canalReserva": "Web",
    "tipo": "Reserva",
    "montoTotal": 480.00,
    "regimen": "AD",
    "hotel": {
      "idHotel": 1,
      "nombre": "Gran Hotel del Mar"
    },
    "cliente": {
      "idCliente": 16,
      "nombre": "Carlos",
      "apellidos": "Rodríguez Martínez",
      "correoElectronico": "carlos.rodriguez@example.com"
    },
    "huespedes": [
      {
        "idCliente": 16,
        "nombre": "Carlos",
        "apellidos": "Rodríguez Martínez"
      },
      {
        "idCliente": 17,
        "nombre": "Ana",
        "apellidos": "Rodríguez Martínez"
      }
    ]
  }
}
```

---

## Headers HTTP Requeridos

### Para Peticiones POST

```
Content-Type: application/json
Accept: application/json
```

### Para Peticiones GET

```
Accept: application/json
```

---

## Validaciones y Restricciones

### Cliente
- `correoElectronico`: Debe ser único en el sistema (UNIQUE constraint)
- `DNI`: Debe ser único en el sistema (UNIQUE constraint)
- `nombre`: Requerido, máximo 100 caracteres
- `apellidos`: Requerido, máximo 150 caracteres

### Reserva
- `fechaEntrada`: Debe ser menor a `fechaSalida`
- `fechaSalida`: Debe ser mayor o igual a `fechaEntrada`
- `idCliente_paga`: Cliente debe existir en la base de datos
- `tipo`: Solo acepta "Reserva" o "Walkin"

### Disponibilidad
- No se pueden reservar habitaciones ya ocupadas
- Las fechas no pueden ser en el pasado
- Mínimo 1 noche de estancia

---

## Notas Técnicas

### Formato de Fechas
Todas las fechas se transmiten en formato **ISO 8601**:
```
YYYY-MM-DD
```

Ejemplo: `2024-12-01`

### Moneda
- **Formato**: Decimal con 2 cifras
- **Símbolo**: EUR (€)
- **Separador Decimal**: Punto (.)
- **Ejemplos**: `100.00`, `150.50`, `1000.99`

### Códigos de Error
- `VALIDATION_ERROR`: Falló validación de datos
- `NOT_FOUND`: Recurso no encontrado
- `DUPLICATE_ENTRY`: Registro duplicado (email, DNI)
- `UNAVAILABLE`: Habitación no disponible
- `INTERNAL_ERROR`: Error del servidor

---

## Contacto y Soporte

Para consultas sobre el formato de intercambio de datos:
1. Consulta `WebService/API_GUIDE.md` para documentación completa
2. Importa `WebService/PMS_Demo.postman_collection.json` en Postman
3. Revisa los logs del servidor en `WebService/` para detalles de errores


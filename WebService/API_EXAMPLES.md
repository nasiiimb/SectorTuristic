# 📖 Ejemplos de uso de la API con Prisma

Este archivo contiene ejemplos de peticiones HTTP que puedes usar para probar tu API.

**Herramientas recomendadas:**
- Postman
- Insomnia
- Thunder Client (extensión VS Code)
- REST Client (extensión VS Code)
- Navegador (para peticiones GET)

---

## 🔍 **DISPONIBILIDAD (con precios)**

### Buscar disponibilidad por hotel
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

### Buscar disponibilidad por ciudad
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&ciudad=Palma
```

### Buscar disponibilidad por país
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&pais=España
```

---

## 🏨 **HOTELES**

### Obtener todos los hoteles
```http
GET http://localhost:3000/api/hoteles
```

### Obtener un hotel específico
```http
GET http://localhost:3000/api/hoteles/1
```

### Obtener tipos de habitación de un hotel
```http
GET http://localhost:3000/api/hoteles/1/tiposHabitacion
```

### Crear un nuevo hotel
```http
POST http://localhost:3000/api/hoteles
Content-Type: application/json

{
  "nombre": "Hotel Nuevo",
  "ubicacion": "Calle Principal 1",
  "categoria": "4 estrellas",
  "idCiudad": 1
}
```

### Actualizar un hotel
```http
PUT http://localhost:3000/api/hoteles/1
Content-Type: application/json

{
  "nombre": "Hotel Renovado",
  "categoria": "5 estrellas"
}
```

### Eliminar un hotel
```http
DELETE http://localhost:3000/api/hoteles/1
```

## 🌍 CIUDADES

### Obtener todas las ciudades
```http
GET http://localhost:3000/api/ciudades
```

### Obtener una ciudad específica
```http
GET http://localhost:3000/api/ciudades/1
```

### Crear una nueva ciudad
```http
POST http://localhost:3000/api/ciudades
Content-Type: application/json

{
  "nombre": "Palma de Mallorca",
  "pais": "España"
}
```

## 👤 CLIENTES

### Obtener todos los clientes
```http
GET http://localhost:3000/api/clientes
```

### Obtener un cliente específico
```http
GET http://localhost:3000/api/clientes/1
```

### Crear un nuevo cliente
```http
POST http://localhost:3000/api/clientes
Content-Type: application/json

{
  "nombre": "Juan",
  "apellidos": "García Pérez",
  "correoElectronico": "juan.garcia@email.com",
  "fechaDeNacimiento": "1990-05-15",
  "DNI": "12345678A"
}
```

### Actualizar un cliente
```http
PUT http://localhost:3000/api/clientes/1
Content-Type: application/json

{
  "correoElectronico": "juan.garcia.nuevo@email.com"
}
```

---

## 📅 **RESERVAS (con identificadores naturales)**

### Buscar reservas por cliente (útil para PMS)
```http
GET http://localhost:3000/api/reservas/buscar/cliente?nombre=Juan
```

```http
GET http://localhost:3000/api/reservas/buscar/cliente?apellido=Pérez
```

```http
GET http://localhost:3000/api/reservas/buscar/cliente?nombre=Juan&apellido=Pérez
```

### Obtener todas las reservas
```http
GET http://localhost:3000/api/reservas
```

### Obtener una reserva específica
```http
GET http://localhost:3000/api/reservas/1
```

### Crear una nueva reserva
```http
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "tipo": "Reserva",
  "canalReserva": "Web",
  "hotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "MP",
  "clientePaga": {
    "nombre": "Juan",
    "apellidos": "García Pérez",
    "correoElectronico": "juan.garcia@email.com",
    "DNI": "12345678A",
    "fechaDeNacimiento": "1990-05-15"
  },
  "huespedes": [
    {
      "nombre": "Juan",
      "apellidos": "García Pérez",
      "correoElectronico": "juan.garcia@email.com",
      "DNI": "12345678A",
      "fechaDeNacimiento": "1990-05-15"
    },
    {
      "nombre": "María",
      "apellidos": "López Sánchez",
      "correoElectronico": "maria.lopez@email.com",
      "DNI": "87654321B",
      "fechaDeNacimiento": "1992-08-20"
    }
  ]
}
```

**Nota:** 
- `tipo` puede ser: "Reserva" o "Walkin"
- `regimen` debe ser el código (MP, PC, AD, SA)
- `clientePaga` es el objeto con los datos del cliente que paga
- `huespedes` es un array con los datos de todos los huéspedes (opcional)
- Si el cliente o huéspedes ya existen en la BD (por DNI), se usan los existentes

### Actualizar una reserva
```http
PUT http://localhost:3000/api/reservas/1
Content-Type: application/json

{
  "fechaEntrada": "2025-12-02",
  "fechaSalida": "2025-12-06",
  "canalReserva": "Teléfono",
  "tipo": "Reserva",
  "idTipoHabitacion": 2
}
```

**Nota:** Solo se pueden actualizar reservas antes del check-in. Se puede cambiar fechas, canal, tipo y tipo de habitación.

### Cancelar una reserva (libera disponibilidad)
```http
DELETE http://localhost:3000/api/reservas/1
```

---

## 🔑 **CHECK-IN / CHECK-OUT**

### Hacer check-in (especificar habitación)
```http
POST http://localhost:3000/api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201"
}
```

**Nota:** El número de habitación debe coincidir con el tipo reservado y pertenecer al hotel correcto.

---

## 📋 **CONTRATOS (Check-ins/Check-outs)**

### Obtener todos los contratos
```http
GET http://localhost:3000/api/contratos
```

**Respuesta de ejemplo:**
```json
{
  "total": 5,
  "activos": 2,
  "finalizados": 3,
  "contratos": [
    {
      "idContrato": 1,
      "montoTotal": "750",
      "fechaCheckIn": "2025-10-29T17:43:41.000Z",
      "fechaCheckOut": "2025-10-29T17:43:41.000Z",
      "numeroHabitacion": "H1-301",
      "estado": "Finalizado",
      "reserva": {
        "idReserva": 1,
        "fechaEntrada": "2025-11-01T00:00:00.000Z",
        "fechaSalida": "2025-11-06T00:00:00.000Z",
        "canalReserva": "Web",
        "tipo": "Reserva",
        "clientePaga": {
          "idCliente": 1,
          "nombre": "Maria",
          "apellidos": "Garcia Lopez",
          "correoElectronico": "maria.garcia@email.com",
          "DNI": "11111111A"
        },
        "hotel": {
          "idHotel": 1,
          "nombre": "Gran Hotel del Mar",
          "ubicacion": "Paseo Maritimo, 10, Palma",
          "categoria": 5
        },
        "regimen": {
          "idRegimen": 4,
          "codigo": "PC"
        },
        "tipoHabitacion": {
          "idTipoHabitacion": 3,
          "categoria": "Suite Junior",
          "camasIndividuales": 0,
          "camasDobles": 2
        },
        "numeroNoches": 5
      },
      "habitacion": {
        "numeroHabitacion": "H1-301",
        "idTipoHabitacion": 3,
        "idHotel": 1,
        "hotel": {
          "idHotel": 1,
          "nombre": "Gran Hotel del Mar"
        },
        "tipoHabitacion": {
          "idTipoHabitacion": 3,
          "categoria": "Suite Junior"
        }
      }
    }
  ]
}
```

### Hacer check-out
```http
POST http://localhost:3000/api/contratos/1/checkout
```

---

## 🛎️ **SERVICIOS ADICIONALES**

### Obtener todos los servicios
```http
GET http://localhost:3000/api/servicios
```

### Obtener un servicio por código
```http
GET http://localhost:3000/api/servicios/SPA
```

### Añadir servicio a una pernoctación
```http
POST http://localhost:3000/api/pernoctaciones/1/servicios
Content-Type: application/json

{
  "codigoServicio": "SPA"
}
```

---

## 🛏️ **TIPOS DE HABITACIÓN**

### Obtener todos los tipos de habitación
```http
GET http://localhost:3000/api/tipos-habitacion
```

---

## 🍽️ **REGÍMENES**

### Obtener todos los regímenes
```http
GET http://localhost:3000/api/regimenes
```

### Obtener un régimen por código
```http
GET http://localhost:3000/api/regimenes/MP
```

---

## 🏥 **HEALTH CHECK**

### Verificar que el servidor está funcionando
```http
GET http://localhost:3000/health
```

---

## 🎯 **FLUJO COMPLETO - Ejemplo Práctico**

### 1. Buscar disponibilidad
```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

### 2. Crear reserva
```http
POST http://localhost:3000/api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "tipo": "Reserva",
  "canalReserva": "Web",
  "hotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "MP",
  "clientePaga": {
    "nombre": "Juan",
    "apellidos": "García Pérez",
    "correoElectronico": "juan.garcia@email.com",
    "DNI": "12345678A",
    "fechaDeNacimiento": "1990-05-15"
  },
  "huespedes": [
    {
      "nombre": "Juan",
      "apellidos": "García Pérez",
      "correoElectronico": "juan.garcia@email.com",
      "DNI": "12345678A",
      "fechaDeNacimiento": "1990-05-15"
    },
    {
      "nombre": "María",
      "apellidos": "López Sánchez",
      "correoElectronico": "maria.lopez@email.com",
      "DNI": "87654321B",
      "fechaDeNacimiento": "1992-08-20"
    }
  ]
}
```

### 3. Hacer check-in
```http
POST http://localhost:3000/api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201"
}
```

### 4. Añadir servicio
```http
POST http://localhost:3000/api/pernoctaciones/1/servicios
Content-Type: application/json

{
  "codigoServicio": "SPA"
}
```

### 5. Hacer check-out
```http
POST http://localhost:3000/api/contratos/1/checkout
```

---

## 📝 **Notas Importantes**

- ✅ La API usa **identificadores naturales** (nombres de hotel, categorías, códigos de régimen)
- ✅ Los **huéspedes se pueden especificar en la reserva o añadirse después**
- ✅ El **cliente que paga se especifica con un objeto** con todos sus datos
- ✅ Si el cliente o huéspedes ya existen (por DNI), se reutilizan
- ✅ La **disponibilidad cuenta pernoctaciones** (reservas), no contratos (check-ins)
- ✅ Los **precios son dinámicos** según categoría de hotel y tipo de habitación
- ✅ Las fechas deben estar en formato **YYYY-MM-DD**
- ✅ El **tipo de reserva** puede ser "Reserva" o "Walkin"
- ✅ Los **códigos de régimen** son: MP (Media Pensión), PC (Pensión Completa), AD (Alojamiento y Desayuno), SA (Solo Alojamiento)
- ✅ Todas las respuestas incluyen datos relacionados (joins automáticos con Prisma)

---

## 🔧 **Ejemplos con cURL (PowerShell)**

### Buscar disponibilidad
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran" | Select-Object -ExpandProperty Content
```

### Crear reserva
```powershell
$body = @{
  fechaEntrada = "2025-12-01"
  fechaSalida = "2025-12-05"
  tipo = "Reserva"
  canalReserva = "Web"
  hotel = "Gran Hotel Miramar"
  tipoHabitacion = "Doble Superior"
  regimen = "MP"
  clientePaga = @{
    nombre = "Juan"
    apellidos = "García Pérez"
    correoElectronico = "juan.garcia@email.com"
    DNI = "12345678A"
    fechaDeNacimiento = "1990-05-15"
  }
  huespedes = @(
    @{
      nombre = "Juan"
      apellidos = "García Pérez"
      correoElectronico = "juan.garcia@email.com"
      DNI = "12345678A"
      fechaDeNacimiento = "1990-05-15"
    },
    @{
      nombre = "María"
      apellidos = "López Sánchez"
      correoElectronico = "maria.lopez@email.com"
      DNI = "87654321B"
      fechaDeNacimiento = "1992-08-20"
    }
  )
} | ConvertTo-Json -Depth 3

Invoke-WebRequest -Uri "http://localhost:3000/api/reservas" -Method POST -Body $body -ContentType "application/json" | Select-Object -ExpandProperty Content
```

### Obtener todos los hoteles
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/hoteles" | Select-Object -ExpandProperty Content
```

---

## 📚 **Más Información**

Para detalles completos de cada endpoint, consulta:
- `API_DOCUMENTATION.md` - Documentación completa
- `TESTING_GUIDE.md` - Guía de pruebas paso a paso

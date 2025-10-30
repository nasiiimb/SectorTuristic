# 🎬 Demo Postman - Flujo Completo de Reserva

## 📋 Configuración Inicial
- **Base URL**: `http://localhost:3000/api`
- **Puerto**: 3000
- Asegúrate de que el servidor esté corriendo: `npm run dev`

---

## 🔄 Flujo Completo: Disponibilidad → Reserva → Check-in → Check-out

### 1️⃣ Consultar Disponibilidad de Habitaciones

**Endpoint**: `GET /disponibilidad`

**Query Parameters**:
- `fechaEntrada`: `2024-12-01`
- `fechaSalida`: `2024-12-05`
- `idHotel`: `1`
- `idTipoHabitacion`: `1`

**URL Completa**:
```
http://localhost:3000/api/disponibilidad?fechaEntrada=2024-12-01&fechaSalida=2024-12-05&idHotel=1&idTipoHabitacion=1
```

**Respuesta Esperada** (200 OK):
```json
{
  "disponible": true,
  "habitacionesDisponibles": [
    "101",
    "102",
    "103"
  ],
  "totalDisponibles": 3,
  "detalles": {
    "fechaEntrada": "2024-12-01",
    "fechaSalida": "2024-12-05",
    "noches": 4,
    "hotel": "Hotel Paraíso",
    "tipoHabitacion": "Doble"
  }
}
```

---

### 2️⃣ Crear una Reserva

**Endpoint**: `POST /reservas`

**Headers**:
```
Content-Type: application/json
```

**Body (raw JSON)**:
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

**Respuesta Esperada** (201 Created):
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
    "apellidos": "García López",
    "correoElectronico": "maria.garcia@example.com",
    "DNI": "12345678A"
  },
  "pernoctaciones": [
    {
      "idPernoctacion": 40,
      "fechaPernoctacion": "2024-12-01T00:00:00.000Z",
      "idTipoHabitacion": 1
    },
    {
      "idPernoctacion": 41,
      "fechaPernoctacion": "2024-12-02T00:00:00.000Z",
      "idTipoHabitacion": 1
    },
    {
      "idPernoctacion": 42,
      "fechaPernoctacion": "2024-12-03T00:00:00.000Z",
      "idTipoHabitacion": 1
    },
    {
      "idPernoctacion": 43,
      "fechaPernoctacion": "2024-12-04T00:00:00.000Z",
      "idTipoHabitacion": 1
    }
  ]
}
```

**⚠️ IMPORTANTE**: Anota el `idReserva` que te devuelve (ej: 10), lo necesitarás para los siguientes pasos.

---

### 3️⃣ Hacer Check-in (Crear Contrato)

**Endpoint**: `POST /contratos`

**Headers**:
```
Content-Type: application/json
```

**Body (raw JSON)**:
```json
{
  "idReserva": 10,
  "numeroHabitacion": "101",
  "montoTotal": 400.00
}
```

**Respuesta Esperada** (201 Created):
```json
{
  "idContrato": 5,
  "montoTotal": 400,
  "fechaCheckIn": "2024-10-30T12:45:30.123Z",
  "fechaCheckOut": null,
  "idReserva": 10,
  "numeroHabitacion": "101",
  "reserva": {
    "idReserva": 10,
    "fechaEntrada": "2024-12-01T00:00:00.000Z",
    "fechaSalida": "2024-12-05T00:00:00.000Z",
    "tipo": "Reserva",
    "clientePaga": {
      "nombre": "María",
      "apellidos": "García López",
      "correoElectronico": "maria.garcia@example.com"
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

**⚠️ IMPORTANTE**: Anota el `idContrato` que te devuelve (ej: 5), lo necesitarás para el checkout.

---

### 4️⃣ Hacer Check-out (Finalizar Estancia)

**Endpoint**: `PUT /contratos/:idContrato/checkout`

**URL**: 
```
http://localhost:3000/api/contratos/5/checkout
```
*(Reemplaza `5` con el idContrato que obtuviste en el paso anterior)*

**Headers**:
```
Content-Type: application/json
```

**Body**: *(vacío o sin body)*

**Respuesta Esperada** (200 OK):
```json
{
  "message": "Check-out realizado exitosamente",
  "contrato": {
    "idContrato": 5,
    "montoTotal": 400,
    "fechaCheckIn": "2024-10-30T12:45:30.123Z",
    "fechaCheckOut": "2024-10-30T13:00:15.456Z",
    "idReserva": 10,
    "numeroHabitacion": "101",
    "reserva": {
      "idReserva": 10,
      "fechaEntrada": "2024-12-01T00:00:00.000Z",
      "fechaSalida": "2024-12-05T00:00:00.000Z",
      "clientePaga": {
        "nombre": "María",
        "apellidos": "García López",
        "correoElectronico": "maria.garcia@example.com"
      }
    }
  }
}
```

---

## 📊 Endpoints Adicionales para el Video (Opcionales)

### 5️⃣ Ver Detalles de la Reserva

**Endpoint**: `GET /reservas/:idReserva`

**URL**: 
```
http://localhost:3000/api/reservas/10
```

**Respuesta**: Detalles completos de la reserva con cliente, pernoctaciones, etc.

---

### 6️⃣ Listar Todos los Hoteles

**Endpoint**: `GET /hoteles`

**URL**: 
```
http://localhost:3000/api/hoteles
```

**Respuesta**: Lista de todos los hoteles con sus ciudades.

---

### 7️⃣ Ver Tipos de Habitación de un Hotel

**Endpoint**: `GET /hoteles/:idHotel/tiposHabitacion`

**URL**: 
```
http://localhost:3000/api/hoteles/1/tiposHabitacion
```

**Respuesta**: Tipos de habitación disponibles en el hotel.

---

## 🎯 Orden Recomendado para el Video

1. **Mostrar hoteles disponibles** → `GET /hoteles`
2. **Consultar disponibilidad** → `GET /disponibilidad` (fechas 2024-12-01 a 2024-12-05)
3. **Crear reserva** → `POST /reservas` (guarda el idReserva)
4. **Ver detalles de la reserva** → `GET /reservas/:idReserva`
5. **Hacer check-in** → `POST /contratos` (guarda el idContrato)
6. **Hacer check-out** → `PUT /contratos/:idContrato/checkout`
7. **Verificar contrato finalizado** → `GET /contratos/:idContrato`

---

## 🔧 Tips para el Video

- ✅ Inicia el servidor antes: `cd WebService && npm run dev`
- ✅ Usa fechas futuras para evitar validaciones
- ✅ Copia los IDs generados (idReserva, idContrato) para usarlos en siguientes pasos
- ✅ Muestra las respuestas en formato Pretty (Postman lo hace automáticamente)
- ✅ Ten preparada la base de datos con datos de prueba

---

## 🚨 Posibles Errores y Soluciones

### Error 404 - Hotel/Habitación no encontrado
- Verifica que `idHotel: 1` y `idTipoHabitacion: 1` existan en tu BD

### Error 409 - Conflicto (email duplicado)
- Cambia el email del cliente en cada prueba: `maria.garcia2@example.com`

### Error 400 - Datos inválidos
- Revisa que las fechas estén en formato `YYYY-MM-DD`
- Asegúrate de que `fechaSalida > fechaEntrada`
- Verifica que el tipo sea `"Reserva"` o `"Walkin"` (exacto)

---

## 📁 Importar a Postman

Puedes importar esta colección creando un archivo JSON en Postman o copiando cada endpoint manualmente.

**¡Buena suerte con tu video! 🎥**

# Ejemplos de uso de la API con Prisma

Este archivo contiene ejemplos de peticiones HTTP que puedes usar para probar tu API.
Puedes usar herramientas como Postman, Insomnia, o la extensión REST Client de VS Code.

## 🏨 HOTELES

### Obtener todos los hoteles
```http
GET http://localhost:3000/api/hoteles
```

### Obtener un hotel específico
```http
GET http://localhost:3000/api/hoteles/1
```

### Crear un nuevo hotel
```http
POST http://localhost:3000/api/hoteles
Content-Type: application/json

{
  "nombre": "Hotel Paradise",
  "ubicacion": "Playa de Palma",
  "categoria": 5,
  "idCiudad": 1
}
```

### Actualizar un hotel
```http
PUT http://localhost:3000/api/hoteles/1
Content-Type: application/json

{
  "nombre": "Hotel Paradise Renovado",
  "categoria": 5
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

## 📅 RESERVAS

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
  "fechaEntrada": "2025-11-01",
  "fechaSalida": "2025-11-05",
  "canalReserva": "Web",
  "tipo": "Reserva",
  "idCliente_paga": 1,
  "idPrecioRegimen": 1,
  "huespedes": [1, 2]
}
```

### Actualizar una reserva
```http
PUT http://localhost:3000/api/reservas/1
Content-Type: application/json

{
  "fechaSalida": "2025-11-06",
  "canalReserva": "Telefono"
}
```

### Cancelar una reserva
```http
DELETE http://localhost:3000/api/reservas/1
```

## 🏥 Health Check

### Verificar que el servidor está funcionando
```http
GET http://localhost:3000/health
```

## 📝 Notas

- Todas las respuestas incluyen los datos relacionados (joins automáticos)
- Los campos de fecha deben estar en formato ISO: "YYYY-MM-DD"
- Los errores devuelven código 500 con un mensaje descriptivo
- Las búsquedas por ID que no existen devuelven 404

## 🔧 Ejemplos con cURL

### Crear un hotel
```bash
curl -X POST http://localhost:3000/api/hoteles \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Hotel Paradise",
    "ubicacion": "Playa de Palma",
    "categoria": 5,
    "idCiudad": 1
  }'
```

### Obtener todos los hoteles
```bash
curl http://localhost:3000/api/hoteles
```

### Obtener un hotel específico
```bash
curl http://localhost:3000/api/hoteles/1
```

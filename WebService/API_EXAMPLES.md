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

### Crear una nueva reserva (solo quien paga)
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

**Nota:** Los huéspedes se especifican en el check-in, no en la reserva.

### Actualizar una reserva
```http
PUT http://localhost:3000/api/reservas/1
Content-Type: application/json

{
  "regimen": "Pensión Completa"
}
```

### Cancelar una reserva (libera disponibilidad)
```http
DELETE http://localhost:3000/api/reservas/1
```

---

## 🔑 **CHECK-IN / CHECK-OUT**

### Hacer check-in (especificar huéspedes aquí)
```http
POST http://localhost:3000/api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201",
  "dniHuespedes": ["12345678A", "87654321B"]
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
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "dniClientePaga": "12345678A"
}
```

### 3. Hacer check-in
```http
POST http://localhost:3000/api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201",
  "dniHuespedes": ["12345678A", "87654321B"]
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

- ✅ La API usa **identificadores naturales** (nombres, DNI) no IDs internos
- ✅ Los **huéspedes se especifican en el check-in**, no en la reserva
- ✅ La **disponibilidad cuenta pernoctaciones** (reservas), no contratos (check-ins)
- ✅ Los **precios son dinámicos** según categoría de hotel y tipo de habitación
- ✅ Las fechas deben estar en formato **YYYY-MM-DD**
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
  nombreHotel = "Gran Hotel Miramar"
  tipoHabitacion = "Doble Superior"
  regimen = "Media Pensión"
  dniClientePaga = "12345678A"
} | ConvertTo-Json

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

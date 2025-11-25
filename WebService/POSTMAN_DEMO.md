# 🎬 Demo Postman - Flujo Completo de Reserva

## 📋 Configuración Inicial
- **Base URL**: `http://localhost:3000/api`
- **Puerto**: 3000
- Asegúrate de que el servidor esté corriendo: `npm run dev`

⚠️ **IMPORTANTE: Todas las rutas están en PLURAL**
- ✅ `/api/reservas` (correcto)
- ❌ `/api/reserva` (incorrecto)
- ✅ `/api/hoteles` (correcto)
- ✅ `/api/contratos` (correcto)

---

## 🔄 Flujo Completo: Disponibilidad → Reserva → Check-in → Check-out

### 1️⃣ Consultar Disponibilidad de Habitaciones por Ciudad

**Endpoint**: `GET /disponibilidad`

**Query Parameters**:
- `fechaEntrada`: `2024-12-01`
- `fechaSalida`: `2024-12-05`
- `ciudad`: `Palma`

**URL Completa**:
```
http://localhost:3000/api/disponibilidad?fechaEntrada=2024-12-01&fechaSalida=2024-12-05&ciudad=Palma
```

**Nota**: La respuesta muestra **todos los hoteles de Palma** que tienen disponibilidad en esas fechas.

---

### 2️⃣ Crear una Reserva

**Endpoint**: `POST /reservas` ⚠️ **(Nota: plural "reservas", no "reserva")**

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

**Notas importantes**: 
- `hotel`: Nombre del hotel (ej: "Gran Hotel del Mar")
- `tipoHabitacion`: Nombre del tipo de habitación (ej: "Doble Superior")
- `regimen`: Código del régimen (ej: "AD" para Alojamiento y Desayuno)
- `clientePaga`: Objeto con los datos del cliente que paga
- `huespedes`: Array con los datos de los huéspedes (puede incluir al cliente que paga)
- **Códigos de régimen disponibles**: SA, AD, MP, PC, TI

**⚠️ IMPORTANTE**: Anota el `idReserva` que te devuelve la respuesta, lo necesitarás para los siguientes pasos.

---


### 4️⃣ Hacer Check-in

**Endpoint**: `POST /reservas/:idReserva/checkin`

**URL**: 
```
http://localhost:3000/api/reservas/1/checkin
```
*(Reemplaza `1` con el idReserva que obtuviste)*

**Headers**:
```
Content-Type: application/json
```

**Body (raw JSON)**:
```json
{
  "numeroHabitacion": "H1-101"
}
```

**Nota**: El check-in registra la fecha y hora de entrada del cliente usando la zona horaria del país donde está ubicado el hotel.

---


### 5️⃣ Hacer Check-out (Finalizar Estancia)

**Endpoint**: `POST /contratos/:idContrato/checkout`

**URL**: 
```
http://localhost:3000/api/contratos/1/checkout
```
*(Reemplaza `1` con el idContrato que obtuviste en el paso anterior)*

**Headers**:
```
Content-Type: application/json
```

**Body**: *(vacío o sin body)*

---

## 📊 Endpoints Adicionales para el Video (Opcionales)

### 6️⃣ Ver Detalles de la Reserva

**Endpoint**: `GET /reservas/:idReserva`

**URL**: 
```
http://localhost:3000/api/reservas/10
```
*(Reemplaza `10` con el idReserva que obtuviste)*

---

### 7️⃣ Listar Todos los Hoteles

**Endpoint**: `GET /hoteles`

**URL**: 
```
http://localhost:3000/api/hoteles
```

---

### 8️⃣ Ver Tipos de Habitación de un Hotel

**Endpoint**: `GET /hoteles/:idHotel/tiposHabitacion`

**URL**: 
```
http://localhost:3000/api/hoteles/1/tiposHabitacion
```

---

## 🎯 Orden Recomendado para el Video

1. **Mostrar hoteles disponibles** → `GET /hoteles`
2. **Consultar disponibilidad por ciudad** → `GET /disponibilidad?ciudad=Palma&fechaEntrada=2024-12-01&fechaSalida=2024-12-05`
3. **Crear reserva** → `POST /reservas` (guarda el idReserva)
4. **Ver detalles de la reserva** → `GET /reservas/:idReserva`
5. **Crear contrato** → `POST /contratos` (guarda el idContrato)
6. **Hacer check-in** → `POST /reservas/:idReserva/checkin`
7. **Hacer check-out** → `PUT /contratos/:idContrato/checkout`
8. **Verificar contrato finalizado** → `GET /contratos/:idContrato`

---

## 🔧 Tips para el Video

- ✅ Inicia el servidor antes: `cd WebService && npm run dev`
- ✅ Usa fechas futuras para evitar validaciones
- ✅ Copia los IDs generados (idReserva, idContrato) para usarlos en siguientes pasos
- ✅ Muestra las respuestas en formato Pretty (Postman lo hace automáticamente)
- ✅ Ten preparada la base de datos con datos de prueba

---

## 🚨 Posibles Errores y Soluciones

### Error 404 - Hotel/Ciudad no encontrada
- Verifica que la ciudad "Palma" exista en tu BD
- Prueba con otras ciudades: "Barcelona", "Madrid", etc.

### Error 409 - Conflicto (email duplicado)
- Cambia el email del cliente en cada prueba: `maria.garcia2@example.com`

### Error 400 - Datos inválidos
- Revisa que las fechas estén en formato `YYYY-MM-DD`
- Asegúrate de que `fechaSalida > fechaEntrada`
- Verifica que el tipo sea `"Reserva"` o `"Walkin"` (exacto)
- Asegúrate de proporcionar al menos un filtro: `ciudad`, `hotel` o `pais`

---

## 📁 Importar a Postman

Puedes importar esta colección creando un archivo JSON en Postman o copiando cada endpoint manualmente.

---

## 🎯 EJEMPLO ADICIONAL: Segundo Cliente (Carlos Martínez)

### 📝 Reserva para Carlos Martínez

**Endpoint**: `POST /reservas`

**Body**:
```json
{
  "fechaEntrada": "2024-12-10",
  "fechaSalida": "2024-12-15",
  "canalReserva": "Booking",
  "tipo": "Reserva",
  "hotel": "Hotel Palma Centro",
  "tipoHabitacion": "Individual",
  "regimen": "MP",
  "clientePaga": {
    "nombre": "Carlos",
    "apellidos": "Martínez Ruiz",
    "correoElectronico": "carlos.martinez@example.com",
    "DNI": "87654321B",
    "fechaDeNacimiento": "1985-08-22"
  },
  "huespedes": [
    {
      "nombre": "Carlos",
      "apellidos": "Martínez Ruiz",
      "correoElectronico": "carlos.martinez@example.com",
      "DNI": "87654321B"
    }
  ]
}
```

**Detalles**:
- Hotel: Hotel Palma Centro (4 estrellas)
- Tipo: Individual
- Régimen: MP (Media Pensión)
- Fechas: Del 10 al 15 de diciembre (5 noches)

**⚠️ Anota el `idReserva` de la respuesta**

---

### 🏨 Crear Contrato para Carlos Martínez

**Endpoint**: `POST /contratos`

**Body**:
```json
{
  "idReserva": 2,
  "numeroHabitacion": "201",
  "montoTotal": 575.00
}
```

**Cálculo del monto**:
- Habitación Individual: 80.00€ x 5 noches = 400.00€
- Régimen MP (Media Pensión): 35.00€ x 5 noches = 175.00€
- **Total: 575.00€**

**⚠️ Anota el `idContrato` de la respuesta**

---

### ✅ Check-in para Carlos Martínez

**Endpoint**: `POST /reservas/:idReserva/checkin`

**URL**:
```
http://localhost:3000/api/reservas/2/checkin
```
*(Reemplaza `2` con el idReserva real que obtuviste)*

**Body**:
```json
{
  "numeroHabitacion": "201"
}
```

---

### 🚪 Check-out para Carlos Martínez

**Endpoint**: `PUT /contratos/2/checkout`

**URL**:
```
http://localhost:3000/api/contratos/2/checkout
```
*(Reemplaza `2` con el idContrato real que obtuviste)*

**Body**: *(vacío)*

---

**¡Buena suerte con tu video! 🎥**

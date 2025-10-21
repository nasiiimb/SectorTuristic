# 🔄 CORRECCIÓN CRÍTICA: Lógica de Disponibilidad

**Fecha**: 21 de Octubre, 2025  
**Estado**: ✅ CORREGIDO

---

## ❌ PROBLEMA IDENTIFICADO

### Lógica INCORRECTA (Anterior)
La disponibilidad se calculaba basándose en **contratos** (habitaciones físicas asignadas).

```typescript
// ❌ INCORRECTO: Buscaba contratos existentes
const reservasOcupadas = await prisma.reserva.findMany({
  where: {
    contrato: {
      habitacion: {
        idHotel: hotelEncontrado.idHotel,
      },
    },
  },
});
```

**Problema**: Los contratos solo se crean en el **check-in**, NO en la reserva.

---

## ✅ SOLUCIÓN CORRECTA

### Flujo Real del Sistema

```
1. RESERVA → Cliente reserva un TIPO de habitación (ej: "Doble Superior")
   ├─ Se crea: Reserva
   ├─ Se crea: Pernoctaciones (vinculadas al tipo de habitación)
   └─ NO se asigna habitación física todavía

2. CHECK-IN → Se asigna una habitación física específica
   ├─ Se crea: Contrato (vincula reserva + habitación física)
   └─ Ahora sí se asigna: "H1-201"

3. CHECK-OUT → Se cierra el contrato
   └─ Se actualiza: fechaCheckOut en Contrato
```

### Lógica CORRECTA (Nueva)

```typescript
// ✅ CORRECTO: Cuenta reservas por tipo de habitación
// 1. Contar total de habitaciones físicas por tipo
const habitacionesPorTipo = await prisma.habitacion.groupBy({
  by: ['idTipoHabitacion'],
  where: { idHotel: hotelEncontrado.idHotel },
  _count: { numeroHabitacion: true },
});

// 2. Contar reservas activas por tipo (mediante pernoctaciones)
const reservasEnRango = await prisma.reserva.findMany({
  where: {
    AND: [
      { fechaEntrada: { lt: salida } },
      { fechaSalida: { gt: entrada } },
    ],
  },
  include: { pernoctaciones: true },
});

// 3. Calcular: disponibles = total - reservadas
const disponibles = totalHabitaciones - reservasActuales;
```

---

## 📊 Ejemplo Práctico

### Hotel con 12 habitaciones

```
Gran Hotel del Mar:
├─ 2 habitaciones Doble Estándar (H1-101, H1-102)
├─ 4 habitaciones Doble Superior (H1-201, H1-202, H1-203, H1-204)
└─ 6 habitaciones Suite Junior (H1-301 ... H1-306)
```

### Escenario: 3 Reservas para el 1-5 de Diciembre

```sql
-- Reserva 1: Juan reserva "Doble Superior" (sin asignar habitación todavía)
INSERT INTO Reserva (fechaEntrada, fechaSalida, ...) VALUES ('2025-12-01', '2025-12-05', ...);
INSERT INTO Pernoctacion (idReserva, idTipoHabitacion, fecha) VALUES (1, 2, '2025-12-01'), ...;

-- Reserva 2: María reserva "Suite Junior" (sin asignar habitación todavía)
INSERT INTO Reserva (fechaEntrada, fechaSalida, ...) VALUES ('2025-12-01', '2025-12-05', ...);
INSERT INTO Pernoctacion (idReserva, idTipoHabitacion, fecha) VALUES (2, 3, '2025-12-01'), ...;

-- Reserva 3: Pedro reserva "Doble Superior" (sin asignar habitación todavía)
INSERT INTO Reserva (fechaEntrada, fechaSalida, ...) VALUES ('2025-12-01', '2025-12-05', ...);
INSERT INTO Pernoctacion (idReserva, idTipoHabitacion, fecha) VALUES (3, 2, '2025-12-01'), ...;
```

### ❌ Lógica Anterior (INCORRECTA)

```
Buscaba contratos → No encuentra ninguno (porque no se ha hecho check-in)
Resultado: "12 habitaciones disponibles" ❌ FALSO
```

**Problema**: Permitiría hacer más reservas de las que hay habitaciones físicas.

### ✅ Lógica Nueva (CORRECTA)

```javascript
// Doble Estándar (idTipo=1)
Total: 2 habitaciones físicas
Reservas: 0
Disponibles: 2 ✅

// Doble Superior (idTipo=2)
Total: 4 habitaciones físicas
Reservas: 2 (Juan y Pedro)
Disponibles: 2 ✅

// Suite Junior (idTipo=3)
Total: 6 habitaciones físicas
Reservas: 1 (María)
Disponibles: 5 ✅
```

**Resultado Correcto**:
```json
{
  "tiposDisponibles": [
    {
      "categoria": "Doble Estándar",
      "disponibles": 2,
      "totalHabitaciones": 2,
      "reservasActuales": 0,
      "precioPorNoche": "150"
    },
    {
      "categoria": "Doble Superior",
      "disponibles": 2,
      "totalHabitaciones": 4,
      "reservasActuales": 2,
      "precioPorNoche": "200"
    },
    {
      "categoria": "Suite Junior",
      "disponibles": 5,
      "totalHabitaciones": 6,
      "reservasActuales": 1,
      "precioPorNoche": "300"
    }
  ]
}
```

---

## 🔍 Diferencias Clave

| Aspecto | ❌ Lógica Anterior | ✅ Lógica Correcta |
|---------|-------------------|-------------------|
| **Qué cuenta** | Contratos (habitaciones asignadas) | Reservas (por tipo de habitación) |
| **Cuándo se crea** | En el check-in | En la reserva |
| **Tabla usada** | `Contrato` | `Pernoctacion` |
| **Relación** | Reserva → Contrato → Habitación | Reserva → Pernoctacion → TipoHabitacion |
| **Problema** | No refleja reservas sin check-in | ✅ Refleja todas las reservas |

---

## 📋 Nueva Estructura de Respuesta

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
      "precioPorNoche": "150",
      "codigoTarifa": "TARIFA_5E_DBL_STD",
      "disponibles": 2,              ← NUEVO: Habitaciones disponibles
      "totalHabitaciones": 2,        ← NUEVO: Total de este tipo
      "reservasActuales": 0          ← NUEVO: Reservas activas
    }
  ],
  "totalTiposDisponibles": 3
}
```

### Campos Nuevos

- **`disponibles`**: Cantidad de habitaciones de este tipo que se pueden reservar
- **`totalHabitaciones`**: Total de habitaciones físicas de este tipo en el hotel
- **`reservasActuales`**: Cantidad de reservas activas para este tipo en las fechas consultadas

---

## 🔄 Flujo Completo Corregido

### 1️⃣ Cliente busca disponibilidad
```http
GET /api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran
```

**Sistema verifica**:
- ✅ ¿Cuántas habitaciones "Doble Superior" tiene el hotel? → 4
- ✅ ¿Cuántas reservas "Doble Superior" hay para esas fechas? → 2
- ✅ Disponibles: 4 - 2 = **2 habitaciones** ✅

### 2️⃣ Cliente hace reserva
```http
POST /api/reservas
{
  "tipoHabitacion": "Doble Superior",
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05"
}
```

**Sistema crea**:
- ✅ Reserva (idReserva=4)
- ✅ Pernoctaciones (vinculadas a idTipoHabitacion=2)
- ❌ NO crea Contrato todavía

### 3️⃣ Cliente hace check-in
```http
POST /api/contratos/checkin
{
  "idReserva": 4
}
```

**Sistema asigna**:
- ✅ Busca habitación física disponible del tipo "Doble Superior"
- ✅ Asigna: H1-201 (primera disponible)
- ✅ Crea Contrato (vincula reserva 4 + habitación H1-201)

### 4️⃣ Cliente hace check-out
```http
PUT /api/contratos/:idContrato/checkout
```

**Sistema actualiza**:
- ✅ Actualiza Contrato: fechaCheckOut = hoy
- ✅ La habitación H1-201 queda libre para nuevas reservas

---

## ✅ Ventajas de la Corrección

1. **Refleja la realidad**: No puedes reservar más habitaciones de las que existen
2. **Previene overbooking**: El sistema sabe cuántas reservas hay realmente
3. **Coherente con el modelo**: Reservas → Tipos, Check-in → Habitaciones físicas
4. **Información útil**: Muestra cuántas disponibles, cuántas reservadas

---

## 🧪 Pruebas de Validación

### Caso 1: Sin reservas
```
Hotel con 4 Doble Superior
Reservas en rango: 0
Resultado: disponibles = 4 ✅
```

### Caso 2: Con reservas
```
Hotel con 4 Doble Superior
Reservas en rango: 2
Resultado: disponibles = 2 ✅
```

### Caso 3: Totalmente reservado
```
Hotel con 4 Doble Superior
Reservas en rango: 4
Resultado: tipo NO aparece en tiposDisponibles ✅
```

### Caso 4: Reservas fuera de rango
```
Hotel con 4 Doble Superior
Reservas: 
  - 2 para 1-5 dic (dentro del rango) ✅
  - 1 para 10-15 dic (fuera del rango) ❌ no cuenta
Resultado: disponibles = 2 ✅
```

---

## 🎯 Resumen Ejecutivo

### Problema
La lógica anterior contaba **contratos** (check-in) en lugar de **reservas**.

### Impacto
Permitía hacer más reservas de las que había habitaciones físicas (overbooking).

### Solución
Contar **pernoctaciones** (que se crean en la reserva) para cada tipo de habitación.

### Resultado
✅ Sistema previene overbooking correctamente  
✅ Muestra disponibilidad real en tiempo real  
✅ Coherente con el flujo: Reserva → Check-in → Check-out

---

**Estado**: ✅ IMPLEMENTADO Y CORREGIDO  
**Prioridad**: 🔴 CRÍTICO (afecta funcionalidad core del sistema)

---

_Actualizado: 21 de Octubre, 2025_

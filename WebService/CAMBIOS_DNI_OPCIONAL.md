# 🔄 Cambios Realizados: DNI y Fecha de Nacimiento Opcionales

**Fecha**: 21 de Octubre de 2025  
**Razón**: Simplificar el proceso de reserva. El DNI y fecha de nacimiento se añaden en el check-in

---

## ✅ **Cambios Implementados**

### **1. Schema de Prisma Actualizado** (`prisma/schema.prisma`)

**Campo DNI ahora es opcional:**

```prisma
model Cliente {
  idCliente          Int                 @id @default(autoincrement())
  nombre             String              @db.VarChar(100)       // ✅ OBLIGATORIO
  apellidos          String              @db.VarChar(150)       // ✅ OBLIGATORIO
  correoElectronico  String              @unique @db.VarChar(255)  // ✅ OBLIGATORIO
  fechaDeNacimiento  DateTime?           @db.Date               // ❌ OPCIONAL
  DNI                String?             @unique @db.VarChar(20)   // ❌ OPCIONAL (CAMBIO)
  reservasPagadas    Reserva[]           @relation("ClientePaga")
  reservasHuespedes  Reserva_Huespedes[]
}
```

**Antes:**
```prisma
DNI String @unique @db.VarChar(20)  // Era obligatorio
```

**Después:**
```prisma
DNI String? @unique @db.VarChar(20)  // Ahora es opcional (con ?)
```

---

### **2. Base de Datos Actualizada** (`BD/dump.sql`)

**Tabla Cliente modificada:**

```sql
CREATE TABLE Cliente (
  idCliente INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellidos VARCHAR(150) NOT NULL,
  correoElectronico VARCHAR(255) NOT NULL UNIQUE,
  fechaDeNacimiento DATE,           -- OPCIONAL
  DNI VARCHAR(20) UNIQUE            -- OPCIONAL (sin NOT NULL)
);
```

**Antes:**
```sql
DNI VARCHAR(20) NOT NULL UNIQUE  -- Era obligatorio
```

**Después:**
```sql
DNI VARCHAR(20) UNIQUE  -- Ahora permite NULL
```

---

## 📋 **Flujo de Trabajo Actualizado**

### **Paso 1: Crear Cliente para Reserva**

Solo se requieren **3 campos obligatorios**:

```http
POST /api/clientes
Content-Type: application/json

{
  "nombre": "María",
  "apellidos": "López Sánchez",
  "correoElectronico": "maria@email.com"
  // DNI y fechaDeNacimiento son OPCIONALES
}
```

**Campos obligatorios:**
- ✅ `nombre`
- ✅ `apellidos`
- ✅ `correoElectronico`

**Campos opcionales:**
- ❌ `fechaDeNacimiento`
- ❌ `DNI`

---

### **Paso 2: Crear Reserva**

Identificar al cliente que paga:

**Opción A: Con DNI** (si el cliente ya lo tiene)
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

**Opción B: Con Email** (si el cliente NO tiene DNI)
```http
POST /api/reservas
Content-Type: application/json

{
  "fechaEntrada": "2025-12-01",
  "fechaSalida": "2025-12-05",
  "nombreHotel": "Gran Hotel Miramar",
  "tipoHabitacion": "Doble Superior",
  "regimen": "Media Pensión",
  "emailClientePaga": "maria@email.com"
}
```

**⚠️ Importante:** Los **huéspedes NO se especifican** en la reserva, se añaden en el check-in.

---

### **Paso 3: Antes del Check-in - Actualizar DNI**

Si el cliente no tiene DNI, **debe añadirse antes del check-in**:

```http
PUT /api/clientes/1
Content-Type: application/json

{
  "DNI": "87654321B",
  "fechaDeNacimiento": "1990-05-15"
}
```

---

### **Paso 4: Check-in (Aquí se especifican los huéspedes)**

```http
POST /api/reservas/1/checkin
Content-Type: application/json

{
  "numeroHabitacion": "201",
  "dniHuespedes": ["12345678A", "87654321B"]
}
```

**⚠️ Importante:** 
- Todos los clientes en `dniHuespedes` **deben tener DNI** antes del check-in
- Si algún cliente no tiene DNI, actualízalo primero con `PUT /api/clientes/:id`

---

## 📚 **Documentación Actualizada**

### **Archivos modificados:**

| Archivo | Cambios |
|---------|---------|
| `prisma/schema.prisma` | ✅ DNI ahora es `String?` (opcional) |
| `BD/dump.sql` | ✅ DNI sin `NOT NULL` |
| `API_DOCUMENTATION.md` | ✅ Documentado que DNI es opcional |
| `TESTING_GUIDE.md` | ✅ Añadido flujo de trabajo completo |

---

## 🔍 **Casos de Uso**

### **Caso 1: Reserva por Teléfono (sin DNI)**

1. Recepcionista crea cliente con nombre, apellidos y email
2. Crea reserva usando el email del cliente
3. **Días después**, cuando el cliente llega al hotel:
   - Recepcionista pide el DNI
   - Actualiza el cliente: `PUT /api/clientes/:id`
   - Hace check-in con los DNIs de todos los huéspedes

### **Caso 2: Reserva Online (con DNI)**

1. Cliente se registra online con todos sus datos (incluido DNI)
2. Crea reserva usando su DNI
3. En check-in, se especifican los huéspedes con sus DNIs

### **Caso 3: Grupo de Huéspedes**

1. Líder del grupo crea reserva (puede tener o no DNI)
2. Antes del check-in:
   - Se crean todos los huéspedes adicionales
   - Se actualizan sus DNIs: `PUT /api/clientes/:id`
3. En check-in, se especifican todos los DNIs de los huéspedes

---

## 🚀 **Ventajas del Cambio**

✅ **Reservas más rápidas**: No se requiere DNI para crear la reserva  
✅ **Flexibilidad**: Permite reservas por teléfono sin toda la información  
✅ **Mejor UX**: El cliente puede reservar sin tener todos sus documentos a mano  
✅ **Proceso natural**: DNI se añade cuando el cliente llega físicamente al hotel  
✅ **Menos fricción**: Reduce barreras para hacer una reserva  

---

## ⚠️ **Consideraciones Importantes**

### **Validación en Check-in**

El endpoint de check-in **debe validar** que:
- ✅ Todos los DNIs en `dniHuespedes` existen en la base de datos
- ✅ Todos los clientes tienen su campo `DNI` relleno
- ❌ Si algún cliente no tiene DNI, el check-in falla con error 400

### **Identificación del Cliente**

Al crear una reserva, se puede identificar al cliente por:
- **DNI** (`dniClientePaga`): Si el cliente ya tiene DNI registrado
- **Email** (`emailClientePaga`): Si el cliente no tiene DNI aún

---

## 🔄 **Pasos para Aplicar los Cambios**

Si necesitas aplicar estos cambios en tu entorno:

```bash
# 1. Regenerar Prisma Client
cd WebService
npx prisma generate

# 2. Recrear la base de datos
cd ../BD
mysql -u pms_user -ppms_password123 -e "DROP DATABASE IF EXISTS pms_database; CREATE DATABASE pms_database;"
Get-Content dump.sql | mysql -u pms_user -ppms_password123 pms_database
Get-Content insert.sql | mysql -u pms_user -ppms_password123 pms_database

# 3. Reiniciar el servidor
cd ../WebService
npm run dev
```

---

## ✅ **Resumen**

| Campo | Antes | Después | Cuándo se añade |
|-------|-------|---------|-----------------|
| `nombre` | Obligatorio | Obligatorio | Al crear cliente |
| `apellidos` | Obligatorio | Obligatorio | Al crear cliente |
| `correoElectronico` | Obligatorio | Obligatorio | Al crear cliente |
| `fechaDeNacimiento` | Opcional | Opcional | Al crear cliente o antes del check-in |
| **`DNI`** | **Obligatorio** | **Opcional** | **Antes del check-in** |

---

¡Cambios completados y documentados! 🎉

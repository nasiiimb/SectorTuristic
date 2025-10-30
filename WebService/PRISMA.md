# 🔷 Guía de Prisma ORM

Esta guía explica cómo funciona Prisma en este proyecto y cómo utilizarlo eficientemente.

## 📚 ¿Qué es Prisma?

**Prisma** es un ORM (Object-Relational Mapping) moderno para Node.js y TypeScript que simplifica el acceso a bases de datos. En lugar de escribir SQL directamente, usas métodos de JavaScript/TypeScript con tipado automático.

## 🏗️ Arquitectura de Prisma en este Proyecto

```
WebService/
├── prisma/
│   └── schema.prisma          # Esquema de la base de datos
├── src/
│   ├── config/
│   │   └── prisma.ts          # Instancia única de Prisma Client
│   └── api/
│       └── *.routes.ts        # Uso de Prisma en endpoints
```

## 📄 El Schema de Prisma

El archivo `prisma/schema.prisma` define:

### 1. Configuración del Cliente
```prisma
generator client {
  provider = "prisma-client-js"
}
```

### 2. Conexión a la Base de Datos
```prisma
datasource db {
  provider = "mysql"
  url      = env("DATABASE_URL")
}
```

### 3. Modelos de Datos
```prisma
model Hotel {
  idHotel       Int          @id @default(autoincrement())
  nombre        String       @db.VarChar(100)
  ubicacion     String       @db.VarChar(255)
  categoria     Int
  idCiudad      Int
  ciudad        Ciudad       @relation(fields: [idCiudad], references: [idCiudad])
  habitaciones  Habitacion[]
  
  @@index([idCiudad])
}
```

## 🔧 Configuración de Prisma Client

En `src/config/prisma.ts` creamos una instancia única (singleton):

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

export default prisma;
```

Esto evita crear múltiples conexiones a la base de datos.

## 📖 Operaciones Básicas con Prisma

### 1. **Consultar (SELECT)**

#### Obtener todos los registros
```typescript
const hoteles = await prisma.hotel.findMany();
```

#### Obtener un registro por ID
```typescript
const hotel = await prisma.hotel.findUnique({
  where: { idHotel: 1 }
});
```

#### Consultar con condiciones
```typescript
const hoteles = await prisma.hotel.findMany({
  where: {
    categoria: { gte: 4 },  // mayor o igual a 4
    ciudad: {
      pais: "España"
    }
  }
});
```

### 2. **Incluir Relaciones (JOIN)**

```typescript
const hotel = await prisma.hotel.findUnique({
  where: { idHotel: 1 },
  include: {
    ciudad: true,              // Incluye la ciudad relacionada
    habitaciones: {            // Incluye habitaciones
      include: {
        tipoHabitacion: true   // Y su tipo
      }
    }
  }
});
```

### 3. **Crear (INSERT)**

```typescript
const nuevoHotel = await prisma.hotel.create({
  data: {
    nombre: "Hotel Paraíso",
    ubicacion: "Playa del Carmen",
    categoria: 5,
    idCiudad: 1
  }
});
```

#### Crear con relaciones
```typescript
const reserva = await prisma.reserva.create({
  data: {
    fechaEntrada: new Date("2024-12-01"),
    fechaSalida: new Date("2024-12-05"),
    tipo: "Reserva",
    clientePaga: {
      create: {                    // Crea el cliente al mismo tiempo
        nombre: "Juan",
        apellidos: "Pérez",
        correoElectronico: "juan@example.com"
      }
    },
    pernoctaciones: {
      create: [                    // Crea múltiples pernoctaciones
        { fechaPernoctacion: new Date("2024-12-01"), idTipoHabitacion: 1 },
        { fechaPernoctacion: new Date("2024-12-02"), idTipoHabitacion: 1 }
      ]
    }
  }
});
```

### 4. **Actualizar (UPDATE)**

```typescript
const hotelActualizado = await prisma.hotel.update({
  where: { idHotel: 1 },
  data: {
    categoria: 5,
    ubicacion: "Nueva ubicación"
  }
});
```

#### Actualizar o crear (upsert)
```typescript
const cliente = await prisma.cliente.upsert({
  where: { DNI: "12345678A" },
  update: {                        // Si existe, actualiza
    nombre: "Juan Carlos",
    email: "nuevo@example.com"
  },
  create: {                        // Si no existe, crea
    DNI: "12345678A",
    nombre: "Juan Carlos",
    apellidos: "Pérez",
    correoElectronico: "nuevo@example.com"
  }
});
```

### 5. **Eliminar (DELETE)**

```typescript
await prisma.hotel.delete({
  where: { idHotel: 1 }
});
```

#### Eliminar múltiples
```typescript
await prisma.reserva.deleteMany({
  where: {
    fechaEntrada: { lt: new Date("2024-01-01") }
  }
});
```

## 🔍 Filtros y Operadores

### Operadores de Comparación
```typescript
await prisma.hotel.findMany({
  where: {
    categoria: { equals: 5 },      // igual a
    categoria: { not: 3 },          // diferente de
    categoria: { gt: 3 },           // mayor que
    categoria: { gte: 4 },          // mayor o igual
    categoria: { lt: 5 },           // menor que
    categoria: { lte: 4 },          // menor o igual
    categoria: { in: [4, 5] },      // en lista
    categoria: { notIn: [1, 2] }    // no en lista
  }
});
```

### Operadores de Texto
```typescript
await prisma.hotel.findMany({
  where: {
    nombre: { contains: "Paraíso" },     // contiene
    nombre: { startsWith: "Hotel" },     // empieza con
    nombre: { endsWith: "Beach" },       // termina con
    nombre: { mode: 'insensitive' }      // case-insensitive
  }
});
```

### Operadores Lógicos
```typescript
await prisma.hotel.findMany({
  where: {
    AND: [
      { categoria: { gte: 4 } },
      { ciudad: { pais: "España" } }
    ],
    OR: [
      { nombre: { contains: "Paraíso" } },
      { nombre: { contains: "Beach" } }
    ],
    NOT: {
      categoria: 1
    }
  }
});
```

## 📊 Ordenar y Paginar

### Ordenar
```typescript
const hoteles = await prisma.hotel.findMany({
  orderBy: {
    categoria: 'desc',      // descendente
    nombre: 'asc'           // ascendente
  }
});
```

### Paginar
```typescript
const hoteles = await prisma.hotel.findMany({
  skip: 10,      // Saltar los primeros 10
  take: 5        // Tomar los siguientes 5
});
```

## 🔗 Relaciones en Prisma

### Tipos de Relaciones

#### 1. Uno a Muchos (1:N)
```prisma
model Hotel {
  habitaciones  Habitacion[]  // Un hotel tiene muchas habitaciones
}

model Habitacion {
  hotel  Hotel  @relation(fields: [idHotel], references: [idHotel])
  idHotel Int
}
```

#### 2. Muchos a Muchos (N:M)
```prisma
model Reserva_Huespedes {
  idReserva  Int
  idCliente  Int
  reserva    Reserva  @relation(fields: [idReserva], references: [idReserva])
  cliente    Cliente  @relation(fields: [idCliente], references: [idCliente])
  
  @@id([idReserva, idCliente])
}
```

### Consultas con Relaciones

```typescript
// Include: trae todos los campos relacionados
const hotel = await prisma.hotel.findUnique({
  where: { idHotel: 1 },
  include: {
    ciudad: true,
    habitaciones: true
  }
});

// Select: elige campos específicos
const hotel = await prisma.hotel.findUnique({
  where: { idHotel: 1 },
  select: {
    nombre: true,
    categoria: true,
    ciudad: {
      select: {
        nombre: true,
        pais: true
      }
    }
  }
});
```

## 🎯 Casos de Uso Reales del Proyecto

### 1. Consultar Disponibilidad
```typescript
const habitacionesOcupadas = await prisma.contrato.findMany({
  where: {
    fechaCheckIn: { lte: fechaSalida },
    OR: [
      { fechaCheckOut: null },
      { fechaCheckOut: { gte: fechaEntrada } }
    ],
    habitacion: {
      idHotel: parseInt(idHotel),
      idTipoHabitacion: parseInt(idTipoHabitacion)
    }
  },
  select: { numeroHabitacion: true }
});
```

### 2. Crear Reserva Completa
```typescript
const reserva = await prisma.reserva.create({
  data: {
    fechaEntrada,
    fechaSalida,
    tipo,
    idCliente_paga: cliente.idCliente,
    idPrecioRegimen,
    pernoctaciones: {
      create: pernoctaciones.map(p => ({
        fechaPernoctacion: new Date(p.fechaPernoctacion),
        idTipoHabitacion: p.idTipoHabitacion
      }))
    },
    reservaHuespedes: {
      create: huespedes.map(h => ({
        idCliente: h.idCliente
      }))
    }
  },
  include: {
    clientePaga: true,
    pernoctaciones: true
  }
});
```

### 3. Actualizar Cliente Existente
```typescript
const cliente = await prisma.cliente.upsert({
  where: { DNI: clienteData.DNI },
  update: {
    nombre: clienteData.nombre,
    apellidos: clienteData.apellidos,
    correoElectronico: clienteData.correoElectronico
  },
  create: clienteData
});
```

## 🛠️ Comandos Útiles de Prisma

```bash
# Generar el cliente de Prisma
npm run prisma:generate

# Abrir Prisma Studio (GUI)
npm run prisma:studio

# Crear migración (cambios en schema)
npm run prisma:migrate

# Sincronizar schema con BD (desarrollo)
npm run prisma:push

# Ver estado de migraciones
npx prisma migrate status

# Resetear base de datos (¡CUIDADO!)
npx prisma migrate reset
```

## 🚨 Manejo de Errores de Prisma

### Errores Comunes

```typescript
import { Prisma } from '@prisma/client';

try {
  await prisma.hotel.create({ /* ... */ });
} catch (error) {
  if (error instanceof Prisma.PrismaClientKnownRequestError) {
    // P2002: Violación de restricción única
    if (error.code === 'P2002') {
      console.log('Ya existe un registro con esos datos únicos');
    }
    
    // P2025: Registro no encontrado
    if (error.code === 'P2025') {
      console.log('El registro no existe');
    }
    
    // P2003: Violación de clave foránea
    if (error.code === 'P2003') {
      console.log('Referencia a un registro inexistente');
    }
  }
}
```

## 📈 Mejores Prácticas

### ✅ DO (Hacer)
- Usa `include` solo cuando necesites los datos relacionados
- Usa `select` para optimizar queries grandes
- Implementa paginación en listados grandes
- Usa transacciones para operaciones múltiples
- Valida datos antes de insertar

### ❌ DON'T (No hacer)
- No uses `findMany()` sin límites en tablas grandes
- No hagas queries dentro de loops (N+1 problem)
- No expongas errores de Prisma directamente al cliente
- No uses `prisma.$executeRaw()` si puedes evitarlo

## 🔐 Transacciones

Para operaciones que deben ser atómicas:

```typescript
await prisma.$transaction(async (tx) => {
  const cliente = await tx.cliente.create({ /* ... */ });
  
  const reserva = await tx.reserva.create({
    data: {
      idCliente_paga: cliente.idCliente,
      /* ... */
    }
  });
  
  await tx.pernoctacion.createMany({ /* ... */ });
});
```

## 📚 Recursos Adicionales

- [Documentación oficial de Prisma](https://www.prisma.io/docs)
- [Prisma Schema Reference](https://www.prisma.io/docs/reference/api-reference/prisma-schema-reference)
- [Prisma Client API](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)

---

**Prisma hace que trabajar con bases de datos sea más seguro, rápido y productivo! 🚀**

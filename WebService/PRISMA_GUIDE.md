# Guía de uso de Prisma en el proyecto

## ¿Qué es Prisma?

Prisma es un ORM (Object-Relational Mapping) moderno para Node.js y TypeScript que facilita el trabajo con bases de datos. En lugar de escribir consultas SQL directamente, puedes usar métodos TypeScript con autocompletado completo.

## Configuración actual

Tu proyecto ya está configurado con Prisma y listo para usar. Los cambios realizados incluyen:

### 1. Archivos creados/modificados

- ✅ `prisma/schema.prisma` - Schema de Prisma con todos los modelos de tu base de datos
- ✅ `.env` - Configuración de conexión a MySQL
- ✅ `src/config/prisma.ts` - Cliente de Prisma para usar en toda la aplicación
- ✅ `src/api/hotel.routes.ts` - Rutas actualizadas para usar Prisma

### 2. Dependencias instaladas

- `@prisma/client` - Cliente de Prisma para realizar consultas
- `prisma` - CLI de Prisma para migraciones y gestión de base de datos

## Scripts disponibles

En el `package.json` se han añadido los siguientes scripts:

```bash
# Generar el cliente de Prisma después de cambios en el schema
npm run prisma:generate

# Abrir Prisma Studio (GUI para explorar y editar datos)
npm run prisma:studio

# Crear y aplicar migraciones
npm run prisma:migrate

# Sincronizar el schema con la base de datos sin migraciones
npm run prisma:push
```

## Cómo usar Prisma

### Ejemplo básico - Obtener todos los hoteles

```typescript
import prisma from '../config/prisma';

// Obtener todos los hoteles
const hoteles = await prisma.hotel.findMany();

// Obtener hoteles con su ciudad
const hotelesConCiudad = await prisma.hotel.findMany({
  include: {
    ciudad: true,
  },
});
```

### Buscar por ID

```typescript
const hotel = await prisma.hotel.findUnique({
  where: {
    idHotel: 1,
  },
  include: {
    ciudad: true,
    habitaciones: true,
  },
});
```

### Crear un registro

```typescript
const nuevoHotel = await prisma.hotel.create({
  data: {
    nombre: "Hotel Paradise",
    ubicacion: "Palma de Mallorca",
    categoria: 5,
    idCiudad: 1,
  },
});
```

### Actualizar un registro

```typescript
const hotelActualizado = await prisma.hotel.update({
  where: {
    idHotel: 1,
  },
  data: {
    categoria: 5,
  },
});
```

### Eliminar un registro

```typescript
await prisma.hotel.delete({
  where: {
    idHotel: 1,
  },
});
```

### Consultas con filtros

```typescript
// Hoteles de categoría 5
const hotelesLujo = await prisma.hotel.findMany({
  where: {
    categoria: 5,
  },
});

// Hoteles que contienen "Beach" en el nombre
const hotelesPlaya = await prisma.hotel.findMany({
  where: {
    nombre: {
      contains: "Beach",
    },
  },
});

// Múltiples condiciones
const hotelesEspecificos = await prisma.hotel.findMany({
  where: {
    AND: [
      { categoria: { gte: 4 } }, // Mayor o igual a 4
      { idCiudad: 1 },
    ],
  },
});
```

## Ventajas de usar Prisma

1. **Type-safety**: TypeScript completo con autocompletado
2. **Relaciones automáticas**: Fácil acceso a datos relacionados
3. **Migraciones**: Control de versiones de la base de datos
4. **Prisma Studio**: GUI para explorar y editar datos
5. **Sin SQL**: Menos errores en las consultas
6. **Documentación**: Excelente documentación oficial

## Prisma Studio

Para explorar visualmente tu base de datos:

```bash
npm run prisma:studio
```

Esto abrirá una interfaz web en `http://localhost:5555` donde podrás ver y editar todos los datos.

## Sincronizar con la base de datos existente

Si tu base de datos ya tiene datos y quieres asegurarte de que Prisma está sincronizado:

```bash
npm run prisma:push
```

Este comando sincroniza el schema de Prisma con tu base de datos MySQL existente.

## Más información

- [Documentación oficial de Prisma](https://www.prisma.io/docs)
- [Prisma Client API Reference](https://www.prisma.io/docs/reference/api-reference/prisma-client-reference)
- [Guía de consultas de Prisma](https://www.prisma.io/docs/concepts/components/prisma-client/crud)

## Próximos pasos

1. ✅ Crear rutas para otras entidades (Cliente, Reserva, etc.)
2. ✅ Implementar validaciones con middleware
3. ✅ Agregar manejo de errores más robusto
4. ✅ Implementar paginación en las consultas
5. ✅ Agregar autenticación y autorización

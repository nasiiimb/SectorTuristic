#  WebService - Sistema de Gestión Hotelera (PMS)

##  Descripción

Este WebService es una API REST desarrollada para gestionar un sistema de Property Management System (PMS) para el sector turístico. Permite administrar hoteles, reservas, clientes, contratos y toda la operativa hotelera.

##  Arquitectura del Proyecto

El proyecto está organizado siguiendo una arquitectura modular y escalable:

```
WebService/
├── src/
│   ├── app.ts                    # Punto de entrada de la aplicación
│   ├── api/                      # Rutas de la API (endpoints)
│   │   ├── ciudad.routes.ts
│   │   ├── cliente.routes.ts
│   │   ├── contrato.routes.ts
│   │   ├── disponibilidad.routes.ts
│   │   ├── hotel.routes.ts
│   │   ├── pernoctacion.routes.ts
│   │   ├── regimen.routes.ts
│   │   ├── reserva.routes.ts
│   │   ├── servicio.routes.ts
│   │   └── tipoHabitacion.routes.ts
│   ├── config/                   # Configuración
│   │   ├── database.ts
│   │   └── prisma.ts
│   ├── middleware/               # Middleware personalizado
│   │   └── errorHandler.ts
│   └── models/                   # Modelos de datos
│       └── hotel.model.ts
├── prisma/
│   └── schema.prisma             # Esquema de la base de datos
└── package.json
```

##  Tecnologías Utilizadas

- **Node.js**: Entorno de ejecución de JavaScript
- **Express.js v5**: Framework web para crear la API REST
- **TypeScript**: Superset de JavaScript con tipado estático
- **Prisma ORM**: Object-Relational Mapping para interactuar con la base de datos
- **MySQL**: Sistema de gestión de base de datos relacional
- **ts-node-dev**: Herramienta de desarrollo para ejecutar TypeScript con hot-reload

##  Funcionalidades Principales

### 1. Gestión de Hoteles
- Listar todos los hoteles
- Obtener detalles de un hotel específico
- Crear, actualizar y eliminar hoteles
- Consultar tipos de habitación disponibles por hotel

### 2. Gestión de Reservas
- Crear nuevas reservas (con actualización automática de clientes existentes)
- Consultar reservas por ID
- Listar todas las reservas
- Filtrar reservas por hotel, fechas o cliente
- Cancelar reservas

### 3. Gestión de Disponibilidad
- Consultar disponibilidad de habitaciones por fechas
- Verificar habitaciones disponibles por tipo y hotel

### 4. Gestión de Contratos (Check-in/Check-out)
- Realizar check-in (crear contrato)
- Realizar check-out (finalizar estancia)
- Consultar detalles de contratos

### 5. Catálogos
- Ciudades
- Tipos de habitación
- Regímenes alimentarios
- Servicios adicionales
- Clientes

##  Manejo de Errores

El sistema cuenta con un middleware centralizado de manejo de errores (`errorHandler.ts`) que incluye:

### **asyncHandler Wrapper**
Envuelve todas las funciones asíncronas para capturar errores automáticamente sin necesidad de bloques try-catch en cada endpoint.

```typescript
router.get('/', asyncHandler(async (req, res) => {
  const hoteles = await prisma.hotel.findMany();
  res.status(200).json(hoteles);
}));
```

### **Errores Personalizados**
- `NotFoundError (404)`: Recurso no encontrado
- `ValidationError (400)`: Datos de entrada inválidos
- `ConflictError (409)`: Conflicto con datos existentes
- `BadRequestError (400)`: Petición incorrecta

### **Manejo de Errores de Prisma**
- `P2002`: Violación de restricción única (409 Conflict)
- `P2025`: Registro no encontrado (404 Not Found)
- `P2003`: Violación de clave foránea (400 Bad Request)

##  Características Especiales

### **Actualización Inteligente de Clientes**
Al crear una reserva, si el cliente ya existe (por DNI), se actualizan sus datos automáticamente en lugar de crear un duplicado:

```typescript
// Si el DNI existe, actualiza nombre, apellidos, email
// Si no existe, crea un nuevo cliente
```

### **Validación de Disponibilidad**
El endpoint de disponibilidad verifica:
- Habitaciones no ocupadas en el rango de fechas
- Habitaciones sin contratos activos
- Habitaciones disponibles por tipo y hotel

##  Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/hoteles` | Lista todos los hoteles |
| GET | `/api/hoteles/:id` | Detalles de un hotel |
| GET | `/api/hoteles/:id/tiposHabitacion` | Tipos de habitación de un hotel |
| POST | `/api/reservas` | Crear nueva reserva |
| GET | `/api/reservas/:id` | Detalles de una reserva |
| GET | `/api/disponibilidad` | Consultar disponibilidad |
| POST | `/api/contratos` | Hacer check-in |
| PUT | `/api/contratos/:id/checkout` | Hacer check-out |
| GET | `/api/clientes` | Lista de clientes |
| GET | `/api/regimenes` | Regímenes alimentarios |
| GET | `/api/servicios` | Servicios adicionales |

##  Flujo de Trabajo Típico

1. **Consultar disponibilidad** → `GET /api/disponibilidad`
2. **Crear reserva** → `POST /api/reservas`
3. **Hacer check-in** → `POST /api/contratos`
4. **Hacer check-out** → `PUT /api/contratos/:id/checkout`

##  Notas Importantes

- Todos los endpoints usan el middleware `asyncHandler` para manejo automático de errores
- Las fechas deben estar en formato ISO (YYYY-MM-DD)
- Los tipos de reserva son: `"Reserva"` o `"Walkin"`
- El sistema valida automáticamente claves foráneas y datos únicos
- Los errores retornan JSON estructurado con código HTTP apropiado



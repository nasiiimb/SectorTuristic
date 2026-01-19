# GDS (Global Distribution System)

Sistema de distribución global para reservas hoteleras. Interfaz web moderna que permite buscar disponibilidad de hoteles y realizar reservas a través del Channel Manager.

## Descripción

El GDS es una aplicación web completa que conecta clientes finales con el sistema de gestión hotelera. Permite:

- Buscar hoteles por ciudad y fechas
- Consultar disponibilidad de habitaciones
- Ver precios en tiempo real
- Realizar reservas online
- Gestionar reservas existentes

## Arquitectura

El proyecto está dividido en dos partes:

### Backend (Node.js + TypeScript + Express)
- Puerto: 8010
- API RESTful
- Comunicación con Channel Manager (puerto 8001)
- Comunicación con WebService (puerto 3000)
- Base de datos SQLite local para cache

### Frontend (Vue 3 + Vite)
- Puerto: 5174
- Interfaz de usuario moderna
- Proxy configurado hacia el backend
- Componentes reutilizables
- Sistema de rutas con Vue Router

## Requisitos Previos

- Node.js (versión 16 o superior)
- npm (viene con Node.js)

## Instalación

### 1. Instalar dependencias del backend

```bash
cd GDS/backend
npm install
```

### 2. Instalar dependencias del frontend

```bash
cd GDS/frontend
npm install
```

## Ejecución

### Iniciar Backend (Terminal 1)

```bash
cd GDS/backend
npm run dev
```

El servidor backend estará disponible en `http://localhost:8010`

### Iniciar Frontend (Terminal 2)

```bash
cd GDS/frontend
npm run dev
```

La interfaz web estará disponible en `http://localhost:5174`

## Configuración

### Backend

El backend se conecta automáticamente a:
- **Channel Manager**: `http://localhost:8001`
- **WebService**: `http://localhost:3000`

### Frontend

El frontend tiene configurado un proxy en `vite.config.js` que redirige todas las peticiones `/api/*` al backend en el puerto 8010.

## Funcionalidades

### Búsqueda de Hoteles
- Selección de ciudad
- Rango de fechas (entrada/salida)
- Tipo de habitación
- Número de huéspedes

### Resultados de Búsqueda
- Lista de hoteles disponibles
- Información detallada (nombre, ciudad, servicios)
- Precio por noche
- Disponibilidad en tiempo real

### Proceso de Reserva
- Formulario de datos del cliente
- Confirmación de reserva
- Generación de localizador único
- Guardado local de la reserva

### Gestión de Reservas
- Listado de reservas realizadas
- Visualización de detalles
- Estado de cada reserva

## Estructura del Proyecto

```
GDS/
├── backend/
│   ├── src/
│   │   ├── controllers/     # Controladores de rutas
│   │   ├── services/        # Servicios de comunicación (Channel, WebService)
│   │   ├── models/          # Modelos de datos
│   │   ├── routes/          # Definición de endpoints
│   │   ├── database/        # Configuración de SQLite
│   │   └── app.ts           # Punto de entrada
│   ├── package.json
│   └── tsconfig.json
│
└── frontend/
    ├── src/
    │   ├── views/           # Páginas principales
    │   ├── components/      # Componentes reutilizables
    │   ├── router/          # Configuración de rutas
    │   ├── api/             # Cliente API
    │   └── App.vue          # Componente raíz
    ├── package.json
    └── vite.config.js
```

## Endpoints API

### Hoteles

- `GET /api/hoteles` - Listar todos los hoteles
- `GET /api/hoteles/:id` - Obtener hotel por ID

### Ciudades

- `GET /api/ciudades` - Listar todas las ciudades

### Tipos de Habitación

- `GET /api/tipos-habitacion` - Listar tipos de habitación

### Disponibilidad

- `POST /api/disponibilidad` - Consultar disponibilidad
  ```json
  {
    "ciudad": "Palma",
    "fechaEntrada": "2026-02-01",
    "fechaSalida": "2026-02-05",
    "tipoHabitacion": "Doble"
  }
  ```

### Reservas

- `POST /api/reservas/channel` - Crear reserva vía Channel Manager
- `POST /api/reservas/webservice` - Crear reserva vía WebService
- `GET /api/reservas` - Listar todas las reservas

## Dependencias Principales

### Backend
- express: Framework web
- typescript: Lenguaje tipado
- better-sqlite3: Base de datos SQLite
- axios: Cliente HTTP
- cors: Manejo de CORS
- ts-node-dev: Hot reload en desarrollo

### Frontend
- vue: Framework progresivo
- vue-router: Sistema de rutas
- axios: Cliente HTTP
- vite: Build tool moderno

## Desarrollo

### Comandos Útiles Backend

```bash
npm run dev      # Modo desarrollo con hot-reload
npm run build    # Compilar TypeScript
npm start        # Ejecutar versión compilada
```

### Comandos Útiles Frontend

```bash
npm run dev      # Servidor de desarrollo
npm run build    # Build para producción
npm run preview  # Preview del build
```

## Integración con Otros Sistemas

### Channel Manager
El GDS se comunica con el Channel Manager para:
- Consultar disponibilidad de habitaciones
- Crear reservas directas
- Actualizar stock de habitaciones

### WebService
El GDS también puede crear reservas a través del WebService cuando se requiere:
- Selección de régimen alimenticio
- Información de pago del cliente
- Servicios adicionales

## Notas Importantes

- Las reservas se guardan localmente en SQLite para cache
- El localizador se genera con formato `WS-{id}` o según el sistema
- La interfaz está diseñada para coincidir con el sistema Principal
- El proxy del frontend evita problemas de CORS

## Solución de Problemas

### El frontend no se conecta al backend
Verifica que el backend esté corriendo en el puerto 8010 y que el proxy esté configurado en `vite.config.js`

### Error al crear reservas
Asegúrate de que el Channel Manager (puerto 8001) y el WebService (puerto 3000) estén corriendo

### Errores de compilación TypeScript
Ejecuta `npm install` para asegurarte de que todas las dependencias están instaladas

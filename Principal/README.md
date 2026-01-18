# Principal - Sistema de Reservas Unificado

## Descripción General

Principal es una aplicación web fullstack que actúa como plataforma unificada de reservas hoteleras. Integra múltiples fuentes de disponibilidad (WebService y Channel Manager) en una única interfaz de búsqueda y reserva para los usuarios finales.

## Arquitectura del Sistema

### Stack Tecnológico

**Backend:**
- Node.js + Express + TypeScript
- Puerto: 8010
- Base de datos: MySQL (principal_db)
- Autenticación: JWT (JSON Web Tokens)

**Frontend:**
- Vue 3 + Vite
- Puerto: 5174/5175
- UI: CSS personalizado con tema morado/violeta
- Comunicación: Axios para llamadas API

### Estructura del Proyecto

```
Principal/
├── backend/                 # Servidor Node.js
│   ├── src/
│   │   ├── controllers/    # Lógica de negocio
│   │   │   ├── AuthController.ts
│   │   │   └── BookingController.ts
│   │   ├── services/       # Clientes externos
│   │   │   ├── WebServiceClient.ts
│   │   │   └── ChannelClient.ts
│   │   ├── middleware/     # JWT y validaciones
│   │   ├── config/         # Configuración DB
│   │   ├── types/          # TypeScript interfaces
│   │   └── server.ts       # Punto de entrada
│   ├── package.json
│   └── tsconfig.json
│
├── frontend/               # Aplicación Vue 3
│   ├── src/
│   │   ├── views/         # Páginas principales
│   │   │   ├── Home.vue
│   │   │   ├── Resultados.vue
│   │   │   ├── MisReservas.vue
│   │   │   └── Perfil.vue
│   │   ├── components/    # Componentes reutilizables
│   │   │   ├── Navbar.vue
│   │   │   └── RegimenModal.vue
│   │   ├── api/          # Clientes API
│   │   │   ├── auth.js
│   │   │   └── booking.js
│   │   ├── router/       # Vue Router
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
│
├── package.json           # Scripts de desarrollo unificados
└── README.md             # Esta documentación
```

## Funcionalidades Principales

### 1. Sistema de Autenticación

**Registro de Usuarios:**
- Campos requeridos: nombre, apellidos, email, contraseña
- Campos opcionales: DNI, fecha de nacimiento
- Validación de email único
- Contraseñas hasheadas con bcrypt

**Inicio de Sesión:**
- Login con email y contraseña
- Generación de token JWT válido por 24 horas
- Token almacenado en localStorage
- Persistencia de sesión entre recargas

**Gestión de Sesión:**
- Validación automática de token en cada petición
- Navbar reactivo que muestra/oculta opciones según estado de sesión
- Event system (window events) para sincronizar estado entre componentes

### 2. Búsqueda Unificada de Disponibilidad

El sistema consulta simultáneamente dos fuentes:

**WebService (PMS):**
- API REST en Node.js + Prisma + MySQL
- Puerto: 3000
- Proporciona hoteles con sistema de gestión completo
- Incluye regímenes de alojamiento (SA, AD, MP, PC, TI)
- Requiere selección de régimen al reservar

**Channel Manager:**
- API REST en FastAPI + SQLite
- Puerto: 8001
- Proporciona disponibilidad de canales externos
- Reservas directas sin regímenes
- Sistema de stock con reducción automática

**Proceso de Búsqueda:**
1. Usuario introduce: destino, fechas (entrada/salida), personas
2. Backend consulta ambas fuentes en paralelo (Promise.all)
3. Se unifican resultados añadiendo campo `origen` a cada habitación
4. Frontend muestra lista combinada con indicador de origen

### 3. Sistema de Reservas

#### Flujo para Reservas de Channel:

1. Usuario hace clic en "Reservar"
2. Validación de autenticación
3. Confirmación con detalles (noches, precio total)
4. POST a `/api/book` con `origen: 'Channel'`
5. Backend envía a Channel API (POST `/api/reservas`)
6. Channel valida disponibilidad y reduce stock
7. Se guarda en BD local (principal_db)
8. Respuesta con localizador UUID
9. Redirección a "Mis Reservas"

**Campos enviados a Channel:**
```javascript
{
  hotel_id: number,              // ID del hotel en Channel
  tipo_habitacion_id: number,    // ID del tipo de habitación
  fecha_entrada: 'YYYY-MM-DD',
  fecha_salida: 'YYYY-MM-DD',
  num_huespedes: number
}
```

#### Flujo para Reservas de WebService:

1. Usuario hace clic en "Reservar"
2. Validación de autenticación
3. **Abre modal de selección de régimen**
4. Modal carga regímenes del hotel (GET `/api/regimenes/hotel/{idHotel}`)
5. Usuario selecciona régimen (SA/AD/MP/PC/TI)
6. Modal muestra precio total (habitación + régimen)
7. Confirmación → POST a `/api/book` con `origen: 'WebService'`
8. Backend envía a WebService (POST `/api/reservas`)
9. WebService valida hotel, tipo habitación, régimen, precios
10. Crea cliente si no existe, genera reserva
11. Se guarda en BD local (principal_db)
12. Respuesta con localizador formato `WS-YYYY-#####` (ej: WS-2026-00001)
13. Redirección a "Mis Reservas"

**Campos enviados a WebService:**
```javascript
{
  fechaEntrada: 'YYYY-MM-DD',
  fechaSalida: 'YYYY-MM-DD',
  hotel: 'Nombre del Hotel',
  tipoHabitacion: 'Tipo de Habitación',
  regimen: 'AD',                 // Código del régimen seleccionado
  canal: 'Principal',            // Identificador del canal
  clientePaga: {
    nombre: string,
    apellidos: string,
    correoElectronico: string,
    DNI: string,
    fechaDeNacimiento: string
  },
  huespedes: []
}
```

### 4. Gestión de Reservas del Usuario

**Vista "Mis Reservas":**
- Lista todas las reservas del usuario autenticado
- Muestra origen (Channel/WebService), fechas, hotel, habitación
- Indica estado, localizador, precio
- Diferencia visual por origen

**Datos mostrados:**
- Localizador de reserva
- Hotel y tipo de habitación
- Fechas de entrada/salida
- Número de huéspedes
- Precio total
- Fecha de creación
- Origen de la reserva

### 5. Perfil de Usuario

**Información visualizada:**
- Nombre completo
- Email
- DNI (si proporcionado)
- Fecha de nacimiento (si proporcionada)
- Fecha de registro

## Configuración y Despliegue

### Requisitos Previos

- Node.js v16 o superior
- MySQL 8.0
- WebService ejecutándose en puerto 3000
- Channel Manager ejecutándose en puerto 8001

### Variables de Entorno

Crear archivo `.env` en `Principal/backend/`:

```env
# Base de datos
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=principal_db
DB_PORT=3306

# JWT
JWT_SECRET=tu_secret_key_segura_aqui

# APIs externas
WEBSERVICE_URL=http://localhost:3000
CHANNEL_URL=http://localhost:8001

# Puerto del servidor
PORT=8010
```

### Instalación

```bash
# Instalar dependencias
cd Principal
npm install

# Esto instalará automáticamente:
# - Backend: express, mysql2, bcrypt, jsonwebtoken, axios, typescript
# - Frontend: vue, vue-router, axios, vite
```

### Base de Datos

**Crear base de datos:**
```sql
CREATE DATABASE principal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**Tablas necesarias:**

1. **usuarios**: Almacena datos de usuarios registrados
```sql
CREATE TABLE usuarios (
  id INT AUTO_INCREMENT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  apellidos VARCHAR(100) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  password VARCHAR(255) NOT NULL,
  dni VARCHAR(20),
  fecha_nacimiento DATE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

2. **reservas**: Almacena todas las reservas (Channel y WebService)
```sql
CREATE TABLE reservas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  origen ENUM('Channel', 'WebService') NOT NULL,
  localizador VARCHAR(50) NOT NULL,
  hotel_nombre VARCHAR(255) NOT NULL,
  habitacion_tipo VARCHAR(100) NOT NULL,
  fecha_entrada DATE NOT NULL,
  fecha_salida DATE NOT NULL,
  num_huespedes INT NOT NULL,
  precio_total DECIMAL(10,2) NOT NULL,
  estado VARCHAR(50) DEFAULT 'confirmada',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

### Ejecución

**Modo Desarrollo (Recomendado):**
```bash
# Desde la raíz de Principal/
npm run dev
```

Este comando ejecuta concurrentemente:
- Backend en http://localhost:8010
- Frontend en http://localhost:5174

**Modo Producción:**
```bash
# Compilar backend
cd backend
npm run build

# Compilar frontend
cd ../frontend
npm run build

# Ejecutar backend (sirve también el frontend compilado)
cd ../backend
npm start
```

## Integración con Sistemas Externos

### WebService

**Endpoints utilizados:**

- `GET /api/disponibilidad/buscar`
  - Parámetros: ciudad, fechaEntrada, fechaSalida, numeroPersonas
  - Respuesta: Array de hoteles con habitaciones disponibles

- `GET /api/regimenes/hotel/{idHotel}`
  - Respuesta: Lista de regímenes disponibles con precios

- `POST /api/reservas`
  - Body: Datos de reserva completos
  - Respuesta: Reserva creada con localizador

**Transformación de datos:**
- El WebService devuelve estructura compleja con hoteles y tipos de habitación
- Principal transforma a formato plano: una habitación = un resultado
- Añade campo `origen: 'WebService'` y `idHotel` para identificación

### Channel Manager

**Endpoints utilizados:**

- `GET /api/disponibilidad`
  - Parámetros: destino, fecha_entrada, fecha_salida, personas
  - Respuesta: Array de habitaciones disponibles

- `POST /api/reservas`
  - Body: Datos de reserva
  - Respuesta: Reserva creada con UUID

**Transformación de datos:**
- Channel devuelve resultados directos por habitación
- Principal añade campo `origen: 'Channel'`
- Mapea campos al formato unificado

## Paleta de Colores

El sistema utiliza una paleta morada/violeta:

```css
--primary: #667eea → #764ba2 (degradado)
--secondary: #9333ea
--accent: #6b46c1
--hover: tonos más oscuros de morado
```

## API Endpoints del Principal

### Autenticación

**POST /api/auth/register**
```json
Request:
{
  "nombre": "Juan",
  "apellidos": "Pérez",
  "email": "juan@example.com",
  "password": "password123",
  "dni": "12345678A",           // Opcional
  "fecha_nacimiento": "1990-01-01"  // Opcional
}

Response:
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "token": "jwt_token_here",
  "usuario": {
    "id": 1,
    "nombre": "Juan",
    "apellidos": "Pérez",
    "email": "juan@example.com"
  }
}
```

**POST /api/auth/login**
```json
Request:
{
  "email": "juan@example.com",
  "password": "password123"
}

Response:
{
  "success": true,
  "token": "jwt_token_here",
  "usuario": {
    "id": 1,
    "nombre": "Juan",
    "apellidos": "Pérez",
    "email": "juan@example.com",
    "dni": "12345678A",
    "fecha_nacimiento": "1990-01-01"
  }
}
```

**GET /api/auth/me**
```
Headers: Authorization: Bearer {token}

Response:
{
  "success": true,
  "usuario": { /* datos del usuario */ }
}
```

### Búsqueda y Reservas

**GET /api/search**
```
Query params:
- destino: string
- fecha_entrada: YYYY-MM-DD
- fecha_salida: YYYY-MM-DD
- personas: number

Response:
{
  "success": true,
  "habitaciones": [
    {
      "id": "unique_id",
      "hotel": "Hotel Name",
      "nombre": "Habitación Doble",
      "precio": 150.00,
      "origen": "WebService" | "Channel",
      "foto_url": "https://...",
      "capacidad": 2,
      // Campos específicos según origen
      "idHotel": 1,           // Solo WebService
      "hotelId": 1            // Solo Channel
    }
  ],
  "resumen": {
    "total": 10,
    "webservice": 6,
    "channel": 4
  }
}
```

**POST /api/book**
```json
Headers: Authorization: Bearer {token}

Request:
{
  "origen": "WebService" | "Channel",
  "habitacion_id": "id_habitacion",
  "hotel_nombre": "Hotel Name",
  "habitacion_tipo": "Habitación Doble",
  "fecha_entrada": "2026-01-20",
  "fecha_salida": "2026-01-25",
  "num_huespedes": 2,
  "precio_total": 750.00,
  // Campos específicos por origen:
  "hotel_id": 1,              // Solo Channel
  "regimen": "AD",            // Solo WebService
  "idHotel": 1                // Solo WebService
}

Response:
{
  "success": true,
  "message": "Reserva creada exitosamente",
  "reserva": {
    "id": 1,
    "localizador": "WS-2026-00001" | "uuid",
    "origen": "WebService" | "Channel",
    /* más detalles */
  }
}
```

**GET /api/reservas**
```
Headers: Authorization: Bearer {token}

Response:
{
  "success": true,
  "reservas": [
    {
      "id": 1,
      "localizador": "WS-2026-00001",
      "origen": "WebService",
      "hotel_nombre": "Hotel Name",
      "habitacion_tipo": "Habitación Doble",
      "fecha_entrada": "2026-01-20",
      "fecha_salida": "2026-01-25",
      "num_huespedes": 2,
      "precio_total": 750.00,
      "estado": "confirmada",
      "created_at": "2026-01-18T10:30:00.000Z"
    }
  ]
}
```

## Componentes Frontend Destacados

### RegimenModal.vue

Modal especializado para selección de régimen en reservas de WebService.

**Props:**
- `visible`: Boolean - Controla visibilidad
- `room`: Object - Datos de la habitación
- `hotelId`: Number - ID del hotel para cargar regímenes
- `nights`: Number - Número de noches
- `roomPrice`: Number - Precio de la habitación

**Eventos:**
- `@confirm`: Emite régimen seleccionado y precio total
- `@close`: Emite cuando se cierra el modal

**Funcionamiento:**
1. Se monta cuando `visible=true` (v-if)
2. En `mounted()` carga regímenes del WebService
3. Muestra lista de regímenes con precios
4. Permite selección con feedback visual
5. Calcula precio total: (habitación + régimen) × noches
6. Confirma y devuelve régimen seleccionado

### Navbar.vue

Componente de navegación reactivo.

**Características:**
- Detecta estado de autenticación desde localStorage
- Escucha evento `auth-change` para actualizarse
- Muestra opciones diferentes según estado:
  - No autenticado: Inicio, Registro, Login
  - Autenticado: Inicio, Mis Reservas, Perfil, Cerrar Sesión
- Indicador visual del usuario activo

## Manejo de Errores

### Backend

- Validaciones de campos obligatorios
- Manejo de errores de BD con try-catch
- Mensajes descriptivos en respuestas de error
- Logs de errores en consola con contexto

### Frontend

- Interceptores de Axios para errores HTTP
- Redirección a login si token inválido (401)
- Mensajes de error amigables con `alert()`
- Validación de campos antes de envío

## Seguridad

### Autenticación
- Contraseñas hasheadas con bcrypt (10 rounds)
- Tokens JWT con expiración de 24 horas
- Validación de token en cada petición protegida
- Middleware de autenticación en rutas privadas

### Base de Datos
- Queries parametrizadas (prevención SQL injection)
- Validación de tipos de datos
- Foreign keys para integridad referencial

### Frontend
- Validación de inputs
- Sanitización de datos antes de envío
- Tokens almacenados solo en localStorage (no cookies)
- Redirección automática a login en sesión expirada

## Exclusiones y Archivos Ignorados

El archivo `.gitignore` debe incluir:

```
# Dependencias
node_modules/
backend/node_modules/
frontend/node_modules/

# Build
backend/dist/
frontend/dist/

# Environment
.env
backend/.env

# Logs
*.log
npm-debug.log*

# OS
.DS_Store
Thumbs.db

# IDE
.vscode/
.idea/
*.swp
*.swo
```

## Solución de Problemas Comunes

### Error de CORS

Si aparecen errores de CORS al conectar con WebService o Channel:
- Verificar que ambos servicios tengan configurados los headers CORS
- WebService: Comprobar middleware CORS en `app.ts`
- Channel: Verificar CORS en configuración de FastAPI

### Token inválido

Si el token expira constantemente:
- Verificar sincronización de hora del sistema
- Comprobar que JWT_SECRET coincida en todas las instancias
- Revisar tiempo de expiración en AuthController

### Reservas no se guardan

- Verificar conexión a BD (principal_db)
- Comprobar que WebService/Channel estén activos
- Revisar logs del backend para errores específicos
- Validar que el usuario esté autenticado

### Modal de regímenes no carga

- Verificar que WebService esté activo en puerto 3000
- Comprobar que `idHotel` se pase correctamente como prop
- Revisar logs del navegador para errores de red
- Validar endpoint `/api/regimenes/hotel/{idHotel}` en WebService

## Roadmap y Mejoras Futuras

- Implementar filtros avanzados (precio, categoría, servicios)
- Sistema de cancelación de reservas
- Pasarela de pago integrada
- Notificaciones por email
- Historial completo de reservas (activas/pasadas/canceladas)
- Panel de administración
- Soporte multiidioma
- Modo oscuro
- PWA (Progressive Web App)

## Soporte y Contacto

Para reportar bugs o sugerir mejoras, contactar con el equipo de desarrollo.

## Licencia

Proyecto académico - UIB 2026

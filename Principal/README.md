# Principal - Motor de Reservas Unificado

## Descripción General

**Principal** es un sistema de reservas unificado que integra múltiples proveedores de alojamiento en una única plataforma. Actúa como agregador y punto de entrada único para búsqueda y reserva de habitaciones de hotel.

> **Versión**: 1.0.0  
> **Última actualización**: 18 de Enero 2026
> **Estado**: Producción Ready ✅

## Arquitectura del Sistema

### Componentes Principales

```
Principal/
├── backend/          # Servidor Node.js + Express + TypeScript
│   ├── src/
│   │   ├── controllers/     # Lógica de negocio
│   │   ├── services/        # Clientes para APIs externas
│   │   ├── config/          # Configuración de BD y servicios
│   │   ├── middleware/      # Autenticación JWT
│   │   └── types/           # Definiciones TypeScript
│   └── package.json
│
└── frontend/         # Aplicación Vue 3 + Vite
    ├── src/
    │   ├── views/           # Páginas principales
    │   ├── components/      # Componentes reutilizables
    │   ├── api/             # Clientes HTTP
    │   ├── router/          # Configuración de rutas
    │   └── assets/          # Recursos estáticos
    └── package.json
```

## Integraciones

### Proveedores Integrados

1. **WebService** (Puerto 3000)
   - Sistema PMS completo con gestión de reservas
   - Regímenes de alojamiento (SA, AD, MP, PC, TI)
   - Gestión de contratos y precios
   - Base de datos: MySQL (Prisma ORM)
   - Localizadores: `WS-2026-00001`
   - **Canal identificado como**: `Principal`

2. **Channel** (Puerto 8001)
   - Channel Manager para distribución
   - Gestión de disponibilidad en tiempo real
   - Base de datos: SQLite
   - Framework: FastAPI (Python)
   - Localizadores: UUID

### Flujo de Datos

```
Usuario → Frontend (Vue) → Backend (Express) → WebService / Channel
                                              ↓
                                         Base de Datos
```

## Instalación y Configuración

### Prerrequisitos

- **Node.js**: v16 o superior
- **npm**: v7 o superior
- **MySQL**: Para el backend del Principal y WebService
- **Python 3.9+**: Para el Channel Manager (debe estar ejecutándose)

### Instalación

```bash
# Clonar el repositorio
cd Principal

# Instalar dependencias (backend + frontend)
npm install

# Configurar base de datos MySQL
# Crear la base de datos 'principal_db'
mysql -u root -p -e "CREATE DATABASE principal_db;"
```

### Configuración de Base de Datos

**Backend Principal** (`backend/src/config/database.ts`):
```typescript
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root',
  password: 'tu_password',
  database: 'principal_db',
  waitForConnections: true,
  connectionLimit: 10
});
```

### Crear Tablas

```sql
-- Tabla de usuarios
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

-- Tabla de reservas
CREATE TABLE reservas (
  id INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id INT NOT NULL,
  localizador VARCHAR(50) NOT NULL,
  origen ENUM('WebService', 'Channel') NOT NULL,
  hotel_nombre VARCHAR(255) NOT NULL,
  habitacion_tipo VARCHAR(255) NOT NULL,
  fecha_entrada DATE NOT NULL,
  fecha_salida DATE NOT NULL,
  num_huespedes INT NOT NULL,
  precio_total DECIMAL(10,2) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
  INDEX idx_usuario (usuario_id),
  INDEX idx_localizador (localizador)
);
```

## Ejecución

### Desarrollo (Recomendado)

```bash
# Ejecutar backend + frontend simultáneamente
npm run dev
```

Esto ejecuta:
- **Backend**: `http://localhost:8010`
- **Frontend**: `http://localhost:5174` o `http://localhost:5175`

### Ejecución Individual

```bash
# Solo backend
cd backend
npm run dev

# Solo frontend
cd frontend
npm run dev
```

### Producción

```bash
# Compilar frontend
cd frontend
npm run build

# Iniciar backend en producción
cd backend
npm start
```

## API Endpoints

### Autenticación

#### POST `/api/auth/register`
Registro de nuevo usuario.

**Body:**
```json
{
  "nombre": "Juan",
  "apellidos": "Pérez García",
  "email": "juan@example.com",
  "password": "contraseña123",
  "dni": "12345678A",           // Opcional
  "fecha_nacimiento": "1990-01-15"  // Opcional
}
```

**Response:**
```json
{
  "message": "Usuario registrado exitosamente",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "email": "juan@example.com"
  }
}
```

#### POST `/api/auth/login`
Inicio de sesión.

**Body:**
```json
{
  "email": "juan@example.com",
  "password": "contraseña123"
}
```

**Response:**
```json
{
  "message": "Login exitoso",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "nombre": "Juan",
    "apellidos": "Pérez García",
    "email": "juan@example.com"
  }
}
```

### Búsqueda y Disponibilidad

#### GET `/api/search`
Buscar habitaciones disponibles en todos los proveedores.

**Query Parameters:**
- `ciudad`: Ciudad de destino
- `fecha_entrada`: Fecha de entrada (YYYY-MM-DD)
- `fecha_salida`: Fecha de salida (YYYY-MM-DD)
- `personas`: Número de huéspedes

**Ejemplo:**
```
GET /api/search?ciudad=Palma&fecha_entrada=2026-06-01&fecha_salida=2026-06-07&personas=2
```

**Response:**
```json
{
  "habitaciones": [
    {
      "id": "1-101",
      "nombre": "Habitación Doble Superior",
      "hotel": "Gran Hotel del Mar",
      "ciudad": "Palma",
      "precio": 120.50,
      "foto_url": "https://...",
      "origen": "WebService",
      "idHotel": 1,
      "capacidad": 2
    },
    {
      "id": "uuid-habitacion",
      "nombre": "Suite Junior",
      "hotel": "Hotel Playa",
      "ciudad": "Ibiza",
      "precio": 95.00,
      "foto_url": "https://...",
      "origen": "Channel",
      "hotelId": "hotel-uuid-123"
    }
  ],
  "total": 15,
  "filtros_aplicados": {
    "ciudad": "Palma",
    "fecha_entrada": "2026-06-01",
    "fecha_salida": "2026-06-07",
    "personas": 2
  },
  "estadisticas": {
    "webservice": 8,
    "channel": 7
  }
}
```

### Reservas

#### POST `/api/book`
Crear una nueva reserva (requiere autenticación).

**Headers:**
```
Authorization: Bearer <token>
```

**Body para WebService:**
```json
{
  "origen": "WebService",
  "habitacion_id": "1-101",
  "hotel_nombre": "Gran Hotel del Mar",
  "habitacion_tipo": "Habitación Doble Superior",
  "fecha_entrada": "2026-06-01",
  "fecha_salida": "2026-06-07",
  "num_huespedes": 2,
  "precio_total": 845.00,
  "regimen": "AD",
  "idHotel": 1
}
```

**Body para Channel:**
```json
{
  "origen": "Channel",
  "habitacion_id": "uuid-habitacion",
  "hotel_nombre": "Hotel Playa",
  "habitacion_tipo": "Suite Junior",
  "fecha_entrada": "2026-06-01",
  "fecha_salida": "2026-06-07",
  "num_huespedes": 2,
  "precio_total": 570.00,
  "hotel_id": "hotel-uuid-123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Reserva en WebService creada exitosamente",
  "localizador": "WS-2026-00001",
  "reserva": {
    "id": 123,
    "origen": "WebService",
    "fecha_entrada": "2026-06-01",
    "fecha_salida": "2026-06-07",
    "precio_total": 845.00
  }
}
```

#### GET `/api/reservas`
Obtener todas las reservas del usuario autenticado.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "success": true,
  "reservas": [
    {
      "id": 1,
      "localizador": "WS-2026-00001",
      "hotel_nombre": "Gran Hotel del Mar",
      "habitacion_tipo": "Habitación Doble Superior",
      "fecha_entrada": "2026-06-01T00:00:00.000Z",
      "fecha_salida": "2026-06-07T00:00:00.000Z",
      "num_huespedes": 2,
      "precio_total": "845.00",
      "origen": "WebService",
      "created_at": "2026-01-18T10:30:00.000Z"
    }
  ]
}
```

## Frontend - Componentes Principales

### Vistas

#### `Home.vue`
Página de inicio con buscador principal.
- Formulario de búsqueda (ciudad, fechas, personas)
- Validación de fechas
- Redirección a resultados

#### `Resultados.vue`
Listado de habitaciones disponibles.
- Filtros aplicados
- Tarjetas de habitaciones
- Modal de selección de régimen (WebService)
- Botones de reserva por proveedor

#### `MisReservas.vue`
Historial de reservas del usuario.
- Lista de todas las reservas
- Localizadores
- Detalles completos
- Filtrado por origen

#### `Login.vue` / `Registro.vue`
Autenticación de usuarios.
- Formularios de login/registro
- Validación de campos
- Gestión de tokens JWT

### Componentes

#### `NavBar.vue`
Barra de navegación principal.
- Enlaces a secciones
- Estado de autenticación reactivo
- Logout funcional
- Escucha eventos de autenticación (`auth-change`)

#### `RegimenModal.vue`
Modal para seleccionar régimen de alojamiento (WebService).
- Carga dinámica de regímenes desde WebService API
- Cálculo automático de precio total
- Descripción detallada de cada régimen:
  - **SA**: Solo Alojamiento
  - **AD**: Alojamiento y Desayuno
  - **MP**: Media Pensión (desayuno + comida o cena)
  - **PC**: Pensión Completa (desayuno + comida + cena)
  - **TI**: Todo Incluido (todas las comidas y bebidas)

## Autenticación

### Sistema JWT

El sistema utiliza JSON Web Tokens para autenticación:

1. Usuario se registra/inicia sesión
2. Backend genera token JWT firmado
3. Frontend almacena token en `localStorage`
4. Token se envía en header `Authorization: Bearer <token>` en cada petición
5. Backend valida token en middleware de autenticación

### Persistencia de Sesión

```javascript
// Guardar token
localStorage.setItem('token', token);
localStorage.setItem('user', JSON.stringify(user));

// Recuperar token
const token = localStorage.getItem('token');
const user = JSON.parse(localStorage.getItem('user'));

// Limpiar sesión
localStorage.removeItem('token');
localStorage.removeItem('user');
```

### Eventos de Autenticación

```javascript
// Emitir evento de cambio de autenticación
window.dispatchEvent(new Event('auth-change'));

// Escuchar cambios (en NavBar)
window.addEventListener('auth-change', () => {
  this.checkAuth();
});
```

## Flujo de Reserva Detallado

### Reserva WebService

1. Usuario busca disponibilidad
2. Selecciona habitación de WebService
3. **Modal de régimen** se abre automáticamente
4. Sistema llama a `GET /api/regimenes/hotel/{idHotel}` del WebService
5. Usuario ve lista de regímenes con precios
6. Usuario selecciona un régimen
7. Se calcula precio total: `(precio_habitación + precio_régimen) × noches`
8. Usuario confirma reserva
9. Backend envía petición a WebService con:
   ```json
   {
     "fechaEntrada": "2026-06-01",
     "fechaSalida": "2026-06-07",
     "hotel": "Gran Hotel del Mar",
     "tipoHabitacion": "Habitación Doble Superior",
     "regimen": "AD",
     "clientePaga": { /* datos del usuario */ },
     "canal": "Principal"
   }
   ```
10. WebService crea reserva y genera localizador: `WS-2026-00001`
11. Backend guarda reserva en BD local
12. Usuario recibe confirmación con localizador

### Reserva Channel

1. Usuario busca disponibilidad
2. Selecciona habitación de Channel
3. Confirmación directa (sin modal de régimen)
4. Backend envía petición a Channel con:
   ```json
   {
     "hotel_id": "uuid-hotel",
     "tipo_habitacion_id": "uuid-habitacion",
     "fecha_entrada": "2026-06-01",
     "fecha_salida": "2026-06-07",
     "num_huespedes": 2,
     "email_cliente": "user@example.com"
   }
   ```
5. Channel reduce disponibilidad automáticamente (stock - 1 por día)
6. Channel genera UUID como localizador
7. Backend guarda reserva en BD local
8. Usuario recibe confirmación con localizador UUID

## Diseño y Estilo

### Paleta de Colores (Tema Púrpura)

```css
:root {
  --primary: #9333ea;      /* Púrpura principal */
  --primary-dark: #6b46c1; /* Púrpura oscuro */
  --gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  --text: #1f2937;         /* Texto principal */
  --background: #f9fafb;   /* Fondo claro */
}
```

### Características de Diseño

- **Framework CSS**: Tailwind CSS (utility-first)
- **Componentes**: Diseño modular y reutilizable
- **Responsive**: Adaptado a móvil, tablet y desktop
- **Animaciones**: Transiciones suaves en modales y elementos
- **Iconos**: Font Awesome para iconografía

## Dependencias Principales

### Backend

```json
{
  "express": "^4.18.2",
  "typescript": "^5.0.0",
  "mysql2": "^3.6.0",
  "axios": "^1.6.0",
  "jsonwebtoken": "^9.0.2",
  "bcrypt": "^5.1.1",
  "dotenv": "^16.0.3",
  "cors": "^2.8.5",
  "concurrently": "^8.2.0"
}
```

### Frontend

```json
{
  "vue": "^3.3.4",
  "vue-router": "^4.2.5",
  "axios": "^1.6.0",
  "vite": "^5.0.0"
}
```

## Manejo de Errores

### Backend

```typescript
// Errores controlados con mensajes específicos
try {
  const resultado = await WebServiceClient.crearReserva(data);
  res.json({ success: true, data: resultado });
} catch (error) {
  console.error('[ERROR] Error al crear reserva:', error);
  res.status(500).json({ 
    success: false, 
    message: error.message || 'Error del servidor' 
  });
}
```

### Frontend

```javascript
// Manejo con try-catch y alertas al usuario
try {
  const response = await bookingAPI.book(reservationData);
  alert('¡Reserva confirmada!\n\nLocalizador: ' + response.data.localizador);
  this.$router.push('/mis-reservas');
} catch (error) {
  const errorMsg = error.response?.data?.message || error.message;
  alert('Error al procesar la reserva: ' + errorMsg);
  console.error('Detalles del error:', error.response?.data);
}
```

## Logs y Debugging

### Niveles de Log (Backend)

```
[BACKEND]    - Logs generales del backend
[DEBUG]      - Información de depuración detallada
[WebService] - Comunicación con WebService
[Channel]    - Comunicación con Channel
[AUTH]       - Autenticación y autorización
[ERROR]      - Errores del sistema
```

### Ejemplo de Logs

```
[BACKEND] Servidor iniciado en puerto 8010
[BACKEND] Conexión a la base de datos establecida
[DEBUG] WebService respondió: 8 habitaciones
[DEBUG] Channel respondió: 7 habitaciones
[DEBUG] Total habitaciones: 15
[AUTH] Usuario autenticado: juan@example.com
[WebService] Reserva creada: WS-2026-00001
[Channel] Reserva creada: uuid-localizador
```

## Seguridad

### Medidas Implementadas

1. **Contraseñas Hasheadas**: bcrypt con 10 salt rounds
2. **JWT Tokens**: Firmados con secret key, sin expiración (considerar añadir)
3. **CORS Configurado**: Headers permitidos para todos los orígenes (desarrollo)
4. **SQL Injection Protection**: Prepared statements con mysql2
5. **Validación de Entrada**: Sanitización básica de datos
6. **Autenticación en Rutas**: Middleware `authenticateToken` en rutas protegidas

### Recomendaciones de Seguridad para Producción

- [ ] Añadir expiración a tokens JWT (ej: 24h)
- [ ] Implementar refresh tokens
- [ ] Configurar CORS solo para dominios específicos
- [ ] Añadir rate limiting
- [ ] Implementar HTTPS obligatorio
- [ ] Validación más estricta de entrada
- [ ] Logs de auditoría

## Configuración de Servicios Externos

### WebService

El WebService debe estar ejecutándose en `http://localhost:3000`. Endpoints requeridos:

- `GET /api/disponibilidad` - Búsqueda de habitaciones
- `GET /api/regimenes/hotel/:idHotel` - Obtener regímenes de un hotel
- `POST /api/reservas` - Crear nueva reserva

### Channel

El Channel debe estar ejecutándose en `http://localhost:8001`. Endpoints requeridos:

- `GET /api/disponibilidad` - Búsqueda de habitaciones
- `POST /api/reservas` - Crear nueva reserva

## Troubleshooting

### Error: "Cannot connect to database"
**Causa**: Credenciales MySQL incorrectas o servidor no corriendo.
**Solución**: 
1. Verificar que MySQL esté ejecutándose
2. Comprobar credenciales en `backend/src/config/database.ts`
3. Verificar que la base de datos `principal_db` existe

### Error: "WebService no responde"
**Causa**: WebService no está ejecutándose o puerto incorrecto.
**Solución**:
1. Verificar que WebService esté en `http://localhost:3000`
2. Comprobar logs del WebService
3. Ejecutar `npm run dev` en la carpeta WebService

### Error: "Channel no responde"
**Causa**: Channel no está ejecutándose o puerto incorrecto.
**Solución**:
1. Verificar que Channel esté en `http://localhost:8001`
2. Ejecutar Python FastAPI: `cd Channel && uvicorn src.main:app --reload`

### Error: "Token inválido" o "No autorizado"
**Causa**: Token JWT expirado o corrupto.
**Solución**:
1. Cerrar sesión en el frontend
2. Volver a iniciar sesión
3. Verificar que `localStorage` contenga el token

### Frontend no carga o muestra página en blanco
**Causa**: Dependencias no instaladas o error de compilación.
**Solución**:
1. Ejecutar `npm install` en `frontend/`
2. Verificar consola del navegador para errores
3. Comprobar que Vite esté en puerto 5174

### Modal de régimen se queda cargando
**Causa**: WebService no responde o CORS bloqueado.
**Solución**:
1. Verificar que WebService tenga CORS habilitado
2. Comprobar en Network tab del navegador la petición
3. Verificar endpoint `/api/regimenes/hotel/:idHotel`

## Scripts Disponibles

```json
{
  "dev": "concurrently \"npm --prefix backend run dev\" \"npm --prefix frontend run dev\"",
  "install-all": "npm install && cd backend && npm install && cd ../frontend && npm install"
}
```

- **`npm run dev`**: Ejecuta backend y frontend simultáneamente
- **`npm run install-all`**: Instala todas las dependencias del proyecto

## Estructura de Base de Datos

### Usuarios

| Campo             | Tipo         | Descripción                    |
|-------------------|--------------|--------------------------------|
| id                | INT (PK)     | ID único del usuario           |
| nombre            | VARCHAR(100) | Nombre del usuario             |
| apellidos         | VARCHAR(100) | Apellidos del usuario          |
| email             | VARCHAR(255) | Email único (login)            |
| password          | VARCHAR(255) | Contraseña hasheada (bcrypt)   |
| dni               | VARCHAR(20)  | DNI/NIF (opcional)             |
| fecha_nacimiento  | DATE         | Fecha de nacimiento (opcional) |
| created_at        | TIMESTAMP    | Fecha de registro              |

### Reservas

| Campo            | Tipo           | Descripción                         |
|------------------|----------------|-------------------------------------|
| id               | INT (PK)       | ID único de la reserva              |
| usuario_id       | INT (FK)       | Referencia al usuario               |
| localizador      | VARCHAR(50)    | Código de reserva único             |
| origen           | ENUM           | 'WebService' o 'Channel'            |
| hotel_nombre     | VARCHAR(255)   | Nombre del hotel                    |
| habitacion_tipo  | VARCHAR(255)   | Tipo de habitación                  |
| fecha_entrada    | DATE           | Fecha de check-in                   |
| fecha_salida     | DATE           | Fecha de check-out                  |
| num_huespedes    | INT            | Número de huéspedes                 |
| precio_total     | DECIMAL(10,2)  | Precio total de la reserva          |
| created_at       | TIMESTAMP      | Fecha de creación de la reserva     |

## Licencia

Este proyecto es parte del sistema SectorTuristic desarrollado en la Universitat de les Illes Balears (UIB).

## Contacto y Soporte

Para dudas, consultas o reportar problemas sobre el sistema Principal:
- Revisar esta documentación
- Consultar logs del backend y frontend
- Verificar que todos los servicios estén ejecutándose

---

**Última actualización**: Enero 2026  
**Versión**: 1.0.0  
**Stack**: Node.js + TypeScript + Express + Vue 3 + MySQL

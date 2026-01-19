# Principal - Booking Engine

Sistema de reservas hoteleras que actúa como orquestador unificando la oferta de dos proveedores: **WebService** (Node.js/TypeScript) y **Channel** (Python/FastAPI).

## � Inicio Rápido

```bash
# Instalar todas las dependencias (backend + frontend)
npm run install-all

# Lanzar backend (8010) y frontend (5174) simultáneamente
npm run dev
```

Esto ejecutará:
- **Backend**: `http://localhost:8010` (Express + TypeScript)
- **Frontend**: `http://localhost:5174` (Vue 3 + Vite)

## �📋 Descripción

Principal es un motor de reservas que:
- Busca disponibilidad en múltiples proveedores de forma simultánea
- Gestiona usuarios y autenticación de forma independiente con JWT
- Almacena un histórico de reservas
- Ofrece una interfaz web moderna con Vue.js 3

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────┐
│           Principal Frontend (Vue.js)        │
│              Puerto 5174                     │
└──────────────────┬──────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────┐
│       Principal Backend (Node.js)            │
│              Puerto 8010                     │
│    - JWT Auth                                │
│    - Búsqueda unificada                      │
│    - Gestión de reservas                     │
└─────────┬──────────────────┬─────────────────┘
          │                  │
          ▼                  ▼
┌──────────────────┐  ┌──────────────────┐
│   WebService     │  │    Channel       │
│   (Node.js)      │  │   (FastAPI)      │
│   Puerto 3000    │  │   Puerto 8001    │
└──────────────────┘  └──────────────────┘
```

## 🗄️ Bases de Datos

El proyecto utiliza **MySQL** con las siguientes bases de datos:

- `pms_db`: Base de datos del WebService (PMS)
- `channel_manager`: Base de datos del Channel Manager
- `principal_db`: Base de datos propia de Principal (usuarios y reservas)

## 🚀 Instalación y Configuración

### Prerrequisitos

- Node.js 18+ y npm
- Python 3.8+
- MySQL 8.0+
- Git

### 1. Configurar WebService

```powershell
cd WebService

# Instalar dependencias
npm install

# Configurar variables de entorno
# Editar .env con las credenciales de MySQL

# Ejecutar migraciones de Prisma
npx prisma generate
npx prisma db push --accept-data-loss

# Agregar campo localizador a tabla reservas (si no existe)
# Conectarse a MySQL y ejecutar:
# ALTER TABLE Reserva ADD COLUMN localizador VARCHAR(191) UNIQUE DEFAULT (UUID());

# Iniciar el servidor
npm run dev
```

El WebService estará disponible en `http://localhost:3000`

### 2. Configurar Channel

```powershell
cd Channel

# Crear entorno virtual Python
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
# Editar src/config.py con las credenciales de MySQL

# Iniciar el servidor
python -m src.main
```

El Channel estará disponible en `http://localhost:8001`

### 3. Configurar Principal

```powershell
cd Principal

# Instalar dependencias (backend + frontend)
npm run install-all

# Configurar variables de entorno del backend
cd backend
cp .env.example .env
# Editar .env con tus credenciales
cd ..

# Crear la base de datos principal_db
# Conectarse a MySQL como root y ejecutar:
Get-Content database\setup.sql | mysql -u root -p

# Iniciar backend (8010) y frontend (5174) simultáneamente
npm run dev
```

- **Backend**: `http://localhost:8010`
- **Frontend**: `http://localhost:5174`

### Scripts Disponibles

```bash
# Desarrollo
npm run dev              # Backend + Frontend en paralelo
npm run dev:backend      # Solo backend (modo desarrollo)
npm run dev:frontend     # Solo frontend (modo desarrollo)

# Producción
npm run build            # Compilar backend y frontend
npm run start            # Iniciar backend compilado

# Instalación
npm run install-all      # Instalar todas las dependencias
```

## 🔧 Variables de Entorno

### Principal Backend (.env)

```env
# Base de datos
DB_HOST=localhost
DB_PORT=3306
DB_USER=pms_user
DB_PASSWORD=pms_password123
DB_NAME=principal_db

# JWT
JWT_SECRET=tu_clave_secreta_muy_segura_cambiala_en_produccion

# URLs de proveedores
WEBSERVICE_URL=http://localhost:3000
CHANNEL_URL=http://localhost:8001

# Puerto del servidor
PORT=8010
```

## 📚 API Endpoints

### Autenticación

- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/profile` - Obtener perfil (requiere JWT)

### Reservas

- `GET /api/booking/search` - Buscar habitaciones disponibles
  - Query params: `ciudad`, `fecha_entrada`, `fecha_salida`, `personas`
- `POST /api/booking/book` - Crear reserva (requiere JWT)
- `GET /api/booking/my-reservations` - Ver mis reservas (requiere JWT)
- `GET /api/booking/reservation/:localizador` - Ver detalle de reserva (requiere JWT)

## 💾 Esquema de Base de Datos

### Tabla: usuarios

```sql
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Tabla: reservas

```sql
CREATE TABLE reservas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    localizador_externo VARCHAR(100) NOT NULL,
    origen ENUM('webservice', 'channel') NOT NULL,
    hotel_id INT NOT NULL,
    hotel_nombre VARCHAR(200) NOT NULL,
    habitacion_id INT NOT NULL,
    habitacion_titulo VARCHAR(200) NOT NULL,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    numero_personas INT NOT NULL,
    precio_total DECIMAL(10,2) NOT NULL,
    estado ENUM('confirmada', 'cancelada', 'completada') DEFAULT 'confirmada',
    datos_adicionales JSON,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
```

## 🎯 Flujo de Uso

1. **Registro/Login**: El usuario se registra o inicia sesión en la aplicación
2. **Búsqueda**: Ingresa destino, fechas y número de personas
3. **Resultados**: El sistema consulta WebService y Channel en paralelo
4. **Selección**: El usuario ve habitaciones de ambos proveedores unificadas
5. **Reserva**: Al confirmar, se crea la reserva en el proveedor correspondiente
6. **Histórico**: La reserva se guarda en `principal_db` con su localizador externo

## 🔒 Seguridad

- Contraseñas hasheadas con **bcryptjs** (10 rounds)
- Autenticación JWT con tokens de 7 días
- Validación de datos en frontend y backend
- Middleware de autenticación en rutas protegidas
- Variables sensibles en archivos `.env` (no versionados)

## 🧪 Testing

### Probar el Backend

```powershell
# Probar registro
curl -X POST http://localhost:8010/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{
    "nombre": "Juan",
    "apellidos": "Pérez",
    "email": "juan@example.com",
    "dni": "12345678A",
    "fecha_nacimiento": "1990-01-01",
    "password": "123456"
  }'

# Probar login
curl -X POST http://localhost:8010/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{
    "email": "juan@example.com",
    "password": "123456"
  }'

# Probar búsqueda (sin autenticación)
curl "http://localhost:8010/api/booking/search?ciudad=Palma&fecha_entrada=2024-06-01&fecha_salida=2024-06-05&personas=2"
```

## 📱 Funcionalidades del Frontend

- ✅ Página de inicio con buscador hero
- ✅ Resultados con tarjetas de habitaciones
- ✅ Registro de usuarios (nombre, apellidos, email, DNI, fecha nacimiento)
- ✅ Login con JWT
- ✅ Mis Reservas (historial completo)
- ✅ Diseño responsive
- ✅ Navegación con Vue Router
- ✅ Indicadores de origen (WebService/Channel)

## 🚫 Limitaciones

- No se permite **cancelación** de reservas desde Principal
- Principal solo almacena un **snapshot** de cada reserva
- Para modificaciones, contactar directamente con el proveedor usando el localizador

## 📝 Scripts Disponibles

### Backend

```powershell
npm run dev      # Modo desarrollo con ts-node-dev
npm run build    # Compilar TypeScript a JavaScript
npm start        # Ejecutar versión compilada
```

### Frontend

```powershell
npm run dev      # Servidor de desarrollo Vite
npm run build    # Build de producción
npm run preview  # Vista previa del build
```

## 🛠️ Tecnologías Utilizadas

### Backend
- Node.js + Express
- TypeScript
- MySQL2 (driver MySQL)
- bcryptjs (hash de contraseñas)
- jsonwebtoken (JWT)
- axios (HTTP client)
- uuid (generación de localizadores)

### Frontend
- Vue.js 3 (Composition API)
- Vue Router 4
- Vite 5
- axios (peticiones HTTP)

## 📧 Contacto

Para dudas o problemas, contactar al equipo de desarrollo.

---

**Versión**: 1.0.0  
**Licencia**: Proyecto Académico - UIB

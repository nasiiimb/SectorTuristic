# GDS - Sistema de Distribución Global

Backend del GDS (Global Distribution System) - Orquestador unificado de WebService y Channel.

## 🚀 Características

- **Orquestación Unificada**: Consulta simultánea a WebService y Channel
- **Autenticación JWT**: Sistema seguro de registro y login
- **Gestión de Reservas**: Creación y consulta de reservas en múltiples proveedores
- **API RESTful**: Endpoints bien definidos y documentados

## 📋 Requisitos

- Node.js >= 16.x
- MySQL >= 5.7
- npm o yarn

## 🔧 Instalación

1. **Instalar dependencias:**
```bash
cd backend
npm install
```

2. **Configurar variables de entorno:**

Edita el archivo `.env` con tus configuraciones:
```env
PORT=8010
DB_HOST=localhost
DB_PORT=3306
DB_USER=pms_user
DB_PASSWORD=pms_password123
DB_NAME=principal_db
JWT_SECRET=gds_secret_key_change_in_production
WEBSERVICE_URL=http://localhost:3000
CHANNEL_URL=http://localhost:8001
CORS_ORIGIN=http://localhost:5174
```

3. **Crear la base de datos:**

Asegúrate de que la base de datos `principal_db` existe y tiene las tablas necesarias:
- `usuarios`
- `reservas`

## 🎯 Uso

### Modo desarrollo
```bash
npm run dev
```

### Modo producción
```bash
npm run build
npm start
```

El servidor estará disponible en: `http://localhost:8010`

## 📡 Endpoints

### Autenticación
- `POST /api/auth/register` - Registrar nuevo usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/profile` - Obtener perfil (requiere auth)

### Búsqueda y Reservas
- `GET /api/search` - Buscar disponibilidad en todos los proveedores
- `POST /api/book` - Crear reserva (requiere auth)
- `GET /api/my-reservations` - Mis reservas (requiere auth)
- `GET /api/reservations/:localizador` - Detalle de reserva (requiere auth)

### Sistema
- `GET /` - Información del servicio
- `GET /health` - Health check

## 🏗️ Arquitectura

```
GDS Backend
├── src/
│   ├── config/         # Configuración (BD, etc)
│   ├── controllers/    # Controladores de rutas
│   ├── middleware/     # Middlewares (auth, etc)
│   ├── models/         # Modelos de datos
│   ├── routes/         # Definición de rutas
│   ├── services/       # Servicios (clientes externos)
│   ├── types/          # Tipos TypeScript
│   └── server.ts       # Punto de entrada
├── .env               # Variables de entorno
├── package.json       # Dependencias
└── tsconfig.json      # Configuración TypeScript
```

## 🔄 Flujo de Búsqueda

1. Cliente hace petición a `/api/search`
2. GDS consulta en paralelo:
   - WebService (`http://localhost:3000`)
   - Channel (`http://localhost:8001`)
3. Unifica los resultados
4. Devuelve habitaciones disponibles de ambas fuentes

## 🔄 Flujo de Reserva

1. Usuario autenticado hace petición a `/api/book`
2. GDS valida los datos
3. Crea reserva en el proveedor indicado (WebService o Channel)
4. Guarda la reserva en la BD local con localizador GDS
5. Devuelve confirmación con ambos localizadores

## 🛠️ Tecnologías

- **Express.js** - Framework web
- **TypeScript** - Lenguaje tipado
- **MySQL2** - Cliente de base de datos
- **JWT** - Autenticación
- **Bcrypt** - Hash de contraseñas
- **Axios** - Cliente HTTP
- **CORS** - Manejo de CORS
- **Dotenv** - Variables de entorno

## 📝 Notas

- Los errores de TypeScript mostrados antes de `npm install` son normales
- Una vez instaladas las dependencias, todos los errores se resolverán
- Asegúrate de que WebService y Channel estén corriendo antes de hacer búsquedas

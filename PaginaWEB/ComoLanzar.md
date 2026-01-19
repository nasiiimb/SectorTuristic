# Cómo Lanzar la Página Web

## Guía Completa de Instalación y Ejecución

### Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

- **PHP 8.5+** (con extensiones: pdo_mysql, curl, json)
- **MySQL 8.0+** o **MariaDB 10.5+**
- **Node.js 18+** (para ejecutar el WebService)
- **npm** o **yarn**

### Estructura del Proyecto

```
SectorTuristic/
├── PaginaWEB/          ← Página web (PHP)
├── WebService/         ← API REST (Node.js + Express)
├── BD/                 ← Base de datos (SQL)
└── README.md
```

---

## Paso 1: Configurar la Base de Datos

### Opción A: Usando npm (Recomendado)

```bash
cd WebService
npm install
npm run db:setup
```

Este comando:
1. Conecta a MySQL (localhost:3306, usuario: pms_user, password: pms_password123)
2. Crea la base de datos `pms_database`
3. Ejecuta 59 statements SQL desde `BD/dump-clean.sql`
4. Carga todas las tablas (21 tablas) y datos iniciales
5. Muestra un resumen de los datos insertados

Salida esperada:
```
[OK] Conectado a MySQL
[CREATING] Creando base de datos "pms_database"...
[OK] Base de datos "pms_database" lista
[OK] Conectado a la base de datos "pms_database"
[READING] Leyendo dump-clean.sql...
[EXECUTING] Ejecutando SQL...
[OK] 59 statements ejecutados exitosamente
[INFO] Tablas creadas: 21
[INFO] RESUMEN DE DATOS:
  • Ciudades: 1
  • Hoteles: 3
  • Tipos de Habitación: 4
  • Habitaciones: 36
  • Regímenes: 5
  • Precios de Regímenes: 15
  • Tarifas: 4
  • Servicios: 5
  • Descuentos: 3
[SUCCESS] Base de datos configurada exitosamente!
```

### Opción B: Manual (MySQL CLI)

```bash
# Conectar a MySQL
mysql -u root -p

# En MySQL:
CREATE DATABASE pms_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE pms_database;
SOURCE ../BD/dump-clean.sql;
SHOW TABLES;
```

### Resetear la Base de Datos

Si necesitas limpiar todo y empezar de nuevo:

```bash
cd WebService
npm run db:reset
```

Se te pedirá confirmación escribiendo "SI". Este comando:
1. Elimina la base de datos `pms_database`
2. La recrea desde cero
3. Carga todos los datos iniciales nuevamente

### Variables de Entorno (WebService)

Crear archivo `.env` en `WebService/`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=pms_database
DB_PORT=3306
PORT=3000
```

---

## Paso 2: Lanzar el WebService (API REST)

### Terminal 1: WebService

```bash
cd WebService
npm install
npm run dev
```

Esperarás ver:
```
Server is running on http://localhost:3000
```

El WebService estará disponible en:
- **URL**: http://localhost:3000
- **API**: http://localhost:3000/api

Endpoints principales:
- `GET /api/ciudades` - Listado de ciudades
- `GET /api/disponibilidad` - Disponibilidad de hoteles
- `GET /api/regimenes` - Regímenes de alojamiento
- `POST /api/reservas` - Crear reserva

---

## Paso 3: Lanzar la Página Web (PHP)

### Terminal 2: Servidor PHP

```bash
cd PaginaWEB
php -S localhost:8000
```

Esperarás ver:
```
[Sat Nov 30 09:00:00 2025] PHP 8.5.0 Development Server (http://localhost:8000) started
```

La página web estará disponible en:
- **URL**: http://localhost:8000

---

## Paso 4: Acceder a la Aplicación

### 1. Página de Inicio
- **URL**: http://localhost:8000

### 2. Flujo de Reserva
1. Selecciona país, ciudad, hotel, fechas
2. Haz clic en "Buscar"
3. Selecciona habitación y régimen
4. Haz clic en "Reservar"
5. Confirma los datos y haz clic en "Confirmar y Pagar"

### 3. Datos de Prueba

**Cuenta Demo:**
- Email: `nasimbenyacoub@gmail.com`
- Contraseña: (solicita reset en caso necesario)

**Hoteles Disponibles:**
1. Gran Hotel del Mar (5 estrellas) - Paseo Marítimo
2. Hotel Palma Centro (4 estrellas) - Avinguda de Jaume III
3. Boutique Hotel Casco Antiguo (3 estrellas) - Carrer de Sant Miquel

**Regímenes:**
- SA: Solo Alojamiento
- AD: Alojamiento y Desayuno
- MP: Media Pensión
- PC: Pensión Completa
- TI: Todo Incluido

---

## Troubleshooting

### Error: "Cannot connect to MySQL"

**Solución:**
```bash
# Verificar que MySQL está ejecutándose
# En Windows: Buscar "MySQL" en servicios
# En Linux/Mac: 
sudo systemctl status mysql

# Iniciar si no está corriendo
sudo systemctl start mysql
```

### Error: "Base de datos no existe"

**Solución:**
```bash
cd WebService
npm run db:setup
```

### Error: "Puerto 8000 ya en uso"

**Solución:**
```bash
# Usar otro puerto
cd PaginaWEB
php -S localhost:8001
```

### Error: "Puerto 3000 ya en uso"

**Solución:**
```bash
# Usar otro puerto
cd WebService
PORT=3001 npm run dev
```

### La página carga pero no muestra datos

**Solución:**
1. Abre las herramientas de desarrollador (F12)
2. Ve a la pestaña "Network"
3. Verifica que las peticiones a `http://localhost:3000/api` se completan correctamente
4. Si hay CORS errors, reinicia ambos servidores

---

## Configuración Avanzada

### Cambiar Puerto del WebService

En `WebService/.env`:
```env
PORT=3001
```

### Cambiar Credenciales de Base de Datos

En `WebService/.env`:
```env
DB_HOST=192.168.1.100
DB_USER=usuario
DB_PASSWORD=contraseña
DB_PORT=3307
```

### Resetear la Base de Datos

```bash
cd WebService
npm run db:reset
```

**Nota**: Este comando eliminará todos los datos y recreará las tablas con datos iniciales.

---

## Parar los Servidores

### En la Terminal del WebService
Presiona: `Ctrl + C`

### En la Terminal de PHP
Presiona: `Ctrl + C`

---

## Próximos Pasos

Después de que todo esté funcionando:

1. **Crear reservas** para probar el flujo completo
2. **Revisar logs** en la consola del WebService
3. **Modificar datos** desde la página de administración
4. **Integrar con Gateway de Pagos** (próximamente)

---

## Soporte

Si encuentras problemas:

1. Revisa los logs en ambas terminales
2. Verifica la conectividad a la base de datos
3. Asegúrate de que todos los puertos están disponibles
4. Consulta los archivos README en cada carpeta

---

**Última actualización**: 30 de Noviembre de 2025
**Versión**: 1.0

# 🚀 Cómo Ejecutar el WebService

Esta guía te explica paso a paso cómo configurar y ejecutar el servidor del WebService.

## 📋 Requisitos Previos

Antes de empezar, asegúrate de tener instalado:

- **Node.js** (versión 16 o superior) - [Descargar](https://nodejs.org/)
- **npm** (viene incluido con Node.js)
- **MySQL** (versión 8.0 o superior) - [Descargar](https://dev.mysql.com/downloads/)
- **Git** (opcional, para clonar el repositorio)

## 🔧 Configuración Inicial

### 1. Instalar Dependencias

Abre una terminal en la carpeta `WebService` y ejecuta:

```bash
npm install
```

Esto instalará todas las dependencias necesarias:
- Express.js
- Prisma
- TypeScript
- ts-node-dev
- dotenv
- @types/express
- @types/node

### 2. Configurar la Base de Datos

#### Opción A: Usar los scripts incluidos (Recomendado)

Desde la carpeta `BD`, ejecuta:

```bash
# Windows (PowerShell)
.\crear_bd.bat

# O manualmente:
mysql -u root -p < dump.sql
mysql -u root -p pms_database < insert.sql
```

#### Opción B: Configuración manual

1. Crear la base de datos:
```sql
CREATE DATABASE pms_database CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Crear el usuario:
```sql
CREATE USER 'pms_user'@'localhost' IDENTIFIED BY 'pms_password123';
GRANT ALL PRIVILEGES ON pms_database.* TO 'pms_user'@'localhost';
FLUSH PRIVILEGES;
```

3. Importar el esquema y los datos:
```bash
mysql -u pms_user -ppms_password123 pms_database < BD/dump.sql
mysql -u pms_user -ppms_password123 pms_database < BD/insert.sql
```

### 3. Configurar Variables de Entorno

Crea un archivo `.env` en la carpeta `WebService` con el siguiente contenido:

```env
# URL de conexión a la base de datos
DATABASE_URL="mysql://pms_user:pms_password123@localhost:3306/pms_database"

# Puerto del servidor (opcional, por defecto 3000)
PORT=3000

# Entorno (development, production)
NODE_ENV=development
```

**⚠️ Importante**: Ajusta el usuario, contraseña y nombre de la base de datos según tu configuración.

### 4. Generar el Cliente de Prisma

Esto genera los tipos TypeScript basados en tu esquema de base de datos:

```bash
npm run prisma:generate
```

## ▶️ Ejecutar el Servidor

### Modo Desarrollo (con hot-reload)

Este modo reinicia automáticamente el servidor cuando detecta cambios en los archivos:

```bash
npm run dev
```

**Salida esperada**:
```
[INFO] 12:00:00 ts-node-dev (pid: 1234) started
🚀 Servidor corriendo en http://localhost:3000
```

### Modo Producción

1. Compilar TypeScript a JavaScript:
```bash
npm run build
```

2. Ejecutar el servidor compilado:
```bash
npm start
```

## ✅ Verificar que Funciona

### Opción 1: Navegador
Abre tu navegador y visita:
```
http://localhost:3000/api/hoteles
```

Deberías ver un JSON con la lista de hoteles.

### Opción 2: Terminal (curl)
```bash
curl http://localhost:3000/api/hoteles
```

### Opción 3: PowerShell
```powershell
Invoke-WebRequest -Uri "http://localhost:3000/api/hoteles" -Method GET
```

### Opción 4: Postman
Importa la colección `PMS_Demo.postman_collection.json` y ejecuta las peticiones.

## 🛠️ Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `npm run dev` | Ejecuta el servidor en modo desarrollo con hot-reload |
| `npm start` | Ejecuta el servidor en modo producción (requiere build) |
| `npm run build` | Compila TypeScript a JavaScript en la carpeta `dist/` |
| `npm run prisma:generate` | Genera el cliente de Prisma basado en el schema |
| `npm run prisma:studio` | Abre Prisma Studio (GUI para ver/editar datos) |
| `npm run prisma:migrate` | Crea una nueva migración de base de datos |
| `npm run prisma:push` | Sincroniza el schema con la base de datos (desarrollo) |

## 🔍 Prisma Studio (Opcional)

Para visualizar y editar los datos de la base de datos con una interfaz gráfica:

```bash
npm run prisma:studio
```

Se abrirá automáticamente en `http://localhost:5555`

## 🚨 Solución de Problemas

### Error: "Cannot connect to MySQL server"

**Problema**: No se puede conectar a la base de datos.

**Soluciones**:
1. Verifica que MySQL esté corriendo:
   ```bash
   # Windows
   net start MySQL80
   
   # Verificar servicio
   Get-Service MySQL*
   ```

2. Verifica las credenciales en `.env`
3. Asegúrate de que el usuario tenga permisos

### Error: "Port 3000 is already in use"

**Problema**: El puerto 3000 ya está ocupado.

**Soluciones**:
1. Cambia el puerto en `.env`:
   ```env
   PORT=3001
   ```

2. O mata el proceso que usa el puerto 3000:
   ```bash
   # Windows PowerShell
   Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess | Stop-Process -Force
   ```

### Error: "Prisma Client not found"

**Problema**: El cliente de Prisma no está generado.

**Solución**:
```bash
npm run prisma:generate
```

### Error: "Table 'pms_database.hotel' doesn't exist"

**Problema**: Las tablas no existen en la base de datos.

**Solución**:
```bash
cd ..\BD
mysql -u pms_user -ppms_password123 pms_database < dump.sql
mysql -u pms_user -ppms_password123 pms_database < insert.sql
```

### Error: TypeScript compilation errors

**Problema**: Errores de compilación de TypeScript.

**Solución**:
```bash
# Reinstalar dependencias
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install

# Regenerar Prisma Client
npm run prisma:generate
```

## 📦 Estructura de Carpetas Generadas

Después de la configuración, verás estas carpetas adicionales:

```
WebService/
├── node_modules/          # Dependencias de npm (NO subir a git)
├── dist/                  # Código JavaScript compilado (NO subir a git)
└── src/generated/prisma/  # Cliente de Prisma generado (NO subir a git)
```

## 🔐 Seguridad

⚠️ **Importante para producción**:
- Nunca subas el archivo `.env` a git
- Cambia las contraseñas por defecto
- Usa variables de entorno del sistema
- Habilita HTTPS
- Implementa autenticación y autorización

## 📞 Testing con Postman

Una vez el servidor esté corriendo, consulta `POSTMAN_DEMO.md` para ver ejemplos de llamadas a la API.

## 🎯 Siguientes Pasos

1. ✅ Servidor corriendo en http://localhost:3000
2. 📖 Lee `README.md` para entender la arquitectura
3. 🧪 Prueba los endpoints con `POSTMAN_DEMO.md`
4. 📚 Aprende más sobre Prisma en `PRISMA.md`

---

**¿Problemas?** Revisa los logs en la terminal donde ejecutaste `npm run dev`

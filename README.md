# Sistema de Gestión Hotelera - Sector Turístico

Proyecto completo de gestión hotelera compuesto por tres módulos principales: Base de Datos, WebService (API REST) y PMS (Property Management System).

## Estructura del Proyecto

```
SectorTuristic/
├── BD/                      # Base de Datos MySQL
│   ├── dump.sql            # Esquema de la base de datos
│   ├── insert.sql          # Datos de prueba
│   ├── crear_bd.bat        # Script para crear BD (Windows)
│   └── PMS.pdf             # Documentación del modelo
│
├── WebService/              # API REST (Backend)
│   ├── src/                # Código fuente TypeScript
│   │   ├── api/           # Controladores REST
│   │   ├── config/        # Configuración de DB
│   │   └── models/        # Modelos Prisma
│   ├── package.json        # Dependencias Node.js
│   ├── tsconfig.json       # Configuración TypeScript
│   └── .env               # Variables de entorno
│
├── PMS/                     # Property Management System (Frontend)
│   ├── src/                # Código fuente Python
│   │   ├── domain/        # Entidades de negocio
│   │   ├── repositories/  # Acceso a datos
│   │   ├── services/      # Lógica de negocio
│   │   ├── ui_gui/        # Interfaz gráfica
│   │   └── infrastructure/ # Configuración
│   ├── main.py             # Punto de entrada
│   ├── requirements.txt    # Dependencias Python
│   └── README.md          # Documentación completa
│
├── crear_zip.ps1           # Script para crear ZIP (Windows)
├── crear_zip.sh            # Script para crear ZIP (Linux/Mac)
└── README.md              # Este archivo
```

## Tutorial de Inicio Rápido

### Prerrequisitos

1. **Node.js 18+**: https://nodejs.org/
2. **Python 3.9+**: https://www.python.org/downloads/
3. **MySQL 8.0+**: https://dev.mysql.com/downloads/mysql/

### Paso 1: Configurar Base de Datos

```bash
cd BD
# Windows:
crear_bd.bat

# Linux/Mac:
mysql -u root -p < dump.sql
mysql -u root -p pms_database < insert.sql
```

### Paso 2: Configurar y Lanzar WebService

```bash
cd WebService

# Instalar dependencias
npm install

# Configurar .env
# Editar DATABASE_URL con tu contraseña de MySQL

# Generar cliente Prisma
npx prisma generate

# Iniciar servidor
npm run dev
```

El servidor estará disponible en: http://localhost:3000

### Paso 3: Lanzar PMS

```bash
cd PMS

# Instalar dependencias
pip install -r requirements.txt

# Iniciar aplicación
python main.py
```

## Documentación Detallada

Para instrucciones completas sobre cómo usar cada módulo, consulta:

- **PMS**: Ver `PMS/README.md` - Guía completa de instalación, configuración y uso
- **WebService**: Documentación de API REST y endpoints
- **BD**: Modelo de datos y esquema de base de datos

## Crear ZIP del Proyecto

Para crear un archivo ZIP del proyecto sin incluir `node_modules` (que puede pesar más de 100MB):

### Windows (PowerShell)

```powershell
# Ejecutar desde la carpeta SectorTuristic
.\crear_zip.ps1
```

O hacer doble clic en `crear_zip.ps1`

### Linux/Mac (Bash)

```bash
# Dar permisos de ejecución (solo primera vez)
chmod +x crear_zip.sh

# Ejecutar
./crear_zip.sh
```

El script creará un archivo `SectorTuristic_YYYY-MM-DD_HH-MM.zip` en la carpeta padre, excluyendo:
- node_modules (dependencias de Node.js)
- .git (control de versiones)
- __pycache__ (cache de Python)
- dist/build (archivos compilados)
- .DS_Store (archivos del sistema)

El ZIP resultante pesará aproximadamente 5-10 MB en lugar de más de 100 MB.

## Tecnologías Utilizadas

### Backend (WebService)
- **Node.js 18+** con **TypeScript 5.9**
- **Express.js** - Framework web
- **Prisma ORM 6.17** - Acceso a base de datos
- **MySQL 8.0** - Base de datos relacional

### Frontend (PMS)
- **Python 3.9+**
- **CustomTkinter 5.2** - Interfaz gráfica moderna
- **Clean Architecture** - Arquitectura en capas
- **SOLID Principles** - Principios de diseño

### Base de Datos
- **MySQL 8.0** - Sistema de gestión de base de datos
- **23 tablas** relacionales
- **Datos de prueba** incluidos

## Características Principales

### WebService
- API REST completa con 50+ endpoints
- Autenticación y validación de datos
- Manejo robusto de errores
- Documentación de API integrada

### PMS
- Interfaz gráfica moderna (Dark Mode)
- Gestión de Clientes, Reservas y Contratos
- Check-in/Check-out de huéspedes
- Consultas de disponibilidad
- Búsquedas avanzadas
- Validaciones en tiempo real

### Base de Datos
- Modelo relacional normalizado
- Integridad referencial
- Datos de prueba para 3 hoteles
- Soporte para múltiples regímenes y tipos de habitación

## Flujo de Trabajo Típico

1. **Buscar disponibilidad** en fechas y ciudad específicas
2. **Crear reserva** con datos del cliente
3. **Crear contrato** asignando habitación y monto
4. **Realizar check-in** al llegar el cliente
5. **Gestionar servicios** durante la estancia
6. **Realizar check-out** al finalizar

## Puertos Utilizados

- **3000**: WebService (API REST)
- **3306**: MySQL Database

## Solución de Problemas

### El WebService no inicia
- Verifica que MySQL esté ejecutándose
- Revisa el archivo `.env` con las credenciales correctas
- Ejecuta `npx prisma generate` para regenerar el cliente

### El PMS no se conecta al WebService
- Verifica que el WebService esté corriendo en http://localhost:3000
- Revisa `PMS/src/infrastructure/config.py` para la URL correcta

### Error de dependencias
- WebService: Elimina `node_modules` y ejecuta `npm install`
- PMS: Ejecuta `pip install -r requirements.txt` de nuevo

## Mantenimiento

### Actualizar Dependencias

**WebService:**
```bash
npm update
npm audit fix
```

**PMS:**
```bash
pip install --upgrade -r requirements.txt
```

### Backup de Base de Datos

```bash
mysqldump -u root -p pms_database > backup_$(date +%Y%m%d).sql
```

## Licencia

Proyecto académico - Universidad de las Islas Baleares (UIB)

## Contacto

Para soporte o consultas sobre el proyecto, contacta con el equipo de desarrollo.

---

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025

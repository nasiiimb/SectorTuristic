# PMS - Property Management System

Sistema de Gestión Hotelera con Clean Architecture y Principios SOLID

## Descripción

El PMS (Property Management System) es una aplicación de escritorio moderna con interfaz gráfica que permite a los empleados de la cadena hotelera (recepcionistas, personal de reservas, etc.) gestionar:

- **Clientes**: Altas, modificaciones, búsquedas y consultas
- **Reservas**: Crear, modificar, cancelar reservas, check-in/check-out
- **Contratos**: Gestión de contratos activos y finalizados
- **Consultas**: Hoteles, tipos de habitación, regímenes, ciudades, disponibilidad

## Características de la Interfaz

### Diseño Profesional
- **Framework**: CustomTkinter 5.2.0 (Material Design-inspired)
- **Tema**: Dark mode profesional
- **Colores**: Paleta turquesa/verde azulado (#2B7A78)
- **Tipografía**: Fuentes modernas escalables
- **Componentes**: Botones redondeados, sombras, efectos hover
- **UX**: Layout responsive, tablas scrollables, selección por click

### Componentes Visuales
- **Ventana Principal**: Header profesional con gradiente y footer informativo
- **Pestañas**: Sistema de navegación moderno (Clientes, Reservas, Consultas)
- **Formularios**: Campos con validación visual en tiempo real
- **Tablas**: Filas alternadas con colores semánticos y scroll automático
- **Botones**: Iconos visuales con colores por acción (verde=crear, azul=editar, rojo=eliminar)

## 🏗️ Arquitectura

El PMS implementa **Clean Architecture** con 5 capas claramente separadas y sigue los **principios SOLID**. **NO accede directamente a la base de datos**, toda la comunicación se realiza a través del **WebService REST API**.

```
┌─────────────────────────────────────────────────────────────┐
│                    PMS (Python + CustomTkinter)              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🟣 UI LAYER (Presentation)                          │  │
│  │  - MainWindow (CustomTkinter)                        │  │
│  │  - ClientePanel, ReservaPanel, ConsultaPanel        │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🟡 SERVICE LAYER (Business Logic)                   │  │
│  │  - ClienteService, ReservaService, ConsultaService  │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🟢 REPOSITORY LAYER (Data Access)                   │  │
│  │  - IRepository[T] interface                          │  │
│  │  - ClienteRepository, ReservaRepository, etc.        │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🔴 INFRASTRUCTURE LAYER                             │  │
│  │  - APIClient (HTTP adapter)                          │  │
│  │  - Config (settings)                                 │  │
│  └────────────────────┬─────────────────────────────────┘  │
│                       │                                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  🔵 DOMAIN LAYER (Entities + Value Objects)          │  │
│  │  - Cliente, Reserva, Hotel, Contrato                │  │
│  │  - Business rules and validations                    │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP/REST (JSON)
                          ▼
                 ┌─────────────────┐
                 │   WebService    │
                 │   (Node.js)     │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  MySQL Database │
                 └─────────────────┘
```

## 📁 Estructura del Proyecto

```
PMS/
├── main.py                    # Entry point + DI Container
├── requirements.txt           # Dependencies
├── README.md                  # Documentation
└── src/
    ├── domain/               # 🔵 DOMAIN LAYER
    │   ├── cliente.py       # Cliente entity + validations
    │   ├── reserva.py       # Reserva aggregate + business rules
    │   ├── hotel.py         # Hotel, Ciudad, TipoHabitacion, Regimen
    │   └── contrato.py      # Contrato entity
    │
    ├── repositories/         # 🟢 REPOSITORY LAYER
    │   ├── base.py          # IRepository[T] interface
    │   ├── cliente_repository.py
    │   ├── reserva_repository.py
    │   ├── hotel_repository.py
    │   ├── ciudad_repository.py
    │   ├── tipo_habitacion_repository.py
    │   ├── regimen_repository.py
    │   └── contrato_repository.py
    │
    ├── services/             # 🟡 SERVICE LAYER
    │   ├── cliente_service.py      # Cliente business logic
    │   ├── reserva_service.py      # Reserva + Check-in/out
    │   └── consulta_service.py     # Read-only queries
    │
    ├── ui_gui/               # 🟣 PRESENTATION LAYER
    │   ├── __init__.py
    │   ├── main_window.py          # Main window + tabs
    │   ├── cliente_panel.py        # Cliente CRUD panel
    │   ├── reserva_panel.py        # Reserva CRUD + Check-in/out
    │   └── consulta_panel.py       # Multi-tab read-only views
    │
    ├── infrastructure/       # 🔴 INFRASTRUCTURE LAYER
    │   ├── config.py        # Configuration management
    │   └── api_client.py    # HTTP client adapter
    │
    └── utils/
        ├── console.py       # Console utilities
        └── validators.py   # Input validators
```

## Tutorial Completo: Cómo Lanzar Todo el Sistema

Este tutorial te guiará paso a paso para poner en marcha todo el sistema PMS desde cero.

### Requisitos Previos

Antes de comenzar, asegúrate de tener instalado:

1. **Node.js** (versión 18 o superior)
   - Descargar de: https://nodejs.org/
   - Verificar instalación: `node --version`

2. **Python 3.9+**
   - Descargar de: https://www.python.org/downloads/
   - Verificar instalación: `python --version` o `python3 --version`

3. **MySQL Server** (versión 8.0 o superior)
   - Descargar de: https://dev.mysql.com/downloads/mysql/
   - Asegúrate de recordar el usuario y contraseña de root
   - La base de datos debe llamarse: **PMS54870695D** (PMS + NIF del alumno)

### PASO 1: Configurar la Base de Datos

La base de datos debe llamarse **PMS54870695D** (PMS + NIF del alumno).

1. Abre una terminal o símbolo del sistema

2. Navega a la carpeta BD:
   ```bash
   cd "C:\UIB\Solucions Turistiques\practica\SectorTuristic\BD"
   ```

3. Ejecuta el script de creación de base de datos:
   
   **En Windows:**
   ```bash
   crear_bd.bat
   ```
   
   **En Linux/Mac:**
   ```bash
   mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS PMS54870695D CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
   mysql -u root -p PMS54870695D < dump.sql
   mysql -u root -p PMS54870695D < insert.sql
   ```

4. Verifica que la base de datos se haya creado correctamente:
   ```bash
   mysql -u root -p
   ```
   Luego ejecuta:
   ```sql
   USE PMS54870695D;
   SHOW TABLES;
   EXIT;
   ```

### PASO 2: Configurar y Lanzar el WebService

1. Abre una terminal y navega a la carpeta WebService:
   ```bash
   cd "C:\UIB\Solucions Turistiques\practica\SectorTuristic\WebService"
   ```

2. Instala las dependencias de Node.js (solo la primera vez):
   ```bash
   npm install
   ```
   Este comando instalará todas las librerías necesarias definidas en package.json.

3. Configura la conexión a la base de datos:
   
   Abre el archivo `.env` en la carpeta WebService y verifica/modifica:
   ```
   DATABASE_URL="mysql://root:tu_password@localhost:3306/PMS54870695D"
   PORT=3000
   ```
   Reemplaza `tu_password` con la contraseña de MySQL que configuraste.
   
   **IMPORTANTE**: El nombre de la base de datos debe ser **PMS54870695D** (PMS + NIF del alumno).

4. Sincroniza el esquema de base de datos con Prisma:
   ```bash
   npx prisma generate
   ```

5. Inicia el servidor:
   ```bash
   npm run dev
   ```

6. Si todo está correcto, verás:
   ```
   Servidor corriendo en http://localhost:3000
   Base de datos conectada
   ```

   **IMPORTANTE**: Mantén esta terminal abierta mientras uses el PMS. El WebService debe estar ejecutándose todo el tiempo.

### PASO 3: Configurar y Lanzar el PMS

1. Abre una **NUEVA** terminal (el WebService debe seguir ejecutándose en la otra)

2. Navega a la carpeta PMS:
   ```bash
   cd "C:\UIB\Solucions Turistiques\practica\SectorTuristic\PMS"
   ```

3. Instala las dependencias de Python (solo la primera vez):
   ```bash
   pip install -r requirements.txt
   ```
   
   Si usas Python 3 explícitamente:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. Verifica que el WebService esté corriendo:
   
   Abre tu navegador y visita: http://localhost:3000/api/hoteles
   
   Deberías ver una respuesta JSON con la lista de hoteles.

5. Inicia la aplicación PMS:
   ```bash
   python main.py
   ```
   
   O en algunos sistemas:
   ```bash
   python3 main.py
   ```

6. La interfaz gráfica del PMS se abrirá automáticamente.

### Resumen de Terminales Necesarias

Para que el sistema funcione completamente, necesitas tener abiertas:

**Terminal 1 - WebService:**
```bash
cd "C:\UIB\Solucions Turistiques\practica\SectorTuristic\WebService"
npm run dev
```

**Terminal 2 - PMS:**
```bash
cd "C:\UIB\Solucions Turistiques\practica\SectorTuristic\PMS"
python main.py
```

### Verificación del Sistema

Una vez todo esté ejecutándose, verifica:

1. **WebService**: http://localhost:3000/api/hoteles debe devolver datos
2. **Base de datos**: MySQL debe estar corriendo
3. **PMS**: La ventana gráfica debe aparecer con las pestañas Clientes, Reservas y Consultas

## Instalación Rápida (Para Desarrollo)

Si ya has configurado todo previamente y solo necesitas iniciar:

1. Inicia MySQL (si no está como servicio automático)
2. Terminal 1: `cd WebService && npm run dev`
3. Terminal 2: `cd PMS && python main.py`

## Guía de Uso

### Interfaz Principal

Al iniciar la aplicación, verás la ventana principal con 3 pestañas:

1. **Gestión de Clientes**
2. **Gestión de Reservas**
3. **Consultas Generales**

### 1. Gestión de Clientes

Permite:
- **Listar** todos los clientes
- **Buscar** clientes por nombre o apellido
- **Ver detalles** de un cliente específico
- **Crear** nuevos clientes
- **Modificar** datos de clientes existentes

**Ejemplo de creación de cliente:**
```
Nombre: María
Apellidos: García López
Email: maria.garcia@example.com
DNI: 12345678A
Fecha de nacimiento: 15/05/1990
```

### 2. Gestión de Reservas

Funcionalidades:
- **Listar** todas las reservas
- **Buscar** reservas por cliente
- **Ver detalles** de una reserva
- **Crear** nueva reserva (con consulta de disponibilidad)
- **Modificar** reserva existente
- **Cancelar** reserva
- **Crear contrato** para una reserva
- **Check-in** (registrar llegada del cliente)
- **Check-out** (registrar salida del cliente)

**Flujo completo de una reserva:**
1. Crear reserva → Consulta disponibilidad y crea la reserva
2. Crear contrato → Asigna habitación y monto
3. Check-in → Registra la llegada del cliente
4. Check-out → Registra la salida y finaliza la estancia

### 3. Consultas Generales

Permite consultar:
- **Hoteles** de la cadena (con detalles)
- **Tipos de habitación** disponibles
- **Regímenes** (SA, AD, MP, PC, TI)
- **Ciudades** donde opera la cadena
- **Disponibilidad** por fechas y ubicación
- **Contratos** activos y finalizados

## Características Técnicas

### Interfaz Amigable
- **Colores semánticos** para mejor legibilidad
- **Tablas formateadas** para visualización de datos
- **Mensajes de éxito/error** claros y descriptivos
- **Validaciones en tiempo real** de entrada de datos

### Validaciones
- Fechas en formato correcto (DD/MM/YYYY)
- Números enteros y decimales válidos
- Campos requeridos no vacíos
- Confirmaciones para acciones críticas (cancelar, eliminar)

### Manejo de Errores
- Conexión con WebService
- Errores de API (404, 409, 400, etc.)
- Validaciones de negocio
- Errores inesperados

## Configuración Avanzada

Edita `src/infrastructure/config.py` para cambiar:

```python
# URL del WebService
API_BASE_URL = "http://localhost:3000/api"

# Timeout de peticiones (segundos)
REQUEST_TIMEOUT = 10

# Formatos de fecha
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
```

## Ejemplos de Uso

### Crear una Reserva

1. Menú Principal → **2. Gestión de Reservas**
2. Seleccionar → **4. Crear nueva reserva**
3. Ingresar fechas:
   - Entrada: `01/12/2024`
   - Salida: `05/12/2024`
4. Ingresar ciudad: `Palma`
5. Ver hoteles disponibles
6. Seleccionar:
   - Hotel: `Gran Hotel del Mar`
   - Tipo: `Doble Superior`
   - Régimen: `AD`
7. Ingresar datos del cliente
8. Agregar huéspedes
9. Confirmar reserva

### Realizar Check-in

1. Menú Principal → **2. Gestión de Reservas**
2. Seleccionar → **7. Crear contrato**
   - ID Reserva: `1`
   - Habitación: `101`
   - Monto: (calculado automáticamente)
3. Seleccionar → **8. Realizar check-in**
   - ID Reserva: `1`
   - Habitación: `101`

## Solución de Problemas

### Error: "No se pudo conectar al WebService"

**Solución:**
1. Verifica que el WebService esté ejecutándose:
   ```bash
   cd ../WebService
   npm run dev
   ```
2. Verifica que esté en el puerto 3000
3. Comprueba la URL en `config.py`

### Error: "Import could not be resolved"

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: Fechas inválidas

**Solución:**
- Usa el formato `DD/MM/YYYY` (ejemplo: `25/12/2024`)
- Asegúrate de que la fecha de salida sea posterior a la de entrada

## Endpoints Utilizados

El PMS consume los siguientes endpoints del WebService:

| Módulo | Endpoint | Método |
|--------|----------|--------|
| Clientes | `/api/clientes` | GET, POST |
| Clientes | `/api/clientes/:id` | GET, PUT |
| Clientes | `/api/clientes/buscar` | GET |
| Reservas | `/api/reservas` | GET, POST |
| Reservas | `/api/reservas/:id` | GET, PUT, DELETE |
| Reservas | `/api/reservas/buscar/cliente` | GET |
| Reservas | `/api/reservas/:id/checkin` | POST |
| Contratos | `/api/contratos` | GET, POST |
| Contratos | `/api/contratos/:id` | GET |
| Contratos | `/api/contratos/:id/checkout` | PUT |
| Hoteles | `/api/hoteles` | GET |
| Hoteles | `/api/hoteles/:id` | GET |
| Hoteles | `/api/hoteles/:id/tiposHabitacion` | GET |
| Disponibilidad | `/api/disponibilidad` | GET |
| Tipos Habitación | `/api/tiposHabitacion` | GET |
| Regímenes | `/api/regimenes` | GET |
| Ciudades | `/api/ciudades` | GET |

## Uso Interno

Esta aplicación está diseñada para ser utilizada por:
- **Recepcionistas** de hoteles
- **Personal de Central de Reservas**
- **Gestores de la cadena hotelera**

## Licencia

Aplicación de uso interno - Cadena Hotelera

## Componentes Relacionados

- **WebService**: API REST en Node.js/Express/TypeScript (`../WebService`)
- **Base de Datos**: MySQL con esquema Prisma (`../BD`)

---

**Versión:** 1.0.0  
**Última actualización:** Noviembre 2025

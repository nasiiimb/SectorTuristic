# 🏨 PMS - Property Management System

Sistema de Gestión Hotelera con **Clean Architecture** y **Principios SOLID**

## 📋 Descripción

El PMS (Property Management System) es una aplicación de **escritorio moderna con interfaz gráfica** que permite a los empleados de la cadena hotelera (recepcionistas, personal de reservas, etc.) gestionar:

- **Clientes**: Altas, modificaciones, búsquedas y consultas
- **Reservas**: Crear, modificar, cancelar reservas, check-in/check-out
- **Operaciones**: Gestión de contratos y disponibilidad
- **Consultas**: Hoteles, tipos de habitación, regímenes, ciudades, contratos

## ✨ Características de la Interfaz Moderna

### 🎨 Diseño Profesional
- **Framework**: CustomTkinter 5.2.0 (Material Design-inspired)
- **Tema**: Dark mode profesional
- **Colores**: Paleta turquesa/verde azulado (#2B7A78)
- **Tipografía**: Fuentes modernas escalables
- **Componentes**: Botones redondeados, sombras, efectos hover
- **UX**: Layout responsive, tablas scrollables, selección por click

### 🖼️ Componentes Visuales
- **Main Window**: Header profesional con gradiente + Footer informativo
- **Tabs**: Sistema de pestañas moderno (Clientes, Reservas, Consultas)
- **Formularios**: Inputs con placeholders, validación visual
- **Tablas**: Filas alternadas, colores semánticos, auto-scroll
- **Botones**: Iconos emoji + colores por acción (verde=crear, azul=editar, rojo=eliminar)

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

## 🚀 Instalación

### Requisitos Previos

- **Python 3.9+** instalado
- **WebService** ejecutándose en `http://localhost:3000`
- **MySQL** con base de datos `pms_database`

### Paso 1: Instalar dependencias

Abre una terminal en la carpeta `PMS` y ejecuta:

```bash
pip install -r requirements.txt
```

Esto instalará:
- `requests==2.31.0` - Para peticiones HTTP al WebService
- `colorama==0.4.6` - Para colores en consola
- `tabulate==0.9.0` - Para tablas formateadas
- `python-dateutil==2.8.2` - Para manejo de fechas
- `customtkinter==5.2.0` - Framework moderno de UI
- `Pillow==10.0.0` - Soporte de imágenes para CustomTkinter
- `setuptools` - Herramientas de empaquetado Python

### Paso 2: Verificar que el WebService esté corriendo

Antes de ejecutar el PMS, asegúrate de que el WebService esté activo:

```bash
# En otra terminal, navega a la carpeta WebService
cd ../WebService

# Ejecuta el servidor
npm run dev
```

Deberías ver:
```
🚀 Servidor corriendo en http://localhost:3000
```

## ▶️ Ejecución

```bash
python main.py
```

O en algunos sistemas:

```bash
python3 main.py
```

## 📖 Guía de Uso

### Menú Principal

Al iniciar la aplicación, verás el menú principal con 3 opciones:

1. **👤 Gestión de Clientes**
2. **📅 Gestión de Reservas**
3. **📊 Consultas Generales**

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

## 🎨 Características

### Interfaz Amigable
- 🎨 **Colores** para mejor legibilidad
- 📊 **Tablas formateadas** para datos
- ✓ **Mensajes de éxito/error** claros
- ⚠️ **Validaciones** de entrada

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

## 🔧 Configuración

Edita `config.py` para cambiar:

```python
# URL del WebService
API_BASE_URL = "http://localhost:3000/api"

# Timeout de peticiones (segundos)
REQUEST_TIMEOUT = 10

# Formatos de fecha
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
```

## 📝 Ejemplos de Uso

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

## 🐛 Solución de Problemas

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

## 📚 Endpoints Utilizados

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

## 👥 Uso Interno

Esta aplicación está diseñada para ser utilizada por:
- **Recepcionistas** de hoteles
- **Personal de Central de Reservas**
- **Gestores de la cadena hotelera**

## 📄 Licencia

Aplicación de uso interno - Cadena Hotelera

## 🔗 Relacionado

- **WebService**: API REST en Node.js/Express (`../WebService`)
- **Base de Datos**: MySQL (`../BD`)

---

**Versión:** 1.0.0  
**Última actualización:** Octubre 2025

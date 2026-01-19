# PaginaWEB - Frontend del Sistema de Reservas

Frontend en PHP para el sistema de reservas hoteleras. Diseño profesional y moderno inspirado en portales hoteleros como Meliá.

## Contenido

- `index.php` - Página principal con Hero Section y buscador
- `resultados.php` - Listado de habitaciones disponibles con imágenes
- `auth.php` - Inicio de sesión
- `registro.php` - Registro de nuevos usuarios
- `confirmar.php` - Confirmación y resumen de reserva
- `config.php` - Configuración y funciones auxiliares
- `style.css` - Estilos CSS profesionales y responsive
- `API_GUIDE.md` - Documentación de la API del WebService

## Requisitos

- PHP 7.4 o superior
- Extensión cURL habilitada
- WebService ejecutándose en `http://localhost:3000`
- Base de datos MySQL con las tablas actualizadas

## Instalación

### 1. Actualizar Base de Datos

Ejecuta los scripts SQL actualizados:

```bash
# Desde la carpeta BD
mysql -u root -p < dump.sql
mysql -u root -p < insert.sql
```

Los cambios incluyen:
- Campo `foto_url` en `TipoHabitacion`
- Campos `email` y `password` en `Cliente`

### 2. Iniciar WebService

```bash
cd ../WebService
npm install
npm run dev
```

El WebService debe estar corriendo en `http://localhost:3000`

### 3. Configurar Servidor Web

Puedes usar cualquiera de estas opciones:

#### Opción A: PHP Built-in Server (Desarrollo)
```bash
cd PaginaWEB
php -S localhost:8000
```

Luego abre: `http://localhost:8000`

#### Opción B: XAMPP / WAMP
1. Copia la carpeta `PaginaWEB` a `htdocs` (XAMPP) o `www` (WAMP)
2. Abre: `http://localhost/PaginaWEB`

#### Opción C: Apache/Nginx
Configura un VirtualHost apuntando a la carpeta `PaginaWEB`

## Características de Diseño

### Hero Section
- Imagen de fondo full-width
- Título y descripción centrados
- Buscador flotante con diseño horizontal

### Buscador
- Campos: Destino, Fecha Entrada, Fecha Salida
- Validación de fechas en cliente
- Búsqueda por ciudad

### Tarjetas de Habitaciones
- **Imagen grande** de la habitación (campo `foto_url`)
- Información del hotel (nombre y estrellas)
- Categoría de habitación
- Características (camas)
- Precio destacado
- Botón de reserva

### Responsive
- Adaptado para móvil y escritorio
- Grid flexible
- Navegación mobile-friendly

## Autenticación

### Registro
- Nombre, Apellidos, Email, DNI obligatorios
- Fecha de nacimiento opcional
- Password hasheado con `password_hash()`
- Validación de email único y DNI único

### Login
- Email y contraseña
- Verificación con `password_verify()`
- Sesión persistente

### Reservas sin Login
Si un usuario intenta reservar sin estar logueado:
1. Se guardan los datos en sesión
2. Se redirige al login
3. Tras login exitoso, se redirige a confirmar reserva

## Flujo de Usuario

1. **Búsqueda** (`index.php`)
   - Usuario ingresa destino y fechas
   - Clic en "Buscar"

2. **Resultados** (`resultados.php`)
   - Se muestran habitaciones disponibles con **FOTOS**
   - Cada tarjeta muestra: hotel, categoría, precio
   - Clic en "Reservar"

3. **Confirmación** (`confirmar.php`)
   - Si no está logueado → redirige a `auth.php`
   - Muestra resumen de la reserva
   - Informa que el pago es en el hotel
   - Clic en "Confirmar Reserva"

4. **Reserva Creada**
   - Se crea la reserva en el backend
   - Se muestra número de confirmación
   - Se puede volver al inicio

## Endpoints del WebService Utilizados

### Disponibilidad
```
GET /api/disponibilidad?ciudad=Palma&fechaEntrada=2025-12-01&fechaSalida=2025-12-05
```
Retorna hoteles con habitaciones disponibles, incluyendo `foto_url`

### Clientes
```
POST /api/clientes
```
Crea un nuevo cliente (registro)

```
GET /api/clientes?correoElectronico=email@example.com
```
Busca cliente por email (login)

### Reservas
```
POST /api/reservas
```
Crea una nueva reserva

## Configuración

En `config.php` puedes modificar:

```php
// URL del WebService
define('API_BASE_URL', 'http://localhost:3000/api');
```

## Estructura de Datos

### Sesión de Usuario
```php
$_SESSION['user'] = [
    'idCliente' => 1,
    'nombre' => 'Juan',
    'apellidos' => 'Pérez',
    'email' => 'juan@example.com'
];
```

### Datos de Reserva Pendiente
```php
$_SESSION['pending_reservation'] = [
    'idHotel' => 1,
    'idTipoHabitacion' => 2,
    'fechaEntrada' => '2025-12-01',
    'fechaSalida' => '2025-12-05',
    'precioTotal' => 400.00,
    // ...
];
```

## Personalización de Estilos

En `style.css` puedes modificar las variables CSS:

```css
:root {
    --primary-color: #2c3e50;      /* Color principal */
    --secondary-color: #3498db;    /* Color secundario (botones) */
    --accent-color: #e74c3c;       /* Color de acento (reservar) */
}
```

## Notas Importantes

1. **Pago**: No hay pasarela de pago. Todo se paga en el hotel.
2. **Imágenes**: Las URLs de las fotos vienen de la base de datos (campo `foto_url`)
3. **Seguridad**: 
   - Passwords hasheados con `password_hash()`
   - Escape de HTML con `htmlspecialchars()`
   - Validación en cliente y servidor

## Solución de Problemas

### Error: "No se puede conectar con el servidor"
- Verifica que el WebService esté corriendo en `http://localhost:3000`
- Revisa que cURL esté habilitado en PHP

### Error: "Campo foto_url desconocido"
- Ejecuta los scripts SQL actualizados
- Verifica que la columna `foto_url` existe en `TipoHabitacion`

### Las imágenes no se muestran
- Verifica que las URLs en `foto_url` sean válidas
- Si usas rutas locales, asegúrate de tener las imágenes en el servidor

## Próximas Mejoras

- [ ] Panel de "Mis Reservas"
- [ ] Cancelación de reservas
- [ ] Filtros adicionales (precio, estrellas)
- [ ] Sistema de valoraciones
- [ ] Newsletter

## Licencia

Sector Turístico © 2025

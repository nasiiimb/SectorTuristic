# Rol
Actúa como un Desarrollador Senior Full Stack PHP con experiencia en UI/UX.

# Contexto y Estructura del Proyecto
Estoy trabajando en un sistema de reservas existente con la siguiente estructura de carpetas:
- `/SECTORTURISTIC` (Raíz del proyecto)
  - `/BD`: Contiene el archivo **`dump.sql`**.
  - `/WebService`: Contiene el API Backend (existente).
  - `/PaginaWeb`: Carpeta destinada al Frontend (donde está este archivo y `API_GUIDE.md`).
  - `prompt.md`: Este archivo.

# Objetivo Principal
1.  Actualizar la estructura de datos (`dump.sql`) para soportar usuarios y **fotos de habitaciones**.
2.  Actualizar el Backend (`/WebService`) para autenticación y envío de imágenes.
3.  Crear un Frontend en `/PaginaWeb` con un diseño **profesional, visual y atractivo**, inspirado en portales hoteleros modernos (tipo Meliá).

# Requisitos de Diseño (UI/UX) - IMPORTANTE
El diseño no puede ser básico. Debe lucir profesional:
- **Estilo:** Minimalista, elegante, uso de espacios en blanco (whitespace), tipografía sans-serif limpia (como Roboto o Open Sans).
- **Home (`index.php`):**
    - Debe tener un **"Hero Section"** (una imagen grande de fondo que ocupe la parte superior).
    - **Barra de Búsqueda:** Flotando sobre la imagen o justo debajo, una barra horizontal blanca que contenga: "Entrada", "Salida", "Habitaciones/Personas" y el botón "Buscar".
    - **No incluir:** No pongas opciones de "Vuelo + Hotel" ni "Código de descuento". Solo reserva de hotel pura.
- **Resultados (`resultados.php`):**
    - Las habitaciones deben mostrarse en "Tarjetas" (Cards) con sombra suave.
    - Cada tarjeta debe mostrar: **FOTO de la habitación** (grande), Título, Descripción breve y Precio destacado.
- **Responsive:** La web debe verse bien en móvil y escritorio.
- **CSS:** Usa un archivo `style.css` bien estructurado o estilos en línea organizados si es poco código.

# Tareas a realizar (Paso a Paso)

## 1. Actualización Base de Datos (Archivo `/BD/dump.sql`)
Modifica el código SQL en `dump.sql`:
1.  **Tabla `cliente`:** Añade columnas `email` (UNIQUE) y `password` (VARCHAR).
2.  **Tabla de Habitaciones (o `tipo_habitacion`):** Busca la tabla donde se definen los tipos de habitación y añade una columna `foto_url` (VARCHAR) para guardar la ruta de la imagen.
3.  **Datos de prueba:** En los `INSERT` de habitaciones, añade rutas de ejemplo (ej: `../WebService/img/habitacion_standard.jpg` o usa placeholder urls como `https://placehold.co/600x400` para que se vea algo al probar).

## 2. Refactorización Web Service (Carpeta `/WebService`)
- **Endpoint Disponibilidad:** Modifica la respuesta JSON para que incluya el campo `foto_url` de cada habitación encontrada.
- **Endpoint Registro:** Crea lógica para registrar usuarios (hash password).
- **Endpoint Reserva:** Valida email/password y crea la reserva sin pedir pago (pago en hotel).

## 3. Actualización Documentación (`/PaginaWeb/API_GUIDE.md`)
Actualiza los esquemas JSON en la documentación:
- El JSON de respuesta de disponibilidad ahora debe mostrar el campo de la imagen.

## 4. Desarrollo Frontend (Carpeta `/PaginaWeb`)
Desarrolla las páginas PHP consumiendo el WS.

- **`index.php`:** Portada con el diseño "Hero" y buscador horizontal descrito arriba.
- **`resultados.php`:** Lista de tarjetas con **IMÁGENES**.
    - Al pintar la habitación, usa la URL que viene del JSON en una etiqueta `<img>`.
- **`auth.php` y `registro.php`:** Formularios limpios y centrados para Login/Registro.
- **`confirmar.php`:** Muestra resumen y confirmación.
    - **Nota:** No hay pasarela de pago. Al confirmar, la reserva queda hecha directamente.

# Entregables
Dame el código en bloques separados, indicando claramente el nombre del archivo y la ruta donde debe guardarse. Empieza por el SQL.
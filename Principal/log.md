# Registro de Desarrollo - Principal

> **Última actualización**: 22 de Diciembre de 2025

## Rol: Arquitecto de Software y Desarrollador Full Stack (Node/Vue)

## Contexto del Proyecto
Estamos en la fase final. Tienes acceso a todo el código actual.
Vamos a crear un nuevo sistema centralizado llamado *"Principal"* (un Booking Engine). Este sistema actuará como un orquestador que unifica la oferta de dos proveedores distintos:
1.  */WebService* (Proveedor externo simulado).
2.  */Channel* (Proveedor interno).

El objetivo es que un usuario se loguee en Principal, busque disponibilidad (fusionada de ambos orígenes) y realice reservas.

---

## Requisitos Técnicos Globales
* *Backend Principal:* Node.js (Servidor nuevo).
* *Frontend Principal:* Vue.js (SPA nueva).
* *Base de Datos Principal:* MySQL (Nueva base de datos para usuarios y registros de reservas propias).
* *Estilo Visual:* Debe replicar el diseño y flujo de usuario (embudo de conversión) que existe actualmente en /PaginaWeb (aunque esa esté en PHP, migraremos el concepto visual a Vue).

---

## Tareas por Módulo (Paso a Paso)

### 1. Modificaciones en el Proveedor /WebService (Prioridad Alta)
Actualmente, el WebService procesa reservas pero no devuelve un identificador.
* *Base de Datos (/BD):* Modifica el schema.prisma (o estructura SQL) usado por el WebService. Añade un campo localizador (String/Varchar, Unique) a la tabla de Reservas.
    * IMPORTANTE: Esta BD es compartida con el módulo /PMS. Asegúrate de que el cambio en la tabla (ej. hacer el campo nullable inicialmente o con default) *no rompa* el funcionamiento actual del PMS.
* *Endpoint de Reserva:* Modifica el endpoint documentado en /WebService/ApiDocumentation.md.
    * Genera un código alfanumérico único al crear la reserva.
    * Guárdalo en la BD.
    * *Devuelve* este localizador en el JSON de respuesta.

### 2. Modificaciones en el Proveedor /Channel
* *Nuevo Endpoint:* Crea un endpoint REST (ej: POST /api/reserve) en el servidor del Channel.
* *Lógica:*
    * Recibe ID de habitación y fechas.
    * Verifica disponibilidad en su propia BD.
    * Resta disponibilidad (Stock - 1).
    * Devuelve un localizador generado internamente o el ID de la transacción.

### 3. Backend de Principal (Node.js + MySQL)
Crea un servidor nuevo que orqueste todo:
* *Base de Datos:* Configura una conexión MySQL para Principal. Necesitarás tablas para:
    * Usuarios (Login/Registro).
    * Reservas (Para guardar: ID Usuario, Localizador externo, Origen ['WebService'|'Channel'], Estado, Fechas, Precio).
* *Endpoint GET /search:*
    * Recibe fechas y pax.
    * Ejecuta en paralelo:
        1.  Llamada HTTP a /WebService (endpoint disponibilidad).
        2.  Consulta SQL directa a la BD de /Channel (para obtener disponibilidad).
    * Unifica los resultados en un array común y lo devuelve al front.
* *Endpoint POST /book:*
    * Recibe datos del usuario y la habitación seleccionada.
    * *Si el origen es WebService:* Llama al endpoint del WebService -> Obtiene localizador -> Guarda registro en BD Principal.
    * *Si el origen es Channel:* Llama al nuevo endpoint del Channel -> Obtiene confirmación -> Guarda registro en BD Principal.

### 4. Frontend de Principal (Vue.js)
Basándote en la UX de /PaginaWeb:
* *Home:* Buscador de fechas (Check-in/Check-out) y Pax.
* *Resultados:* Lista unificada de habitaciones (mezclando WS y Channel). Muestra fotos, descripción y precio.
* *Reservar:*
    * Requiere Login previo.
    * Al pulsar "Reservar", llama a Principal POST /book.
    * Muestra pantalla de confirmación con el *Localizador* obtenido.

---

## Instrucciones de Ejecución
1.  Realiza primero los cambios en la BD y el código del /WebService (verificando que /PMS sigue compilando/funcionando).
2.  Implementa el endpoint de reserva en /Channel.
3.  Levanta el Backend de /Principal con su conexión a MySQL.
4.  Desarrolla el Frontend en Vue.js.

Empieza analizando el archivo /WebService/ApiDocumentation.md para entender qué debemos modificar.
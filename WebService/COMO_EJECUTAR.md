# Cómo Ejecutar el WebService

## Requisitos Previos

- Node.js (versión 16 o superior)
- MySQL (versión 8.0 o superior)

## Pasos para Ejecutar

### 1. Instalar Dependencias

```bash
npm install
```

### 2. Configurar Base de Datos

Crea un archivo `.env` en la carpeta `WebService`:

```env
DATABASE_URL="mysql://pms_user:pms_password123@localhost:3306/pms_database"
PORT=3000
NODE_ENV=development
```

### 3. Generar Cliente de Prisma

```bash
npm run prisma:generate
```

### 4. Ejecutar el Servidor

```bash
npm run dev
```

El servidor estará disponible en `http://localhost:3000`

## Verificar que Funciona

Abre tu navegador y visita:
```
http://localhost:3000/api/hoteles
```

## Comandos Útiles

- `npm run dev` - Ejecutar en modo desarrollo
- `npm run prisma:studio` - Ver/editar datos en interfaz gráfica (localhost:5555)

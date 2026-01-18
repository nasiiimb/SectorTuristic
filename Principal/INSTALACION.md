# Guía de Instalación y Ejecución - Principal

## Instalación Rápida

### 1. Configurar Base de Datos
```bash
# Crear la base de datos MySQL
mysql -u root -p < database/setup.sql
```

### 2. Configurar Variables de Entorno
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
notepad .env
```

### 3. Instalar Dependencias

#### Backend
```bash
cd backend
npm install
npm run build
```

#### Frontend
```bash
cd frontend
npm install
npm run build
```

## Ejecución en Desarrollo

### Modo desarrollo (con hot-reload)
```bash
# En una terminal - Backend
cd backend
npm run dev

# En otra terminal - Frontend
cd frontend
npm run dev
```

El frontend estará disponible en: http://localhost:5173
El backend estará disponible en: http://localhost:3002

## Notas Importantes

- Asegúrate de que WebService (puerto 3000) y Channel (puerto 8001) estén funcionando
- La base de datos MySQL debe estar corriendo en el puerto 3306
- Revisa los logs en caso de errores de conexión

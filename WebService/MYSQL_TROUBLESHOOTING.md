# Solución a problemas comunes de conexión con MySQL

## Error: "Unknown authentication plugin 'auth_gssapi_client'"

Este error ocurre cuando hay un problema con el método de autenticación de MySQL. Aquí hay varias soluciones:

### Solución 1: Actualizar el string de conexión

Modifica tu archivo `.env` para incluir parámetros adicionales:

```env
DATABASE_URL="mysql://pms_user:pms_password123@localhost:3306/pms_database?sslaccept=strict"
```

O para desarrollo local sin SSL:

```env
DATABASE_URL="mysql://pms_user:pms_password123@localhost:3306/pms_database?sslmode=disable"
```

### Solución 2: Cambiar el plugin de autenticación en MySQL

Si tienes acceso a MySQL como administrador, ejecuta estos comandos:

```sql
-- Conectarse como root
mysql -u root -p

-- Cambiar el plugin de autenticación del usuario
ALTER USER 'pms_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pms_password123';
FLUSH PRIVILEGES;
```

### Solución 3: Crear el usuario correctamente

Si necesitas crear el usuario desde cero:

```sql
-- Conectarse como root
mysql -u root -p

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS pms_database;

-- Crear el usuario con el plugin correcto
CREATE USER IF NOT EXISTS 'pms_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'pms_password123';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON pms_database.* TO 'pms_user'@'localhost';
FLUSH PRIVILEGES;
```

### Solución 4: Verificar la instalación de MySQL

Asegúrate de que tienes MySQL instalado y corriendo:

```bash
# En Windows PowerShell
Get-Service MySQL*

# Para iniciar el servicio si está detenido
Start-Service MySQL80  # o el nombre de tu servicio MySQL
```

### Solución 5: Usar XAMPP o WAMP

Si estás usando XAMPP o WAMP:

1. Abre el Panel de Control de XAMPP/WAMP
2. Inicia el servicio MySQL
3. Abre phpMyAdmin
4. Ve a la pestaña "Cuentas de usuario"
5. Edita el usuario `pms_user` y cambia el plugin de autenticación a `mysql_native_password`

## Verificar la conexión

Después de aplicar cualquiera de las soluciones, prueba la conexión:

```bash
# Generar el cliente de Prisma
npm run prisma:generate

# Sincronizar con la base de datos (opcional si la BD ya existe)
npm run prisma:db:push

# O simplemente ejecuta tu aplicación
npm run dev
```

## Crear las tablas desde cero

Si tu base de datos está vacía y quieres crear todas las tablas:

### Opción 1: Usar el archivo SQL existente
```bash
# Navega a la carpeta BD
cd "c:\UIB\Solucions Turistiques\practica\SectorTuristic\BD"

# Ejecuta el script .bat
crear_bd.bat
```

### Opción 2: Usar Prisma para crear las tablas
```bash
# Este comando creará las tablas basándose en tu schema.prisma
npm run prisma:push
```

## Prisma Studio

Una vez que la conexión funcione, puedes usar Prisma Studio para explorar tus datos:

```bash
npm run prisma:studio
```

Esto abrirá una interfaz web en `http://localhost:5555`

## Contacto adicional

Si sigues teniendo problemas:

1. Verifica que MySQL esté instalado y corriendo
2. Verifica que el usuario y contraseña en `.env` sean correctos
3. Verifica que la base de datos `pms_database` exista
4. Intenta conectarte manualmente con un cliente MySQL para descartar problemas de red/firewall

# 📋 Resumen de Correcciones de Codificación

## ✅ Archivos Modificados

### 1. `crear_bd.bat` (ACTUALIZADO)
**Cambios:**
- ✅ Ahora crea la BD con: `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`
- ✅ Usa `--default-character-set=utf8mb4` en conexiones MySQL

**Antes:**
```batch
mysql -u %DB_USER% -p%DB_PASS% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"
```

**Después:**
```batch
mysql -u %DB_USER% -p%DB_PASS% --default-character-set=utf8mb4 -e "CREATE DATABASE IF NOT EXISTS %DB_NAME% CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
```

---

### 2. `dump.sql` (ACTUALIZADO)
**Cambios:**
- ✅ Añadidas directivas de codificación al inicio
- ✅ Versión actualizada a 2.3

**Añadido al inicio:**
```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;
```

---

### 3. `insert.sql` (ACTUALIZADO)
**Cambios:**
- ✅ Añadidas directivas de codificación al inicio

**Añadido al inicio:**
```sql
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;
SET character_set_connection=utf8mb4;
```

---

### 4. `WebService/.env` (ACTUALIZADO)
**Cambios:**
- ✅ Añadido parámetro `charset=utf8mb4` a la URL de conexión

**Antes:**
```
DATABASE_URL="mysql://pms_user:pms_password123@localhost:3306/pms_database"
```

**Después:**
```
DATABASE_URL="mysql://pms_user:pms_password123@localhost:3306/pms_database?charset=utf8mb4"
```

---

## 📝 Archivos Nuevos

### 5. `fix_encoding.sql` (NUEVO)
Script SQL para convertir una base de datos existente a UTF-8.

**Contenido:**
- Convierte la base de datos a utf8mb4
- Convierte todas las 21 tablas a utf8mb4
- Muestra mensaje de confirmación

---

### 6. `fix_encoding.bat` (NUEVO)
Script batch para ejecutar fácilmente la corrección de codificación.

**Uso:**
```bash
fix_encoding.bat
```

---

### 7. `README_ENCODING.md` (NUEVO)
Documentación completa sobre:
- El problema de codificación
- Cómo solucionarlo (2 opciones)
- Cómo verificar que está corregido
- Información técnica sobre UTF-8

---

## 🎯 Instrucciones de Uso

### Si aún NO has creado la base de datos:
```bash
cd BD
crear_bd.bat
```
✅ ¡Listo! La BD se creará con UTF-8 correctamente.

### Si YA tienes la base de datos creada:
```bash
cd BD
fix_encoding.bat
```
✅ Convertirá la BD existente a UTF-8 sin perder datos.

---

## 🧪 Prueba que Funciona

Después de aplicar las correcciones, prueba insertar datos con caracteres especiales:

```sql
USE pms_database;

INSERT INTO Ciudad (nombre, pais) VALUES 
('Málaga', 'España'),
('A Coruña', 'España'),
('Cáceres', 'España'),
('Ávila', 'España');

-- Consulta para verificar
SELECT * FROM Ciudad WHERE pais = 'España';
```

**Resultado esperado:**
Los caracteres especiales (á, ñ, ó, etc.) deben mostrarse correctamente.

---

## ⚠️ Notas Importantes

1. **utf8mb4** es mejor que **utf8** en MySQL:
   - `utf8` en MySQL solo soporta 3 bytes (incompleto)
   - `utf8mb4` soporta 4 bytes (UTF-8 completo, incluyendo emojis)

2. **Prisma** ahora usará UTF-8 automáticamente gracias al cambio en `.env`

3. **No perderás datos** al usar `fix_encoding.bat` en una BD existente

---

## 📊 Verificación

Para verificar que todo está correcto, ejecuta en MySQL:

```sql
-- Ver codificación de la BD
SHOW CREATE DATABASE pms_database;

-- Ver codificación de las tablas
SHOW TABLE STATUS FROM pms_database;

-- Ver variables del sistema
SHOW VARIABLES LIKE 'char%';
```

**Deberías ver `utf8mb4` en todos los resultados.**

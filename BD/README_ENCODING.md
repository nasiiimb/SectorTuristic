# 🔧 Corrección de Codificación de Base de Datos

## Problema
La base de datos MySQL puede tener problemas con caracteres especiales en español (ñ, á, é, í, ó, ú, ü) si no se configura correctamente la codificación UTF-8.

## Solución

### ✅ Opción 1: Crear la base de datos desde cero (RECOMENDADO)

Si aún no tienes datos importantes en la base de datos, simplemente ejecuta:

```bash
crear_bd.bat
```

Este script ahora **crea automáticamente** la base de datos con codificación UTF-8 (utf8mb4).

### 🔄 Opción 2: Corregir una base de datos existente

Si ya tienes la base de datos creada y con datos, ejecuta:

```bash
fix_encoding.bat
```

Este script **convertirá** todas las tablas existentes a UTF-8 sin perder datos.

## Cambios Realizados

### 1. `crear_bd.bat` - Mejorado
- ✅ Ahora crea la base de datos con `CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`
- ✅ Usa `--default-character-set=utf8mb4` en todas las conexiones MySQL

### 2. `dump.sql` - Actualizado
- ✅ Incluye `SET NAMES utf8mb4` al inicio
- ✅ Versión actualizada a 2.3

### 3. `insert.sql` - Actualizado
- ✅ Incluye `SET NAMES utf8mb4` al inicio

### 4. `fix_encoding.sql` - NUEVO
- ✅ Script para convertir todas las tablas a UTF-8
- ✅ Convierte la base de datos y todas las tablas

### 5. `fix_encoding.bat` - NUEVO
- ✅ Ejecuta automáticamente la corrección de codificación

## Verificar la Codificación

Puedes verificar que la codificación está correcta ejecutando en MySQL:

```sql
-- Ver codificación de la base de datos
SHOW CREATE DATABASE pms_database;

-- Ver codificación de una tabla específica
SHOW CREATE TABLE Cliente;

-- Ver todas las variables de codificación
SHOW VARIABLES LIKE 'character_set%';
```

Deberías ver `utf8mb4` en todos los resultados.

## Probar con Caracteres Especiales

Después de la corrección, prueba insertar datos con caracteres especiales:

```sql
INSERT INTO Ciudad (nombre, pais) VALUES 
('Málaga', 'España'),
('A Coruña', 'España');

-- Debería funcionar sin problemas con ñ, á, ó, ü, etc.
```

## ℹ️ Información Técnica

**utf8mb4** es la implementación completa de UTF-8 en MySQL que:
- ✅ Soporta todos los caracteres Unicode (incluyendo emojis)
- ✅ Es compatible con caracteres especiales del español
- ✅ Es el estándar recomendado por MySQL desde la versión 8.0

**utf8mb4_unicode_ci** es un collation que:
- ✅ Hace comparaciones case-insensitive (no distingue mayúsculas/minúsculas)
- ✅ Soporta correctamente la ordenación de caracteres especiales en español

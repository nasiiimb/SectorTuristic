@ECHO OFF
:: -----------------------------------------
:: Script para crear y poblar la base de datos PMS
:: -----------------------------------------

:: --- Configuración ---
SET DB_NAME=PMS54870695D
SET DB_USER=root
SET SCHEMA_FILE=dump.sql
SET DATA_FILE=insert.sql

:: --- Lógica del Script ---
ECHO --- Iniciando la creacion de la base de datos ---

:: 1. Crea la base de datos y el esquema
ECHO -> Creando la base de datos '%DB_NAME%' y el esquema...
mysql -u %DB_USER% -p --default-character-set=utf8mb4 -e "CREATE DATABASE IF NOT EXISTS %DB_NAME% CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
mysql -u %DB_USER% -p --default-character-set=utf8mb4 %DB_NAME% < %SCHEMA_FILE%
ECHO Esquema creado con exito.

:: 2. Inserta los datos de ejemplo
ECHO -> Insertando datos de ejemplo...
mysql -u %DB_USER% -p --default-character-set=utf8mb4 %DB_NAME% < %DATA_FILE%
ECHO Datos insertados con exito.

ECHO --- ✅ Proceso completado ---
PAUSE
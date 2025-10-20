@ECHO OFF
:: -----------------------------------------
:: Script para crear y poblar la base de datos PMS
:: -----------------------------------------

:: --- Configuración ---
SET DB_NAME=pms_database
SET DB_USER=pms_user
SET DB_PASS=pms_password123
SET SCHEMA_FILE=dump.sql
SET DATA_FILE=insert.sql

:: --- Lógica del Script ---
ECHO --- Iniciando la creacion de la base de datos ---

:: 1. Crea la base de datos y el esquema
ECHO -> Creando la base de datos '%DB_NAME%' y el esquema...
mysql -u %DB_USER% -p%DB_PASS% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%;"
mysql -u %DB_USER% -p%DB_PASS% %DB_NAME% < %SCHEMA_FILE%
ECHO Esquema creado con exito.

:: 2. Inserta los datos de ejemplo
ECHO -> Insertando datos de ejemplo...
mysql -u %DB_USER% -p%DB_PASS% %DB_NAME% < %DATA_FILE%
ECHO Datos insertados con exito.

ECHO --- ✅ Proceso completado ---
PAUSE
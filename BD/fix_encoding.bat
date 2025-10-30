@ECHO OFF
:: -----------------------------------------
:: Script para corregir la codificación de una base de datos existente
:: Usar este script si la base de datos ya fue creada sin UTF-8
:: -----------------------------------------

:: --- Configuración ---
SET DB_NAME=pms_database
SET DB_USER=pms_user
SET DB_PASS=pms_password123
SET FIX_FILE=fix_encoding.sql

:: --- Lógica del Script ---
ECHO --- Corrigiendo la codificacion de la base de datos ---

ECHO -> Aplicando correccion de UTF-8 a la base de datos '%DB_NAME%'...
mysql -u %DB_USER% -p%DB_PASS% --default-character-set=utf8mb4 %DB_NAME% < %FIX_FILE%

IF %ERRORLEVEL% EQU 0 (
    ECHO --- ✅ Codificacion corregida exitosamente ---
) ELSE (
    ECHO --- ❌ Error al corregir la codificacion ---
)

PAUSE

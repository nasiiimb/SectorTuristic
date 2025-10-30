@ECHO OFF
:: -----------------------------------------
:: Script para corregir datos mal codificados
:: -----------------------------------------

:: --- Configuración ---
SET DB_NAME=pms_database
SET DB_USER=pms_user
SET DB_PASS=pms_password123
SET FIX_FILE=fix_data.sql

:: --- Lógica del Script ---
ECHO --- Corrigiendo datos mal codificados ---

ECHO -> Aplicando correcciones a los datos...
mysql -u %DB_USER% -p%DB_PASS% --default-character-set=utf8mb4 %DB_NAME% < %FIX_FILE%

IF %ERRORLEVEL% EQU 0 (
    ECHO --- ✅ Datos corregidos exitosamente ---
) ELSE (
    ECHO --- ❌ Error al corregir los datos ---
)

PAUSE

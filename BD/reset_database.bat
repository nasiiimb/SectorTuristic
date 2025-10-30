@ECHO OFF
:: -----------------------------------------
:: Script para resetear la base de datos
:: -----------------------------------------

SET DB_NAME=pms_database
SET DB_USER=pms_user
SET DB_PASS=pms_password123
SET RESET_FILE=reset_database.sql

ECHO =====================================================
ECHO   RESETEANDO BASE DE DATOS
ECHO =====================================================
ECHO.
ECHO Este script va a:
ECHO   - Borrar TODOS los datos existentes
ECHO   - Reinsertar datos iniciales limpios
ECHO.
ECHO ADVERTENCIA: Se perderan todos los datos actuales
ECHO.
PAUSE
ECHO.

ECHO -> Limpiando y reinsertando datos...
mysql -u %DB_USER% -p%DB_PASS% --default-character-set=utf8mb4 %DB_NAME% < %RESET_FILE%

IF %ERRORLEVEL% EQU 0 (
    ECHO.
    ECHO =====================================================
    ECHO   OK BASE DE DATOS RESETEADA
    ECHO =====================================================
) ELSE (
    ECHO.
    ECHO =====================================================
    ECHO   ERROR AL RESETEAR BASE DE DATOS
    ECHO =====================================================
)

ECHO.
PAUSE

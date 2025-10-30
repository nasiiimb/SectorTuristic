@ECHO OFF
:: -----------------------------------------
:: Script para ejecutar operaciones de prueba
:: -----------------------------------------

:: --- Configuración ---
SET DB_NAME=pms_database
SET DB_USER=pms_user
SET DB_PASS=pms_password123
SET TEST_FILE=test_operaciones.sql

:: --- Lógica del Script ---
ECHO =====================================================
ECHO   EJECUTANDO OPERACIONES DE PRUEBA DEL HOTEL
ECHO =====================================================
ECHO.
ECHO Este script va a:
ECHO   - Crear 14 clientes nuevos
ECHO   - Crear 10 reservas distintas
ECHO   - Hacer 5 check-ins
ECHO   - Hacer 3 check-outs
ECHO.
ECHO Presione cualquier tecla para continuar...
PAUSE > NUL
ECHO.

ECHO -> Ejecutando operaciones...
mysql -u %DB_USER% -p%DB_PASS% --default-character-set=utf8mb4 %DB_NAME% < %TEST_FILE%

IF %ERRORLEVEL% EQU 0 (
    ECHO.
    ECHO =====================================================
    ECHO   ✅ OPERACIONES COMPLETADAS EXITOSAMENTE
    ECHO =====================================================
) ELSE (
    ECHO.
    ECHO =====================================================
    ECHO   ❌ ERROR AL EJECUTAR OPERACIONES
    ECHO =====================================================
)

ECHO.
PAUSE

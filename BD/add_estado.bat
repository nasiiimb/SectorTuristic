@echo off
REM Script para añadir el campo estado a la tabla Reserva
REM Ejecutar desde la carpeta BD

echo Añadiendo campo 'estado' a la tabla Reserva...
mysql -u pms_user -ppms_password123 pms_database < add_estado_reserva.sql

if %errorlevel% equ 0 (
    echo.
    echo ✓ Campo 'estado' añadido correctamente
    echo.
) else (
    echo.
    echo ✗ Error al ejecutar el script SQL
    echo.
)

pause

#!/bin/bash
# Script para crear ZIP del proyecto SectorTuristic
# Incluye exportacion de la base de datos PMS54870695D
# Fecha: Noviembre 2025

# Colores
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
WHITE='\033[1;37m'
DARK_YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${CYAN}============================================================${NC}"
echo -e "${CYAN}  Preparando entrega de SectorTuristic${NC}"
echo -e "${CYAN}  Base de datos: PMS54870695D (PMS + NIF alumno)${NC}"
echo -e "${CYAN}============================================================${NC}"
echo ""

# Configuración
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROYECTO_DIR="$SCRIPT_DIR"
NOMBRE_PROYECTO="SectorTuristic_54870695D"
FECHA_ACTUAL=$(date +"%Y-%m-%d_%H-%M")
NOMBRE_ZIP="${NOMBRE_PROYECTO}_${FECHA_ACTUAL}.zip"
RUTA_ZIP="$(dirname "$PROYECTO_DIR")/$NOMBRE_ZIP"
DB_NAME="PMS54870695D"
DB_USER="pms_user"
DB_PASS="pms_password123"
EXPORT_PATH="$PROYECTO_DIR/BD/export_database.sql"

echo -e "${YELLOW}[1/5] Exportando base de datos...${NC}"

# Exportar la base de datos
echo -e "${CYAN}   Exportando $DB_NAME a BD/export_database.sql...${NC}"
if command -v mysqldump &> /dev/null; then
    mysqldump -u "$DB_USER" -p"$DB_PASS" --default-character-set=utf8mb4 --single-transaction --routines --triggers "$DB_NAME" > "$EXPORT_PATH" 2>/dev/null
    
    if [ -f "$EXPORT_PATH" ]; then
        TAMANO_EXPORT=$(du -k "$EXPORT_PATH" | cut -f1)
        echo -e "${GREEN}   Base de datos exportada exitosamente ($TAMANO_EXPORT KB)${NC}"
    else
        echo -e "${YELLOW}   ADVERTENCIA: No se pudo exportar la base de datos${NC}"
        echo -e "${YELLOW}   Continuando sin export_database.sql...${NC}"
    fi
else
    echo -e "${YELLOW}   ADVERTENCIA: mysqldump no encontrado${NC}"
    echo -e "${YELLOW}   Continuando sin export_database.sql...${NC}"
fi
echo ""

echo -e "${YELLOW}[2/5] Verificando carpetas...${NC}"

# Verificar que estamos en la carpeta correcta
if [ ! -d "$PROYECTO_DIR/PMS" ]; then
    echo -e "${RED}ERROR: No se encontró la carpeta PMS. Asegúrate de ejecutar el script desde la carpeta SectorTuristic.${NC}"
    exit 1
fi

if [ ! -d "$PROYECTO_DIR/WebService" ]; then
    echo -e "${RED}ERROR: No se encontró la carpeta WebService.${NC}"
    exit 1
fi

echo -e "${GREEN}   Carpeta PMS encontrada${NC}"
echo -e "${GREEN}   Carpeta WebService encontrada${NC}"
echo -e "${GREEN}   Carpeta BD encontrada${NC}"
echo ""

echo -e "${YELLOW}[3/5] Buscando carpetas node_modules...${NC}"

# Buscar todas las carpetas node_modules
NODE_MODULES_COUNT=$(find "$PROYECTO_DIR" -type d -name "node_modules" 2>/dev/null | wc -l)

if [ $NODE_MODULES_COUNT -gt 0 ]; then
    echo -e "${YELLOW}   Encontradas $NODE_MODULES_COUNT carpeta(s) node_modules:${NC}"
    find "$PROYECTO_DIR" -type d -name "node_modules" 2>/dev/null | while read -r path; do
        RELATIVE_PATH="${path#$PROYECTO_DIR}"
        echo -e "${DARK_YELLOW}   - .$RELATIVE_PATH${NC}"
    done
else
    echo -e "${GREEN}   No se encontraron carpetas node_modules${NC}"
fi
echo ""

echo -e "${YELLOW}[4/5] Creando archivo ZIP...${NC}"
echo -e "${CYAN}   Ruta destino: $RUTA_ZIP${NC}"

# Eliminar ZIP anterior si existe
if [ -f "$RUTA_ZIP" ]; then
    echo -e "${DARK_YELLOW}   Eliminando ZIP anterior...${NC}"
    rm -f "$RUTA_ZIP"
fi

# Crear el ZIP excluyendo carpetas innecesarias
cd "$(dirname "$PROYECTO_DIR")"

zip -r "$NOMBRE_ZIP" "$NOMBRE_PROYECTO" \
    -x "*/node_modules/*" \
    -x "*/.git/*" \
    -x "*/__pycache__/*" \
    -x "*/.pytest_cache/*" \
    -x "*/dist/*" \
    -x "*/build/*" \
    -x "*/.DS_Store" \
    -x "*/package-lock.json" \
    -x "*/README.md" \
    -x "*/crear_zip.ps1" \
    -q

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${YELLOW}[5/5] Finalizando...${NC}"
    
    # Obtener tamaño del archivo
    TAMANO_BYTES=$(stat -f%z "$RUTA_ZIP" 2>/dev/null || stat -c%s "$RUTA_ZIP" 2>/dev/null)
    TAMANO_MB=$(echo "scale=2; $TAMANO_BYTES / 1048576" | bc)
    
    # Contar archivos en el ZIP
    TOTAL_ARCHIVOS=$(unzip -l "$RUTA_ZIP" | tail -1 | awk '{print $2}')
    
    echo ""
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}  ZIP creado exitosamente!${NC}"
    echo -e "${GREEN}================================================${NC}"
    echo ""
    echo -e "${CYAN}Detalles:${NC}"
    echo -e "${WHITE}  Archivo: $NOMBRE_ZIP${NC}"
    echo -e "${WHITE}  Ubicación: $RUTA_ZIP${NC}"
    echo -e "${WHITE}  Tamaño: $TAMANO_MB MB${NC}"
    echo -e "${WHITE}  Archivos incluidos: $TOTAL_ARCHIVOS${NC}"
    echo ""
    echo -e "${CYAN}Archivos incluidos:${NC}"
    echo -e "${WHITE}  - Codigo fuente PMS y WebService${NC}"
    echo -e "${WHITE}  - Scripts de base de datos (dump.sql, insert.sql)${NC}"
    echo -e "${GREEN}  - Exportacion de BD: export_database.sql${NC}"
    echo -e "${WHITE}  - Documentacion (README del PMS)${NC}"
    echo ""
    echo -e "${CYAN}Carpetas excluidas:${NC}"
    echo -e "${DARK_YELLOW}  - node_modules (dependencias de Node.js)${NC}"
    echo -e "${DARK_YELLOW}  - .git (control de versiones)${NC}"
    echo -e "${DARK_YELLOW}  - __pycache__ (cache de Python)${NC}"
    echo -e "${DARK_YELLOW}  - Scripts de utilidad (crear_zip.ps1, README.md raiz)${NC}"
    echo ""
    echo -e "${YELLOW}IMPORTANTE: La base de datos se llama PMS54870695D${NC}"
    echo ""
else
    echo -e "${RED}ERROR: Falló la creación del ZIP${NC}"
    exit 1
fi

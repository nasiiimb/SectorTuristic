# Guia de Lanzamiento - Principal Booking Engine

## Orden de Inicio de Servicios

Para que Principal funcione correctamente, debes iniciar los servicios en este orden:

### 1. WebService (Puerto 3000)

```powershell
cd WebService
npm run dev
```

**Verificar**: Accede a http://localhost:3000 - deberias ver un mensaje o documentacion de la API.

---

### 2. Channel Manager (Puerto 8001)

```powershell
cd Channel
.\venv\Scripts\Activate.ps1  # Activar entorno virtual
python -m src.main
```

**Verificar**: Accede a http://localhost:8001/docs - veras la documentacion Swagger de FastAPI.

---

### 3. Principal (Backend + Frontend)

**AHORA ES MUY FACIL - UN SOLO COMANDO:**

```powershell
cd Principal
npm run dev
```

Este comando ejecuta automaticamente:
- Backend en http://localhost:8010
- Frontend en http://localhost:5174

**Verificar**: 
- Backend: http://localhost:8010/health - deberias ver `{"status":"ok"}`
- Frontend: http://localhost:5174 - veras la pagina de inicio del Booking Engine

---

## Script de Lanzamiento Rapido

Puedes abrir **3 terminales de PowerShell** y ejecutar cada comando en una:

**Terminal 1 - WebService:**
```powershell
cd C:\UIB\Solucions Turistiques\practica\SectorTuristic\WebService; npm run dev
```

**Terminal 2 - Channel:**
```powershell
cd C:\UIB\Solucions Turistiques\practica\SectorTuristic\Channel; .\venv\Scripts\Activate.ps1; python -m src.main
```

**Terminal 3 - Principal (Backend + Frontend):**
```powershell
cd C:\UIB\Solucions Turistiques\practica\SectorTuristic\Principal; npm run dev
```

---

## Checklist Pre-Lanzamiento

Antes de iniciar los servicios, asegurate de:

- [ ] MySQL está ejecutándose
- [ ] Las bases de datos están creadas (`pms_db`, `channel_manager`, `principal_db`)
- [ ] WebService tiene el campo `localizador` en la tabla `Reserva`
- [ ] Channel tiene el endpoint `/api/reservas/reserve`
- [ ] Principal Backend tiene el archivo `.env` configurado
- [ ] Todas las dependencias están instaladas (`npm install` en cada proyecto Node.js)
- [ ] El entorno virtual de Python esta creado y activado para Channel
- [ ] Has instalado las dependencias del Principal con `npm install`

---

## Verificacion del Sistema

Una vez todos los servicios esten corriendo, prueba el flujo completo:

1. **Abre** http://localhost:5174
2. **Registrate** con un usuario nuevo
3. **Inicia sesion** con ese usuario
4. **Busca** habitaciones (ej: Palma, 2026-06-01 a 2026-06-05, 2 personas)
5. **Selecciona** una habitacion del WebService y elige un regimen (SA/AD/MP/PC/TI)
6. **Reserva** una habitacion
7. **Verifica** en "Mis Reservas" que aparece el localizador (formato WS-2026-##### o UUID)

---

## Solucion de Problemas

### Error: Puerto en uso

```powershell
# Encontrar proceso usando puerto (ejemplo: 8010)
Get-NetTCPConnection -LocalPort 8010 | Select OwningProcess
# Matar proceso
Stop-Process -Id <PID>
```

### Error: Base de datos no existe

```powershell
# Conectar a MySQL
mysql -u root -p
# Crear base de datos
CREATE DATABASE principal_db;
# Ejecutar script de setup si existe
USE principal_db;
# O crear las tablas manualmente (ver README.md)
```

### Error: JWT_SECRET no definido

```powershell
# Verificar que existe el archivo .env en Principal/backend
cd Principal\backend
Get-Content .env
# Si no existe, crear uno nuevo
# Agregar: JWT_SECRET=tu_clave_secreta_aqui
```

### Error: CORS al conectar con WebService/Channel

- Verificar que ambos servicios esten activos
- Comprobar que WebService tenga configurados los headers CORS en app.ts
- Revisar que las URLs en el backend sean correctas (localhost:3000 y localhost:8001)

### Error: Cannot find module

```powershell
# Reinstalar dependencias
cd <directorio-del-proyecto>
Remove-Item node_modules -Recurse -Force
Remove-Item package-lock.json
npm install
```

---

## Puertos Utilizados

| Servicio | Puerto | URL |
|----------|--------|-----|
| WebService | 3000 | http://localhost:3000 |
| Channel | 8001 | http://localhost:8001 |
| Principal Backend | 8010 | http://localhost:8010 |
| Principal Frontend | 5174 | http://localhost:5174 |

---

## Proximos Pasos

Despues del lanzamiento:

1. Crear usuarios de prueba en el sistema
2. Verificar que las busquedas devuelven resultados de ambos proveedores
3. Probar el flujo de reserva con regimen (WebService) y sin regimen (Channel)
4. Comprobar que las reservas se guardan correctamente en `principal_db`
5. Verificar que los localizadores tienen el formato correcto:
   - WebService: WS-2026-00001
   - Channel: UUID

---

**Listo para reservar!**

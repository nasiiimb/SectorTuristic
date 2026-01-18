# Testing Guide - Principal

## Tipos de Tests Implementados

### 1. Tests de Integración Backend
- Pruebas de endpoints de autenticación
- Verificación de conexión con WebService
- Validación de respuestas del Channel
- Tests de búsqueda unificada

### 2. Tests de Frontend
- Tests unitarios de componentes Vue
- Validación de formularios
- Navegación entre vistas
- Integración con API backend

## Ejecutar Tests

```bash
# Backend tests
cd backend
npm test

# Frontend tests
cd frontend
npm run test
```

## Coverage Report

Para generar un reporte de cobertura:

```bash
npm run test:coverage
```

## Tests Manuales Recomendados

1. **Flujo completo de reserva**
   - Registrarse como usuario nuevo
   - Buscar disponibilidad
   - Seleccionar habitación
   - Confirmar reserva
   - Verificar en "Mis Reservas"

2. **Validación de integración**
   - Verificar resultados de ambos proveedores
   - Comprobar localizadores únicos
   - Validar precios y regímenes

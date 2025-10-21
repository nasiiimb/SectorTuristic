# 💰 Sistema de Tarifas - Sector Turístico

## 📊 Matriz de Precios por Noche

Los precios varían según dos factores principales:
1. **Categoría del hotel** (número de estrellas)
2. **Tipo de habitación** (categoría de la habitación)

### 🏨 Hoteles en Palma

| **Tipo de Habitación** | **Gran Hotel del Mar** (5★) | **Hotel Palma Centro** (4★) | **Boutique Casco Antiguo** (3★) |
|------------------------|------------------------------|------------------------------|----------------------------------|
| **Individual**          | 120€/noche                   | 90€/noche                    | 60€/noche                        |
| **Doble Estándar**      | 150€/noche                   | 110€/noche                   | 75€/noche                        |
| **Doble Superior**      | 200€/noche                   | 145€/noche                   | 100€/noche                       |
| **Suite Junior**        | 300€/noche                   | 220€/noche                   | 150€/noche                       |

---

## 🎯 Lógica de Precios

### Por Categoría de Hotel
- **Hotel 5 estrellas**: Precios premium (×2 respecto al hotel 3★)
- **Hotel 4 estrellas**: Precios medios-altos (×1.5 respecto al hotel 3★)
- **Hotel 3 estrellas**: Precios base

### Por Tipo de Habitación
- **Individual**: Precio base (más económico)
- **Doble Estándar**: +25% sobre Individual
- **Doble Superior**: +67% sobre Individual
- **Suite Junior**: +150% sobre Individual (más exclusivo)

---

## 📋 Códigos de Tarifas

Cada tarifa tiene un código único que identifica hotel y tipo:

### Hotel 5★ - Gran Hotel del Mar
- `TARIFA_5E_IND` → 120€ (Individual)
- `TARIFA_5E_DBL_STD` → 150€ (Doble Estándar)
- `TARIFA_5E_DBL_SUP` → 200€ (Doble Superior)
- `TARIFA_5E_SUITE` → 300€ (Suite Junior)

### Hotel 4★ - Hotel Palma Centro
- `TARIFA_4E_IND` → 90€ (Individual)
- `TARIFA_4E_DBL_STD` → 110€ (Doble Estándar)
- `TARIFA_4E_DBL_SUP` → 145€ (Doble Superior)
- `TARIFA_4E_SUITE` → 220€ (Suite Junior)

### Hotel 3★ - Boutique Hotel Casco Antiguo
- `TARIFA_3E_IND` → 60€ (Individual)
- `TARIFA_3E_DBL_STD` → 75€ (Doble Estándar)
- `TARIFA_3E_DBL_SUP` → 100€ (Doble Superior)
- `TARIFA_3E_SUITE` → 150€ (Suite Junior)

---

## 🔍 Cómo Ver las Tarifas en el API

### Endpoint de Disponibilidad
Cuando buscas disponibilidad, el sistema incluye automáticamente el precio:

```http
GET http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran Hotel
```

**Respuesta incluye:**
```json
{
  "tiposDisponibles": [
    {
      "categoria": "Doble Superior",
      "precioPorNoche": "200.00",
      "codigoTarifa": "TARIFA_5E_DBL_SUP"
    }
  ]
}
```

---

## 💡 Ejemplo Completo: Cálculo de Precio Total

### Escenario
- **Hotel**: Gran Hotel del Mar (5★)
- **Habitación**: Doble Superior
- **Noches**: 4 (del 1 al 5 de diciembre)

### Cálculo
```
Precio por noche: 200€
Número de noches: 4
Total sin régimen: 200€ × 4 = 800€
```

Si se añade régimen:
```
Alojamiento y Desayuno (AD): 800€ + (20€ × 4 noches × 2 personas) = 960€
Media Pensión (MP): 800€ + (35€ × 4 noches × 2 personas) = 1,080€
Pensión Completa (PC): 800€ + (50€ × 4 noches × 2 personas) = 1,200€
```

---

## 🛠️ Estructura Técnica

### Tablas Relacionadas
1. **Tarifa**: Contiene el código y precio base
2. **Hotel_Tarifa**: Relaciona Hotel + Tarifa + TipoHabitacion
3. **TipoHabitacion**: Define la categoría de habitación

### Consulta Ejemplo (SQL)
```sql
SELECT 
    h.nombre AS hotel,
    h.categoria AS estrellas,
    th.categoria AS tipo_habitacion,
    t.codigo AS codigo_tarifa,
    t.precio AS precio_por_noche
FROM Hotel_Tarifa ht
JOIN Hotel h ON h.idHotel = ht.idHotel
JOIN TipoHabitacion th ON th.idTipoHabitacion = ht.idTipoHabitacion
JOIN Tarifa t ON t.idTarifa = ht.idTarifa
WHERE h.idHotel = 1;
```

---

## 📈 Futuras Mejoras (Opcional)

Podrías extender el sistema con:
- ✨ **Temporadas**: Precios diferentes para temporada alta/baja
- 🎉 **Promociones**: Descuentos por días festivos o eventos
- 👥 **Grupos**: Tarifas especiales para reservas múltiples
- 📅 **Early Bird**: Descuentos por reserva anticipada
- 🕒 **Last Minute**: Precios reducidos para reservas de último momento

---

**Última actualización**: Octubre 2025

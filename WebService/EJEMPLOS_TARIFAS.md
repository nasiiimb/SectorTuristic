# 🧪 Ejemplos de Prueba con Tarifas

## 🔍 Prueba 1: Ver Disponibilidad con Precios

### Hotel 5 Estrellas - Gran Hotel del Mar
```bash
curl "http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Gran%20Hotel"
```

**Respuesta Esperada:**
```json
{
  "hotel": {
    "nombre": "Gran Hotel del Mar",
    "ubicacion": "Paseo Marítimo, 10, Palma",
    "categoria": 5,
    "ciudad": "Palma",
    "pais": "España"
  },
  "tiposDisponibles": [
    {
      "idTipoHabitacion": 1,
      "categoria": "Doble Estándar",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "150.00",
      "codigoTarifa": "TARIFA_5E_DBL_STD"
    },
    {
      "idTipoHabitacion": 2,
      "categoria": "Doble Superior",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "200.00",
      "codigoTarifa": "TARIFA_5E_DBL_SUP"
    },
    {
      "idTipoHabitacion": 3,
      "categoria": "Suite Junior",
      "camasIndividuales": 0,
      "camasDobles": 2,
      "precioPorNoche": "300.00",
      "codigoTarifa": "TARIFA_5E_SUITE"
    }
  ],
  "totalHabitacionesDisponibles": 12
}
```

---

### Hotel 4 Estrellas - Hotel Palma Centro
```bash
curl "http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Palma%20Centro"
```

**Respuesta Esperada:**
```json
{
  "hotel": {
    "nombre": "Hotel Palma Centro",
    "ubicacion": "Avinguda de Jaume III, 25, Palma",
    "categoria": 4,
    "ciudad": "Palma",
    "pais": "España"
  },
  "tiposDisponibles": [
    {
      "idTipoHabitacion": 4,
      "categoria": "Individual",
      "camasIndividuales": 1,
      "camasDobles": 0,
      "precioPorNoche": "90.00",
      "codigoTarifa": "TARIFA_4E_IND"
    },
    {
      "idTipoHabitacion": 1,
      "categoria": "Doble Estándar",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "110.00",
      "codigoTarifa": "TARIFA_4E_DBL_STD"
    },
    {
      "idTipoHabitacion": 2,
      "categoria": "Doble Superior",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "145.00",
      "codigoTarifa": "TARIFA_4E_DBL_SUP"
    }
  ],
  "totalHabitacionesDisponibles": 12
}
```

---

### Hotel 3 Estrellas - Boutique Hotel Casco Antiguo
```bash
curl "http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&hotel=Boutique"
```

**Respuesta Esperada:**
```json
{
  "hotel": {
    "nombre": "Boutique Hotel Casco Antiguo",
    "ubicacion": "Carrer de Sant Miquel, 5, Palma",
    "categoria": 3,
    "ciudad": "Palma",
    "pais": "España"
  },
  "tiposDisponibles": [
    {
      "idTipoHabitacion": 1,
      "categoria": "Doble Estándar",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "75.00",
      "codigoTarifa": "TARIFA_3E_DBL_STD"
    },
    {
      "idTipoHabitacion": 2,
      "categoria": "Doble Superior",
      "camasIndividuales": 0,
      "camasDobles": 1,
      "precioPorNoche": "100.00",
      "codigoTarifa": "TARIFA_3E_DBL_SUP"
    }
  ],
  "totalHabitacionesDisponibles": 12
}
```

---

## 🏙️ Prueba 2: Buscar por Ciudad (Todos los Hoteles)

```bash
curl "http://localhost:3000/api/disponibilidad?fechaEntrada=2025-12-01&fechaSalida=2025-12-05&ciudad=Palma"
```

**Respuesta**: Lista con los 3 hoteles de Palma, cada uno con sus tarifas correspondientes.

---

## 💰 Comparativa de Precios

### Habitación Doble Estándar (4 noches)
| Hotel | Categoría | Precio/Noche | Total 4 Noches |
|-------|-----------|--------------|----------------|
| Gran Hotel del Mar | 5★ | 150€ | **600€** |
| Hotel Palma Centro | 4★ | 110€ | **440€** |
| Boutique Casco Antiguo | 3★ | 75€ | **300€** |

### Habitación Doble Superior (4 noches)
| Hotel | Categoría | Precio/Noche | Total 4 Noches |
|-------|-----------|--------------|----------------|
| Gran Hotel del Mar | 5★ | 200€ | **800€** |
| Hotel Palma Centro | 4★ | 145€ | **580€** |
| Boutique Casco Antiguo | 3★ | 100€ | **400€** |

### Suite Junior (4 noches)
| Hotel | Categoría | Precio/Noche | Total 4 Noches |
|-------|-----------|--------------|----------------|
| Gran Hotel del Mar | 5★ | 300€ | **1,200€** |
| Hotel Palma Centro | 4★ | 220€ | **880€** |
| Boutique Casco Antiguo | 3★ | 150€ | **600€** |

---

## 📊 Verificar Tarifas en la Base de Datos

### Consulta SQL para ver todas las tarifas
```sql
SELECT 
    h.nombre AS Hotel,
    h.categoria AS Estrellas,
    th.categoria AS TipoHabitacion,
    t.codigo AS CodigoTarifa,
    t.precio AS PrecioPorNoche
FROM Hotel_Tarifa ht
JOIN Hotel h ON h.idHotel = ht.idHotel
JOIN TipoHabitacion th ON th.idTipoHabitacion = ht.idTipoHabitacion
JOIN Tarifa t ON t.idTarifa = ht.idTarifa
ORDER BY h.categoria DESC, th.categoria;
```

---

## 🎯 Uso con Postman/Thunder Client

### Request
- **Method**: GET
- **URL**: `http://localhost:3000/api/disponibilidad`
- **Query Params**:
  - `fechaEntrada`: 2025-12-01
  - `fechaSalida`: 2025-12-05
  - `hotel`: Gran Hotel

### Headers
```
Accept: application/json
```

---

## ✅ Checklist de Validación

- [ ] Los precios aparecen en la respuesta de disponibilidad
- [ ] Los códigos de tarifa son correctos (TARIFA_5E_DBL_STD, etc.)
- [ ] Los precios reflejan la categoría del hotel
- [ ] Los precios reflejan el tipo de habitación
- [ ] Hotel 5★ tiene precios más altos que 4★ y 3★
- [ ] Suite tiene precio más alto que Doble Superior
- [ ] Doble Superior tiene precio más alto que Doble Estándar
- [ ] Individual tiene el precio más económico

---

**Fecha de prueba**: Octubre 2025
**Estado**: ✅ Implementado y funcional

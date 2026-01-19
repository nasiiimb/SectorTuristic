from src.database import SessionLocal
from src.models import Disponibilidad, TipoHabitacion, Hotel
from datetime import date

db = SessionLocal()

# Ver disponibilidad para 2026-02-01 a 2026-02-03
fecha_inicio = date(2026, 2, 1)
fecha_fin = date(2026, 2, 3)

print(f"Buscando disponibilidad entre {fecha_inicio} y {fecha_fin} para 2 huéspedes")
print("=" * 60)

# Ver todos los tipos de habitación
tipos = db.query(TipoHabitacion).all()
print(f"\nTipos de habitación total: {len(tipos)}")

for tipo in tipos:
    hotel = db.query(Hotel).filter(Hotel.id == tipo.hotel_id).first()
    print(f"\n  - {tipo.nombre} (ID: {tipo.id})")
    print(f"    Hotel: {hotel.nombre if hotel else 'N/A'}")
    print(f"    Capacidad: {tipo.capacidad_max}")
    print(f"    Precio base: {tipo.precio_base}")
    print(f"    Foto URL: {tipo.foto_url}")
    
    # Ver disponibilidad para este tipo
    disps = db.query(Disponibilidad).filter(
        Disponibilidad.tipo_habitacion_id == tipo.id,
        Disponibilidad.fecha >= fecha_inicio,
        Disponibilidad.fecha < fecha_fin
    ).all()
    
    print(f"    Disponibilidad:")
    for d in disps:
        print(f"      {d.fecha}: {d.cantidad_disponible} habitaciones")

db.close()

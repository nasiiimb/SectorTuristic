"""
Channel Manager - Rutas de Disponibilidad
"""
from typing import List, Optional
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..database import get_db
from ..models import Disponibilidad, TipoHabitacion, Hotel, User
from ..schemas import (
    DisponibilidadCreate, 
    DisponibilidadUpdate,
    DisponibilidadResponse, 
    DisponibilidadBulkCreate,
    ConsultaDisponibilidad
)
from .auth import get_current_user

router = APIRouter(prefix="/disponibilidad", tags=["Disponibilidad"])


@router.get("/", response_model=List[DisponibilidadResponse])
def listar_disponibilidad(
    hotel_id: Optional[int] = None,
    tipo_habitacion_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar disponibilidad del usuario"""
    query = db.query(Disponibilidad).join(TipoHabitacion).join(Hotel).filter(
        Hotel.user_id == current_user.id
    )
    
    if hotel_id:
        query = query.filter(TipoHabitacion.hotel_id == hotel_id)
    if tipo_habitacion_id:
        query = query.filter(Disponibilidad.tipo_habitacion_id == tipo_habitacion_id)
    if fecha_inicio:
        query = query.filter(Disponibilidad.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Disponibilidad.fecha <= fecha_fin)
    
    return query.order_by(Disponibilidad.fecha).all()


@router.get("/calendario")
def obtener_calendario(
    hotel_id: int,
    mes: int = Query(..., ge=1, le=12),
    anio: int = Query(..., ge=2024),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener disponibilidad en formato calendario para un hotel"""
    # Verificar que el hotel pertenece al usuario
    hotel = db.query(Hotel).filter(
        Hotel.id == hotel_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    # Calcular rango de fechas del mes
    fecha_inicio = date(anio, mes, 1)
    if mes == 12:
        fecha_fin = date(anio + 1, 1, 1) - timedelta(days=1)
    else:
        fecha_fin = date(anio, mes + 1, 1) - timedelta(days=1)
    
    # Obtener tipos de habitación del hotel
    tipos = db.query(TipoHabitacion).filter(
        TipoHabitacion.hotel_id == hotel_id,
        TipoHabitacion.activo == True
    ).all()
    
    # Obtener disponibilidad
    disponibilidades = db.query(Disponibilidad).filter(
        Disponibilidad.tipo_habitacion_id.in_([t.id for t in tipos]),
        Disponibilidad.fecha >= fecha_inicio,
        Disponibilidad.fecha <= fecha_fin
    ).all()
    
    # Organizar por tipo y fecha
    calendario = {}
    for tipo in tipos:
        calendario[tipo.id] = {
            "tipo_id": tipo.id,
            "tipo_nombre": tipo.nombre,
            "cantidad_total": tipo.cantidad_total,
            "precio_base": tipo.precio_base,
            "dias": {}
        }
    
    for disp in disponibilidades:
        calendario[disp.tipo_habitacion_id]["dias"][disp.fecha.isoformat()] = {
            "disponible": disp.cantidad_disponible,
            "precio": disp.precio,
            "cerrado": disp.cerrado
        }
    
    return {
        "hotel": {
            "id": hotel.id,
            "nombre": hotel.nombre
        },
        "mes": mes,
        "anio": anio,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "tipos_habitacion": list(calendario.values())
    }


@router.post("/", response_model=DisponibilidadResponse)
def crear_disponibilidad(
    disponibilidad: DisponibilidadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear o actualizar disponibilidad para una fecha"""
    # Verificar que la habitación pertenece al usuario
    habitacion = db.query(TipoHabitacion).join(Hotel).filter(
        TipoHabitacion.id == disponibilidad.tipo_habitacion_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    
    # Verificar si ya existe para esa fecha
    existente = db.query(Disponibilidad).filter(
        Disponibilidad.tipo_habitacion_id == disponibilidad.tipo_habitacion_id,
        Disponibilidad.fecha == disponibilidad.fecha
    ).first()
    
    if existente:
        # Actualizar existente
        for key, value in disponibilidad.model_dump().items():
            setattr(existente, key, value)
        db.commit()
        db.refresh(existente)
        return existente
    
    # Crear nuevo
    db_disp = Disponibilidad(**disponibilidad.model_dump())
    db.add(db_disp)
    db.commit()
    db.refresh(db_disp)
    return db_disp


@router.post("/bulk")
def crear_disponibilidad_bulk(
    bulk: DisponibilidadBulkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear/actualizar disponibilidad para un rango de fechas"""
    # Verificar que la habitación pertenece al usuario
    habitacion = db.query(TipoHabitacion).join(Hotel).filter(
        TipoHabitacion.id == bulk.tipo_habitacion_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    
    fecha_actual = bulk.fecha_inicio
    creados = 0
    actualizados = 0
    
    while fecha_actual <= bulk.fecha_fin:
        existente = db.query(Disponibilidad).filter(
            Disponibilidad.tipo_habitacion_id == bulk.tipo_habitacion_id,
            Disponibilidad.fecha == fecha_actual
        ).first()
        
        if existente:
            existente.cantidad_disponible = bulk.cantidad_disponible
            if bulk.precio is not None:
                existente.precio = bulk.precio
            actualizados += 1
        else:
            db_disp = Disponibilidad(
                tipo_habitacion_id=bulk.tipo_habitacion_id,
                fecha=fecha_actual,
                cantidad_disponible=bulk.cantidad_disponible,
                precio=bulk.precio
            )
            db.add(db_disp)
            creados += 1
        
        fecha_actual += timedelta(days=1)
    
    db.commit()
    
    return {
        "message": "Disponibilidad actualizada",
        "creados": creados,
        "actualizados": actualizados
    }


@router.put("/{disponibilidad_id}", response_model=DisponibilidadResponse)
def actualizar_disponibilidad(
    disponibilidad_id: int,
    disponibilidad: DisponibilidadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar una disponibilidad específica"""
    db_disp = db.query(Disponibilidad).join(TipoHabitacion).join(Hotel).filter(
        Disponibilidad.id == disponibilidad_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not db_disp:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    
    update_data = disponibilidad.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_disp, key, value)
    
    db.commit()
    db.refresh(db_disp)
    return db_disp


@router.delete("/{disponibilidad_id}")
def eliminar_disponibilidad(
    disponibilidad_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar una disponibilidad"""
    db_disp = db.query(Disponibilidad).join(TipoHabitacion).join(Hotel).filter(
        Disponibilidad.id == disponibilidad_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not db_disp:
        raise HTTPException(status_code=404, detail="Disponibilidad no encontrada")
    
    db.delete(db_disp)
    db.commit()
    return {"message": "Disponibilidad eliminada"}


@router.get("/buscar")
def buscar_disponibilidad_publica(
    fecha_inicio: date = Query(..., description="Fecha de entrada"),
    fecha_fin: date = Query(..., description="Fecha de salida"),
    num_huespedes: int = Query(..., description="Número de huéspedes"),
    db: Session = Depends(get_db)
):
    """
    Endpoint público para buscar disponibilidad de habitaciones
    No requiere autenticación - usado por sistemas externos como Principal
    """
    from sqlalchemy import func
    
    # Buscar tipos de habitación que tengan capacidad suficiente
    tipos_habitacion = db.query(TipoHabitacion).filter(
        TipoHabitacion.capacidad_max >= num_huespedes
    ).all()
    
    resultados = []
    
    for tipo in tipos_habitacion:
        # Obtener el hotel
        hotel = db.query(Hotel).filter(Hotel.id == tipo.hotel_id).first()
        if not hotel:
            continue
        
        # Verificar disponibilidad para todas las fechas del rango
        fecha_actual = fecha_inicio
        disponibilidad_minima = None
        precio_total_acumulado = 0
        tiene_disponibilidad_completa = True
        
        while fecha_actual < fecha_fin:
            disp = db.query(Disponibilidad).filter(
                Disponibilidad.tipo_habitacion_id == tipo.id,
                Disponibilidad.fecha == fecha_actual
            ).first()
            
            if disp and disp.cantidad_disponible > 0:
                if disponibilidad_minima is None:
                    disponibilidad_minima = disp.cantidad_disponible
                else:
                    disponibilidad_minima = min(disponibilidad_minima, disp.cantidad_disponible)
                precio_total_acumulado += (disp.precio or 100)  # Precio por defecto 100 si no está definido
            else:
                # No hay disponibilidad para esta fecha
                tiene_disponibilidad_completa = False
                break
            
            fecha_actual += timedelta(days=1)
        
        # Solo incluir si hay disponibilidad para todas las fechas
        if tiene_disponibilidad_completa and disponibilidad_minima and disponibilidad_minima > 0:
            # Foto por defecto si no tiene
            foto_url = "https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800"
            
            resultados.append({
                "tipo_habitacion_id": tipo.id,
                "tipo_nombre": tipo.nombre,
                "hotel_id": hotel.id,
                "hotel_nombre": hotel.nombre,
                "descripcion": tipo.descripcion or f"Habitación {tipo.nombre}",
                "capacidad_max": tipo.capacidad_max,
                "precio": precio_total_acumulado,
                "cantidad_disponible": int(disponibilidad_minima),
                "foto_url": foto_url,
                "servicios": tipo.servicios or ""
            })
    
    return resultados

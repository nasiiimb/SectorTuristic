"""
Channel Manager - Rutas de Habitaciones (Tipos de Habitación)
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Hotel, TipoHabitacion, User
from ..schemas import (
    TipoHabitacionCreate, 
    TipoHabitacionUpdate, 
    TipoHabitacionResponse,
    TipoHabitacionConHotel
)
from .auth import get_current_user

router = APIRouter(prefix="/habitaciones", tags=["Habitaciones"])


@router.get("/", response_model=List[TipoHabitacionConHotel])
def listar_habitaciones(
    hotel_id: Optional[int] = None,
    activo: Optional[bool] = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar tipos de habitación del usuario"""
    # Solo habitaciones de hoteles del usuario
    query = db.query(TipoHabitacion).join(Hotel).filter(
        Hotel.user_id == current_user.id
    )
    
    if hotel_id:
        query = query.filter(TipoHabitacion.hotel_id == hotel_id)
    
    if activo is not None:
        query = query.filter(TipoHabitacion.activo == activo)
    
    return query.order_by(TipoHabitacion.hotel_id, TipoHabitacion.nombre).all()


@router.get("/{habitacion_id}", response_model=TipoHabitacionConHotel)
def obtener_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener un tipo de habitación por ID"""
    habitacion = db.query(TipoHabitacion).join(Hotel).filter(
        TipoHabitacion.id == habitacion_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    return habitacion


@router.post("/", response_model=TipoHabitacionResponse)
def crear_habitacion(
    habitacion: TipoHabitacionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo tipo de habitación"""
    # Verificar que el hotel pertenece al usuario
    hotel = db.query(Hotel).filter(
        Hotel.id == habitacion.hotel_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    db_habitacion = TipoHabitacion(**habitacion.model_dump())
    db.add(db_habitacion)
    db.commit()
    db.refresh(db_habitacion)
    return db_habitacion


@router.put("/{habitacion_id}", response_model=TipoHabitacionResponse)
def actualizar_habitacion(
    habitacion_id: int,
    habitacion: TipoHabitacionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar un tipo de habitación"""
    db_habitacion = db.query(TipoHabitacion).join(Hotel).filter(
        TipoHabitacion.id == habitacion_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not db_habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    
    update_data = habitacion.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_habitacion, key, value)
    
    db.commit()
    db.refresh(db_habitacion)
    return db_habitacion


@router.delete("/{habitacion_id}")
def eliminar_habitacion(
    habitacion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar un tipo de habitación"""
    db_habitacion = db.query(TipoHabitacion).join(Hotel).filter(
        TipoHabitacion.id == habitacion_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not db_habitacion:
        raise HTTPException(status_code=404, detail="Habitación no encontrada")
    
    db.delete(db_habitacion)
    db.commit()
    return {"message": f"Habitación '{db_habitacion.nombre}' eliminada correctamente"}

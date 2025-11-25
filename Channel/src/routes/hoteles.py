"""
Channel Manager - Rutas de Hoteles
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Header
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Hotel, User
from ..schemas import HotelCreate, HotelUpdate, HotelResponse, HotelConHabitaciones
from .auth import get_current_user

router = APIRouter(prefix="/hoteles", tags=["Hoteles"])


@router.get("/", response_model=List[HotelResponse])
def listar_hoteles(
    activo: Optional[bool] = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Listar hoteles del usuario actual"""
    query = db.query(Hotel).filter(Hotel.user_id == current_user.id)
    
    if activo is not None:
        query = query.filter(Hotel.activo == activo)
    
    return query.order_by(Hotel.nombre).all()


@router.get("/{hotel_id}", response_model=HotelConHabitaciones)
def obtener_hotel(
    hotel_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Obtener un hotel por ID con sus habitaciones"""
    hotel = db.query(Hotel).filter(
        Hotel.id == hotel_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    return hotel


@router.post("/", response_model=HotelResponse)
def crear_hotel(
    hotel: HotelCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Crear un nuevo hotel"""
    db_hotel = Hotel(
        **hotel.model_dump(),
        user_id=current_user.id
    )
    db.add(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


@router.put("/{hotel_id}", response_model=HotelResponse)
def actualizar_hotel(
    hotel_id: int, 
    hotel: HotelUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Actualizar un hotel"""
    db_hotel = db.query(Hotel).filter(
        Hotel.id == hotel_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    update_data = hotel.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_hotel, key, value)
    
    db.commit()
    db.refresh(db_hotel)
    return db_hotel


@router.delete("/{hotel_id}")
def eliminar_hotel(
    hotel_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Eliminar un hotel"""
    db_hotel = db.query(Hotel).filter(
        Hotel.id == hotel_id,
        Hotel.user_id == current_user.id
    ).first()
    
    if not db_hotel:
        raise HTTPException(status_code=404, detail="Hotel no encontrado")
    
    db.delete(db_hotel)
    db.commit()
    return {"message": f"Hotel '{db_hotel.nombre}' eliminado correctamente"}

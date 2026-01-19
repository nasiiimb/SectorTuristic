"""
Channel Manager - Rutas de Reservas
"""
from datetime import date, datetime
from typing import Optional
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db
from ..models import TipoHabitacion, Hotel, Disponibilidad
from ..models.models import Reserva

router = APIRouter(prefix="/reservas", tags=["Reservas"])


class ReservaCreate(BaseModel):
    """Schema para crear reserva - acepta todos los campos del cliente"""
    hotel_id: Optional[int] = None
    tipo_habitacion_id: int
    fecha_entrada: date
    fecha_salida: date
    num_habitaciones: int = 1
    num_huespedes: int = 1
    cliente_nombre: Optional[str] = None
    cliente_email: Optional[str] = None
    cliente_telefono: Optional[str] = None
    notas: Optional[str] = None


class ReservaResponse(BaseModel):
    """Schema de respuesta"""
    id: int
    localizador: str
    hotel_id: int
    tipo_habitacion_id: int
    fecha_entrada: date
    fecha_salida: date
    num_habitaciones: int
    num_huespedes: int
    precio_total: Optional[float]
    estado: str
    cliente_nombre: Optional[str]
    cliente_email: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


@router.post("/crear", response_model=ReservaResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(data: ReservaCreate, db: Session = Depends(get_db)):
    """
    Endpoint para crear reserva
    - Valida tipo de habitacion y hotel
    - Verifica disponibilidad
    - Calcula precio total
    - Reduce stock
    - Genera localizador unico
    """
    
    # Validar tipo de habitacion
    tipo = db.query(TipoHabitacion).filter(
        TipoHabitacion.id == data.tipo_habitacion_id,
        TipoHabitacion.activo == True
    ).first()
    
    if not tipo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tipo de habitacion {data.tipo_habitacion_id} no encontrado"
        )
    
    # Validar hotel
    hotel = db.query(Hotel).filter(
        Hotel.id == tipo.hotel_id,
        Hotel.activo == True
    ).first()
    
    if not hotel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hotel no encontrado o inactivo"
        )
    
    # Validar fechas
    if data.fecha_salida <= data.fecha_entrada:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Fecha de salida debe ser posterior a fecha de entrada"
        )
    
    # Verificar disponibilidad para todas las noches
    current_date = data.fecha_entrada
    unavailable_dates = []
    
    while current_date < data.fecha_salida:
        disp = db.query(Disponibilidad).filter(
            Disponibilidad.tipo_habitacion_id == data.tipo_habitacion_id,
            Disponibilidad.fecha == current_date,
            Disponibilidad.cerrado == False
        ).first()
        
        if not disp or disp.cantidad_disponible < data.num_habitaciones:
            unavailable_dates.append(current_date.isoformat())
        
        current_date = date.fromordinal(current_date.toordinal() + 1)
    
    if unavailable_dates:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Sin disponibilidad en fechas: {', '.join(unavailable_dates)}"
        )
    
    # Calcular precio total
    total_price = 0.0
    current_date = data.fecha_entrada
    
    while current_date < data.fecha_salida:
        disp = db.query(Disponibilidad).filter(
            Disponibilidad.tipo_habitacion_id == data.tipo_habitacion_id,
            Disponibilidad.fecha == current_date
        ).first()
        
        if disp and disp.precio:
            total_price += disp.precio * data.num_habitaciones
        
        current_date = date.fromordinal(current_date.toordinal() + 1)
    
    # Generar localizador
    localizador = str(uuid.uuid4())
    
    # Crear reserva
    reserva = Reserva(
        hotel_id=hotel.id,
        tipo_habitacion_id=data.tipo_habitacion_id,
        fecha_entrada=data.fecha_entrada,
        fecha_salida=data.fecha_salida,
        num_habitaciones=data.num_habitaciones,
        num_huespedes=data.num_huespedes,
        precio_total=total_price if total_price > 0 else None,
        cliente_nombre=data.cliente_nombre,
        cliente_email=data.cliente_email,
        cliente_telefono=data.cliente_telefono,
        estado="confirmada",
        reserva_pms_id=localizador,
        notas=data.notas
    )
    
    db.add(reserva)
    
    # Reducir disponibilidad
    current_date = data.fecha_entrada
    while current_date < data.fecha_salida:
        disp = db.query(Disponibilidad).filter(
            Disponibilidad.tipo_habitacion_id == data.tipo_habitacion_id,
            Disponibilidad.fecha == current_date
        ).first()
        
        if disp:
            disp.cantidad_disponible -= data.num_habitaciones
        
        current_date = date.fromordinal(current_date.toordinal() + 1)
    
    # Guardar todo
    db.commit()
    db.refresh(reserva)
    
    # Respuesta
    return ReservaResponse(
        id=reserva.id,
        localizador=localizador,
        hotel_id=reserva.hotel_id,
        tipo_habitacion_id=reserva.tipo_habitacion_id,
        fecha_entrada=reserva.fecha_entrada,
        fecha_salida=reserva.fecha_salida,
        num_habitaciones=reserva.num_habitaciones,
        num_huespedes=reserva.num_huespedes,
        precio_total=reserva.precio_total,
        estado=reserva.estado,
        cliente_nombre=reserva.cliente_nombre,
        cliente_email=reserva.cliente_email,
        created_at=reserva.created_at
    )


@router.get("/{reserva_id}", response_model=ReservaResponse)
async def get_reservation(reserva_id: int, db: Session = Depends(get_db)):
    """Obtener reserva por ID"""
    reserva = db.query(Reserva).filter(Reserva.id == reserva_id).first()
    
    if not reserva:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Reserva {reserva_id} no encontrada"
        )
    
    return ReservaResponse(
        id=reserva.id,
        localizador=reserva.reserva_pms_id or "N/A",
        hotel_id=reserva.hotel_id,
        tipo_habitacion_id=reserva.tipo_habitacion_id,
        fecha_entrada=reserva.fecha_entrada,
        fecha_salida=reserva.fecha_salida,
        num_habitaciones=reserva.num_habitaciones,
        num_huespedes=reserva.num_huespedes,
        precio_total=reserva.precio_total,
        estado=reserva.estado,
        cliente_nombre=reserva.cliente_nombre,
        cliente_email=reserva.cliente_email,
        created_at=reserva.created_at
    )

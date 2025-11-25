from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    nombre: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    nombre: Optional[str] = None
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class HotelBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = "España"
    codigo_postal: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    web: Optional[str] = None
    estrellas: Optional[int] = 3
    descripcion: Optional[str] = None


class HotelCreate(HotelBase):
    pass


class HotelUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    ciudad: Optional[str] = None
    pais: Optional[str] = None
    codigo_postal: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    web: Optional[str] = None
    estrellas: Optional[int] = None
    descripcion: Optional[str] = None


class HotelResponse(HotelBase):
    id: int
    user_id: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TipoHabitacionBase(BaseModel):
    codigo: str
    nombre: str
    descripcion: Optional[str] = None
    capacidad_min: int = 1
    capacidad_max: int = 2
    camas: Optional[str] = None
    superficie: Optional[int] = None
    servicios: Optional[str] = None


class TipoHabitacionCreate(TipoHabitacionBase):
    hotel_id: int


class TipoHabitacionUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad_min: Optional[int] = None
    capacidad_max: Optional[int] = None
    camas: Optional[str] = None
    superficie: Optional[int] = None
    servicios: Optional[str] = None


class TipoHabitacionResponse(TipoHabitacionBase):
    id: int
    hotel_id: int
    activo: bool

    class Config:
        from_attributes = True


class HotelConHabitaciones(HotelResponse):
    habitaciones: List["TipoHabitacionResponse"] = []


class TipoHabitacionConHotel(TipoHabitacionResponse):
    hotel: Optional["HotelResponse"] = None


class DisponibilidadBase(BaseModel):
    tipo_habitacion_id: int
    fecha: date
    cantidad_disponible: int
    precio: float


class DisponibilidadCreate(DisponibilidadBase):
    pass


class DisponibilidadUpdate(BaseModel):
    cantidad_disponible: Optional[int] = None
    precio: Optional[float] = None


class DisponibilidadResponse(DisponibilidadBase):
    id: int

    class Config:
        from_attributes = True


class DisponibilidadBulkCreate(BaseModel):
    tipo_habitacion_id: int
    fecha_inicio: date
    fecha_fin: date
    cantidad_disponible: int
    precio: float


class ConsultaDisponibilidad(BaseModel):
    hotel_id: Optional[int] = None
    tipo_habitacion_id: Optional[int] = None
    fecha_inicio: date
    fecha_fin: date


class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int


class MessageResponse(BaseModel):
    message: str
    success: bool = True


# ============ RESERVAS ============

class ReservaBase(BaseModel):
    hotel_id: int
    tipo_habitacion_id: int
    fecha_entrada: date
    fecha_salida: date
    num_habitaciones: int = 1
    num_huespedes: int = 1
    precio_total: Optional[float] = None
    cliente_nombre: Optional[str] = None
    cliente_email: Optional[str] = None
    cliente_telefono: Optional[str] = None
    notas: Optional[str] = None


class ReservaCreate(ReservaBase):
    reserva_pms_id: Optional[str] = None  # ID de referencia del PMS


class ReservaUpdate(BaseModel):
    estado: Optional[str] = None  # confirmada, cancelada, completada
    notas: Optional[str] = None


class ReservaResponse(ReservaBase):
    id: int
    estado: str
    reserva_pms_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    fecha_cancelacion: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReservaConDetalles(ReservaResponse):
    """Reserva con información del hotel y tipo de habitación"""
    hotel: Optional["HotelResponse"] = None
    tipo_habitacion: Optional["TipoHabitacionResponse"] = None


class EstadisticasReservas(BaseModel):
    """Estadísticas de reservas por hotel o general"""
    total_reservas: int
    reservas_confirmadas: int
    reservas_canceladas: int
    reservas_completadas: int
    ingresos_totales: float
    promedio_por_reserva: float

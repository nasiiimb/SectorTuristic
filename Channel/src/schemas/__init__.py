"""
Channel Manager - Schemas Package
"""
from .schemas import (
    UserCreate, UserLogin, UserResponse, TokenResponse,
    HotelBase, HotelCreate, HotelResponse, HotelUpdate, HotelConHabitaciones,
    TipoHabitacionBase, TipoHabitacionCreate, TipoHabitacionResponse, TipoHabitacionUpdate, TipoHabitacionConHotel,
    DisponibilidadBase, DisponibilidadCreate, DisponibilidadUpdate, DisponibilidadResponse, DisponibilidadBulkCreate, ConsultaDisponibilidad,
    PaginatedResponse, MessageResponse
)

__all__ = [
    "UserCreate", "UserLogin", "UserResponse", "TokenResponse",
    "HotelBase", "HotelCreate", "HotelResponse", "HotelUpdate", "HotelConHabitaciones",
    "TipoHabitacionBase", "TipoHabitacionCreate", "TipoHabitacionResponse", "TipoHabitacionUpdate", "TipoHabitacionConHotel",
    "DisponibilidadBase", "DisponibilidadCreate", "DisponibilidadUpdate", "DisponibilidadResponse", "DisponibilidadBulkCreate", "ConsultaDisponibilidad",
    "PaginatedResponse", "MessageResponse"
]

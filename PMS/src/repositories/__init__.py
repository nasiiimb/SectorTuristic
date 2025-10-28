"""
Repository Pattern - Capa de acceso a datos
Principio de Inversión de Dependencias e Interfaz Segregation
"""

from .base import IRepository, RepositoryException
from .cliente_repository import ClienteRepository
from .reserva_repository import ReservaRepository
from .hotel_repository import (
    HotelRepository,
    CiudadRepository,
    TipoHabitacionRepository,
    RegimenRepository
)
from .contrato_repository import ContratoRepository
from .disponibilidad_repository import DisponibilidadRepository

__all__ = [
    'IRepository',
    'RepositoryException',
    'ClienteRepository',
    'ReservaRepository',
    'HotelRepository',
    'CiudadRepository',
    'TipoHabitacionRepository',
    'RegimenRepository',
    'ContratoRepository',
    'DisponibilidadRepository'
]

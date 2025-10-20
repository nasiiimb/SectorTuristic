"""
Domain Layer - Entidades del dominio
"""

from .cliente import Cliente
from .reserva import Reserva, TipoReserva
from .hotel import Hotel, TipoHabitacion, Regimen, Ciudad
from .contrato import Contrato

__all__ = [
    'Cliente',
    'Reserva',
    'TipoReserva',
    'Hotel',
    'TipoHabitacion',
    'Regimen',
    'Ciudad',
    'Contrato'
]

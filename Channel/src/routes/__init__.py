"""
Channel Manager - Routes Package
"""
from .auth import router as auth_router
from .hoteles import router as hoteles_router
from .habitaciones import router as habitaciones_router
from .disponibilidad import router as disponibilidad_router
from .reservas import router as reservas_router

__all__ = ["auth_router", "hoteles_router", "habitaciones_router", "disponibilidad_router", "reservas_router"]

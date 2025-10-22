"""
Configuración de la aplicación
Principio de Responsabilidad Única: Solo maneja configuración
"""
from dataclasses import dataclass
from typing import Optional
import os


@dataclass(frozen=True)  # Immutable
class Config:
    """
    Configuración inmutable de la aplicación.
    Siguiendo el patrón Configuration Object.
    """
    api_base_url: str = "http://localhost:3000/api"
    request_timeout: int = 10
    date_format: str = "%Y-%m-%d"
    datetime_format: str = "%Y-%m-%d %H:%M:%S"
    app_name: str = "PMS - Sistema de Gestión Hotelera"
    app_version: str = "2.0.0"
    
    @classmethod
    def from_env(cls) -> 'Config':
        """
        Crea la configuración desde variables de entorno.
        Permite sobreescribir la configuración sin modificar código.
        """
        return cls(
            api_base_url=os.getenv('PMS_API_URL', cls.api_base_url),
            request_timeout=int(os.getenv('PMS_TIMEOUT', cls.request_timeout)),
        )
    
    def __str__(self) -> str:
        return f"Config(api_url={self.api_base_url})"

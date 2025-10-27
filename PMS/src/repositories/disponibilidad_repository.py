"""
DisponibilidadRepository - Consulta de disponibilidad de habitaciones
Maneja el endpoint de disponibilidad según el API real
"""
from typing import List, Dict, Any, Optional
from repositories.base import RepositoryException
from infrastructure import APIClient
from datetime import date


class DisponibilidadRepository:
    """
    Repository para consultar disponibilidad de habitaciones.
    No sigue IRepository porque no es una entidad CRUD tradicional.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Constructor con inyección de dependencias
        
        Args:
            api_client: Cliente HTTP para comunicación con el API
        """
        self._api = api_client
    
    def consultar_por_ciudad(
        self,
        ciudad: str,
        fecha_entrada: date,
        fecha_salida: date
    ) -> List[Dict[str, Any]]:
        """
        Consulta disponibilidad de hoteles en una ciudad.
        
        Args:
            ciudad: Nombre de la ciudad
            fecha_entrada: Fecha de entrada (YYYY-MM-DD)
            fecha_salida: Fecha de salida (YYYY-MM-DD)
            
        Returns:
            Lista de hoteles con tipos de habitación disponibles:
            [
                {
                    "idHotel": 1,
                    "nombre": "Hotel Paraíso",
                    "ubicacion": "...",
                    "categoria": 5,
                    "ciudad": {...},
                    "tiposDisponibles": [
                        {
                            "idTipoHabitacion": 1,
                            "categoria": "Doble",
                            "disponibles": 5,
                            "precioPorNoche": 100.00,
                            ...
                        }
                    ],
                    "totalTiposDisponibles": 2
                }
            ]
        """
        params = {
            "ciudad": ciudad,
            "fechaEntrada": fecha_entrada.strftime("%Y-%m-%d"),
            "fechaSalida": fecha_salida.strftime("%Y-%m-%d")
        }
        
        response = self._api.get("disponibilidad", params)
        if not response.success:
            error_msg = response.error
            if isinstance(error_msg, dict):
                error_msg = error_msg.get('message', str(error_msg))
            raise RepositoryException(f"Error al consultar disponibilidad: {error_msg}")
        
        return response.data if response.data else []
    
    def consultar_por_hotel(
        self,
        hotel: str,
        fecha_entrada: date,
        fecha_salida: date
    ) -> Dict[str, Any]:
        """
        Consulta disponibilidad de un hotel específico.
        
        Args:
            hotel: Nombre del hotel
            fecha_entrada: Fecha de entrada (YYYY-MM-DD)
            fecha_salida: Fecha de salida (YYYY-MM-DD)
            
        Returns:
            Información del hotel con tipos disponibles:
            {
                "hotel": {
                    "nombre": "Hotel Paraíso",
                    "ubicacion": "...",
                    "categoria": 5,
                    "ciudad": "Palma",
                    "pais": "España"
                },
                "tiposDisponibles": [...],
                "totalTiposDisponibles": 2
            }
        """
        params = {
            "hotel": hotel,
            "fechaEntrada": fecha_entrada.strftime("%Y-%m-%d"),
            "fechaSalida": fecha_salida.strftime("%Y-%m-%d")
        }
        
        response = self._api.get("disponibilidad", params)
        if not response.success:
            error_msg = response.error
            if isinstance(error_msg, dict):
                error_msg = error_msg.get('message', str(error_msg))
            raise RepositoryException(f"Error al consultar disponibilidad: {error_msg}")
        
        return response.data if response.data else {}
    
    def consultar_por_pais(
        self,
        pais: str,
        fecha_entrada: date,
        fecha_salida: date
    ) -> List[Dict[str, Any]]:
        """
        Consulta disponibilidad de hoteles en un país.
        
        Args:
            pais: Nombre del país
            fecha_entrada: Fecha de entrada (YYYY-MM-DD)
            fecha_salida: Fecha de salida (YYYY-MM-DD)
            
        Returns:
            Lista de hoteles con disponibilidad (mismo formato que consultar_por_ciudad)
        """
        params = {
            "pais": pais,
            "fechaEntrada": fecha_entrada.strftime("%Y-%m-%d"),
            "fechaSalida": fecha_salida.strftime("%Y-%m-%d")
        }
        
        response = self._api.get("disponibilidad", params)
        if not response.success:
            error_msg = response.error
            if isinstance(error_msg, dict):
                error_msg = error_msg.get('message', str(error_msg))
            raise RepositoryException(f"Error al consultar disponibilidad: {error_msg}")
        
        return response.data if response.data else []
    
    def hay_disponibilidad(
        self,
        hotel: Optional[str] = None,
        ciudad: Optional[str] = None,
        pais: Optional[str] = None,
        fecha_entrada: date = None,
        fecha_salida: date = None
    ) -> bool:
        """
        Verifica si hay disponibilidad en general.
        
        Args:
            hotel: Nombre del hotel (opcional)
            ciudad: Nombre de la ciudad (opcional)
            pais: Nombre del país (opcional)
            fecha_entrada: Fecha de entrada
            fecha_salida: Fecha de salida
            
        Returns:
            True si hay al menos un tipo de habitación disponible, False si no
        """
        try:
            if hotel:
                resultado = self.consultar_por_hotel(hotel, fecha_entrada, fecha_salida)
                return resultado.get('totalTiposDisponibles', 0) > 0
            elif ciudad:
                resultado = self.consultar_por_ciudad(ciudad, fecha_entrada, fecha_salida)
                return len(resultado) > 0
            elif pais:
                resultado = self.consultar_por_pais(pais, fecha_entrada, fecha_salida)
                return len(resultado) > 0
            else:
                raise ValueError("Debe proporcionar hotel, ciudad o país")
        except RepositoryException:
            return False

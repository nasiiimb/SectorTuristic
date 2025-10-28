"""
ReservaRepository - Acceso a datos de Reservas
Implementa IRepository para la entidad Reserva
"""
from typing import List, Optional
from repositories.base import IRepository, RepositoryException
from domain import Reserva
from infrastructure import APIClient


class ReservaRepository(IRepository[Reserva]):
    """Repository para gestionar reservas a través del API"""
    
    def __init__(self, api_client: APIClient):
        """
        Constructor con inyección de dependencias
        
        Args:
            api_client: Cliente HTTP para comunicación con el API
        """
        self._api = api_client
    
    def find_all(self) -> List[Reserva]:
        """Obtiene TODAS las reservas (activas y canceladas)"""
        response = self._api.get("reservas")
        if not response.success:
            raise RepositoryException(f"Error al obtener reservas: {response.error}")
        
        return [Reserva.from_dict(data) for data in response.data]
    
    def find_all_activas(self) -> List[Reserva]:
        """Obtiene solo reservas activas (para PMS)"""
        response = self._api.get("reservas/activas")
        if not response.success:
            raise RepositoryException(f"Error al obtener reservas activas: {response.error}")
        
        return [Reserva.from_dict(data) for data in response.data]
    
    def find_by_id(self, id: int) -> Optional[Reserva]:
        """Busca una reserva por ID"""
        response = self._api.get(f"reservas/{id}")
        if not response.success:
            if response.status_code == 404:
                return None
            raise RepositoryException(f"Error al buscar reserva: {response.error}")
        
        return Reserva.from_dict(response.data)
    
    def create(self, reserva: Reserva) -> Reserva:
        """Crea una nueva reserva"""
        response = self._api.post("reservas", reserva.to_dict())
        if not response.success:
            raise RepositoryException(f"Error al crear reserva: {response.error}")
        
        return Reserva.from_dict(response.data)
    
    def update(self, id: int, reserva: Reserva) -> Reserva:
        """Actualiza una reserva existente"""
        response = self._api.put(f"reservas/{id}", reserva.to_dict())
        if not response.success:
            raise RepositoryException(f"Error al actualizar reserva: {response.error}")
        
        return Reserva.from_dict(response.data)
    
    def delete(self, id: int) -> bool:
        """Elimina una reserva"""
        response = self._api.delete(f"reservas/{id}")
        if not response.success:
            raise RepositoryException(f"Error al eliminar reserva: {response.error}")
        
        return True
    
    def find_by_cliente(self, id_cliente: int) -> List[Reserva]:
        """Busca reservas por cliente"""
        response = self._api.get(f"/reservas?idCliente={id_cliente}")
        if not response.success:
            raise RepositoryException(f"Error al buscar reservas del cliente: {response.error}")
        
        return [Reserva.from_dict(data) for data in response.data]
    
    def find_activas(self) -> List[Reserva]:
        """Obtiene reservas activas (futuras y en curso)"""
        response = self._api.get("/reservas?estado=activa")
        if not response.success:
            raise RepositoryException(f"Error al obtener reservas activas: {response.error}")
        
        return [Reserva.from_dict(data) for data in response.data]
    
    def cancelar(self, id_reserva: int) -> Reserva:
        """
        Cancela una reserva (cambia su estado a Cancelada)
        
        Args:
            id_reserva: ID de la reserva a cancelar
            
        Returns:
            Reserva actualizada
        """
        response = self._api.patch(f"reservas/{id_reserva}/cancelar")
        if not response.success:
            raise RepositoryException(f"Error al cancelar reserva: {response.error}")
        
        # La API devuelve {message, reserva}
        return Reserva.from_dict(response.data.get('reserva', response.data))

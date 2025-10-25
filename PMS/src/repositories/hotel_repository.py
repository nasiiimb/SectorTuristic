"""
HotelRepository - Acceso a datos de Hoteles y entidades relacionadas
"""
from typing import List, Optional
from repositories.base import IRepository, RepositoryException
from domain import Hotel, Ciudad, TipoHabitacion, Regimen
from infrastructure import APIClient


class HotelRepository(IRepository[Hotel]):
    """Repository para gestionar hoteles"""
    
    def __init__(self, api_client: APIClient):
        self._api = api_client
    
    def find_all(self) -> List[Hotel]:
        """Obtiene todos los hoteles"""
        response = self._api.get("hoteles")
        if not response.success:
            raise RepositoryException(f"Error al obtener hoteles: {response.error}")
        
        return [Hotel.from_dict(data) for data in response.data]
    
    def find_by_id(self, id: int) -> Optional[Hotel]:
        """Busca un hotel por ID"""
        response = self._api.get(f"hoteles/{id}")
        if not response.success:
            if response.status_code == 404:
                return None
            raise RepositoryException(f"Error al buscar hotel: {response.error}")
        
        return Hotel.from_dict(response.data)
    
    def create(self, hotel: Hotel) -> Hotel:
        """Crea un nuevo hotel"""
        response = self._api.post("hoteles", hotel.to_dict())
        if not response.success:
            raise RepositoryException(f"Error al crear hotel: {response.error}")
        
        return Hotel.from_dict(response.data)
    
    def update(self, id: int, hotel: Hotel) -> Hotel:
        """Actualiza un hotel"""
        response = self._api.put(f"hoteles/{id}", hotel.to_dict())
        if not response.success:
            raise RepositoryException(f"Error al actualizar hotel: {response.error}")
        
        return Hotel.from_dict(response.data)
    
    def delete(self, id: int) -> bool:
        """Elimina un hotel"""
        response = self._api.delete(f"hoteles/{id}")
        if not response.success:
            raise RepositoryException(f"Error al eliminar hotel: {response.error}")
        
        return True
    
    def find_by_ciudad(self, id_ciudad: int) -> List[Hotel]:
        """Busca hoteles por ciudad"""
        response = self._api.get(f"hoteles?idCiudad={id_ciudad}")
        if not response.success:
            raise RepositoryException(f"Error al buscar hoteles: {response.error}")
        
        return [Hotel.from_dict(data) for data in response.data]


class CiudadRepository(IRepository[Ciudad]):
    """Repository para gestionar ciudades"""
    
    def __init__(self, api_client: APIClient):
        self._api = api_client
    
    def find_all(self) -> List[Ciudad]:
        """Obtiene todas las ciudades"""
        response = self._api.get("ciudades")
        if not response.success:
            raise RepositoryException(f"Error al obtener ciudades: {response.error}")
        
        return [Ciudad.from_dict(data) for data in response.data]
    
    def find_by_id(self, id: int) -> Optional[Ciudad]:
        """Busca una ciudad por ID"""
        response = self._api.get(f"ciudades/{id}")
        if not response.success:
            if response.status_code == 404:
                return None
            raise RepositoryException(f"Error al buscar ciudad: {response.error}")
        
        return Ciudad.from_dict(response.data)
    
    def create(self, ciudad: Ciudad) -> Ciudad:
        raise NotImplementedError("Creación de ciudades no permitida")
    
    def update(self, id: int, ciudad: Ciudad) -> Ciudad:
        raise NotImplementedError("Modificación de ciudades no permitida")
    
    def delete(self, id: int) -> bool:
        raise NotImplementedError("Eliminación de ciudades no permitida")


class TipoHabitacionRepository(IRepository[TipoHabitacion]):
    """Repository para tipos de habitación"""
    
    def __init__(self, api_client: APIClient):
        self._api = api_client
    
    def find_all(self) -> List[TipoHabitacion]:
        """Obtiene todos los tipos de habitación"""
        response = self._api.get("tiposHabitacion")
        if not response.success:
            raise RepositoryException(f"Error al obtener tipos de habitación: {response.error}")
        
        return [TipoHabitacion.from_dict(data) for data in response.data]
    
    def find_by_id(self, id: int) -> Optional[TipoHabitacion]:
        """Busca un tipo de habitación por ID"""
        response = self._api.get(f"tiposHabitacion/{id}")
        if not response.success:
            if response.status_code == 404:
                return None
            raise RepositoryException(f"Error al buscar tipo de habitación: {response.error}")
        
        return TipoHabitacion.from_dict(response.data)
    
    def create(self, tipo: TipoHabitacion) -> TipoHabitacion:
        raise NotImplementedError("Creación de tipos no permitida")
    
    def update(self, id: int, tipo: TipoHabitacion) -> TipoHabitacion:
        raise NotImplementedError("Modificación de tipos no permitida")
    
    def delete(self, id: int) -> bool:
        raise NotImplementedError("Eliminación de tipos no permitida")


class RegimenRepository(IRepository[Regimen]):
    """Repository para regímenes"""
    
    def __init__(self, api_client: APIClient):
        self._api = api_client
    
    def find_all(self) -> List[Regimen]:
        """Obtiene todos los regímenes"""
        response = self._api.get("regimenes")
        if not response.success:
            raise RepositoryException(f"Error al obtener regímenes: {response.error}")
        
        return [Regimen.from_dict(data) for data in response.data]
    
    def find_by_id(self, id: int) -> Optional[Regimen]:
        """Busca un régimen por ID"""
        response = self._api.get(f"regimenes/{id}")
        if not response.success:
            if response.status_code == 404:
                return None
            raise RepositoryException(f"Error al buscar régimen: {response.error}")
        
        return Regimen.from_dict(response.data)
    
    def create(self, regimen: Regimen) -> Regimen:
        raise NotImplementedError("Creación de regímenes no permitida")
    
    def update(self, id: int, regimen: Regimen) -> Regimen:
        raise NotImplementedError("Modificación de regímenes no permitida")
    
    def delete(self, id: int) -> bool:
        raise NotImplementedError("Eliminación de regímenes no permitida")

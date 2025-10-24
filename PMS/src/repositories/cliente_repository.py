"""
Cliente Repository - Implementación concreta del Repository Pattern
Responsabilidad: Acceso a datos de clientes via API
"""
from typing import List, Optional
from domain import Cliente
from infrastructure import APIClient
from repositories.base import IRepository, RepositoryException


class ClienteRepository(IRepository[Cliente]):
    """
    Repositorio de clientes que usa el WebService como fuente de datos.
    Implementa IRepository[Cliente] siguiendo el Dependency Inversion Principle.
    """
    
    def __init__(self, api_client: APIClient):
        """
        Inyección de dependencias: recibe el cliente API
        """
        self._api = api_client
    
    def find_all(self) -> List[Cliente]:
        """Obtiene todos los clientes"""
        response = self._api.get("clientes")
        if not response.success:
            raise RepositoryException(f"Error al obtener clientes: {response.error}")
        
        return [Cliente.from_dict(data) for data in response.data]
    
    def find_by_id(self, id: int) -> Optional[Cliente]:
        """Busca un cliente por ID"""
        response = self._api.get(f"clientes/{id}")
        if not response.success:
            return None
        
        return Cliente.from_dict(response.data)
    
    def create(self, entity: Cliente) -> Optional[Cliente]:
        """Crea un nuevo cliente"""
        response = self._api.post("clientes", entity.to_dict())
        if not response.success:
            raise RepositoryException(f"Error al crear cliente: {response.error}")
        
        return Cliente.from_dict(response.data)
    
    def update(self, id: int, entity: Cliente) -> Optional[Cliente]:
        """Actualiza un cliente"""
        response = self._api.put(f"clientes/{id}", entity.to_dict())
        if not response.success:
            raise RepositoryException(f"Error al actualizar cliente: {response.error}")
        
        return Cliente.from_dict(response.data)
    
    def delete(self, id: int) -> bool:
        """Elimina un cliente (no implementado en API)"""
        raise NotImplementedError("La API no soporta eliminación de clientes")
    
    def buscar(self, nombre: Optional[str] = None, apellido: Optional[str] = None) -> List[Cliente]:
        """Busca clientes por nombre o apellido"""
        params = {}
        if nombre:
            params['nombre'] = nombre
        if apellido:
            params['apellido'] = apellido
        
        response = self._api.get("clientes/buscar", params)
        if not response.success:
            return []
        
        return [Cliente.from_dict(data) for data in response.data.get('clientes', [])]

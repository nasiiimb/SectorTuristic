"""
Base Repository - Interfaz abstracta
Principio de Inversión de Dependencias: Depend on abstractions, not concretions
Principio de Segregación de Interfaces: Interfaces pequeñas y específicas
"""
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

T = TypeVar('T')  # Tipo genérico para las entidades


class IRepository(ABC, Generic[T]):
    """
    Interfaz base para todos los repositorios.
    Define el contrato que deben cumplir todos los repositorios.
    
    Permite cambiar la implementación (API, Base de Datos, Mock) sin afectar
    el resto de la aplicación (Dependency Inversion Principle).
    """
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """
        Obtiene todas las entidades.
        
        Returns:
            Lista de entidades del tipo T
        """
        pass
    
    @abstractmethod
    def find_by_id(self, id: int) -> Optional[T]:
        """
        Busca una entidad por su ID.
        
        Args:
            id: Identificador de la entidad
            
        Returns:
            La entidad encontrada o None si no existe
        """
        pass
    
    @abstractmethod
    def create(self, entity: T) -> Optional[T]:
        """
        Crea una nueva entidad.
        
        Args:
            entity: Entidad a crear
            
        Returns:
            La entidad creada con su ID asignado o None si falla
        """
        pass
    
    @abstractmethod
    def update(self, id: int, entity: T) -> Optional[T]:
        """
        Actualiza una entidad existente.
        
        Args:
            id: Identificador de la entidad
            entity: Entidad con los datos actualizados
            
        Returns:
            La entidad actualizada o None si falla
        """
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        """
        Elimina una entidad.
        
        Args:
            id: Identificador de la entidad
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        pass


class RepositoryException(Exception):
    """Excepción personalizada para errores del repositorio"""
    
    def __init__(self, message: str, original_error: Optional[Exception] = None):
        super().__init__(message)
        self.original_error = original_error

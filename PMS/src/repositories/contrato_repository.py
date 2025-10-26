"""
ContratoRepository - Acceso a datos de Contratos (Check-in/Check-out)
Implementa IRepository para la entidad Contrato según API real
"""
from typing import List, Optional
from repositories.base import IRepository, RepositoryException
from domain import Contrato
from infrastructure import APIClient


class ContratoRepository(IRepository[Contrato]):
    """Repository para gestionar contratos a través del API"""
    
    def __init__(self, api_client: APIClient):
        """
        Constructor con inyección de dependencias
        
        Args:
            api_client: Cliente HTTP para comunicación con el API
        """
        self._api = api_client
    
    def find_all(self) -> List[Contrato]:
        """Obtiene todos los contratos"""
        response = self._api.get("contratos")
        if not response.success:
            raise RepositoryException(f"Error al obtener contratos: {response.error}")
        
        # El backend retorna un objeto con {total, activos, finalizados, contratos}
        # Extraer el array de contratos
        data = response.data
        if isinstance(data, dict) and 'contratos' in data:
            contratos_data = data['contratos']
        elif isinstance(data, list):
            # Por compatibilidad si el backend retorna directamente una lista
            contratos_data = data
        else:
            raise RepositoryException(f"Se esperaba una lista de contratos o un objeto con 'contratos', se recibió {type(data)}")
        
        contratos = []
        for item in contratos_data:
            try:
                if isinstance(item, dict):
                    contratos.append(Contrato.from_dict(item))
                else:
                    print(f"Advertencia: Se omitió un elemento que no es diccionario: {type(item)}")
            except Exception as e:
                print(f"Error al parsear contrato: {e}")
                continue
        
        return contratos
    
    def find_by_id(self, id: int) -> Optional[Contrato]:
        """Busca un contrato por ID"""
        response = self._api.get(f"contratos/{id}")
        if not response.success:
            if response.status_code == 404:
                return None
            raise RepositoryException(f"Error al buscar contrato: {response.error}")
        
        return Contrato.from_dict(response.data)
    
    def create(self, contrato: Contrato) -> Contrato:
        """
        Crea un nuevo contrato (realiza check-in).
        
        Args:
            contrato: Contrato con idReserva, numeroHabitacion y montoTotal
            
        Returns:
            Contrato creado con fechaCheckIn asignada
        """
        response = self._api.post("contratos", contrato.to_dict())
        if not response.success:
            error_msg = response.error
            if isinstance(error_msg, dict):
                error_msg = error_msg.get('message', str(error_msg))
            raise RepositoryException(f"Error al crear contrato (check-in): {error_msg}")
        
        return Contrato.from_dict(response.data)
    
    def update(self, id: int, contrato: Contrato) -> Contrato:
        """
        Actualiza un contrato (no soportado directamente por la API).
        Usa checkout() para hacer check-out.
        """
        raise NotImplementedError("Para hacer check-out usa el método checkout()")
    
    def delete(self, id: int) -> bool:
        """Elimina un contrato (no soportado por la API)"""
        raise NotImplementedError("La API no soporta eliminación de contratos")
    
    def checkout(self, id_contrato: int) -> Contrato:
        """
        Realiza el check-out de un contrato.
        
        Args:
            id_contrato: ID del contrato
            
        Returns:
            Contrato actualizado con fechaCheckOut asignada
        """
        response = self._api.put(f"contratos/{id_contrato}/checkout")
        if not response.success:
            error_msg = response.error
            if isinstance(error_msg, dict):
                error_msg = error_msg.get('message', str(error_msg))
            raise RepositoryException(f"Error al hacer check-out: {error_msg}")
        
        # La API retorna { "message": "...", "contrato": {...} }
        if isinstance(response.data, dict) and 'contrato' in response.data:
            return Contrato.from_dict(response.data['contrato'])
        
        return Contrato.from_dict(response.data)
    
    def find_by_reserva(self, id_reserva: int) -> Optional[Contrato]:
        """
        Busca el contrato asociado a una reserva.
        
        Args:
            id_reserva: ID de la reserva
            
        Returns:
            Contrato si existe, None si no
        """
        # La API no tiene endpoint directo, obtenemos todos y filtramos
        contratos = self.find_all()
        for contrato in contratos:
            if contrato.id_reserva == id_reserva:
                return contrato
        return None
    
    def find_activos(self) -> List[Contrato]:
        """
        Obtiene contratos activos (con check-in pero sin check-out).
        
        Returns:
            Lista de contratos activos
        """
        contratos = self.find_all()
        return [c for c in contratos if c.esta_activo]
    
    def find_finalizados(self) -> List[Contrato]:
        """
        Obtiene contratos finalizados (con check-out).
        
        Returns:
            Lista de contratos finalizados
        """
        contratos = self.find_all()
        return [c for c in contratos if c.esta_finalizado]

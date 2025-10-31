"""
ClienteService - Lógica de negocio para gestión de clientes
Principio de Responsabilidad Única: Solo lógica de clientes
"""
from typing import List, Optional
from repositories import ClienteRepository, RepositoryException
from domain import Cliente
from utils.validators import (
    validar_email,
    validar_dni,
    normalizar_dni,
    normalizar_email,
    normalizar_texto
)


class ClienteService:
    """
    Servicio para gestionar clientes
    Encapsula la lógica de negocio y validaciones
    """
    
    def __init__(self, cliente_repo: ClienteRepository):
        """
        Constructor con inyección de dependencias
        
        Args:
            cliente_repo: Repositorio de clientes
        """
        self._cliente_repo = cliente_repo
    
    def listar_todos(self) -> List[Cliente]:
        """Obtiene todos los clientes"""
        try:
            return self._cliente_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al listar clientes: {str(e)}")
    
    def listar_clientes(self) -> List[Cliente]:
        """Alias de listar_todos() para compatibilidad con UI"""
        return self.listar_todos()
    
    def buscar_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Busca un cliente por ID"""
        try:
            return self._cliente_repo.find_by_id(id_cliente)
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar cliente: {str(e)}")
    
    def buscar_por_dni(self, dni: str) -> List[Cliente]:
        """Busca clientes por DNI"""
        try:
            dni_normalizado = normalizar_dni(dni)
            return self._cliente_repo.buscar(dni_normalizado)
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar por DNI: {str(e)}")
    
    def crear_cliente(
        self,
        nombre: str,
        apellidos: str,
        correo: str,
        dni: str,
        fecha_nacimiento: str
    ) -> Cliente:
        """
        Crea un nuevo cliente con validaciones
        
        Args:
            nombre: Nombre del cliente
            apellidos: Apellidos del cliente
            correo: Correo electrónico
            dni: DNI
            fecha_nacimiento: Fecha de nacimiento (YYYY-MM-DD)
            
        Returns:
            Cliente creado
            
        Raises:
            ServiceException: Si hay errores de validación
        """
        # Normalizar datos
        nombre = normalizar_texto(nombre)
        apellidos = normalizar_texto(apellidos)
        correo = normalizar_email(correo)
        dni = normalizar_dni(dni)
        
        # Validar
        if not validar_email(correo):
            raise ServiceException("El correo electrónico no es válido")
        
        if not validar_dni(dni):
            raise ServiceException("El DNI no es válido")
        
        # Verificar que no exista
        clientes_existentes = self.buscar_por_dni(dni)
        if clientes_existentes:
            raise ServiceException(f"Ya existe un cliente con DNI {dni}")
        
        try:
            # Crear entidad
            cliente = Cliente(
                nombre=nombre,
                apellidos=apellidos,
                correo_electronico=correo,
                dni=dni,
                fecha_nacimiento=fecha_nacimiento
            )
            
            # Persistir
            return self._cliente_repo.create(cliente)
            
        except RepositoryException as e:
            raise ServiceException(f"Error al crear cliente: {str(e)}")
        except ValueError as e:
            raise ServiceException(f"Datos inválidos: {str(e)}")
    
    def actualizar_cliente(
        self,
        id_cliente: int,
        nombre: str = None,
        apellidos: str = None,
        correo: str = None,
        fecha_nacimiento: str = None
    ) -> Cliente:
        """
        Actualiza un cliente existente
        
        Args:
            id_cliente: ID del cliente
            nombre: Nuevo nombre (opcional)
            apellidos: Nuevos apellidos (opcional)
            correo: Nuevo correo (opcional)
            fecha_nacimiento: Nueva fecha nacimiento (opcional)
            
        Returns:
            Cliente actualizado
        """
        try:
            # Obtener cliente existente
            cliente = self._cliente_repo.find_by_id(id_cliente)
            if not cliente:
                raise ServiceException(f"Cliente con ID {id_cliente} no encontrado")
            
            # Preparar datos actualizados
            datos = {}
            
            if nombre:
                datos['nombre'] = normalizar_texto(nombre)
            
            if apellidos:
                datos['apellidos'] = normalizar_texto(apellidos)
            
            if correo:
                correo_normalizado = normalizar_email(correo)
                if not validar_email(correo_normalizado):
                    raise ServiceException("El correo electrónico no es válido")
                datos['correo_electronico'] = correo_normalizado
            
            if fecha_nacimiento:
                datos['fecha_nacimiento'] = fecha_nacimiento
            
            # Actualizar
            cliente.actualizar_datos(**datos)
            return self._cliente_repo.update(id_cliente, cliente)
            
        except RepositoryException as e:
            raise ServiceException(f"Error al actualizar cliente: {str(e)}")
        except ValueError as e:
            raise ServiceException(f"Datos inválidos: {str(e)}")
    
    def eliminar_cliente(self, id_cliente: int) -> bool:
        """Elimina un cliente"""
        try:
            cliente = self._cliente_repo.find_by_id(id_cliente)
            if not cliente:
                raise ServiceException(f"Cliente con ID {id_cliente} no encontrado")
            
            return self._cliente_repo.delete(id_cliente)
            
        except RepositoryException as e:
            raise ServiceException(f"Error al eliminar cliente: {str(e)}")


class ServiceException(Exception):
    """Excepción para errores en la capa de servicios"""
    pass

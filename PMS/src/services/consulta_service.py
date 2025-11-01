"""
ConsultaService - Servicio para consultas de todas las tablas
"""
from typing import List, Dict, Any
from datetime import date
from repositories import (
    ClienteRepository,
    ReservaRepository,
    HotelRepository,
    CiudadRepository,
    TipoHabitacionRepository,
    RegimenRepository,
    ContratoRepository,
    DisponibilidadRepository,
    RepositoryException
)
from domain import Cliente, Reserva, Hotel, Ciudad, TipoHabitacion, Regimen, Contrato
from services.cliente_service import ServiceException


class ConsultaService:
    """
    Servicio para consultas de todas las entidades del sistema
    Principio de Responsabilidad Única: Solo consultas
    """
    
    def __init__(
        self,
        cliente_repo: ClienteRepository,
        reserva_repo: ReservaRepository,
        hotel_repo: HotelRepository,
        ciudad_repo: CiudadRepository,
        tipo_hab_repo: TipoHabitacionRepository,
        regimen_repo: RegimenRepository,
        contrato_repo: ContratoRepository,
        disponibilidad_repo: DisponibilidadRepository
    ):
        """Constructor con inyección de dependencias"""
        self._cliente_repo = cliente_repo
        self._reserva_repo = reserva_repo
        self._hotel_repo = hotel_repo
        self._ciudad_repo = ciudad_repo
        self._tipo_hab_repo = tipo_hab_repo
        self._regimen_repo = regimen_repo
        self._contrato_repo = contrato_repo
        self._disponibilidad_repo = disponibilidad_repo
    
    def consultar_clientes(self) -> List[Cliente]:
        """Consulta todos los clientes"""
        try:
            return self._cliente_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar clientes: {str(e)}")
    
    def consultar_reservas(self) -> List[Reserva]:
        """Consulta todas las reservas"""
        try:
            return self._reserva_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar reservas: {str(e)}")
    
    def obtener_hoteles(self) -> List[Hotel]:
        """Consulta todos los hoteles"""
        try:
            return self._hotel_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar hoteles: {str(e)}")
    
    def consultar_ciudades(self) -> List[Ciudad]:
        """Consulta todas las ciudades"""
        try:
            return self._ciudad_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar ciudades: {str(e)}")
    
    def consultar_tipos_habitacion(self) -> List[TipoHabitacion]:
        """Consulta todos los tipos de habitación"""
        try:
            return self._tipo_hab_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar tipos de habitación: {str(e)}")
    
    def consultar_regimenes(self) -> List[Regimen]:
        """Consulta todos los regímenes"""
        try:
            return self._regimen_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar regímenes: {str(e)}")
    
    def consultar_contratos(self) -> List[Contrato]:
        """Consulta todos los contratos"""
        try:
            return self._contrato_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar contratos: {str(e)}")
    
    def buscar_contrato_por_id(self, id_contrato: int) -> Contrato:
        """Busca un contrato específico"""
        try:
            contrato = self._contrato_repo.find_by_id(id_contrato)
            if not contrato:
                raise ServiceException(f"Contrato con ID {id_contrato} no encontrado")
            return contrato
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar contrato: {str(e)}")
    
    def buscar_cliente_por_id(self, id_cliente: int) -> Cliente:
        """Busca un cliente específico"""
        try:
            cliente = self._cliente_repo.find_by_id(id_cliente)
            if not cliente:
                raise ServiceException(f"Cliente con ID {id_cliente} no encontrado")
            return cliente
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar cliente: {str(e)}")
    
    def buscar_reserva_por_id(self, id_reserva: int) -> Reserva:
        """Busca una reserva específica"""
        try:
            reserva = self._reserva_repo.find_by_id(id_reserva)
            if not reserva:
                raise ServiceException(f"Reserva con ID {id_reserva} no encontrada")
            return reserva
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar reserva: {str(e)}")
    
    def buscar_hotel_por_id(self, id_hotel: int) -> Hotel:
        """Busca un hotel específico"""
        try:
            hotel = self._hotel_repo.find_by_id(id_hotel)
            if not hotel:
                raise ServiceException(f"Hotel con ID {id_hotel} no encontrado")
            return hotel
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar hotel: {str(e)}")
    
    def consultar_reservas_por_cliente(self, id_cliente: int) -> List[Reserva]:
        """Consulta reservas de un cliente específico"""
        try:
            return self._reserva_repo.find_by_cliente(id_cliente)
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar reservas del cliente: {str(e)}")
    
    def consultar_hoteles_por_ciudad(self, id_ciudad: int) -> List[Hotel]:
        """Consulta hoteles de una ciudad específica"""
        try:
            return self._hotel_repo.find_by_ciudad(id_ciudad)
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar hoteles de la ciudad: {str(e)}")
    
    def consultar_disponibilidad_ciudad(
        self,
        ciudad: str,
        fecha_entrada: date,
        fecha_salida: date
    ) -> List[Dict[str, Any]]:
        """
        Consulta disponibilidad en una ciudad
        
        Args:
            ciudad: Nombre de la ciudad
            fecha_entrada: Fecha de entrada
            fecha_salida: Fecha de salida
            
        Returns:
            Lista de hoteles con disponibilidad
        """
        try:
            return self._disponibilidad_repo.consultar_por_ciudad(
                ciudad, fecha_entrada, fecha_salida
            )
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar disponibilidad: {str(e)}")
    
    def consultar_disponibilidad_hotel(
        self,
        hotel: str,
        fecha_entrada: date,
        fecha_salida: date
    ) -> Dict[str, Any]:
        """
        Consulta disponibilidad en un hotel específico
        
        Args:
            hotel: Nombre del hotel
            fecha_entrada: Fecha de entrada
            fecha_salida: Fecha de salida
            
        Returns:
            Información del hotel con tipos disponibles
        """
        try:
            return self._disponibilidad_repo.consultar_por_hotel(
                hotel, fecha_entrada, fecha_salida
            )
        except RepositoryException as e:
            raise ServiceException(f"Error al consultar disponibilidad: {str(e)}")

"""
ReservaService - Lógica de negocio para gestión de reservas
"""
from typing import List, Optional
from datetime import datetime
from repositories import ReservaRepository, HotelRepository, ContratoRepository, RepositoryException
from domain import Reserva, TipoReserva
from utils.validators import validar_rango_fechas, validar_fecha_futura
from services.cliente_service import ServiceException


class ReservaService:
    """Servicio para gestionar reservas"""
    
    def __init__(
        self,
        reserva_repo: ReservaRepository,
        hotel_repo: HotelRepository,
        contrato_repo: ContratoRepository
    ):
        """
        Constructor con inyección de dependencias
        
        Args:
            reserva_repo: Repositorio de reservas
            hotel_repo: Repositorio de hoteles
            contrato_repo: Repositorio de contratos
        """
        self._reserva_repo = reserva_repo
        self._hotel_repo = hotel_repo
        self._contrato_repo = contrato_repo
    
    def listar_todas(self) -> List[Reserva]:
        """Obtiene todas las reservas"""
        try:
            return self._reserva_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al listar reservas: {str(e)}")
    
    def buscar_por_id(self, id_reserva: int) -> Optional[Reserva]:
        """Busca una reserva por ID"""
        try:
            return self._reserva_repo.find_by_id(id_reserva)
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar reserva: {str(e)}")
    
    def listar_reservas(self, id_cliente: int = None) -> List[Reserva]:
        """Obtiene reservas, opcionalmente filtradas por cliente"""
        try:
            if id_cliente:
                return self._reserva_repo.find_by_cliente(id_cliente)
            return self._reserva_repo.find_all()
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar reservas del cliente: {str(e)}")
    
    def listar_activas(self) -> List[Reserva]:
        """Obtiene reservas activas"""
        try:
            return self._reserva_repo.find_activas()
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar reservas activas: {str(e)}")
    
    def crear_reserva(
        self,
        id_cliente: int,
        id_hotel: int,
        id_tipo_habitacion: int,
        id_regimen: int,
        fecha_entrada: str,
        fecha_salida: str,
        tipo: str = "Estandar",
        cliente_paga: bool = True,
        precio_regimen: float = 0.0
    ) -> Reserva:
        """
        Crea una nueva reserva con validaciones
        
        Args:
            id_cliente: ID del cliente
            id_hotel: ID del hotel
            id_tipo_habitacion: ID del tipo de habitación
            id_regimen: ID del régimen
            fecha_entrada: Fecha de entrada (YYYY-MM-DD)
            fecha_salida: Fecha de salida (YYYY-MM-DD)
            tipo: Tipo de reserva (Estandar/Directa)
            cliente_paga: Si el cliente paga o agencia
            precio_regimen: Precio del régimen
            
        Returns:
            Reserva creada
        """
        # Validar fechas
        if not validar_rango_fechas(fecha_entrada, fecha_salida):
            raise ServiceException("La fecha de salida debe ser posterior a la de entrada")
        
        if not validar_fecha_futura(fecha_entrada):
            raise ServiceException("La fecha de entrada debe ser futura")
        
        # Validar tipo
        try:
            tipo_enum = TipoReserva[tipo]
        except KeyError:
            raise ServiceException(f"Tipo de reserva inválido. Debe ser 'Estandar' o 'Directa'")
        
        try:
            # Crear entidad
            reserva = Reserva(
                id_cliente=id_cliente,
                id_hotel=id_hotel,
                id_tipo_habitacion=id_tipo_habitacion,
                id_regimen=id_regimen,
                fecha_entrada=fecha_entrada,
                fecha_salida=fecha_salida,
                tipo=tipo_enum,
                cliente_paga=cliente_paga,
                precio_regimen=precio_regimen
            )
            
            # Persistir
            return self._reserva_repo.create(reserva)
            
        except RepositoryException as e:
            raise ServiceException(f"Error al crear reserva: {str(e)}")
        except ValueError as e:
            raise ServiceException(f"Datos inválidos: {str(e)}")
    
    def modificar_reserva(
        self,
        id_reserva: int,
        fecha_entrada: str = None,
        fecha_salida: str = None,
        id_tipo_habitacion: int = None,
        id_regimen: int = None
    ) -> Reserva:
        """
        Modifica una reserva existente
        
        Args:
            id_reserva: ID de la reserva
            fecha_entrada: Nueva fecha de entrada (opcional)
            fecha_salida: Nueva fecha de salida (opcional)
            id_tipo_habitacion: Nuevo tipo de habitación (opcional)
            id_regimen: Nuevo régimen (opcional)
            
        Returns:
            Reserva actualizada
        """
        try:
            # Obtener reserva
            reserva = self._reserva_repo.find_by_id(id_reserva)
            if not reserva:
                raise ServiceException(f"Reserva con ID {id_reserva} no encontrada")
            
            # Verificar que se puede modificar
            if not reserva.puede_modificarse():
                raise ServiceException("No se puede modificar una reserva ya iniciada o finalizada")
            
            # Actualizar campos
            if fecha_entrada:
                reserva.fecha_entrada = fecha_entrada
            
            if fecha_salida:
                reserva.fecha_salida = fecha_salida
            
            if id_tipo_habitacion:
                reserva.id_tipo_habitacion = id_tipo_habitacion
            
            if id_regimen:
                reserva.id_regimen = id_regimen
            
            # Validar nuevas fechas
            if not validar_rango_fechas(reserva.fecha_entrada, reserva.fecha_salida):
                raise ServiceException("La fecha de salida debe ser posterior a la de entrada")
            
            return self._reserva_repo.update(id_reserva, reserva)
            
        except RepositoryException as e:
            raise ServiceException(f"Error al modificar reserva: {str(e)}")
        except ValueError as e:
            raise ServiceException(f"Datos inválidos: {str(e)}")
    
    def eliminar_reserva(self, id_reserva: int) -> bool:
        """Elimina una reserva"""
        try:
            reserva = self._reserva_repo.find_by_id(id_reserva)
            if not reserva:
                raise ServiceException(f"Reserva con ID {id_reserva} no encontrada")
            
            if not reserva.puede_modificarse():
                raise ServiceException("No se puede eliminar una reserva ya iniciada o finalizada")
            
            return self._reserva_repo.delete(id_reserva)
            
        except RepositoryException as e:
            raise ServiceException(f"Error al eliminar reserva: {str(e)}")
    
    def hacer_checkin(self, id_reserva: int, numero_habitacion: str, monto_total: float) -> dict:
        """
        Realiza check-in de una reserva creando un contrato
        
        Args:
            id_reserva: ID de la reserva
            numero_habitacion: Número de habitación asignada
            monto_total: Monto total del contrato
            
        Returns:
            Diccionario con success, contrato y message
        """
        try:
            from domain import Contrato
            
            # Crear contrato
            contrato = Contrato(
                id_reserva=id_reserva,
                numero_habitacion=numero_habitacion,
                monto_total=monto_total
            )
            
            # Persistir (esto hace el check-in automáticamente)
            contrato_creado = self._contrato_repo.create(contrato)
            
            return {
                'success': True,
                'contrato': contrato_creado,
                'message': 'Check-in realizado correctamente'
            }
        except RepositoryException as e:
            raise ServiceException(f"Error al hacer check-in: {str(e)}")
        except ValueError as e:
            raise ServiceException(f"Datos inválidos: {str(e)}")
    
    def hacer_checkout(self, id_contrato: int) -> dict:
        """
        Realiza check-out de un contrato
        
        Args:
            id_contrato: ID del contrato
            
        Returns:
            Diccionario con success, contrato y message
        """
        try:
            contrato = self._contrato_repo.checkout(id_contrato)
            return {
                'success': True,
                'contrato': contrato,
                'message': 'Check-out realizado correctamente'
            }
        except RepositoryException as e:
            raise ServiceException(f"Error al hacer check-out: {str(e)}")
    
    def buscar_contrato_por_reserva(self, id_reserva: int):
        """Busca el contrato de una reserva"""
        try:
            return self._contrato_repo.find_by_reserva(id_reserva)
        except RepositoryException as e:
            raise ServiceException(f"Error al buscar contrato: {str(e)}")
    
    def cancelar_reserva(self, id_reserva: int) -> dict:
        """
        Cancela una reserva (cambia su estado a Cancelada)
        
        Args:
            id_reserva: ID de la reserva a cancelar
            
        Returns:
            Diccionario con success, reserva y message
        """
        try:
            # Buscar la reserva
            reserva = self._reserva_repo.find_by_id(id_reserva)
            
            if not reserva:
                raise ServiceException(f"Reserva #{id_reserva} no encontrada")
            
            # Validar que puede cancelarse
            if not reserva.puede_cancelarse():
                if reserva.esta_cancelada():
                    raise ServiceException("La reserva ya está cancelada")
                elif reserva.tiene_contrato:
                    raise ServiceException("No se puede cancelar una reserva con check-in realizado")
                else:
                    raise ServiceException("No se puede cancelar esta reserva")
            
            # Cancelar
            reserva_cancelada = self._reserva_repo.cancelar(id_reserva)
            
            return {
                'success': True,
                'reserva': reserva_cancelada,
                'message': 'Reserva cancelada exitosamente'
            }
        except RepositoryException as e:
            raise ServiceException(f"Error al cancelar reserva: {str(e)}")
        except ServiceException:
            raise
        except Exception as e:
            raise ServiceException(f"Error inesperado al cancelar: {str(e)}")

"""
Entidad Reserva - Domain Model
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

from .cliente import Cliente
from .hotel import PrecioRegimen, TipoHabitacion


class TipoReserva(Enum):
    """Tipos de reserva disponibles"""
    RESERVA = "Reserva"
    WALKIN = "Walkin"


class EstadoReserva(Enum):
    """Estados posibles de una reserva"""
    ACTIVA = "Activa"
    CANCELADA = "Cancelada"


@dataclass
class DetallePrecio:
    """Value Object para los detalles de precio de una reserva"""
    precio_habitacion_por_noche: float
    precio_regimen_por_noche: float
    numero_noches: int
    subtotal_habitacion: float
    subtotal_regimen: float
    descuentos: float
    precio_total: float
    
    @classmethod
    def from_dict(cls, data: dict) -> 'DetallePrecio':
        return cls(
            precio_habitacion_por_noche=float(data.get('precioHabitacionPorNoche', 0)),
            precio_regimen_por_noche=float(data.get('precioRegimenPorNoche', 0)),
            numero_noches=int(data.get('numeroNoches', 0)),
            subtotal_habitacion=float(data.get('subtotalHabitacion', 0)),
            subtotal_regimen=float(data.get('subtotalRegimen', 0)),
            descuentos=float(data.get('descuentos', 0)),
            precio_total=float(data.get('precioTotal', 0))
        )


@dataclass
class Reserva:
    """
    Representa una reserva de hotel.
    Agregado raíz que contiene la lógica de negocio de las reservas.
    """
    fecha_entrada: date
    fecha_salida: date
    tipo: TipoReserva
    estado: EstadoReserva = EstadoReserva.ACTIVA
    cliente_paga: Optional[Cliente] = None
    precio_regimen: Optional[PrecioRegimen] = None
    id_reserva: Optional[int] = None
    canal_reserva: Optional[str] = None
    huespedes: List[Cliente] = field(default_factory=list)
    detalle_precio: Optional[DetallePrecio] = None
    tiene_contrato: bool = False
    
    # Compatibility fields for GUI and services
    id_cliente: Optional[int] = None
    id_hotel: Optional[int] = None
    id_tipo_habitacion: Optional[int] = None
    id_regimen: Optional[int] = None
    
    def __post_init__(self):
        """Validaciones del dominio"""
        if self.fecha_salida <= self.fecha_entrada:
            raise ValueError("La fecha de salida debe ser posterior a la fecha de entrada")
        
        if not self.huespedes:
            # Si no hay huéspedes y cliente_paga existe, añadirlo
            if self.cliente_paga:
                self.huespedes = [self.cliente_paga]
    
    @property
    def numero_noches(self) -> int:
        """Calcula el número de noches"""
        return (self.fecha_salida - self.fecha_entrada).days
    
    @property
    def esta_confirmada(self) -> bool:
        """Indica si la reserva está confirmada (tiene contrato)"""
        return self.tiene_contrato
    
    def puede_modificarse(self) -> bool:
        """
        Determina si la reserva puede ser modificada.
        Regla de negocio: No se puede modificar si ya tiene check-in.
        """
        return not self.tiene_contrato
    
    def puede_cancelarse(self) -> bool:
        """
        Determina si la reserva puede ser cancelada.
        Regla de negocio: No se puede cancelar si ya tiene check-in o está cancelada.
        """
        return not self.tiene_contrato and self.estado == EstadoReserva.ACTIVA
    
    def esta_cancelada(self) -> bool:
        """Indica si la reserva está cancelada"""
        return self.estado == EstadoReserva.CANCELADA
    
    def agregar_huesped(self, cliente: Cliente) -> None:
        """Agrega un huésped a la reserva"""
        if cliente not in self.huespedes:
            self.huespedes.append(cliente)
    
    def to_dict(self) -> dict:
        """Convierte la reserva a diccionario para la API"""
        return {
            "fechaEntrada": self.fecha_entrada.isoformat(),
            "fechaSalida": self.fecha_salida.isoformat(),
            "tipo": self.tipo.value,
            "canalReserva": self.canal_reserva,
            "clientePaga": self.cliente_paga.to_dict(),
            "huespedes": [h.to_dict() for h in self.huespedes]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Reserva':
        """Crea una reserva desde un diccionario de la API"""
        # Parsear fechas
        fecha_entrada_str = data['fechaEntrada']
        fecha_salida_str = data['fechaSalida']
        
        # Manejar diferentes formatos de fecha
        if 'T' in fecha_entrada_str:
            fecha_entrada = datetime.fromisoformat(fecha_entrada_str.replace('Z', '+00:00')).date()
            fecha_salida = datetime.fromisoformat(fecha_salida_str.replace('Z', '+00:00')).date()
        else:
            fecha_entrada = datetime.strptime(fecha_entrada_str, '%Y-%m-%d').date()
            fecha_salida = datetime.strptime(fecha_salida_str, '%Y-%m-%d').date()
        
        # Cliente que paga (puede ser None o un objeto)
        cliente_paga = None
        if data.get('clientePaga'):
            cliente_paga = Cliente.from_dict(data['clientePaga'])
        
        # Precio régimen (puede ser None o un objeto)
        precio_regimen = None
        if data.get('precioRegimen'):
            precio_regimen = PrecioRegimen.from_dict(data['precioRegimen'])
        
        # Tipo de reserva
        tipo_str = data.get('tipo', 'Reserva')
        tipo = TipoReserva.RESERVA if tipo_str == 'Reserva' else TipoReserva.WALKIN
        
        # Estado de reserva
        estado_str = data.get('estado', 'Activa')
        estado = EstadoReserva.ACTIVA if estado_str == 'Activa' else EstadoReserva.CANCELADA
        
        # Huéspedes (puede estar vacío)
        huespedes = []
        if data.get('reservaHuespedes'):
            huespedes = [Cliente.from_dict(h['cliente']) for h in data['reservaHuespedes']]
        
        # Detalle de precio
        detalle_precio = None
        if data.get('precioDetalle'):
            detalle_precio = DetallePrecio.from_dict(data['precioDetalle'])
        
        # Extract IDs for compatibility
        id_cliente = data.get('idCliente_paga') or data.get('idCliente')
        if not id_cliente and cliente_paga:
            id_cliente = cliente_paga.id_cliente
            
        id_hotel = data.get('idHotel')
        if not id_hotel and precio_regimen and precio_regimen.hotel:
            id_hotel = precio_regimen.hotel.id_hotel
            
        id_tipo_habitacion = data.get('idTipoHabitacion')
        
        id_regimen = data.get('idRegimen')
        if not id_regimen and precio_regimen and precio_regimen.regimen:
            id_regimen = precio_regimen.regimen.id_regimen
        
        # Get idPrecioRegimen
        id_precio_regimen = data.get('idPrecioRegimen')
        
        return cls(
            id_reserva=data.get('idReserva'),
            fecha_entrada=fecha_entrada,
            fecha_salida=fecha_salida,
            tipo=tipo,
            estado=estado,
            canal_reserva=data.get('canalReserva'),
            cliente_paga=cliente_paga,
            precio_regimen=precio_regimen,
            huespedes=huespedes,
            detalle_precio=detalle_precio,
            tiene_contrato=data.get('contrato') is not None,
            id_cliente=id_cliente,
            id_hotel=id_hotel,
            id_tipo_habitacion=id_tipo_habitacion,
            id_regimen=id_regimen
        )
    
    def __str__(self) -> str:
        cliente_nombre = self.cliente_paga.nombre_completo if self.cliente_paga else f"Cliente #{self.id_cliente}"
        return f"Reserva #{self.id_reserva} - {cliente_nombre} ({self.fecha_entrada} a {self.fecha_salida})"
    
    def __repr__(self) -> str:
        cliente_nombre = self.cliente_paga.nombre_completo if self.cliente_paga else f"Cliente #{self.id_cliente}"
        return f"Reserva(id={self.id_reserva}, cliente='{cliente_nombre}', noches={self.numero_noches})"

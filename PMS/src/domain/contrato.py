"""
Entidad Contrato - Domain Model
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from .reserva import Reserva


@dataclass
class Contrato:
    """
    Representa un contrato de estancia en el hotel.
    Entidad que gestiona el check-in y check-out.
    """
    id_reserva: int
    numero_habitacion: str
    monto_total: float
    id_contrato: Optional[int] = None
    fecha_checkin: Optional[datetime] = None
    fecha_checkout: Optional[datetime] = None
    reserva: Optional[Reserva] = None
    
    def __post_init__(self):
        """Validaciones del dominio"""
        # Solo validar monto si es un contrato nuevo (sin ID)
        # Los contratos existentes pueden tener monto 0 por datos históricos
        if self.id_contrato is None and self.monto_total <= 0:
            raise ValueError("El monto total debe ser mayor a 0")
        if not self.numero_habitacion or not self.numero_habitacion.strip():
            raise ValueError("El número de habitación no puede estar vacío")
    
    @property
    def esta_activo(self) -> bool:
        """Indica si el contrato está activo (tiene check-in pero no check-out)"""
        return self.fecha_checkin is not None and self.fecha_checkout is None
    
    @property
    def esta_finalizado(self) -> bool:
        """Indica si el contrato está finalizado (tiene check-out)"""
        return self.fecha_checkout is not None
    
    @property
    def estado(self) -> str:
        """Retorna el estado actual del contrato"""
        if self.fecha_checkout:
            return "Finalizado"
        elif self.fecha_checkin:
            return "En curso"
        else:
            return "Pendiente"
    
    def puede_hacer_checkin(self) -> bool:
        """Determina si se puede hacer check-in"""
        return self.fecha_checkin is None
    
    def puede_hacer_checkout(self) -> bool:
        """Determina si se puede hacer check-out"""
        return self.fecha_checkin is not None and self.fecha_checkout is None
    
    def to_dict(self) -> dict:
        """Convierte el contrato a diccionario para la API"""
        return {
            "idReserva": self.id_reserva,
            "numeroHabitacion": self.numero_habitacion,
            "montoTotal": self.monto_total
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Contrato':
        """Crea un contrato desde un diccionario de la API"""
        # Asegurar que data sea un diccionario
        if not isinstance(data, dict):
            raise ValueError(f"Se esperaba un diccionario, se recibió {type(data)}")
        
        # Parsear fechas - manejar diferentes formatos
        fecha_checkin = None
        fecha_checkout = None
        
        if data.get('fechaCheckIn'):
            fecha_str = data['fechaCheckIn']
            if isinstance(fecha_str, str):
                try:
                    if 'T' in fecha_str:
                        fecha_checkin = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                    else:
                        fecha_checkin = datetime.strptime(fecha_str, '%Y-%m-%d')
                except Exception:
                    pass
        
        if data.get('fechaCheckOut'):
            fecha_str = data['fechaCheckOut']
            if isinstance(fecha_str, str):
                try:
                    if 'T' in fecha_str:
                        fecha_checkout = datetime.fromisoformat(fecha_str.replace('Z', '+00:00'))
                    else:
                        fecha_checkout = datetime.strptime(fecha_str, '%Y-%m-%d')
                except Exception:
                    pass
        
        # Reserva (si viene incluida)
        reserva = None
        if data.get('reserva'):
            reserva_data = data['reserva']
            if isinstance(reserva_data, dict):
                from .reserva import Reserva
                try:
                    reserva = Reserva.from_dict(reserva_data)
                except Exception:
                    pass
        
        # Monto total - asegurar que sea un número válido
        monto = 0.0
        try:
            monto = float(data.get('montoTotal', 0))
        except (ValueError, TypeError):
            monto = 0.0
        
        return cls(
            id_contrato=data.get('idContrato'),
            id_reserva=data.get('idReserva'),
            numero_habitacion=str(data.get('numeroHabitacion', '')),
            monto_total=monto,
            fecha_checkin=fecha_checkin,
            fecha_checkout=fecha_checkout,
            reserva=reserva
        )
    
    def __str__(self) -> str:
        return f"Contrato #{self.id_contrato} - Habitación {self.numero_habitacion} ({self.estado})"
    
    def __repr__(self) -> str:
        return f"Contrato(id={self.id_contrato}, habitacion='{self.numero_habitacion}', estado='{self.estado}')"

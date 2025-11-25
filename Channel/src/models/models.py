"""
Channel Manager - Modelos SQLAlchemy
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    """Modelo de Usuario"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    nombre = Column(String(200))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    hoteles = relationship("Hotel", back_populates="usuario")


class Hotel(Base):
    """Modelo de Hotel - pertenece a un usuario"""
    __tablename__ = "hoteles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    nombre = Column(String(200), nullable=False)
    direccion = Column(String(500))
    ciudad = Column(String(100))
    pais = Column(String(100), default="España")
    codigo_postal = Column(String(20))
    telefono = Column(String(50))
    email = Column(String(200))
    web = Column(String(300))
    estrellas = Column(Integer, default=3)
    descripcion = Column(String(1000))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    usuario = relationship("User", back_populates="hoteles")
    habitaciones = relationship("TipoHabitacion", back_populates="hotel", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="hotel", cascade="all, delete-orphan")


class TipoHabitacion(Base):
    """Modelo de Tipo de Habitación"""
    __tablename__ = "tipos_habitacion"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hoteles.id"), nullable=False)
    codigo = Column(String(20))
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(500))
    capacidad_min = Column(Integer, default=1)
    capacidad_max = Column(Integer, default=2)
    camas = Column(String(100))  # Ej: "1 doble" o "2 individuales"
    superficie = Column(Integer)  # metros cuadrados
    servicios = Column(String(500))  # Ej: "WiFi, TV, Minibar, Aire acondicionado"
    activo = Column(Boolean, default=True)
    
    # Relaciones
    hotel = relationship("Hotel", back_populates="habitaciones")
    disponibilidades = relationship("Disponibilidad", back_populates="tipo_habitacion", cascade="all, delete-orphan")
    reservas = relationship("Reserva", back_populates="tipo_habitacion", cascade="all, delete-orphan")


class Disponibilidad(Base):
    """Modelo de Disponibilidad por fecha"""
    __tablename__ = "disponibilidad"

    id = Column(Integer, primary_key=True, index=True)
    tipo_habitacion_id = Column(Integer, ForeignKey("tipos_habitacion.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    cantidad_disponible = Column(Integer, default=0)
    precio = Column(Float)
    cerrado = Column(Boolean, default=False)  # Para cerrar ventas en una fecha
    
    # Relaciones
    tipo_habitacion = relationship("TipoHabitacion", back_populates="disponibilidades")


class Reserva(Base):
    """
    Modelo de Reserva - Tracking de reservas realizadas desde PMS
    Este modelo permite al Channel Manager contabilizar y hacer seguimiento
    de todas las reservas que se han realizado a través del sistema.
    """
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    hotel_id = Column(Integer, ForeignKey("hoteles.id"), nullable=False)
    tipo_habitacion_id = Column(Integer, ForeignKey("tipos_habitacion.id"), nullable=False)
    
    # Datos de la reserva
    fecha_entrada = Column(Date, nullable=False)
    fecha_salida = Column(Date, nullable=False)
    num_habitaciones = Column(Integer, default=1)
    num_huespedes = Column(Integer, default=1)
    precio_total = Column(Float)
    
    # Información del cliente 
    cliente_nombre = Column(String(200))
    cliente_email = Column(String(200))
    cliente_telefono = Column(String(50))
    
    # Estado y tracking
    estado = Column(String(20), default="confirmada")  # confirmada, cancelada, completada
    reserva_pms_id = Column(String(100))  
    notas = Column(String(1000))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    fecha_cancelacion = Column(DateTime, nullable=True)
    
    # Relaciones
    hotel = relationship("Hotel", back_populates="reservas")
    tipo_habitacion = relationship("TipoHabitacion", back_populates="reservas")

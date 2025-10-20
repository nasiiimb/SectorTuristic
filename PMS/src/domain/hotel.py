"""
Entidades Hotel - Domain Models
"""
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Ciudad:
    """Representa una ciudad donde opera la cadena"""
    nombre: str
    pais: str
    id_ciudad: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Ciudad':
        return cls(
            id_ciudad=data.get('idCiudad'),
            nombre=data.get('nombre', ''),
            pais=data.get('pais', '')
        )
    
    def __str__(self) -> str:
        return f"{self.nombre}, {self.pais}"


@dataclass
class Hotel:
    """Representa un hotel de la cadena"""
    nombre: str
    ubicacion: str
    categoria: int
    ciudad: Ciudad
    id_hotel: Optional[int] = None
    precios_regimen: Optional[List['PrecioRegimen']] = None
    
    def __post_init__(self):
        if self.categoria < 1 or self.categoria > 5:
            raise ValueError("La categoría debe estar entre 1 y 5")
        if self.precios_regimen is None:
            self.precios_regimen = []
    
    @property
    def estrellas(self) -> str:
        """Retorna la representación en estrellas"""
        return "★" * self.categoria
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Hotel':
        ciudad_data = data.get('ciudad', {})
        ciudad = Ciudad.from_dict(ciudad_data) if ciudad_data else Ciudad("", "")
        
        # Parsear precios_regimen si existen (evitando recursión)
        precios_regimen = []
        if 'preciosRegimen' in data and data['preciosRegimen']:
            # Importación local para evitar recursión circular
            for precio_data in data['preciosRegimen']:
                # No parsear el hotel completo para evitar recursión
                regimen = Regimen.from_dict(precio_data.get('regimen', {}))
                precio_regimen = type('PrecioRegimen', (), {
                    'id_precio_regimen': precio_data.get('idPrecioRegimen'),
                    'regimen': regimen,
                    'precio': float(precio_data.get('precio', 0))
                })()
                precios_regimen.append(precio_regimen)
        
        return cls(
            id_hotel=data.get('idHotel'),
            nombre=data.get('nombre', ''),
            ubicacion=data.get('ubicacion', ''),
            categoria=data.get('categoria', 3),
            ciudad=ciudad,
            precios_regimen=precios_regimen
        )
    
    def __str__(self) -> str:
        return f"{self.nombre} ({self.estrellas}) - {self.ciudad}"


@dataclass
class TipoHabitacion:
    """Representa un tipo de habitación"""
    categoria: str
    camas_individuales: int = 0
    camas_dobles: int = 0
    id_tipo_habitacion: Optional[int] = None
    
    @property
    def capacidad_total(self) -> int:
        """Calcula la capacidad total de personas"""
        return self.camas_individuales + (self.camas_dobles * 2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TipoHabitacion':
        return cls(
            id_tipo_habitacion=data.get('idTipoHabitacion'),
            categoria=data.get('categoria', ''),
            camas_individuales=data.get('camasIndividuales', 0),
            camas_dobles=data.get('camasDobles', 0)
        )
    
    def __str__(self) -> str:
        return f"{self.categoria} (Capacidad: {self.capacidad_total} personas)"


@dataclass
class Regimen:
    """Representa un régimen de alimentación"""
    codigo: str
    id_regimen: Optional[int] = None
    
    @property
    def descripcion(self) -> str:
        """Retorna la descripción del régimen"""
        descripciones = {
            "SA": "Solo Alojamiento",
            "AD": "Alojamiento y Desayuno",
            "MP": "Media Pensión",
            "PC": "Pensión Completa",
            "TI": "Todo Incluido"
        }
        return descripciones.get(self.codigo, "Desconocido")
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Regimen':
        return cls(
            id_regimen=data.get('idRegimen'),
            codigo=data.get('codigo', '')
        )
    
    def __str__(self) -> str:
        return f"{self.codigo} - {self.descripcion}"


@dataclass
class PrecioRegimen:
    """Representa el precio de un régimen en un hotel"""
    hotel: Hotel
    regimen: Regimen
    precio: float
    id_precio_regimen: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PrecioRegimen':
        hotel = Hotel.from_dict(data.get('hotel', {}))
        regimen = Regimen.from_dict(data.get('regimen', {}))
        
        return cls(
            id_precio_regimen=data.get('idPrecioRegimen'),
            hotel=hotel,
            regimen=regimen,
            precio=float(data.get('precio', 0))
        )

"""
Entidad Cliente - Domain Model
"""
from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class Cliente:
    """
    Representa un cliente del hotel.
    Entidad del dominio que encapsula los datos y comportamiento de un cliente.
    """
    nombre: str
    apellidos: str
    correo_electronico: str
    dni: str
    id_cliente: Optional[int] = None
    fecha_nacimiento: Optional[date] = None
    
    def __post_init__(self):
        """Validaciones del dominio"""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not self.apellidos or not self.apellidos.strip():
            raise ValueError("Los apellidos no pueden estar vacíos")
        # Validación flexible de correo: solo verificar si existe, permitir datos históricos
        # Para clientes nuevos (sin id_cliente), la validación será más estricta en el servicio
        if not self.correo_electronico:
            raise ValueError("El correo electrónico no puede estar vacío")
        if not self.dni or not self.dni.strip():
            raise ValueError("El DNI no puede estar vacío")
    
    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del cliente"""
        return f"{self.nombre} {self.apellidos}"
    
    def actualizar_datos(
        self,
        nombre: Optional[str] = None,
        apellidos: Optional[str] = None,
        correo_electronico: Optional[str] = None
    ) -> None:
        """
        Actualiza los datos del cliente.
        Método del dominio que encapsula la lógica de actualización.
        """
        if nombre:
            self.nombre = nombre
        if apellidos:
            self.apellidos = apellidos
        if correo_electronico:
            if not correo_electronico.strip():
                raise ValueError("El correo electrónico no puede estar vacío")
            self.correo_electronico = correo_electronico
    
    def to_dict(self) -> dict:
        """Convierte el cliente a diccionario para la API"""
        data = {
            "nombre": self.nombre,
            "apellidos": self.apellidos,
            "correoElectronico": self.correo_electronico,
            "DNI": self.dni
        }
        if self.fecha_nacimiento:
            data["fechaDeNacimiento"] = self.fecha_nacimiento.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cliente':
        """Crea un cliente desde un diccionario de la API"""
        fecha_nac = None
        if data.get('fechaDeNacimiento'):
            from datetime import datetime
            fecha_str = data['fechaDeNacimiento']
            # Intentar parsear diferentes formatos
            for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]:
                try:
                    fecha_nac = datetime.strptime(fecha_str, fmt).date()
                    break
                except:
                    continue
        
        return cls(
            id_cliente=data.get('idCliente'),
            nombre=data.get('nombre', ''),
            apellidos=data.get('apellidos', ''),
            correo_electronico=data.get('correoElectronico', ''),
            dni=data.get('DNI', ''),
            fecha_nacimiento=fecha_nac
        )
    
    def __str__(self) -> str:
        return f"Cliente({self.nombre_completo}, DNI: {self.dni})"
    
    def __repr__(self) -> str:
        return f"Cliente(id={self.id_cliente}, nombre='{self.nombre_completo}')"

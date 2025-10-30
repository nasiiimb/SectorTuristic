"""
Validators - Funciones de validación
Principio de Responsabilidad Única: Solo validación de datos
"""
import re
from datetime import datetime, date
from typing import Optional


def validar_email(email: str) -> bool:
    """Valida formato de correo electrónico"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(patron, email))


def validar_dni(dni: str) -> bool:
    """Valida formato de DNI español (8 dígitos + letra)"""
    patron = r'^\d{8}[A-Z]$'
    if not re.match(patron, dni.upper()):
        return False
    
    # Validar letra del DNI
    letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
    numero = int(dni[:8])
    letra_calculada = letras[numero % 23]
    return dni[8].upper() == letra_calculada


def validar_fecha(fecha_str: str, formato: str = "%Y-%m-%d") -> bool:
    """Valida formato de fecha"""
    try:
        datetime.strptime(fecha_str, formato)
        return True
    except ValueError:
        return False


def validar_rango_fechas(fecha_entrada: str, fecha_salida: str) -> bool:
    """Valida que fecha_salida sea posterior a fecha_entrada"""
    try:
        entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d")
        salida = datetime.strptime(fecha_salida, "%Y-%m-%d")
        return salida > entrada
    except ValueError:
        return False


def validar_fecha_futura(fecha_str: str) -> bool:
    """Valida que la fecha sea futura"""
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        return fecha >= date.today()
    except ValueError:
        return False


def validar_numero_positivo(numero: float) -> bool:
    """Valida que el número sea positivo"""
    return numero > 0


def validar_estrellas(estrellas: int) -> bool:
    """Valida número de estrellas de hotel (1-5)"""
    return 1 <= estrellas <= 5


def validar_capacidad(capacidad: int) -> bool:
    """Valida capacidad de habitación (1-10)"""
    return 1 <= capacidad <= 10


def normalizar_dni(dni: str) -> str:
    """Normaliza DNI a formato estándar (mayúsculas, sin espacios)"""
    return dni.strip().upper()


def normalizar_email(email: str) -> str:
    """Normaliza email a formato estándar (minúsculas, sin espacios)"""
    return email.strip().lower()


def normalizar_texto(texto: str) -> str:
    """Normaliza texto (capitaliza primera letra, sin espacios extra)"""
    return ' '.join(texto.strip().split()).title()

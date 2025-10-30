"""
Console Utilities - Utilidades para interfaz de consola
Principio de Responsabilidad Única: Solo maneja I/O de consola
"""
import os
from typing import List, Any
from datetime import datetime
from colorama import Fore, Style, init
from tabulate import tabulate

# Inicializar colorama para Windows
init(autoreset=True)


class Colors:
    """Constantes de colores para la consola"""
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    INFO = Fore.BLUE
    RESET = Style.RESET_ALL


def clear_screen():
    """Limpia la pantalla"""
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    """Pausa hasta que el usuario presione Enter"""
    input(f"\n{Colors.INFO}Presiona Enter para continuar...{Colors.RESET}")


def print_header(text: str):
    """Imprime un encabezado destacado"""
    print(f"\n{Colors.HEADER}{'=' * 80}")
    print(f"{text.center(80)}")
    print(f"{'=' * 80}{Colors.RESET}\n")


def print_success(text: str):
    """Imprime mensaje de éxito"""
    print(f"{Colors.SUCCESS}✓ {text}{Colors.RESET}")


def print_error(text: str):
    """Imprime mensaje de error"""
    print(f"{Colors.ERROR}✗ {text}{Colors.RESET}")


def print_warning(text: str):
    """Imprime mensaje de advertencia"""
    print(f"{Colors.WARNING}⚠ {text}{Colors.RESET}")


def print_info(text: str):
    """Imprime mensaje informativo"""
    print(f"{Colors.INFO}ℹ {text}{Colors.RESET}")


def print_table(headers: List[str], rows: List[List[Any]], title: str = None):
    """Imprime una tabla formateada"""
    if title:
        print(f"\n{Colors.HEADER}{title}{Colors.RESET}")
    
    if not rows:
        print_warning("No hay datos para mostrar")
        return
    
    print(f"\n{tabulate(rows, headers=headers, tablefmt='grid')}\n")


def get_input(prompt: str, required: bool = True) -> str:
    """Obtiene entrada del usuario con validación"""
    while True:
        value = input(f"{Colors.INFO}{prompt}{Colors.RESET}").strip()
        if value or not required:
            return value
        print_error("Este campo es requerido")


def get_int_input(prompt: str, min_value: int = None, max_value: int = None) -> int:
    """Obtiene un número entero con validación"""
    while True:
        try:
            value = int(input(f"{Colors.INFO}{prompt}{Colors.RESET}").strip())
            if min_value is not None and value < min_value:
                print_error(f"El valor debe ser >= {min_value}")
                continue
            if max_value is not None and value > max_value:
                print_error(f"El valor debe be <= {max_value}")
                continue
            return value
        except ValueError:
            print_error("Ingresa un número válido")


def get_float_input(prompt: str, min_value: float = None) -> float:
    """Obtiene un número decimal con validación"""
    while True:
        try:
            value = float(input(f"{Colors.INFO}{prompt}{Colors.RESET}").strip())
            if min_value is not None and value < min_value:
                print_error(f"El valor debe ser >= {min_value}")
                continue
            return value
        except ValueError:
            print_error("Ingresa un número válido")


def get_date_input(prompt: str, format: str = "%Y-%m-%d") -> str:
    """Obtiene una fecha con validación"""
    while True:
        date_str = input(f"{Colors.INFO}{prompt} (DD/MM/YYYY): {Colors.RESET}").strip()
        try:
            dt = datetime.strptime(date_str, "%d/%m/%Y")
            return dt.strftime(format)
        except ValueError:
            print_error("Formato inválido. Usa DD/MM/YYYY")


def confirm(prompt: str) -> bool:
    """Pide confirmación al usuario"""
    while True:
        response = input(f"{Colors.WARNING}{prompt} (s/n): {Colors.RESET}").strip().lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print_error("Responde 's' o 'n'")

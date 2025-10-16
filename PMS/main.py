#!/usr/bin/env python3
"""
PMS - Property Management System
Interfaz Gráfica con tkinter
"""
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from infrastructure import Config, APIClient
from repositories import (
    ClienteRepository,
    ReservaRepository,
    HotelRepository,
    CiudadRepository,
    TipoHabitacionRepository,
    RegimenRepository,
    ContratoRepository,
    DisponibilidadRepository
)
from services import ClienteService, ReservaService, ConsultaService
from ui_gui import MainWindow


def main():
    """Punto de entrada de la aplicación"""
    
    # === DEPENDENCY INJECTION CONTAINER ===
    
    # 1. Configuration Layer
    config = Config.from_env()
    
    # 2. Infrastructure Layer
    api_client = APIClient(config)
    
    # 3. Repository Layer
    cliente_repo = ClienteRepository(api_client)
    reserva_repo = ReservaRepository(api_client)
    hotel_repo = HotelRepository(api_client)
    ciudad_repo = CiudadRepository(api_client)
    tipo_hab_repo = TipoHabitacionRepository(api_client)
    regimen_repo = RegimenRepository(api_client)
    contrato_repo = ContratoRepository(api_client)
    disponibilidad_repo = DisponibilidadRepository(api_client)
    
    # 4. Service Layer
    cliente_service = ClienteService(cliente_repo)
    reserva_service = ReservaService(reserva_repo, hotel_repo, contrato_repo)
    consulta_service = ConsultaService(
        cliente_repo,
        reserva_repo,
        hotel_repo,
        ciudad_repo,
        tipo_hab_repo,
        regimen_repo,
        contrato_repo,
        disponibilidad_repo
    )
    
    # 5. Create GUI
    root = tk.Tk()
    app = MainWindow(
        root,
        cliente_service,
        reserva_service,
        consulta_service,
        api_client
    )
    
    # Run application
    root.mainloop()


if __name__ == "__main__":
    main()

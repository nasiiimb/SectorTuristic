"""
Channel Manager - Configuración
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./channel.db")

# Servidor
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8001))

# WebService URL (para conectar con el WebService principal)
WEBSERVICE_URL = os.getenv("WEBSERVICE_URL", "http://localhost:3000")

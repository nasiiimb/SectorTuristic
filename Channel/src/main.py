"""
Channel Manager - Backend FastAPI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_db
from .routes import auth_router, hoteles_router, habitaciones_router, disponibilidad_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Channel Manager API",
    description="API del Channel Manager para gestión hotelera",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth_router, prefix="/api")
app.include_router(hoteles_router, prefix="/api")
app.include_router(habitaciones_router, prefix="/api")
app.include_router(disponibilidad_router, prefix="/api")


@app.on_event("startup")
def startup():
    """Evento de inicio - Inicializar BD"""
    init_db()


@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "servicio": "Channel Manager API",
        "version": "1.0.0",
        "estado": "activo",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "ok"}


# Punto de entrada para ejecución directa
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

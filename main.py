from fastapi import FastAPI
from database import engine, Base

from controllers.usuario import router as usuario_router
from controllers.cliente import router as cliente_router
from controllers.habitacion import router as habitacion_router
from controllers.reserva import router as reserva_router
from controllers.facturacion import router as facturacion_router
from controllers.finanzas import router as finanzas_router
from controllers.configuracion import router as configuracion_router

# Crear todas las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="HotelRes API",
    description="Sistema de Gestión de Reservas de Hoteles",
    version="1.0.0",
)

# Registrar los routers (controladores)
app.include_router(usuario_router)
app.include_router(cliente_router)
app.include_router(habitacion_router)
app.include_router(reserva_router)
app.include_router(facturacion_router)
app.include_router(finanzas_router)
app.include_router(configuracion_router)


@app.get("/", tags=["Root"])
def root():
    return {"mensaje": "Bienvenido a HotelRes API", "docs": "/docs"}

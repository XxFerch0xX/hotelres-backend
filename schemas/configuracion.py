from pydantic import BaseModel
from typing import Optional


class ParametroSistemaCreate(BaseModel):
    nombre_hotel: str
    ruc: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    moneda: str = "USD"
    porcentaje_iva: float = 15.0
    tiempo_expiracion_reserva: int = 24
    politica_cancelacion: Optional[str] = None


class ParametroSistemaUpdate(BaseModel):
    nombre_hotel: Optional[str] = None
    ruc: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    moneda: Optional[str] = None
    porcentaje_iva: Optional[float] = None
    tiempo_expiracion_reserva: Optional[int] = None
    politica_cancelacion: Optional[str] = None


class ParametroSistemaResponse(BaseModel):
    id: int
    nombre_hotel: str
    ruc: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    moneda: str
    porcentaje_iva: float
    tiempo_expiracion_reserva: int
    politica_cancelacion: Optional[str] = None

    class Config:
        from_attributes = True

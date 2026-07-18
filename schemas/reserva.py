from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from models.reserva import EstadoReserva


class ReservaCreate(BaseModel):
    cliente_id: int
    habitacion_ids: List[int]
    fecha_checkin: date
    fecha_checkout: date
    num_huespedes: int
    observaciones: Optional[str] = None
    usuario_id: int


class ReservaUpdate(BaseModel):
    fecha_checkin: Optional[date] = None
    fecha_checkout: Optional[date] = None
    num_huespedes: Optional[int] = None
    observaciones: Optional[str] = None


class CancelacionRequest(BaseModel):
    motivo_cancelacion: str


class ReservaResponse(BaseModel):
    id: int
    cliente_id: int
    fecha_checkin: date
    fecha_checkout: date
    num_huespedes: int
    observaciones: Optional[str] = None
    estado: EstadoReserva
    motivo_cancelacion: Optional[str] = None
    usuario_id: int
    created_at: datetime

    class Config:
        from_attributes = True

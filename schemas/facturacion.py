from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from models.facturacion import MetodoPago


class ConsumoCreate(BaseModel):
    reserva_id: int
    descripcion: str
    categoria: str
    cantidad: int = 1
    precio_unitario: float


class ConsumoResponse(BaseModel):
    id: int
    reserva_id: int
    descripcion: str
    categoria: str
    cantidad: int
    precio_unitario: float
    fecha: datetime

    class Config:
        from_attributes = True


class DetalleFacturaCreate(BaseModel):
    descripcion: str
    cantidad: int
    precio_unitario: float
    subtotal: float


class DetalleFacturaResponse(BaseModel):
    id: int
    factura_id: int
    descripcion: str
    cantidad: int
    precio_unitario: float
    subtotal: float

    class Config:
        from_attributes = True


class FacturaCreate(BaseModel):
    reserva_id: int
    cliente_id: int
    metodo_pago: MetodoPago
    detalles: List[DetalleFacturaCreate]


class FacturaResponse(BaseModel):
    id: int
    reserva_id: int
    cliente_id: int
    numero_factura: str
    subtotal: float
    iva: float
    total: float
    metodo_pago: MetodoPago
    fecha_emision: datetime
    detalles: List[DetalleFacturaResponse] = []

    class Config:
        from_attributes = True


class PagoCreate(BaseModel):
    reserva_id: int
    monto: float
    metodo_pago: MetodoPago
    referencia_transaccion: Optional[str] = None


class PagoResponse(BaseModel):
    id: int
    reserva_id: int
    monto: float
    metodo_pago: MetodoPago
    referencia_transaccion: Optional[str] = None
    fecha: datetime

    class Config:
        from_attributes = True

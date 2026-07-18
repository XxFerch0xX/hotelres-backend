from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.finanzas import TipoCuenta


class CuentaContableCreate(BaseModel):
    codigo: str
    nombre: str
    tipo: TipoCuenta
    descripcion: Optional[str] = None


class CuentaContableUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[TipoCuenta] = None
    descripcion: Optional[str] = None


class CuentaContableResponse(BaseModel):
    id: int
    codigo: str
    nombre: str
    tipo: TipoCuenta
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True


class AsientoContableCreate(BaseModel):
    cuenta_id: int
    descripcion: str
    monto_debito: float = 0.0
    monto_credito: float = 0.0
    referencia_reserva: Optional[int] = None
    usuario_id: int


class AsientoContableResponse(BaseModel):
    id: int
    cuenta_id: int
    fecha: datetime
    descripcion: str
    monto_debito: float
    monto_credito: float
    referencia_reserva: Optional[int] = None
    usuario_id: int

    class Config:
        from_attributes = True


class GastoOperativoCreate(BaseModel):
    descripcion: str
    categoria: str
    cuenta_id: int
    monto: float
    proveedor: Optional[str] = None
    numero_comprobante: Optional[str] = None
    usuario_id: int


class GastoOperativoResponse(BaseModel):
    id: int
    descripcion: str
    categoria: str
    cuenta_id: int
    monto: float
    fecha: datetime
    proveedor: Optional[str] = None
    numero_comprobante: Optional[str] = None
    usuario_id: int

    class Config:
        from_attributes = True

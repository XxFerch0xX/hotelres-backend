from pydantic import BaseModel
from typing import Optional
from datetime import date
from models.cliente import TipoCliente


class ClienteCreate(BaseModel):
    cedula_pasaporte: str
    nombres: str
    apellidos: str
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_cliente: TipoCliente = TipoCliente.NACIONAL
    datos_facturacion: Optional[str] = None


class ClienteUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_cliente: Optional[TipoCliente] = None
    datos_facturacion: Optional[str] = None
    estado: Optional[bool] = None


class ClienteResponse(BaseModel):
    id: int
    cedula_pasaporte: str
    nombres: str
    apellidos: str
    fecha_nacimiento: Optional[date] = None
    nacionalidad: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    tipo_cliente: TipoCliente
    datos_facturacion: Optional[str] = None
    estado: bool

    class Config:
        from_attributes = True

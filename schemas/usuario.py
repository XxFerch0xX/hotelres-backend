from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from models.usuario import RolUsuario


class UsuarioCreate(BaseModel):
    nombres: str
    apellidos: str
    email: str
    password: str
    rol: RolUsuario


class UsuarioUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    email: Optional[str] = None
    rol: Optional[RolUsuario] = None
    estado: Optional[bool] = None


class UsuarioResponse(BaseModel):
    id: int
    nombres: str
    apellidos: str
    email: str
    rol: RolUsuario
    estado: bool
    created_at: datetime

    class Config:
        from_attributes = True

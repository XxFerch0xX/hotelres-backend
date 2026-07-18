from pydantic import BaseModel
from typing import Optional
from models.habitacion import EstadoHabitacion


class TipoHabitacionCreate(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    capacidad_maxima: int
    tarifa_base: float


class TipoHabitacionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    capacidad_maxima: Optional[int] = None
    tarifa_base: Optional[float] = None


class TipoHabitacionResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    capacidad_maxima: int
    tarifa_base: float

    class Config:
        from_attributes = True


class HabitacionCreate(BaseModel):
    numero: str
    piso: int
    tipo_habitacion_id: int
    estado: EstadoHabitacion = EstadoHabitacion.DISPONIBLE
    descripcion_amenidades: Optional[str] = None


class HabitacionUpdate(BaseModel):
    piso: Optional[int] = None
    tipo_habitacion_id: Optional[int] = None
    estado: Optional[EstadoHabitacion] = None
    descripcion_amenidades: Optional[str] = None


class HabitacionResponse(BaseModel):
    id: int
    numero: str
    piso: int
    tipo_habitacion_id: int
    estado: EstadoHabitacion
    descripcion_amenidades: Optional[str] = None

    class Config:
        from_attributes = True

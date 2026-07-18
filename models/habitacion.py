from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from database import Base
import enum


class EstadoHabitacion(str, enum.Enum):
    DISPONIBLE = "DISPONIBLE"
    RESERVADA = "RESERVADA"
    OCUPADA = "OCUPADA"
    MANTENIMIENTO = "MANTENIMIENTO"
    FUERA_SERVICIO = "FUERA_SERVICIO"


class TipoHabitacion(Base):
    __tablename__ = "tipos_habitacion"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200), nullable=True)
    capacidad_maxima = Column(Integer, nullable=False)
    tarifa_base = Column(Float, nullable=False)

    habitaciones = relationship("Habitacion", back_populates="tipo_habitacion")


class Habitacion(Base):
    __tablename__ = "habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(10), unique=True, nullable=False)
    piso = Column(Integer, nullable=False)
    tipo_habitacion_id = Column(Integer, ForeignKey("tipos_habitacion.id"), nullable=False)
    estado = Column(SAEnum(EstadoHabitacion), default=EstadoHabitacion.DISPONIBLE)
    descripcion_amenidades = Column(String(300), nullable=True)

    tipo_habitacion = relationship("TipoHabitacion", back_populates="habitaciones")
    reserva_habitaciones = relationship("ReservaHabitacion", back_populates="habitacion")

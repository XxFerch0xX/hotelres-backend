from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
import enum


class EstadoReserva(str, enum.Enum):
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    EN_CURSO = "EN_CURSO"
    COMPLETADA = "COMPLETADA"
    CANCELADA = "CANCELADA"


class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    fecha_checkin = Column(Date, nullable=False)
    fecha_checkout = Column(Date, nullable=False)
    num_huespedes = Column(Integer, nullable=False)
    observaciones = Column(String(500), nullable=True)
    estado = Column(SAEnum(EstadoReserva), default=EstadoReserva.PENDIENTE)
    motivo_cancelacion = Column(String(300), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    cliente = relationship("Cliente", back_populates="reservas")
    usuario = relationship("Usuario", back_populates="reservas")
    reserva_habitaciones = relationship("ReservaHabitacion", back_populates="reserva", cascade="all, delete-orphan")
    consumos = relationship("Consumo", back_populates="reserva")
    facturas = relationship("Factura", back_populates="reserva")
    pagos = relationship("Pago", back_populates="reserva")


class ReservaHabitacion(Base):
    __tablename__ = "reserva_habitaciones"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)
    habitacion_id = Column(Integer, ForeignKey("habitaciones.id"), nullable=False)

    reserva = relationship("Reserva", back_populates="reserva_habitaciones")
    habitacion = relationship("Habitacion", back_populates="reserva_habitaciones")

from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
import enum


class MetodoPago(str, enum.Enum):
    EFECTIVO = "EFECTIVO"
    TARJETA_CREDITO = "TARJETA_CREDITO"
    TARJETA_DEBITO = "TARJETA_DEBITO"
    TRANSFERENCIA = "TRANSFERENCIA"
    OTRO = "OTRO"


class Consumo(Base):
    __tablename__ = "consumos"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)
    descripcion = Column(String(200), nullable=False)
    categoria = Column(String(100), nullable=False)
    cantidad = Column(Integer, nullable=False, default=1)
    precio_unitario = Column(Float, nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reserva = relationship("Reserva", back_populates="consumos")


class Factura(Base):
    __tablename__ = "facturas"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    numero_factura = Column(String(20), unique=True, nullable=False)
    subtotal = Column(Float, nullable=False)
    iva = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    metodo_pago = Column(SAEnum(MetodoPago), nullable=False)
    fecha_emision = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reserva = relationship("Reserva", back_populates="facturas")
    cliente = relationship("Cliente", back_populates="facturas")
    detalles = relationship("DetalleFactura", back_populates="factura", cascade="all, delete-orphan")


class DetalleFactura(Base):
    __tablename__ = "detalle_facturas"

    id = Column(Integer, primary_key=True, index=True)
    factura_id = Column(Integer, ForeignKey("facturas.id"), nullable=False)
    descripcion = Column(String(200), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    factura = relationship("Factura", back_populates="detalles")


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    reserva_id = Column(Integer, ForeignKey("reservas.id"), nullable=False)
    monto = Column(Float, nullable=False)
    metodo_pago = Column(SAEnum(MetodoPago), nullable=False)
    referencia_transaccion = Column(String(100), nullable=True)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reserva = relationship("Reserva", back_populates="pagos")
# Modelos de facturacion 

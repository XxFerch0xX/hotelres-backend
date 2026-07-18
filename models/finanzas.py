from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base
import enum


class TipoCuenta(str, enum.Enum):
    INGRESO = "INGRESO"
    EGRESO = "EGRESO"
    ACTIVO = "ACTIVO"
    PASIVO = "PASIVO"


class CuentaContable(Base):
    __tablename__ = "cuentas_contables"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo = Column(SAEnum(TipoCuenta), nullable=False)
    descripcion = Column(String(200), nullable=True)

    asientos = relationship("AsientoContable", back_populates="cuenta")
    gastos = relationship("GastoOperativo", back_populates="cuenta")


class AsientoContable(Base):
    __tablename__ = "asientos_contables"

    id = Column(Integer, primary_key=True, index=True)
    cuenta_id = Column(Integer, ForeignKey("cuentas_contables.id"), nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    descripcion = Column(String(200), nullable=False)
    monto_debito = Column(Float, default=0.0)
    monto_credito = Column(Float, default=0.0)
    referencia_reserva = Column(Integer, nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    cuenta = relationship("CuentaContable", back_populates="asientos")
    usuario = relationship("Usuario", back_populates="asientos")


class GastoOperativo(Base):
    __tablename__ = "gastos_operativos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(200), nullable=False)
    categoria = Column(String(100), nullable=False)
    cuenta_id = Column(Integer, ForeignKey("cuentas_contables.id"), nullable=False)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    proveedor = Column(String(100), nullable=True)
    numero_comprobante = Column(String(50), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    cuenta = relationship("CuentaContable", back_populates="gastos")
    usuario = relationship("Usuario", back_populates="gastos")

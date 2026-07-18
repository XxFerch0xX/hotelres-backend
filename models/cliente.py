from sqlalchemy import Column, Integer, String, Date, Boolean, Enum as SAEnum
from sqlalchemy.orm import relationship
from database import Base
import enum


class TipoCliente(str, enum.Enum):
    NACIONAL = "NACIONAL"
    EXTRANJERO = "EXTRANJERO"


class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    cedula_pasaporte = Column(String(20), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=True)
    nacionalidad = Column(String(50), nullable=True)
    direccion = Column(String(200), nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)
    tipo_cliente = Column(SAEnum(TipoCliente), default=TipoCliente.NACIONAL)
    datos_facturacion = Column(String(300), nullable=True)
    estado = Column(Boolean, default=True)

    reservas = relationship("Reserva", back_populates="cliente")
    facturas = relationship("Factura", back_populates="cliente")

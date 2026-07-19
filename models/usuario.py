from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

from database import Base


class RolUsuario(str, enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    RECEPCIONISTA = "RECEPCIONISTA"
    AUDITOR = "AUDITOR"
    GERENTE = "GERENTE"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(SAEnum(RolUsuario), nullable=False)
    estado = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    reservas = relationship("Reserva", back_populates="usuario")
    asientos = relationship("AsientoContable", back_populates="usuario")
    gastos = relationship("GastoOperativo", back_populates="usuario")
    auditorias = relationship("AuditoriaLog", back_populates="usuario")
# Modelos del sistema 

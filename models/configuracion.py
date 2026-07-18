from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class ParametroSistema(Base):
    __tablename__ = "parametros_sistema"

    id = Column(Integer, primary_key=True, index=True)
    nombre_hotel = Column(String(200), nullable=False)
    ruc = Column(String(20), nullable=False)
    direccion = Column(String(300), nullable=True)
    telefono = Column(String(20), nullable=True)
    email = Column(String(150), nullable=True)
    moneda = Column(String(10), default="USD")
    porcentaje_iva = Column(Float, default=15.0)
    tiempo_expiracion_reserva = Column(Integer, default=24)
    politica_cancelacion = Column(Text, nullable=True)


class AuditoriaLog(Base):
    __tablename__ = "auditoria_logs"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    accion = Column(String(50), nullable=False)
    tabla_afectada = Column(String(50), nullable=False)
    registro_id = Column(Integer, nullable=True)
    datos_anteriores = Column(Text, nullable=True)
    datos_nuevos = Column(Text, nullable=True)
    fecha = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    usuario = relationship("Usuario", back_populates="auditorias")

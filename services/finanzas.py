from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from models.finanzas import CuentaContable, AsientoContable, GastoOperativo
from schemas.finanzas import (
    CuentaContableCreate, CuentaContableUpdate,
    AsientoContableCreate, GastoOperativoCreate,
)
from repositories.finanzas import (
    CuentaContableRepository, AsientoContableRepository, GastoOperativoRepository,
)


class CuentaContableService:
    def __init__(self, db: Session):
        self.repo = CuentaContableRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, cuenta_id: int):
        cuenta = self.repo.get_by_id(cuenta_id)
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta contable no encontrada")
        return cuenta

    def crear(self, data: CuentaContableCreate):
        cuenta = CuentaContable(**data.model_dump())
        return self.repo.create(cuenta)

    def actualizar(self, cuenta_id: int, data: CuentaContableUpdate):
        cuenta = self.obtener(cuenta_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cuenta, field, value)
        return self.repo.update(cuenta)

    def eliminar(self, cuenta_id: int):
        cuenta = self.obtener(cuenta_id)
        self.repo.delete(cuenta)
        return {"detail": "Cuenta contable eliminada"}


class AsientoContableService:
    def __init__(self, db: Session):
        self.repo = AsientoContableRepository(db)

    def listar(self):
        return self.repo.get_all()

    def libro_diario(self, fecha_inicio: datetime, fecha_fin: datetime):
        return self.repo.get_by_periodo(fecha_inicio, fecha_fin)

    def crear(self, data: AsientoContableCreate):
        asiento = AsientoContable(**data.model_dump())
        return self.repo.create(asiento)


class GastoOperativoService:
    def __init__(self, db: Session):
        self.repo = GastoOperativoRepository(db)

    def listar(self):
        return self.repo.get_all()

    def crear(self, data: GastoOperativoCreate):
        gasto = GastoOperativo(**data.model_dump())
        return self.repo.create(gasto)

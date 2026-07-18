from sqlalchemy.orm import Session
from models.finanzas import CuentaContable, AsientoContable, GastoOperativo


class CuentaContableRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(CuentaContable).all()

    def get_by_id(self, cuenta_id: int):
        return self.db.query(CuentaContable).filter(CuentaContable.id == cuenta_id).first()

    def create(self, cuenta: CuentaContable):
        self.db.add(cuenta)
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta

    def update(self, cuenta: CuentaContable):
        self.db.commit()
        self.db.refresh(cuenta)
        return cuenta

    def delete(self, cuenta: CuentaContable):
        self.db.delete(cuenta)
        self.db.commit()


class AsientoContableRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(AsientoContable).all()

    def get_by_periodo(self, fecha_inicio, fecha_fin):
        return self.db.query(AsientoContable).filter(
            AsientoContable.fecha >= fecha_inicio,
            AsientoContable.fecha <= fecha_fin
        ).order_by(AsientoContable.fecha).all()

    def create(self, asiento: AsientoContable):
        self.db.add(asiento)
        self.db.commit()
        self.db.refresh(asiento)
        return asiento


class GastoOperativoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(GastoOperativo).all()

    def create(self, gasto: GastoOperativo):
        self.db.add(gasto)
        self.db.commit()
        self.db.refresh(gasto)
        return gasto

from sqlalchemy.orm import Session
from models.configuracion import ParametroSistema, AuditoriaLog


class ParametroSistemaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self):
        return self.db.query(ParametroSistema).first()

    def create(self, param: ParametroSistema):
        self.db.add(param)
        self.db.commit()
        self.db.refresh(param)
        return param

    def update(self, param: ParametroSistema):
        self.db.commit()
        self.db.refresh(param)
        return param


class AuditoriaLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(AuditoriaLog).order_by(AuditoriaLog.fecha.desc()).all()

    def create(self, log: AuditoriaLog):
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log

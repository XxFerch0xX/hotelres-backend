from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.configuracion import ParametroSistema
from schemas.configuracion import ParametroSistemaCreate, ParametroSistemaUpdate
from repositories.configuracion import ParametroSistemaRepository, AuditoriaLogRepository


class ParametroSistemaService:
    def __init__(self, db: Session):
        self.repo = ParametroSistemaRepository(db)

    def obtener(self):
        param = self.repo.get()
        if not param:
            raise HTTPException(status_code=404, detail="Parámetros no configurados")
        return param

    def crear_o_actualizar(self, data: ParametroSistemaCreate):
        param = self.repo.get()
        if param:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(param, field, value)
            return self.repo.update(param)
        else:
            param = ParametroSistema(**data.model_dump())
            return self.repo.create(param)


class AuditoriaService:
    def __init__(self, db: Session):
        self.repo = AuditoriaLogRepository(db)

    def listar(self):
        return self.repo.get_all()

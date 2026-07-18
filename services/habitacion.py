from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.habitacion import TipoHabitacion, Habitacion
from schemas.habitacion import (
    TipoHabitacionCreate, TipoHabitacionUpdate,
    HabitacionCreate, HabitacionUpdate,
)
from repositories.habitacion import TipoHabitacionRepository, HabitacionRepository


class TipoHabitacionService:
    def __init__(self, db: Session):
        self.repo = TipoHabitacionRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, tipo_id: int):
        tipo = self.repo.get_by_id(tipo_id)
        if not tipo:
            raise HTTPException(status_code=404, detail="Tipo de habitación no encontrado")
        return tipo

    def crear(self, data: TipoHabitacionCreate):
        tipo = TipoHabitacion(**data.model_dump())
        return self.repo.create(tipo)

    def actualizar(self, tipo_id: int, data: TipoHabitacionUpdate):
        tipo = self.obtener(tipo_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(tipo, field, value)
        return self.repo.update(tipo)

    def eliminar(self, tipo_id: int):
        tipo = self.obtener(tipo_id)
        self.repo.delete(tipo)
        return {"detail": "Tipo de habitación eliminado"}


class HabitacionService:
    def __init__(self, db: Session):
        self.repo = HabitacionRepository(db)

    def listar(self):
        return self.repo.get_all()

    def listar_disponibles(self):
        return self.repo.get_disponibles()

    def obtener(self, habitacion_id: int):
        hab = self.repo.get_by_id(habitacion_id)
        if not hab:
            raise HTTPException(status_code=404, detail="Habitación no encontrada")
        return hab

    def crear(self, data: HabitacionCreate):
        if self.repo.get_by_numero(data.numero):
            raise HTTPException(status_code=400, detail="Ya existe una habitación con ese número")
        habitacion = Habitacion(**data.model_dump())
        return self.repo.create(habitacion)

    def actualizar(self, habitacion_id: int, data: HabitacionUpdate):
        hab = self.obtener(habitacion_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(hab, field, value)
        return self.repo.update(hab)

    def eliminar(self, habitacion_id: int):
        hab = self.obtener(habitacion_id)
        self.repo.delete(hab)
        return {"detail": "Habitación eliminada"}

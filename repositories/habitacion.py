from sqlalchemy.orm import Session
from models.habitacion import TipoHabitacion, Habitacion


class TipoHabitacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(TipoHabitacion).all()

    def get_by_id(self, tipo_id: int):
        return self.db.query(TipoHabitacion).filter(TipoHabitacion.id == tipo_id).first()

    def create(self, tipo: TipoHabitacion):
        self.db.add(tipo)
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def update(self, tipo: TipoHabitacion):
        self.db.commit()
        self.db.refresh(tipo)
        return tipo

    def delete(self, tipo: TipoHabitacion):
        self.db.delete(tipo)
        self.db.commit()


class HabitacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Habitacion).all()

    def get_by_id(self, habitacion_id: int):
        return self.db.query(Habitacion).filter(Habitacion.id == habitacion_id).first()

    def get_by_numero(self, numero: str):
        return self.db.query(Habitacion).filter(Habitacion.numero == numero).first()

    def get_disponibles(self):
        return self.db.query(Habitacion).filter(Habitacion.estado == "DISPONIBLE").all()

    def create(self, habitacion: Habitacion):
        self.db.add(habitacion)
        self.db.commit()
        self.db.refresh(habitacion)
        return habitacion

    def update(self, habitacion: Habitacion):
        self.db.commit()
        self.db.refresh(habitacion)
        return habitacion

    def delete(self, habitacion: Habitacion):
        self.db.delete(habitacion)
        self.db.commit()
# Repositorio de habitaciones 

from sqlalchemy.orm import Session
from models.reserva import Reserva, ReservaHabitacion


class ReservaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Reserva).all()

    def get_by_id(self, reserva_id: int):
        return self.db.query(Reserva).filter(Reserva.id == reserva_id).first()

    def get_by_cliente(self, cliente_id: int):
        return self.db.query(Reserva).filter(Reserva.cliente_id == cliente_id).all()

    def get_activas(self):
        return self.db.query(Reserva).filter(Reserva.estado == "EN_CURSO").all()

    def create(self, reserva: Reserva):
        self.db.add(reserva)
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def update(self, reserva: Reserva):
        self.db.commit()
        self.db.refresh(reserva)
        return reserva

    def delete(self, reserva: Reserva):
        self.db.delete(reserva)
        self.db.commit()


class ReservaHabitacionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, rh: ReservaHabitacion):
        self.db.add(rh)
        self.db.commit()
        self.db.refresh(rh)
        return rh

    def get_by_reserva(self, reserva_id: int):
        return self.db.query(ReservaHabitacion).filter(
            ReservaHabitacion.reserva_id == reserva_id
        ).all()
# Repositorio de reservas 

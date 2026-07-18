from sqlalchemy.orm import Session
from models.cliente import Cliente


class ClienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Cliente).all()

    def get_by_id(self, cliente_id: int):
        return self.db.query(Cliente).filter(Cliente.id == cliente_id).first()

    def get_by_cedula(self, cedula: str):
        return self.db.query(Cliente).filter(Cliente.cedula_pasaporte == cedula).first()

    def create(self, cliente: Cliente):
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def update(self, cliente: Cliente):
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def delete(self, cliente: Cliente):
        self.db.delete(cliente)
        self.db.commit()

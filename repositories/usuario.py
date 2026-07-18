from sqlalchemy.orm import Session
from models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Usuario).all()

    def get_by_id(self, usuario_id: int):
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_by_email(self, email: str):
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def create(self, usuario: Usuario):
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, usuario: Usuario):
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, usuario: Usuario):
        self.db.delete(usuario)
        self.db.commit()

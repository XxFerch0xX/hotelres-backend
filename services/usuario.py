from fastapi import HTTPException
from sqlalchemy.orm import Session
import bcrypt

from models.usuario import Usuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from repositories.usuario import UsuarioRepository


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, usuario_id: int):
        usuario = self.repo.get_by_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

    def crear(self, data: UsuarioCreate):
        if self.repo.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="El email ya está registrado")
        hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()
        usuario = Usuario(
            nombres=data.nombres,
            apellidos=data.apellidos,
            email=data.email,
            password_hash=hashed,
            rol=data.rol,
        )
        return self.repo.create(usuario)

    def actualizar(self, usuario_id: int, data: UsuarioUpdate):
        usuario = self.obtener(usuario_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(usuario, field, value)
        return self.repo.update(usuario)

    def eliminar(self, usuario_id: int):
        usuario = self.obtener(usuario_id)
        self.repo.delete(usuario)
        return {"detail": "Usuario eliminado"}

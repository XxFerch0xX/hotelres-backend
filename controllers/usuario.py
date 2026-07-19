from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from services.usuario import UsuarioService

router = APIRouter(prefix="/api/usuarios", tags=["Usuarios"])


@router.get("/", response_model=List[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return UsuarioService(db).listar()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return UsuarioService(db).obtener(usuario_id)


@router.post("/", response_model=UsuarioResponse, status_code=201)
def crear_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    return UsuarioService(db).crear(data)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db)):
    return UsuarioService(db).actualizar(usuario_id, data)


@router.delete("/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return UsuarioService(db).eliminar(usuario_id)
# Controlador de usuarios 

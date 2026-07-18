from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.configuracion import ParametroSistemaCreate, ParametroSistemaResponse
from services.configuracion import ParametroSistemaService, AuditoriaService

router = APIRouter(prefix="/api/configuracion", tags=["Configuración"])


@router.get("/parametros", response_model=ParametroSistemaResponse)
def obtener_parametros(db: Session = Depends(get_db)):
    return ParametroSistemaService(db).obtener()


@router.post("/parametros", response_model=ParametroSistemaResponse)
def configurar_parametros(data: ParametroSistemaCreate, db: Session = Depends(get_db)):
    return ParametroSistemaService(db).crear_o_actualizar(data)


@router.get("/auditoria")
def listar_auditoria(db: Session = Depends(get_db)):
    return AuditoriaService(db).listar()

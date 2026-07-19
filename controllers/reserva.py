from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.reserva import ReservaCreate, ReservaUpdate, ReservaResponse, CancelacionRequest
from services.reserva import ReservaService

router = APIRouter(prefix="/api/reservas", tags=["Reservas"])


@router.get("/", response_model=List[ReservaResponse])
def listar_reservas(db: Session = Depends(get_db)):
    return ReservaService(db).listar()


@router.get("/activas", response_model=List[ReservaResponse])
def huespedes_activos(db: Session = Depends(get_db)):
    return ReservaService(db).huespedes_activos()


@router.get("/{reserva_id}", response_model=ReservaResponse)
def obtener_reserva(reserva_id: int, db: Session = Depends(get_db)):
    return ReservaService(db).obtener(reserva_id)


@router.get("/cliente/{cliente_id}", response_model=List[ReservaResponse])
def historial_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return ReservaService(db).historial_cliente(cliente_id)


@router.post("/", response_model=ReservaResponse, status_code=201)
def crear_reserva(data: ReservaCreate, db: Session = Depends(get_db)):
    return ReservaService(db).crear(data)


@router.put("/{reserva_id}", response_model=ReservaResponse)
def actualizar_reserva(reserva_id: int, data: ReservaUpdate, db: Session = Depends(get_db)):
    return ReservaService(db).actualizar(reserva_id, data)


@router.post("/{reserva_id}/checkin", response_model=ReservaResponse)
def checkin(reserva_id: int, db: Session = Depends(get_db)):
    return ReservaService(db).checkin(reserva_id)


@router.post("/{reserva_id}/checkout", response_model=ReservaResponse)
def checkout(reserva_id: int, db: Session = Depends(get_db)):
    return ReservaService(db).checkout(reserva_id)


@router.post("/{reserva_id}/cancelar", response_model=ReservaResponse)
def cancelar(reserva_id: int, data: CancelacionRequest, db: Session = Depends(get_db)):
    return ReservaService(db).cancelar(reserva_id, data)
# Controlador de reservas 

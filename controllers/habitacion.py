from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.habitacion import (
    TipoHabitacionCreate, TipoHabitacionUpdate, TipoHabitacionResponse,
    HabitacionCreate, HabitacionUpdate, HabitacionResponse,
)
from services.habitacion import TipoHabitacionService, HabitacionService

router = APIRouter(prefix="/api/habitaciones", tags=["Habitaciones"])

# --- Tipos de habitación ---

@router.get("/tipos", response_model=List[TipoHabitacionResponse])
def listar_tipos(db: Session = Depends(get_db)):
    return TipoHabitacionService(db).listar()


@router.get("/tipos/{tipo_id}", response_model=TipoHabitacionResponse)
def obtener_tipo(tipo_id: int, db: Session = Depends(get_db)):
    return TipoHabitacionService(db).obtener(tipo_id)


@router.post("/tipos", response_model=TipoHabitacionResponse, status_code=201)
def crear_tipo(data: TipoHabitacionCreate, db: Session = Depends(get_db)):
    return TipoHabitacionService(db).crear(data)


@router.put("/tipos/{tipo_id}", response_model=TipoHabitacionResponse)
def actualizar_tipo(tipo_id: int, data: TipoHabitacionUpdate, db: Session = Depends(get_db)):
    return TipoHabitacionService(db).actualizar(tipo_id, data)


@router.delete("/tipos/{tipo_id}")
def eliminar_tipo(tipo_id: int, db: Session = Depends(get_db)):
    return TipoHabitacionService(db).eliminar(tipo_id)


# --- Habitaciones ---

@router.get("/", response_model=List[HabitacionResponse])
def listar_habitaciones(db: Session = Depends(get_db)):
    return HabitacionService(db).listar()


@router.get("/disponibles", response_model=List[HabitacionResponse])
def listar_disponibles(db: Session = Depends(get_db)):
    return HabitacionService(db).listar_disponibles()


@router.get("/{habitacion_id}", response_model=HabitacionResponse)
def obtener_habitacion(habitacion_id: int, db: Session = Depends(get_db)):
    return HabitacionService(db).obtener(habitacion_id)


@router.post("/", response_model=HabitacionResponse, status_code=201)
def crear_habitacion(data: HabitacionCreate, db: Session = Depends(get_db)):
    return HabitacionService(db).crear(data)


@router.put("/{habitacion_id}", response_model=HabitacionResponse)
def actualizar_habitacion(habitacion_id: int, data: HabitacionUpdate, db: Session = Depends(get_db)):
    return HabitacionService(db).actualizar(habitacion_id, data)


@router.delete("/{habitacion_id}")
def eliminar_habitacion(habitacion_id: int, db: Session = Depends(get_db)):
    return HabitacionService(db).eliminar(habitacion_id)

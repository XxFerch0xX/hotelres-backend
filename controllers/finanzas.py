from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import get_db
from schemas.finanzas import (
    CuentaContableCreate, CuentaContableUpdate, CuentaContableResponse,
    AsientoContableCreate, AsientoContableResponse,
    GastoOperativoCreate, GastoOperativoResponse,
)
from services.finanzas import CuentaContableService, AsientoContableService, GastoOperativoService

router = APIRouter(prefix="/api/finanzas", tags=["Finanzas"])

# --- Cuentas contables ---

@router.get("/cuentas", response_model=List[CuentaContableResponse])
def listar_cuentas(db: Session = Depends(get_db)):
    return CuentaContableService(db).listar()


@router.get("/cuentas/{cuenta_id}", response_model=CuentaContableResponse)
def obtener_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    return CuentaContableService(db).obtener(cuenta_id)


@router.post("/cuentas", response_model=CuentaContableResponse, status_code=201)
def crear_cuenta(data: CuentaContableCreate, db: Session = Depends(get_db)):
    return CuentaContableService(db).crear(data)


@router.put("/cuentas/{cuenta_id}", response_model=CuentaContableResponse)
def actualizar_cuenta(cuenta_id: int, data: CuentaContableUpdate, db: Session = Depends(get_db)):
    return CuentaContableService(db).actualizar(cuenta_id, data)


@router.delete("/cuentas/{cuenta_id}")
def eliminar_cuenta(cuenta_id: int, db: Session = Depends(get_db)):
    return CuentaContableService(db).eliminar(cuenta_id)


# --- Libro diario ---

@router.get("/libro-diario", response_model=List[AsientoContableResponse])
def libro_diario(
    fecha_inicio: datetime = Query(...),
    fecha_fin: datetime = Query(...),
    db: Session = Depends(get_db),
):
    return AsientoContableService(db).libro_diario(fecha_inicio, fecha_fin)


@router.post("/asientos", response_model=AsientoContableResponse, status_code=201)
def crear_asiento(data: AsientoContableCreate, db: Session = Depends(get_db)):
    return AsientoContableService(db).crear(data)


# --- Gastos operativos ---

@router.get("/gastos", response_model=List[GastoOperativoResponse])
def listar_gastos(db: Session = Depends(get_db)):
    return GastoOperativoService(db).listar()


@router.post("/gastos", response_model=GastoOperativoResponse, status_code=201)
def crear_gasto(data: GastoOperativoCreate, db: Session = Depends(get_db)):
    return GastoOperativoService(db).crear(data)

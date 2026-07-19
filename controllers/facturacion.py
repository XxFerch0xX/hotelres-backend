from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from schemas.facturacion import (
    ConsumoCreate, ConsumoResponse,
    FacturaCreate, FacturaResponse,
    PagoCreate, PagoResponse,
)
from services.facturacion import ConsumoService, FacturaService, PagoService

router = APIRouter(prefix="/api/facturacion", tags=["Facturación"])

# --- Consumos ---

@router.get("/consumos/{reserva_id}", response_model=List[ConsumoResponse])
def listar_consumos(reserva_id: int, db: Session = Depends(get_db)):
    return ConsumoService(db).listar_por_reserva(reserva_id)


@router.post("/consumos", response_model=ConsumoResponse, status_code=201)
def crear_consumo(data: ConsumoCreate, db: Session = Depends(get_db)):
    return ConsumoService(db).crear(data)


# --- Facturas ---

@router.get("/facturas", response_model=List[FacturaResponse])
def listar_facturas(db: Session = Depends(get_db)):
    return FacturaService(db).listar()


@router.get("/facturas/{factura_id}", response_model=FacturaResponse)
def obtener_factura(factura_id: int, db: Session = Depends(get_db)):
    return FacturaService(db).obtener(factura_id)


@router.post("/facturas", response_model=FacturaResponse, status_code=201)
def crear_factura(data: FacturaCreate, db: Session = Depends(get_db)):
    return FacturaService(db).crear(data)


# --- Pagos ---

@router.get("/pagos/{reserva_id}", response_model=List[PagoResponse])
def listar_pagos(reserva_id: int, db: Session = Depends(get_db)):
    return PagoService(db).listar_por_reserva(reserva_id)


@router.post("/pagos", response_model=PagoResponse, status_code=201)
def crear_pago(data: PagoCreate, db: Session = Depends(get_db)):
    return PagoService(db).crear(data)
# Controlador de facturacion 

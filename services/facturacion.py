from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.facturacion import Consumo, Factura, DetalleFactura, Pago
from schemas.facturacion import ConsumoCreate, FacturaCreate, PagoCreate
from repositories.facturacion import ConsumoRepository, FacturaRepository, PagoRepository
from repositories.configuracion import ParametroSistemaRepository


class ConsumoService:
    def __init__(self, db: Session):
        self.repo = ConsumoRepository(db)

    def listar_por_reserva(self, reserva_id: int):
        return self.repo.get_by_reserva(reserva_id)

    def crear(self, data: ConsumoCreate):
        consumo = Consumo(**data.model_dump())
        return self.repo.create(consumo)


class FacturaService:
    def __init__(self, db: Session):
        self.repo = FacturaRepository(db)
        self.param_repo = ParametroSistemaRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, factura_id: int):
        factura = self.repo.get_by_id(factura_id)
        if not factura:
            raise HTTPException(status_code=404, detail="Factura no encontrada")
        return factura

    def crear(self, data: FacturaCreate):
        # Calcular subtotal
        subtotal = sum(d.subtotal for d in data.detalles)
        # Obtener IVA de parámetros
        params = self.param_repo.get()
        porcentaje_iva = params.porcentaje_iva if params else 15.0
        iva = subtotal * (porcentaje_iva / 100)
        total = subtotal + iva

        # Generar número de factura
        last_num = self.repo.get_last_number()
        numero_factura = f"FAC-{last_num + 1:06d}"

        factura = Factura(
            reserva_id=data.reserva_id,
            cliente_id=data.cliente_id,
            numero_factura=numero_factura,
            subtotal=subtotal,
            iva=iva,
            total=total,
            metodo_pago=data.metodo_pago,
        )
        factura = self.repo.create(factura)

        # Crear detalles
        for d in data.detalles:
            detalle = DetalleFactura(
                factura_id=factura.id,
                descripcion=d.descripcion,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                subtotal=d.subtotal,
            )
            self.repo.db.add(detalle)
        self.repo.db.commit()
        self.repo.db.refresh(factura)
        return factura


class PagoService:
    def __init__(self, db: Session):
        self.repo = PagoRepository(db)

    def listar_por_reserva(self, reserva_id: int):
        return self.repo.get_by_reserva(reserva_id)

    def crear(self, data: PagoCreate):
        pago = Pago(**data.model_dump())
        return self.repo.create(pago)
# Servicio de facturacion 

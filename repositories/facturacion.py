from sqlalchemy.orm import Session
from models.facturacion import Consumo, Factura, DetalleFactura, Pago


class ConsumoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_reserva(self, reserva_id: int):
        return self.db.query(Consumo).filter(Consumo.reserva_id == reserva_id).all()

    def create(self, consumo: Consumo):
        self.db.add(consumo)
        self.db.commit()
        self.db.refresh(consumo)
        return consumo


class FacturaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Factura).all()

    def get_by_id(self, factura_id: int):
        return self.db.query(Factura).filter(Factura.id == factura_id).first()

    def get_last_number(self):
        last = self.db.query(Factura).order_by(Factura.id.desc()).first()
        return int(last.numero_factura.replace("FAC-", "")) if last else 0

    def create(self, factura: Factura):
        self.db.add(factura)
        self.db.commit()
        self.db.refresh(factura)
        return factura


class PagoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_reserva(self, reserva_id: int):
        return self.db.query(Pago).filter(Pago.reserva_id == reserva_id).all()

    def create(self, pago: Pago):
        self.db.add(pago)
        self.db.commit()
        self.db.refresh(pago)
        return pago

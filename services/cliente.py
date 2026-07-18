from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate
from repositories.cliente import ClienteRepository


class ClienteService:
    def __init__(self, db: Session):
        self.repo = ClienteRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, cliente_id: int):
        cliente = self.repo.get_by_id(cliente_id)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente

    def buscar_por_cedula(self, cedula: str):
        cliente = self.repo.get_by_cedula(cedula)
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente

    def crear(self, data: ClienteCreate):
        if self.repo.get_by_cedula(data.cedula_pasaporte):
            raise HTTPException(status_code=400, detail="Ya existe un cliente con esa cédula/pasaporte")
        cliente = Cliente(**data.model_dump())
        return self.repo.create(cliente)

    def actualizar(self, cliente_id: int, data: ClienteUpdate):
        cliente = self.obtener(cliente_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(cliente, field, value)
        return self.repo.update(cliente)

    def eliminar(self, cliente_id: int):
        cliente = self.obtener(cliente_id)
        self.repo.delete(cliente)
        return {"detail": "Cliente eliminado"}

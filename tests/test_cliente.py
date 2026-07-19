import pytest
from fastapi import HTTPException

from models.cliente import Cliente, TipoCliente
from schemas.cliente import ClienteCreate, ClienteUpdate
from services.cliente import ClienteService
from repositories.cliente import ClienteRepository


class TestClienteRepository:
    """Pruebas unitarias para ClienteRepository."""

    def test_get_all(self, db):
        repo = ClienteRepository(db)
        cliente = Cliente(
            cedula_pasaporte="0912345678", nombres="Juan", apellidos="Pérez",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        result = repo.get_all()
        assert len(result) == 1

    def test_get_by_id(self, db):
        repo = ClienteRepository(db)
        cliente = Cliente(
            cedula_pasaporte="0912345679", nombres="Ana", apellidos="López",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        result = repo.get_by_id(cliente.id)
        assert result.nombres == "Ana"

    def test_get_by_cedula(self, db):
        repo = ClienteRepository(db)
        cliente = Cliente(
            cedula_pasaporte="0912345680", nombres="Carlos", apellidos="Gómez",
            tipo_cliente=TipoCliente.EXTRANJERO
        )
        db.add(cliente)
        db.commit()
        result = repo.get_by_cedula("0912345680")
        assert result is not None
        assert result.nombres == "Carlos"

    def test_get_by_cedula_no_existe(self, db):
        repo = ClienteRepository(db)
        result = repo.get_by_cedula("0000000000")
        assert result is None

    def test_create(self, db):
        repo = ClienteRepository(db)
        cliente = Cliente(
            cedula_pasaporte="0912345681", nombres="María", apellidos="Torres",
            tipo_cliente=TipoCliente.NACIONAL
        )
        result = repo.create(cliente)
        assert result.id is not None

    def test_update(self, db):
        repo = ClienteRepository(db)
        cliente = Cliente(
            cedula_pasaporte="0912345682", nombres="Pedro", apellidos="Ruiz",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        cliente.nombres = "Pedro Actualizado"
        result = repo.update(cliente)
        assert result.nombres == "Pedro Actualizado"

    def test_delete(self, db):
        repo = ClienteRepository(db)
        cliente = Cliente(
            cedula_pasaporte="0912345683", nombres="Luis", apellidos="Mora",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        repo.delete(cliente)
        assert repo.get_by_id(cliente.id) is None


class TestClienteService:
    """Pruebas unitarias para ClienteService."""

    def test_listar(self, db):
        service = ClienteService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_obtener_existente(self, db):
        service = ClienteService(db)
        cliente = Cliente(
            cedula_pasaporte="0912345684", nombres="Test", apellidos="Client",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        result = service.obtener(cliente.id)
        assert result.cedula_pasaporte == "0912345684"

    def test_obtener_no_existente(self, db):
        service = ClienteService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_buscar_por_cedula(self, db):
        service = ClienteService(db)
        cliente = Cliente(
            cedula_pasaporte="0912345685", nombres="Buscar", apellidos="Test",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        result = service.buscar_por_cedula("0912345685")
        assert result.nombres == "Buscar"

    def test_buscar_por_cedula_no_existe(self, db):
        service = ClienteService(db)
        with pytest.raises(HTTPException) as exc:
            service.buscar_por_cedula("0000000000")
        assert exc.value.status_code == 404

    def test_crear(self, db):
        service = ClienteService(db)
        data = ClienteCreate(
            cedula_pasaporte="0912345686", nombres="Nuevo", apellidos="Cliente",
            tipo_cliente=TipoCliente.NACIONAL
        )
        result = service.crear(data)
        assert result.id is not None

    def test_crear_cedula_duplicada(self, db):
        service = ClienteService(db)
        data = ClienteCreate(
            cedula_pasaporte="0912345687", nombres="Dup", apellidos="Test",
            tipo_cliente=TipoCliente.NACIONAL
        )
        service.crear(data)
        with pytest.raises(HTTPException) as exc:
            service.crear(data)
        assert exc.value.status_code == 400

    def test_actualizar(self, db):
        service = ClienteService(db)
        cliente = Cliente(
            cedula_pasaporte="0912345688", nombres="Original", apellidos="Client",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        data = ClienteUpdate(nombres="Actualizado")
        result = service.actualizar(cliente.id, data)
        assert result.nombres == "Actualizado"

    def test_eliminar(self, db):
        service = ClienteService(db)
        cliente = Cliente(
            cedula_pasaporte="0912345689", nombres="Borrar", apellidos="Client",
            tipo_cliente=TipoCliente.NACIONAL
        )
        db.add(cliente)
        db.commit()
        result = service.eliminar(cliente.id)
        assert result["detail"] == "Cliente eliminado"

import pytest
from fastapi import HTTPException

from models.habitacion import TipoHabitacion, Habitacion, EstadoHabitacion
from schemas.habitacion import (
    TipoHabitacionCreate, TipoHabitacionUpdate,
    HabitacionCreate, HabitacionUpdate,
)
from services.habitacion import TipoHabitacionService, HabitacionService
from repositories.habitacion import TipoHabitacionRepository, HabitacionRepository


class TestTipoHabitacionRepository:
    """Pruebas unitarias para TipoHabitacionRepository."""

    def test_get_all(self, db):
        repo = TipoHabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Simple", capacidad_maxima=2, tarifa_base=50.0)
        db.add(tipo)
        db.commit()
        result = repo.get_all()
        assert len(result) == 1

    def test_get_by_id(self, db):
        repo = TipoHabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Doble", capacidad_maxima=4, tarifa_base=80.0)
        db.add(tipo)
        db.commit()
        result = repo.get_by_id(tipo.id)
        assert result.nombre == "Doble"

    def test_create(self, db):
        repo = TipoHabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Suite", capacidad_maxima=3, tarifa_base=150.0)
        result = repo.create(tipo)
        assert result.id is not None

    def test_update(self, db):
        repo = TipoHabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Basic", capacidad_maxima=1, tarifa_base=30.0)
        db.add(tipo)
        db.commit()
        tipo.tarifa_base = 35.0
        result = repo.update(tipo)
        assert result.tarifa_base == 35.0

    def test_delete(self, db):
        repo = TipoHabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Eliminar", capacidad_maxima=1, tarifa_base=20.0)
        db.add(tipo)
        db.commit()
        repo.delete(tipo)
        assert repo.get_by_id(tipo.id) is None


class TestHabitacionRepository:
    """Pruebas unitarias para HabitacionRepository."""

    def test_get_all(self, db):
        repo = HabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Simple", capacidad_maxima=2, tarifa_base=50.0)
        db.add(tipo)
        db.commit()
        hab = Habitacion(numero="101", piso=1, tipo_habitacion_id=tipo.id)
        db.add(hab)
        db.commit()
        result = repo.get_all()
        assert len(result) == 1

    def test_get_by_numero(self, db):
        repo = HabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Doble", capacidad_maxima=4, tarifa_base=80.0)
        db.add(tipo)
        db.commit()
        hab = Habitacion(numero="201", piso=2, tipo_habitacion_id=tipo.id)
        db.add(hab)
        db.commit()
        result = repo.get_by_numero("201")
        assert result is not None
        assert result.piso == 2

    def test_get_disponibles(self, db):
        repo = HabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Suite", capacidad_maxima=3, tarifa_base=150.0)
        db.add(tipo)
        db.commit()
        hab1 = Habitacion(numero="301", piso=3, tipo_habitacion_id=tipo.id, estado=EstadoHabitacion.DISPONIBLE)
        hab2 = Habitacion(numero="302", piso=3, tipo_habitacion_id=tipo.id, estado=EstadoHabitacion.OCUPADA)
        db.add_all([hab1, hab2])
        db.commit()
        result = repo.get_disponibles()
        assert len(result) == 1
        assert result[0].numero == "301"

    def test_create(self, db):
        repo = HabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Familiar", capacidad_maxima=6, tarifa_base=120.0)
        db.add(tipo)
        db.commit()
        hab = Habitacion(numero="401", piso=4, tipo_habitacion_id=tipo.id)
        result = repo.create(hab)
        assert result.id is not None

    def test_delete(self, db):
        repo = HabitacionRepository(db)
        tipo = TipoHabitacion(nombre="Del", capacidad_maxima=1, tarifa_base=20.0)
        db.add(tipo)
        db.commit()
        hab = Habitacion(numero="999", piso=9, tipo_habitacion_id=tipo.id)
        db.add(hab)
        db.commit()
        repo.delete(hab)
        assert repo.get_by_id(hab.id) is None


class TestTipoHabitacionService:
    """Pruebas unitarias para TipoHabitacionService."""

    def test_listar(self, db):
        service = TipoHabitacionService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_obtener_no_existente(self, db):
        service = TipoHabitacionService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_crear(self, db):
        service = TipoHabitacionService(db)
        data = TipoHabitacionCreate(nombre="Nueva", capacidad_maxima=2, tarifa_base=60.0)
        result = service.crear(data)
        assert result.id is not None
        assert result.nombre == "Nueva"

    def test_actualizar(self, db):
        service = TipoHabitacionService(db)
        tipo = TipoHabitacion(nombre="Vieja", capacidad_maxima=2, tarifa_base=40.0)
        db.add(tipo)
        db.commit()
        data = TipoHabitacionUpdate(tarifa_base=45.0)
        result = service.actualizar(tipo.id, data)
        assert result.tarifa_base == 45.0

    def test_eliminar(self, db):
        service = TipoHabitacionService(db)
        tipo = TipoHabitacion(nombre="Borrar", capacidad_maxima=1, tarifa_base=25.0)
        db.add(tipo)
        db.commit()
        result = service.eliminar(tipo.id)
        assert result["detail"] == "Tipo de habitación eliminado"


class TestHabitacionService:
    """Pruebas unitarias para HabitacionService."""

    def test_listar(self, db):
        service = HabitacionService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_listar_disponibles(self, db):
        service = HabitacionService(db)
        result = service.listar_disponibles()
        assert isinstance(result, list)

    def test_obtener_no_existente(self, db):
        service = HabitacionService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_crear(self, db):
        service = HabitacionService(db)
        tipo = TipoHabitacion(nombre="Test", capacidad_maxima=2, tarifa_base=50.0)
        db.add(tipo)
        db.commit()
        data = HabitacionCreate(numero="501", piso=5, tipo_habitacion_id=tipo.id)
        result = service.crear(data)
        assert result.id is not None

    def test_crear_numero_duplicado(self, db):
        service = HabitacionService(db)
        tipo = TipoHabitacion(nombre="Dup", capacidad_maxima=2, tarifa_base=50.0)
        db.add(tipo)
        db.commit()
        data = HabitacionCreate(numero="502", piso=5, tipo_habitacion_id=tipo.id)
        service.crear(data)
        with pytest.raises(HTTPException) as exc:
            service.crear(data)
        assert exc.value.status_code == 400

    def test_actualizar(self, db):
        service = HabitacionService(db)
        tipo = TipoHabitacion(nombre="Upd", capacidad_maxima=2, tarifa_base=50.0)
        db.add(tipo)
        db.commit()
        hab = Habitacion(numero="503", piso=5, tipo_habitacion_id=tipo.id)
        db.add(hab)
        db.commit()
        data = HabitacionUpdate(estado=EstadoHabitacion.MANTENIMIENTO)
        result = service.actualizar(hab.id, data)
        assert result.estado == EstadoHabitacion.MANTENIMIENTO

    def test_eliminar(self, db):
        service = HabitacionService(db)
        tipo = TipoHabitacion(nombre="Del2", capacidad_maxima=1, tarifa_base=20.0)
        db.add(tipo)
        db.commit()
        hab = Habitacion(numero="504", piso=5, tipo_habitacion_id=tipo.id)
        db.add(hab)
        db.commit()
        result = service.eliminar(hab.id)
        assert result["detail"] == "Habitación eliminada"

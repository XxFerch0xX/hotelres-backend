import pytest
from datetime import date
from fastapi import HTTPException

from models.usuario import Usuario, RolUsuario
from models.cliente import Cliente, TipoCliente
from models.habitacion import TipoHabitacion, Habitacion, EstadoHabitacion
from models.reserva import Reserva, ReservaHabitacion, EstadoReserva
from schemas.reserva import ReservaCreate, ReservaUpdate, CancelacionRequest
from services.reserva import ReservaService
from repositories.reserva import ReservaRepository, ReservaHabitacionRepository


def crear_datos_base(db):
    """Helper para crear usuario, cliente y habitación de prueba."""
    usuario = Usuario(
        nombres="Admin", apellidos="Test", email="admin@test.com",
        password_hash="hash", rol=RolUsuario.ADMINISTRADOR
    )
    cliente = Cliente(
        cedula_pasaporte="0900000001", nombres="Huésped", apellidos="Test",
        tipo_cliente=TipoCliente.NACIONAL
    )
    tipo = TipoHabitacion(nombre="Simple", capacidad_maxima=2, tarifa_base=50.0)
    db.add_all([usuario, cliente, tipo])
    db.commit()
    habitacion = Habitacion(numero="101", piso=1, tipo_habitacion_id=tipo.id)
    db.add(habitacion)
    db.commit()
    return usuario, cliente, habitacion


class TestReservaRepository:
    """Pruebas unitarias para ReservaRepository."""

    def test_get_all(self, db):
        repo = ReservaRepository(db)
        result = repo.get_all()
        assert isinstance(result, list)

    def test_get_by_id(self, db):
        repo = ReservaRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id
        )
        db.add(reserva)
        db.commit()
        result = repo.get_by_id(reserva.id)
        assert result is not None

    def test_get_by_cliente(self, db):
        repo = ReservaRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 9, 1),
            fecha_checkout=date(2026, 9, 5), num_huespedes=1,
            usuario_id=usuario.id
        )
        db.add(reserva)
        db.commit()
        result = repo.get_by_cliente(cliente.id)
        assert len(result) == 1

    def test_get_activas(self, db):
        repo = ReservaRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id, estado=EstadoReserva.EN_CURSO
        )
        db.add(reserva)
        db.commit()
        result = repo.get_activas()
        assert len(result) == 1

    def test_create(self, db):
        repo = ReservaRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 10, 1),
            fecha_checkout=date(2026, 10, 3), num_huespedes=2,
            usuario_id=usuario.id
        )
        result = repo.create(reserva)
        assert result.id is not None

    def test_delete(self, db):
        repo = ReservaRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 11, 1),
            fecha_checkout=date(2026, 11, 3), num_huespedes=1,
            usuario_id=usuario.id
        )
        db.add(reserva)
        db.commit()
        repo.delete(reserva)
        assert repo.get_by_id(reserva.id) is None


class TestReservaHabitacionRepository:
    """Pruebas unitarias para ReservaHabitacionRepository."""

    def test_create(self, db):
        repo = ReservaHabitacionRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id
        )
        db.add(reserva)
        db.commit()
        rh = ReservaHabitacion(reserva_id=reserva.id, habitacion_id=hab.id)
        result = repo.create(rh)
        assert result.id is not None

    def test_get_by_reserva(self, db):
        repo = ReservaHabitacionRepository(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id
        )
        db.add(reserva)
        db.commit()
        rh = ReservaHabitacion(reserva_id=reserva.id, habitacion_id=hab.id)
        db.add(rh)
        db.commit()
        result = repo.get_by_reserva(reserva.id)
        assert len(result) == 1


class TestReservaService:
    """Pruebas unitarias para ReservaService."""

    def test_listar(self, db):
        service = ReservaService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_obtener_no_existente(self, db):
        service = ReservaService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_crear_reserva(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[hab.id],
            fecha_checkin=date(2026, 8, 1), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        result = service.crear(data)
        assert result.id is not None
        assert result.estado == EstadoReserva.PENDIENTE

    def test_crear_reserva_fechas_invalidas(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[hab.id],
            fecha_checkin=date(2026, 8, 5), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        with pytest.raises(HTTPException) as exc:
            service.crear(data)
        assert exc.value.status_code == 400

    def test_crear_reserva_habitacion_no_disponible(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        hab.estado = EstadoHabitacion.OCUPADA
        db.commit()
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[hab.id],
            fecha_checkin=date(2026, 8, 1), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        with pytest.raises(HTTPException) as exc:
            service.crear(data)
        assert exc.value.status_code == 400

    def test_crear_reserva_habitacion_inexistente(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[999],
            fecha_checkin=date(2026, 8, 1), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        with pytest.raises(HTTPException) as exc:
            service.crear(data)
        assert exc.value.status_code == 404

    def test_checkin(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[hab.id],
            fecha_checkin=date(2026, 8, 1), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        reserva = service.crear(data)
        result = service.checkin(reserva.id)
        assert result.estado == EstadoReserva.EN_CURSO

    def test_checkin_estado_invalido(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id, estado=EstadoReserva.COMPLETADA
        )
        db.add(reserva)
        db.commit()
        with pytest.raises(HTTPException) as exc:
            service.checkin(reserva.id)
        assert exc.value.status_code == 400

    def test_checkout(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[hab.id],
            fecha_checkin=date(2026, 8, 1), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        reserva = service.crear(data)
        service.checkin(reserva.id)
        result = service.checkout(reserva.id)
        assert result.estado == EstadoReserva.COMPLETADA

    def test_checkout_estado_invalido(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id, estado=EstadoReserva.PENDIENTE
        )
        db.add(reserva)
        db.commit()
        with pytest.raises(HTTPException) as exc:
            service.checkout(reserva.id)
        assert exc.value.status_code == 400

    def test_cancelar(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        data = ReservaCreate(
            cliente_id=cliente.id, habitacion_ids=[hab.id],
            fecha_checkin=date(2026, 8, 1), fecha_checkout=date(2026, 8, 3),
            num_huespedes=2, usuario_id=usuario.id
        )
        reserva = service.crear(data)
        cancel = CancelacionRequest(motivo_cancelacion="Cambio de planes")
        result = service.cancelar(reserva.id, cancel)
        assert result.estado == EstadoReserva.CANCELADA
        assert result.motivo_cancelacion == "Cambio de planes"

    def test_cancelar_estado_invalido(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id, estado=EstadoReserva.COMPLETADA
        )
        db.add(reserva)
        db.commit()
        cancel = CancelacionRequest(motivo_cancelacion="Test")
        with pytest.raises(HTTPException) as exc:
            service.cancelar(reserva.id, cancel)
        assert exc.value.status_code == 400

    def test_historial_cliente(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        result = service.historial_cliente(cliente.id)
        assert isinstance(result, list)

    def test_huespedes_activos(self, db):
        service = ReservaService(db)
        result = service.huespedes_activos()
        assert isinstance(result, list)

    def test_actualizar_reserva(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id, estado=EstadoReserva.PENDIENTE
        )
        db.add(reserva)
        db.commit()
        data = ReservaUpdate(num_huespedes=3)
        result = service.actualizar(reserva.id, data)
        assert result.num_huespedes == 3

    def test_actualizar_reserva_estado_invalido(self, db):
        service = ReservaService(db)
        usuario, cliente, hab = crear_datos_base(db)
        reserva = Reserva(
            cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
            fecha_checkout=date(2026, 8, 3), num_huespedes=2,
            usuario_id=usuario.id, estado=EstadoReserva.COMPLETADA
        )
        db.add(reserva)
        db.commit()
        data = ReservaUpdate(num_huespedes=3)
        with pytest.raises(HTTPException) as exc:
            service.actualizar(reserva.id, data)
        assert exc.value.status_code == 400

import pytest
from datetime import date, datetime, timezone
from fastapi import HTTPException

from models.usuario import Usuario, RolUsuario
from models.cliente import Cliente, TipoCliente
from models.habitacion import TipoHabitacion, Habitacion
from models.reserva import Reserva
from models.facturacion import Consumo, Factura, Pago, MetodoPago
from models.finanzas import CuentaContable, AsientoContable, GastoOperativo, TipoCuenta
from models.configuracion import ParametroSistema
from schemas.facturacion import ConsumoCreate, FacturaCreate, DetalleFacturaCreate, PagoCreate
from schemas.finanzas import CuentaContableCreate, CuentaContableUpdate, AsientoContableCreate, GastoOperativoCreate
from schemas.configuracion import ParametroSistemaCreate
from services.facturacion import ConsumoService, FacturaService, PagoService
from services.finanzas import CuentaContableService, AsientoContableService, GastoOperativoService
from services.configuracion import ParametroSistemaService, AuditoriaService
from repositories.facturacion import ConsumoRepository, FacturaRepository, PagoRepository
from repositories.finanzas import CuentaContableRepository, AsientoContableRepository, GastoOperativoRepository
from repositories.configuracion import ParametroSistemaRepository, AuditoriaLogRepository


def crear_reserva_completa(db):
    """Helper para crear una reserva completa para pruebas de facturación."""
    usuario = Usuario(
        nombres="Admin", apellidos="Test", email="admin_fac@test.com",
        password_hash="hash", rol=RolUsuario.ADMINISTRADOR
    )
    cliente = Cliente(
        cedula_pasaporte="0900000099", nombres="Cliente", apellidos="Fac",
        tipo_cliente=TipoCliente.NACIONAL
    )
    tipo = TipoHabitacion(nombre="Simple", capacidad_maxima=2, tarifa_base=50.0)
    db.add_all([usuario, cliente, tipo])
    db.commit()
    hab = Habitacion(numero="100", piso=1, tipo_habitacion_id=tipo.id)
    db.add(hab)
    db.commit()
    reserva = Reserva(
        cliente_id=cliente.id, fecha_checkin=date(2026, 8, 1),
        fecha_checkout=date(2026, 8, 3), num_huespedes=2,
        usuario_id=usuario.id
    )
    db.add(reserva)
    db.commit()
    return usuario, cliente, reserva


# ==================== CONSUMO ====================

class TestConsumoRepository:
    def test_get_by_reserva(self, db):
        repo = ConsumoRepository(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        consumo = Consumo(
            reserva_id=reserva.id, descripcion="Minibar",
            categoria="Bebidas", cantidad=2, precio_unitario=5.0
        )
        db.add(consumo)
        db.commit()
        result = repo.get_by_reserva(reserva.id)
        assert len(result) == 1

    def test_create(self, db):
        repo = ConsumoRepository(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        consumo = Consumo(
            reserva_id=reserva.id, descripcion="Lavandería",
            categoria="Servicios", cantidad=1, precio_unitario=15.0
        )
        result = repo.create(consumo)
        assert result.id is not None


class TestConsumoService:
    def test_listar_por_reserva(self, db):
        service = ConsumoService(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        result = service.listar_por_reserva(reserva.id)
        assert isinstance(result, list)

    def test_crear(self, db):
        service = ConsumoService(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        data = ConsumoCreate(
            reserva_id=reserva.id, descripcion="Room Service",
            categoria="Alimentos", cantidad=1, precio_unitario=25.0
        )
        result = service.crear(data)
        assert result.id is not None
        assert result.descripcion == "Room Service"


# ==================== FACTURA ====================

class TestFacturaRepository:
    def test_get_all(self, db):
        repo = FacturaRepository(db)
        result = repo.get_all()
        assert isinstance(result, list)

    def test_get_last_number_sin_facturas(self, db):
        repo = FacturaRepository(db)
        result = repo.get_last_number()
        assert result == 0

    def test_create(self, db):
        repo = FacturaRepository(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        factura = Factura(
            reserva_id=reserva.id, cliente_id=cliente.id,
            numero_factura="FAC-000001", subtotal=100.0,
            iva=15.0, total=115.0, metodo_pago=MetodoPago.EFECTIVO
        )
        result = repo.create(factura)
        assert result.id is not None

    def test_get_by_id(self, db):
        repo = FacturaRepository(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        factura = Factura(
            reserva_id=reserva.id, cliente_id=cliente.id,
            numero_factura="FAC-000002", subtotal=200.0,
            iva=30.0, total=230.0, metodo_pago=MetodoPago.TARJETA_CREDITO
        )
        db.add(factura)
        db.commit()
        result = repo.get_by_id(factura.id)
        assert result is not None


class TestFacturaService:
    def test_listar(self, db):
        service = FacturaService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_obtener_no_existente(self, db):
        service = FacturaService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_crear_con_parametros(self, db):
        service = FacturaService(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        # Crear parámetros del sistema con IVA
        param = ParametroSistema(
            nombre_hotel="Hotel Test", ruc="0990000001",
            porcentaje_iva=15.0
        )
        db.add(param)
        db.commit()
        data = FacturaCreate(
            reserva_id=reserva.id, cliente_id=cliente.id,
            metodo_pago=MetodoPago.EFECTIVO,
            detalles=[DetalleFacturaCreate(
                descripcion="2 noches", cantidad=2,
                precio_unitario=50.0, subtotal=100.0
            )]
        )
        result = service.crear(data)
        assert result.numero_factura == "FAC-000001"
        assert result.subtotal == 100.0
        assert result.iva == 15.0
        assert result.total == 115.0

    def test_crear_sin_parametros(self, db):
        service = FacturaService(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        data = FacturaCreate(
            reserva_id=reserva.id, cliente_id=cliente.id,
            metodo_pago=MetodoPago.TRANSFERENCIA,
            detalles=[DetalleFacturaCreate(
                descripcion="1 noche", cantidad=1,
                precio_unitario=80.0, subtotal=80.0
            )]
        )
        result = service.crear(data)
        assert result.iva == 80.0 * 0.15


# ==================== PAGO ====================

class TestPagoRepository:
    def test_get_by_reserva(self, db):
        repo = PagoRepository(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        result = repo.get_by_reserva(reserva.id)
        assert isinstance(result, list)

    def test_create(self, db):
        repo = PagoRepository(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        pago = Pago(
            reserva_id=reserva.id, monto=50.0,
            metodo_pago=MetodoPago.EFECTIVO
        )
        result = repo.create(pago)
        assert result.id is not None


class TestPagoService:
    def test_listar_por_reserva(self, db):
        service = PagoService(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        result = service.listar_por_reserva(reserva.id)
        assert isinstance(result, list)

    def test_crear(self, db):
        service = PagoService(db)
        usuario, cliente, reserva = crear_reserva_completa(db)
        data = PagoCreate(
            reserva_id=reserva.id, monto=100.0,
            metodo_pago=MetodoPago.TARJETA_DEBITO
        )
        result = service.crear(data)
        assert result.monto == 100.0


# ==================== CUENTA CONTABLE ====================

class TestCuentaContableService:
    def test_listar(self, db):
        service = CuentaContableService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_obtener_no_existente(self, db):
        service = CuentaContableService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_crear(self, db):
        service = CuentaContableService(db)
        data = CuentaContableCreate(
            codigo="4.1.01", nombre="Ingresos por reservas",
            tipo=TipoCuenta.INGRESO
        )
        result = service.crear(data)
        assert result.id is not None

    def test_actualizar(self, db):
        service = CuentaContableService(db)
        cuenta = CuentaContable(
            codigo="5.1.01", nombre="Gastos operativos",
            tipo=TipoCuenta.EGRESO
        )
        db.add(cuenta)
        db.commit()
        data = CuentaContableUpdate(nombre="Gastos administrativos")
        result = service.actualizar(cuenta.id, data)
        assert result.nombre == "Gastos administrativos"

    def test_eliminar(self, db):
        service = CuentaContableService(db)
        cuenta = CuentaContable(
            codigo="6.1.01", nombre="Borrar", tipo=TipoCuenta.ACTIVO
        )
        db.add(cuenta)
        db.commit()
        result = service.eliminar(cuenta.id)
        assert result["detail"] == "Cuenta contable eliminada"


# ==================== ASIENTO CONTABLE ====================

class TestAsientoContableService:
    def test_listar(self, db):
        service = AsientoContableService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_crear(self, db):
        service = AsientoContableService(db)
        usuario = Usuario(
            nombres="Cont", apellidos="Test", email="cont@test.com",
            password_hash="hash", rol=RolUsuario.AUDITOR
        )
        cuenta = CuentaContable(
            codigo="4.1.02", nombre="Ingresos", tipo=TipoCuenta.INGRESO
        )
        db.add_all([usuario, cuenta])
        db.commit()
        data = AsientoContableCreate(
            cuenta_id=cuenta.id, descripcion="Pago reserva #1",
            monto_debito=100.0, usuario_id=usuario.id
        )
        result = service.crear(data)
        assert result.id is not None

    def test_libro_diario(self, db):
        service = AsientoContableService(db)
        inicio = datetime(2026, 1, 1, tzinfo=timezone.utc)
        fin = datetime(2026, 12, 31, tzinfo=timezone.utc)
        result = service.libro_diario(inicio, fin)
        assert isinstance(result, list)


# ==================== GASTO OPERATIVO ====================

class TestGastoOperativoService:
    def test_listar(self, db):
        service = GastoOperativoService(db)
        result = service.listar()
        assert isinstance(result, list)

    def test_crear(self, db):
        service = GastoOperativoService(db)
        usuario = Usuario(
            nombres="Admin", apellidos="Gasto", email="gasto@test.com",
            password_hash="hash", rol=RolUsuario.ADMINISTRADOR
        )
        cuenta = CuentaContable(
            codigo="5.1.02", nombre="Suministros", tipo=TipoCuenta.EGRESO
        )
        db.add_all([usuario, cuenta])
        db.commit()
        data = GastoOperativoCreate(
            descripcion="Compra de toallas", categoria="Suministros",
            cuenta_id=cuenta.id, monto=200.0, usuario_id=usuario.id
        )
        result = service.crear(data)
        assert result.id is not None
        assert result.monto == 200.0


# ==================== CONFIGURACION ====================

class TestParametroSistemaService:
    def test_obtener_sin_config(self, db):
        service = ParametroSistemaService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener()
        assert exc.value.status_code == 404

    def test_crear(self, db):
        service = ParametroSistemaService(db)
        data = ParametroSistemaCreate(
            nombre_hotel="Hotel Test", ruc="0990000001"
        )
        result = service.crear_o_actualizar(data)
        assert result.nombre_hotel == "Hotel Test"

    def test_actualizar_existente(self, db):
        service = ParametroSistemaService(db)
        param = ParametroSistema(nombre_hotel="Viejo", ruc="0990000002")
        db.add(param)
        db.commit()
        data = ParametroSistemaCreate(
            nombre_hotel="Nuevo Hotel", ruc="0990000002"
        )
        result = service.crear_o_actualizar(data)
        assert result.nombre_hotel == "Nuevo Hotel"


class TestAuditoriaService:
    def test_listar(self, db):
        service = AuditoriaService(db)
        result = service.listar()
        assert isinstance(result, list)

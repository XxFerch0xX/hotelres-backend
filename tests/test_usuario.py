import pytest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException

from models.usuario import Usuario, RolUsuario
from schemas.usuario import UsuarioCreate, UsuarioUpdate
from services.usuario import UsuarioService
from repositories.usuario import UsuarioRepository


class TestUsuarioRepository:
    """Pruebas unitarias para UsuarioRepository."""

    def test_get_all(self, db):
        repo = UsuarioRepository(db)
        usuario = Usuario(
            nombres="Juan", apellidos="Pérez", email="juan@test.com",
            password_hash="hash123", rol=RolUsuario.ADMINISTRADOR
        )
        db.add(usuario)
        db.commit()
        result = repo.get_all()
        assert len(result) == 1
        assert result[0].nombres == "Juan"

    def test_get_by_id(self, db):
        repo = UsuarioRepository(db)
        usuario = Usuario(
            nombres="Ana", apellidos="López", email="ana@test.com",
            password_hash="hash123", rol=RolUsuario.RECEPCIONISTA
        )
        db.add(usuario)
        db.commit()
        result = repo.get_by_id(usuario.id)
        assert result is not None
        assert result.email == "ana@test.com"

    def test_get_by_id_no_existe(self, db):
        repo = UsuarioRepository(db)
        result = repo.get_by_id(999)
        assert result is None

    def test_get_by_email(self, db):
        repo = UsuarioRepository(db)
        usuario = Usuario(
            nombres="Carlos", apellidos="Gómez", email="carlos@test.com",
            password_hash="hash123", rol=RolUsuario.GERENTE
        )
        db.add(usuario)
        db.commit()
        result = repo.get_by_email("carlos@test.com")
        assert result is not None
        assert result.nombres == "Carlos"

    def test_get_by_email_no_existe(self, db):
        repo = UsuarioRepository(db)
        result = repo.get_by_email("noexiste@test.com")
        assert result is None

    def test_create(self, db):
        repo = UsuarioRepository(db)
        usuario = Usuario(
            nombres="María", apellidos="Torres", email="maria@test.com",
            password_hash="hash123", rol=RolUsuario.AUDITOR
        )
        result = repo.create(usuario)
        assert result.id is not None
        assert result.nombres == "María"

    def test_update(self, db):
        repo = UsuarioRepository(db)
        usuario = Usuario(
            nombres="Pedro", apellidos="Ruiz", email="pedro@test.com",
            password_hash="hash123", rol=RolUsuario.RECEPCIONISTA
        )
        db.add(usuario)
        db.commit()
        usuario.nombres = "Pedro Actualizado"
        result = repo.update(usuario)
        assert result.nombres == "Pedro Actualizado"

    def test_delete(self, db):
        repo = UsuarioRepository(db)
        usuario = Usuario(
            nombres="Luis", apellidos="Mora", email="luis@test.com",
            password_hash="hash123", rol=RolUsuario.GERENTE
        )
        db.add(usuario)
        db.commit()
        repo.delete(usuario)
        assert repo.get_by_id(usuario.id) is None


class TestUsuarioService:
    """Pruebas unitarias para UsuarioService."""

    def test_listar(self, db):
        service = UsuarioService(db)
        usuario = Usuario(
            nombres="Test", apellidos="User", email="test@test.com",
            password_hash="hash123", rol=RolUsuario.ADMINISTRADOR
        )
        db.add(usuario)
        db.commit()
        result = service.listar()
        assert len(result) >= 1

    def test_obtener_existente(self, db):
        service = UsuarioService(db)
        usuario = Usuario(
            nombres="Test", apellidos="User", email="test2@test.com",
            password_hash="hash123", rol=RolUsuario.ADMINISTRADOR
        )
        db.add(usuario)
        db.commit()
        result = service.obtener(usuario.id)
        assert result.email == "test2@test.com"

    def test_obtener_no_existente(self, db):
        service = UsuarioService(db)
        with pytest.raises(HTTPException) as exc:
            service.obtener(999)
        assert exc.value.status_code == 404

    def test_crear(self, db):
        service = UsuarioService(db)
        data = UsuarioCreate(
            nombres="Nuevo", apellidos="Usuario", email="nuevo@test.com",
            password="password123", rol=RolUsuario.RECEPCIONISTA
        )
        result = service.crear(data)
        assert result.id is not None
        assert result.email == "nuevo@test.com"
        assert result.password_hash != "password123"

    def test_crear_email_duplicado(self, db):
        service = UsuarioService(db)
        data = UsuarioCreate(
            nombres="User1", apellidos="Test", email="dup@test.com",
            password="pass", rol=RolUsuario.ADMINISTRADOR
        )
        service.crear(data)
        with pytest.raises(HTTPException) as exc:
            service.crear(data)
        assert exc.value.status_code == 400

    def test_actualizar(self, db):
        service = UsuarioService(db)
        usuario = Usuario(
            nombres="Original", apellidos="Name", email="orig@test.com",
            password_hash="hash123", rol=RolUsuario.ADMINISTRADOR
        )
        db.add(usuario)
        db.commit()
        data = UsuarioUpdate(nombres="Actualizado")
        result = service.actualizar(usuario.id, data)
        assert result.nombres == "Actualizado"

    def test_eliminar(self, db):
        service = UsuarioService(db)
        usuario = Usuario(
            nombres="Borrar", apellidos="User", email="borrar@test.com",
            password_hash="hash123", rol=RolUsuario.ADMINISTRADOR
        )
        db.add(usuario)
        db.commit()
        result = service.eliminar(usuario.id)
        assert result["detail"] == "Usuario eliminado"

    def test_eliminar_no_existente(self, db):
        service = UsuarioService(db)
        with pytest.raises(HTTPException):
            service.eliminar(999)

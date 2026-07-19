from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.reserva import Reserva, ReservaHabitacion, EstadoReserva
from models.habitacion import EstadoHabitacion
from schemas.reserva import ReservaCreate, ReservaUpdate, CancelacionRequest
from repositories.reserva import ReservaRepository, ReservaHabitacionRepository
from repositories.habitacion import HabitacionRepository


class ReservaService:
    def __init__(self, db: Session):
        self.repo = ReservaRepository(db)
        self.rh_repo = ReservaHabitacionRepository(db)
        self.hab_repo = HabitacionRepository(db)

    def listar(self):
        return self.repo.get_all()

    def obtener(self, reserva_id: int):
        reserva = self.repo.get_by_id(reserva_id)
        if not reserva:
            raise HTTPException(status_code=404, detail="Reserva no encontrada")
        return reserva

    def historial_cliente(self, cliente_id: int):
        return self.repo.get_by_cliente(cliente_id)

    def huespedes_activos(self):
        return self.repo.get_activas()

    def crear(self, data: ReservaCreate):
        if data.fecha_checkout <= data.fecha_checkin:
            raise HTTPException(status_code=400, detail="La fecha de checkout debe ser posterior al checkin")

        # Verificar disponibilidad de habitaciones
        for hab_id in data.habitacion_ids:
            hab = self.hab_repo.get_by_id(hab_id)
            if not hab:
                raise HTTPException(status_code=404, detail=f"Habitación {hab_id} no encontrada")
            if hab.estado != EstadoHabitacion.DISPONIBLE:
                raise HTTPException(status_code=400, detail=f"Habitación {hab.numero} no está disponible")

        reserva = Reserva(
            cliente_id=data.cliente_id,
            fecha_checkin=data.fecha_checkin,
            fecha_checkout=data.fecha_checkout,
            num_huespedes=data.num_huespedes,
            observaciones=data.observaciones,
            usuario_id=data.usuario_id,
        )
        reserva = self.repo.create(reserva)

        # Asignar habitaciones y marcarlas como reservadas
        for hab_id in data.habitacion_ids:
            rh = ReservaHabitacion(reserva_id=reserva.id, habitacion_id=hab_id)
            self.rh_repo.create(rh)
            hab = self.hab_repo.get_by_id(hab_id)
            hab.estado = EstadoHabitacion.RESERVADA
            self.hab_repo.update(hab)

        return reserva

    def actualizar(self, reserva_id: int, data: ReservaUpdate):
        reserva = self.obtener(reserva_id)
        if reserva.estado not in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]:
            raise HTTPException(status_code=400, detail="Solo se pueden modificar reservas pendientes o confirmadas")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(reserva, field, value)
        return self.repo.update(reserva)

    def checkin(self, reserva_id: int):
        reserva = self.obtener(reserva_id)
        if reserva.estado not in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]:
            raise HTTPException(status_code=400, detail="La reserva no está en estado válido para check-in")
        reserva.estado = EstadoReserva.EN_CURSO
        # Cambiar estado de habitaciones a OCUPADA
        for rh in self.rh_repo.get_by_reserva(reserva_id):
            hab = self.hab_repo.get_by_id(rh.habitacion_id)
            hab.estado = EstadoHabitacion.OCUPADA
            self.hab_repo.update(hab)
        return self.repo.update(reserva)

    def checkout(self, reserva_id: int):
        reserva = self.obtener(reserva_id)
        if reserva.estado != EstadoReserva.EN_CURSO:
            raise HTTPException(status_code=400, detail="La reserva no está en curso")
        reserva.estado = EstadoReserva.COMPLETADA
        # Liberar habitaciones
        for rh in self.rh_repo.get_by_reserva(reserva_id):
            hab = self.hab_repo.get_by_id(rh.habitacion_id)
            hab.estado = EstadoHabitacion.DISPONIBLE
            self.hab_repo.update(hab)
        return self.repo.update(reserva)

    def cancelar(self, reserva_id: int, data: CancelacionRequest):
        reserva = self.obtener(reserva_id)
        if reserva.estado not in [EstadoReserva.PENDIENTE, EstadoReserva.CONFIRMADA]:
            raise HTTPException(status_code=400, detail="Solo se pueden cancelar reservas pendientes o confirmadas")
        reserva.estado = EstadoReserva.CANCELADA
        reserva.motivo_cancelacion = data.motivo_cancelacion
        # Liberar habitaciones
        for rh in self.rh_repo.get_by_reserva(reserva_id):
            hab = self.hab_repo.get_by_id(rh.habitacion_id)
            hab.estado = EstadoHabitacion.DISPONIBLE
            self.hab_repo.update(hab)
        return self.repo.update(reserva)
# Servicio de reservas 

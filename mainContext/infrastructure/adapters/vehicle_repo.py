from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from mainContext.application.dtos.vehicle_dto import (
    VehicleCreateDTO,
    VehicleDTO,
    VehicleTableRowDTO,
    VehicleUpdateDTO,
)
from mainContext.application.ports.vehicle_repo import VehicleRepo
from mainContext.domain.models.Vehicle import Vehicle
from mainContext.infrastructure.models import Vehicles as VehicleModel, Employees as EmployeeModel


class VehicleRepoImpl(VehicleRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_vehicle(self, dto: VehicleCreateDTO) -> int:
        try:
            model = VehicleModel(
                name=dto.name,
                license_plate=dto.license_plate,
                model=dto.model,
                odometer=dto.odometer,
                employee_id=dto.employee_id,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al crear vehículo: {e}")

    def get_vehicle_by_id(self, vehicle_id: int) -> Optional[Vehicle]:
        model = (
            self.db.query(VehicleModel)
            .options(joinedload(VehicleModel.employee))
            .filter_by(id=vehicle_id)
            .first()
        )
        if not model:
            return None
        return Vehicle(
            id=model.id,
            name=model.name,
            license_plate=model.license_plate,
            employee=model.employee,
            employee_id=model.employee_id,
            model=model.model,
            odometer=model.odometer,
        )

    def list_vehicles(self) -> List[Vehicle]:
        models = self.db.query(VehicleModel).options(joinedload(VehicleModel.employee)).all()
        return [
            Vehicle(
                id=m.id,
                name=m.name,
                license_plate=m.license_plate,
                employee=m.employee,
                employee_id=m.employee_id,
                model=m.model,
                odometer=m.odometer,
            )
            for m in models
        ]

    def list_vehicles_table(self) -> List[VehicleTableRowDTO]:
        rows = (
            self.db.query(
                VehicleModel.id,
                VehicleModel.name,
                VehicleModel.license_plate,
                VehicleModel.model,
                VehicleModel.odometer,
                EmployeeModel.name.label("employee_name"),
                EmployeeModel.lastname.label("employee_lastname"),
            )
            .join(EmployeeModel, VehicleModel.employee_id == EmployeeModel.id, isouter=True)
            .order_by(VehicleModel.id.desc())
            .all()
        )

        result: List[VehicleTableRowDTO] = []
        for row in rows:
            emp_name = row.employee_name or ""
            emp_last = row.employee_lastname or ""
            employee_full_name = f"{emp_name} {emp_last}".strip() or None
            result.append(
                VehicleTableRowDTO(
                    id=row.id,
                    name=row.name,
                    license_plate=row.license_plate,
                    model=row.model,
                    odometer=row.odometer,
                    employee_name=employee_full_name,
                )
            )
        return result

    def update_vehicle(self, vehicle_id: int, dto: VehicleUpdateDTO) -> bool:
        try:
            model = self.db.query(VehicleModel).filter_by(id=vehicle_id).first()
            if not model:
                return False

            if dto.name is not None:
                model.name = dto.name
            if dto.license_plate is not None:
                model.license_plate = dto.license_plate
            if dto.model is not None:
                model.model = dto.model
            if dto.odometer is not None:
                model.odometer = dto.odometer
            if dto.employee_id is not None:
                model.employee_id = dto.employee_id

            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise

    def delete_vehicle(self, vehicle_id: int) -> bool:
        try:
            model = self.db.query(VehicleModel).filter_by(id=vehicle_id).first()
            if not model:
                return False
            self.db.delete(model)
            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            raise

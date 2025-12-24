from datetime import datetime
from typing import List, Optional
from sqlalchemy.orm import Session
from mainContext.application.dtos.service_record_dto import ServiceRecordDTO
from mainContext.application.ports.ServiceRecordRepo import ServiceRecordRepo
from mainContext.infrastructure.models import (
    Employees,
    Fobc01,
    Foem01,
    Foim01,
    Fole01,
    Foos01,
    Fopc02,
    Fosc01,
    Fosp01,
)


class ServiceRecordRepoImpl(ServiceRecordRepo):
    def __init__(self, db: Session):
        self.db = db

    def list_service_records(self, equipment_id: int) -> List[ServiceRecordDTO]:
        records: List[ServiceRecordDTO] = []

        records.extend(self._map_fole01(equipment_id))
        records.extend(self._map_foim01(equipment_id))
        records.extend(self._map_fosp01(equipment_id))
        records.extend(self._map_fosc01(equipment_id))
        records.extend(self._map_foos01(equipment_id))
        records.extend(self._map_foem01(equipment_id))
        records.extend(self._map_fobc01(equipment_id))
        records.extend(self._map_fopc02(equipment_id))

        records.sort(key=lambda item: item.date_created or datetime.min, reverse=True)
        return records

    def _map_fole01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Fole01.id,
                Fole01.date_created,
                Fole01.status,
                Fole01.rating,
                Fole01.rating_comment,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Fole01.employee_id == Employees.id)
            .filter(Fole01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="fole01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=row.rating,
                rating_comment=row.rating_comment,
                file_id=None,
                observations=None,
            )
            for row in rows
        ]

    def _map_foim01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Foim01.id,
                Foim01.date_created,
                Foim01.status,
                Foim01.rating,
                Foim01.rating_comment,
                Foim01.observations,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Foim01.employee_id == Employees.id)
            .filter(Foim01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="foim01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=row.rating,
                rating_comment=row.rating_comment,
                file_id=None,
                observations=row.observations,
            )
            for row in rows
        ]

    def _map_fosp01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Fosp01.id,
                Fosp01.date_created,
                Fosp01.status,
                Fosp01.rating,
                Fosp01.rating_comment,
                Fosp01.observations,
                Fosp01.file_id,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Fosp01.employee_id == Employees.id)
            .filter(Fosp01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="fosp01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=row.rating,
                rating_comment=row.rating_comment,
                file_id=row.file_id,
                observations=row.observations,
            )
            for row in rows
        ]

    def _map_fosc01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Fosc01.id,
                Fosc01.date_created,
                Fosc01.status,
                Fosc01.rating,
                Fosc01.rating_comment,
                Fosc01.observations,
                Fosc01.file_id,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Fosc01.employee_id == Employees.id)
            .filter(Fosc01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="fosc01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=row.rating,
                rating_comment=row.rating_comment,
                file_id=row.file_id,
                observations=row.observations,
            )
            for row in rows
        ]

    def _map_foos01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Foos01.id,
                Foos01.date_created,
                Foos01.status,
                Foos01.rating,
                Foos01.rating_comment,
                Foos01.observations,
                Foos01.file_id,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Foos01.employee_id == Employees.id)
            .filter(Foos01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="foos01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=row.rating,
                rating_comment=row.rating_comment,
                file_id=row.file_id,
                observations=row.observations,
            )
            for row in rows
        ]

    def _map_foem01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Foem01.id,
                Foem01.date_created,
                Foem01.status,
                Foem01.file_id,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Foem01.employee_id == Employees.id)
            .filter(Foem01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="foem01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=None,
                rating_comment=None,
                file_id=row.file_id,
                observations=None,
            )
            for row in rows
        ]

    def _map_fobc01(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Fobc01.id,
                Fobc01.date_created,
                Fobc01.status,
                Fobc01.rating,
                Fobc01.rating_comment,
                Fobc01.observations,
                Fobc01.file_id,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Fobc01.employee_id == Employees.id)
            .filter(Fobc01.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="fobc01",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=row.rating,
                rating_comment=row.rating_comment,
                file_id=row.file_id,
                observations=row.observations,
            )
            for row in rows
        ]

    def _map_fopc02(self, equipment_id: int) -> List[ServiceRecordDTO]:
        rows = (
            self.db.query(
                Fopc02.id,
                Fopc02.date_created,
                Fopc02.status,
                Fopc02.observations,
                Fopc02.file_id,
                Employees.name.label("emp_name"),
                Employees.lastname.label("emp_lastname"),
            )
            .outerjoin(Employees, Fopc02.employee_id == Employees.id)
            .filter(Fopc02.equipment_id == equipment_id)
            .all()
        )

        return [
            ServiceRecordDTO(
                format="fopc02",
                id=row.id,
                date_created=row.date_created,
                employee_name=self._full_name(row.emp_name, row.emp_lastname),
                status=row.status,
                rating=None,
                rating_comment=None,
                file_id=row.file_id,
                observations=row.observations,
            )
            for row in rows
        ]

    def _full_name(self, name: Optional[str], lastname: Optional[str]) -> Optional[str]:
        parts = [part for part in (name, lastname) if part]
        return " ".join(parts) if parts else None

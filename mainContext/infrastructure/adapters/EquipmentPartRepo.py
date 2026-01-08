from typing import List, Optional

from sqlalchemy.orm import Session

from mainContext.application.ports.EquipmentPartRepo import EquipmentPartRepo
from mainContext.application.dtos.equipment_part_dto import (
    EquipmentPartDTO,
    EquipmentPartCreateDTO,
    EquipmentPartUpdateDTO,
)
from mainContext.infrastructure.models import EquipmentParts as EquipmentPartModel


class EquipmentPartRepoImpl(EquipmentPartRepo):
    def __init__(self, db: Session):
        self.db = db

    def _to_dto(self, model: EquipmentPartModel) -> EquipmentPartDTO:
        return EquipmentPartDTO(
            id=model.id,
            part_number=model.part_number,
            description=model.description,
            amount=model.amount,
            equipment_id=model.equipment_id,
        )

    def create_equipment_part(self, dto: EquipmentPartCreateDTO) -> int:
        try:
            model = EquipmentPartModel(
                part_number=dto.part_number,
                description=dto.description,
                amount=dto.amount,
                equipment_id=dto.equipment_id,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al crear parte de equipo: {exc}")

    def get_equipment_part_by_id(self, part_id: int) -> Optional[EquipmentPartDTO]:
        try:
            model = self.db.query(EquipmentPartModel).filter_by(id=part_id).first()
            if not model:
                return None
            return self._to_dto(model)
        except Exception as exc:
            raise Exception(f"Error al obtener parte de equipo: {exc}")

    def get_equipment_parts_by_equipment(self, equipment_id: int) -> List[EquipmentPartDTO]:
        try:
            models = self.db.query(EquipmentPartModel).filter_by(equipment_id=equipment_id).all()
            return [self._to_dto(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar partes de equipo: {exc}")

    def get_all_equipment_parts(self) -> List[EquipmentPartDTO]:
        try:
            models = self.db.query(EquipmentPartModel).all()
            return [self._to_dto(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar partes de equipo: {exc}")

    def update_equipment_part(self, part_id: int, dto: EquipmentPartUpdateDTO) -> bool:
        try:
            model = self.db.query(EquipmentPartModel).filter_by(id=part_id).first()
            if not model:
                return False

            if dto.part_number is not None:
                model.part_number = dto.part_number
            if dto.description is not None:
                model.description = dto.description
            if dto.amount is not None:
                model.amount = dto.amount
            if dto.equipment_id is not None:
                model.equipment_id = dto.equipment_id

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al actualizar parte de equipo: {exc}")

    def delete_equipment_part(self, part_id: int) -> bool:
        try:
            model = self.db.query(EquipmentPartModel).filter_by(id=part_id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al eliminar parte de equipo: {exc}")

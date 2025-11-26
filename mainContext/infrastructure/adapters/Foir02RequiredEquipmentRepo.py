from mainContext.application.ports.Foir02RequiredEquipmentRepo import Foir02RequiredEquipmentRepo
from mainContext.application.dtos.foir02_required_equipment_dto import Foir02RequiredEquipmentDTO, Foir02RequiredEquipmentCreateDTO, Foir02RequiredEquipmentUpdateDTO
from mainContext.infrastructure.models import Foir02RequieredEquipment as Foir02RequiredEquipmentModel
from typing import List, Optional
from sqlalchemy.orm import Session

class Foir02RequiredEquipmentRepoImpl(Foir02RequiredEquipmentRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_foir02_required_equipment(self, dto: Foir02RequiredEquipmentCreateDTO) -> int:
        try:
            model = Foir02RequiredEquipmentModel(
                amount=dto.amount,
                unit=dto.unit,
                type=dto.type,
                name=dto.name
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar equipo requerido FOIR02 en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear equipo requerido FOIR02: {str(e)}")

    def get_foir02_required_equipment_by_id(self, id: int) -> Optional[Foir02RequiredEquipmentDTO]:
        try:
            model = self.db.query(Foir02RequiredEquipmentModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return Foir02RequiredEquipmentDTO(
                id=model.id,
                amount=model.amount,
                unit=model.unit,
                type=model.type,
                name=model.name
            )
        except Exception as e:
            raise Exception(f"Error al obtener equipo requerido FOIR02: {str(e)}")

    def get_all_foir02_required_equipment(self) -> List[Foir02RequiredEquipmentDTO]:
        try:
            models = self.db.query(Foir02RequiredEquipmentModel).all()
            
            return [
                Foir02RequiredEquipmentDTO(
                    id=model.id,
                    amount=model.amount,
                    unit=model.unit,
                    type=model.type,
                    name=model.name
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener equipos requeridos FOIR02: {str(e)}")

    def update_foir02_required_equipment(self, id: int, dto: Foir02RequiredEquipmentUpdateDTO) -> bool:
        try:
            model = self.db.query(Foir02RequiredEquipmentModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.amount is not None:
                model.amount = dto.amount
            if dto.unit is not None:
                model.unit = dto.unit
            if dto.type is not None:
                model.type = dto.type
            if dto.name is not None:
                model.name = dto.name

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar equipo requerido FOIR02: {str(e)}")

    def delete_foir02_required_equipment(self, id: int) -> bool:
        try:
            model = self.db.query(Foir02RequiredEquipmentModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar equipo requerido FOIR02: {str(e)}")

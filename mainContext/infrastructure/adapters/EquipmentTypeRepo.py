from mainContext.application.ports.EquipmentTypeRepo import EquipmentTypeRepo
from mainContext.application.dtos.equipment_type_dto import EquipmentTypeDTO, EquipmentTypeCreateDTO, EquipmentTypeUpdateDTO
from mainContext.infrastructure.models import EquipmentTypes as EquipmentTypeModel
from typing import List, Optional
from sqlalchemy.orm import Session

class EquipmentTypeRepoImpl(EquipmentTypeRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_equipment_type(self, dto: EquipmentTypeCreateDTO) -> int:
        try:
            model = EquipmentTypeModel(
                name=dto.name
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar tipo de equipo en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear tipo de equipo: {str(e)}")

    def get_equipment_type_by_id(self, id: int) -> Optional[EquipmentTypeDTO]:
        try:
            model = self.db.query(EquipmentTypeModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return EquipmentTypeDTO(
                id=model.id,
                name=model.name
            )
        except Exception as e:
            raise Exception(f"Error al obtener tipo de equipo: {str(e)}")

    def get_all_equipment_types(self) -> List[EquipmentTypeDTO]:
        try:
            models = self.db.query(EquipmentTypeModel).all()
            
            return [
                EquipmentTypeDTO(
                    id=model.id,
                    name=model.name
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener tipos de equipo: {str(e)}")

    def update_equipment_type(self, id: int, dto: EquipmentTypeUpdateDTO) -> bool:
        try:
            model = self.db.query(EquipmentTypeModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.name is not None:
                model.name = dto.name

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar tipo de equipo: {str(e)}")

    def delete_equipment_type(self, id: int) -> bool:
        try:
            model = self.db.query(EquipmentTypeModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar tipo de equipo: {str(e)}")

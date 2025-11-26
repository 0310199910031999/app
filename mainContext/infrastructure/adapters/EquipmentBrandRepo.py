from mainContext.application.ports.EquipmentBrandRepo import EquipmentBrandRepo
from mainContext.application.dtos.equipment_brand_dto import EquipmentBrandDTO, EquipmentBrandCreateDTO, EquipmentBrandUpdateDTO
from mainContext.infrastructure.models import EquipmentBrands as EquipmentBrandModel
from typing import List, Optional
from sqlalchemy.orm import Session

class EquipmentBrandRepoImpl(EquipmentBrandRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_equipment_brand(self, dto: EquipmentBrandCreateDTO) -> int:
        try:
            model = EquipmentBrandModel(
                name=dto.name,
                img_path=dto.img_path
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar marca de equipo en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear marca de equipo: {str(e)}")

    def get_equipment_brand_by_id(self, id: int) -> Optional[EquipmentBrandDTO]:
        try:
            model = self.db.query(EquipmentBrandModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return EquipmentBrandDTO(
                id=model.id,
                name=model.name,
                img_path=model.img_path
            )
        except Exception as e:
            raise Exception(f"Error al obtener marca de equipo: {str(e)}")

    def get_all_equipment_brands(self) -> List[EquipmentBrandDTO]:
        try:
            models = self.db.query(EquipmentBrandModel).all()
            
            return [
                EquipmentBrandDTO(
                    id=model.id,
                    name=model.name,
                    img_path=model.img_path
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener marcas de equipo: {str(e)}")

    def update_equipment_brand(self, id: int, dto: EquipmentBrandUpdateDTO) -> bool:
        try:
            model = self.db.query(EquipmentBrandModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.name is not None:
                model.name = dto.name
            if dto.img_path is not None:
                model.img_path = dto.img_path

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar marca de equipo: {str(e)}")

    def delete_equipment_brand(self, id: int) -> bool:
        try:
            model = self.db.query(EquipmentBrandModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar marca de equipo: {str(e)}")

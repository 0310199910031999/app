from typing import List, Optional

from sqlalchemy.orm import Session

from mainContext.application.ports.SparePartCategoryRepo import SparePartCategoryRepo
from mainContext.application.dtos.spare_part_category_dto import (
    SparePartCategoryDTO,
    SparePartCategoryCreateDTO,
    SparePartCategoryUpdateDTO,
)
from mainContext.infrastructure.models import SparePartCategories as SparePartCategoryModel


class SparePartCategoryRepoImpl(SparePartCategoryRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_spare_part_category(self, dto: SparePartCategoryCreateDTO) -> int:
        try:
            model = SparePartCategoryModel(description=dto.description)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al crear categoría de refacciones: {exc}")

    def get_spare_part_category_by_id(self, category_id: int) -> Optional[SparePartCategoryDTO]:
        try:
            model = self.db.query(SparePartCategoryModel).filter_by(id=category_id).first()
            if not model:
                return None
            return SparePartCategoryDTO(id=model.id, description=model.description)
        except Exception as exc:
            raise Exception(f"Error al obtener categoría de refacciones: {exc}")

    def get_all_spare_part_categories(self) -> List[SparePartCategoryDTO]:
        try:
            models = self.db.query(SparePartCategoryModel).all()
            return [
                SparePartCategoryDTO(id=model.id, description=model.description)
                for model in models
            ]
        except Exception as exc:
            raise Exception(f"Error al listar categorías de refacciones: {exc}")

    def update_spare_part_category(self, category_id: int, dto: SparePartCategoryUpdateDTO) -> bool:
        try:
            model = self.db.query(SparePartCategoryModel).filter_by(id=category_id).first()
            if not model:
                return False

            if dto.description is not None:
                model.description = dto.description

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al actualizar categoría de refacciones: {exc}")

    def delete_spare_part_category(self, category_id: int) -> bool:
        try:
            model = self.db.query(SparePartCategoryModel).filter_by(id=category_id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al eliminar categoría de refacciones: {exc}")

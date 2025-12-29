from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from mainContext.application.ports.SparePartRepo import SparePartRepo
from mainContext.application.dtos.spare_part_dto import SparePartDTO, SparePartCreateDTO, SparePartUpdateDTO
from mainContext.application.dtos.spare_part_category_dto import SparePartCategoryDTO
from mainContext.infrastructure.models import SpareParts as SparePartModel, SparePartCategories as SparePartCategoryModel


class SparePartRepoImpl(SparePartRepo):
    def __init__(self, db: Session):
        self.db = db

    def _get_category(self, category_id: int) -> SparePartCategoryModel:
        category = self.db.query(SparePartCategoryModel).filter_by(id=category_id).first()
        if not category:
            raise ValueError("La categoría especificada no existe")
        return category

    def _to_dto(self, model: SparePartModel) -> SparePartDTO:
        category_dto = None
        if model.category:
            category_dto = SparePartCategoryDTO(id=model.category.id, description=model.category.description)
        return SparePartDTO(
            id=model.id,
            description=model.description,
            category_id=model.category_id,
            category=category_dto,
        )

    def create_spare_part(self, dto: SparePartCreateDTO) -> int:
        try:
            self._get_category(dto.category_id)
            model = SparePartModel(description=dto.description, category_id=dto.category_id)
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            return model.id
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al crear refacción: {exc}")

    def get_spare_part_by_id(self, spare_part_id: int) -> Optional[SparePartDTO]:
        try:
            model = (
                self.db.query(SparePartModel)
                .options(joinedload(SparePartModel.category))
                .filter_by(id=spare_part_id)
                .first()
            )
            if not model:
                return None
            return self._to_dto(model)
        except Exception as exc:
            raise Exception(f"Error al obtener refacción: {exc}")

    def get_all_spare_parts(self) -> List[SparePartDTO]:
        try:
            models = self.db.query(SparePartModel).options(joinedload(SparePartModel.category)).all()
            return [self._to_dto(model) for model in models]
        except Exception as exc:
            raise Exception(f"Error al listar refacciones: {exc}")

    def update_spare_part(self, spare_part_id: int, dto: SparePartUpdateDTO) -> bool:
        try:
            model = self.db.query(SparePartModel).filter_by(id=spare_part_id).first()
            if not model:
                return False

            if dto.description is not None:
                model.description = dto.description

            if dto.category_id is not None:
                self._get_category(dto.category_id)
                model.category_id = dto.category_id

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al actualizar refacción: {exc}")

    def delete_spare_part(self, spare_part_id: int) -> bool:
        try:
            model = self.db.query(SparePartModel).filter_by(id=spare_part_id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as exc:
            self.db.rollback()
            raise Exception(f"Error al eliminar refacción: {exc}")

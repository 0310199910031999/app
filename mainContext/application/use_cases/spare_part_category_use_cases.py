from typing import List, Optional

from mainContext.application.ports.SparePartCategoryRepo import SparePartCategoryRepo
from mainContext.application.dtos.spare_part_category_dto import (
    SparePartCategoryDTO,
    SparePartCategoryCreateDTO,
    SparePartCategoryUpdateDTO,
)


class CreateSparePartCategory:
    def __init__(self, repo: SparePartCategoryRepo):
        self.repo = repo

    def execute(self, dto: SparePartCategoryCreateDTO) -> int:
        return self.repo.create_spare_part_category(dto)


class GetSparePartCategoryById:
    def __init__(self, repo: SparePartCategoryRepo):
        self.repo = repo

    def execute(self, category_id: int) -> Optional[SparePartCategoryDTO]:
        return self.repo.get_spare_part_category_by_id(category_id)


class GetAllSparePartCategories:
    def __init__(self, repo: SparePartCategoryRepo):
        self.repo = repo

    def execute(self) -> List[SparePartCategoryDTO]:
        return self.repo.get_all_spare_part_categories()


class UpdateSparePartCategory:
    def __init__(self, repo: SparePartCategoryRepo):
        self.repo = repo

    def execute(self, category_id: int, dto: SparePartCategoryUpdateDTO) -> bool:
        return self.repo.update_spare_part_category(category_id, dto)


class DeleteSparePartCategory:
    def __init__(self, repo: SparePartCategoryRepo):
        self.repo = repo

    def execute(self, category_id: int) -> bool:
        return self.repo.delete_spare_part_category(category_id)

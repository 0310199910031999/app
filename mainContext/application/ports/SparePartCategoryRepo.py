from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.spare_part_category_dto import (
    SparePartCategoryDTO,
    SparePartCategoryCreateDTO,
    SparePartCategoryUpdateDTO,
)


class SparePartCategoryRepo(ABC):
    @abstractmethod
    def create_spare_part_category(self, dto: SparePartCategoryCreateDTO) -> int:
        pass

    @abstractmethod
    def get_spare_part_category_by_id(self, category_id: int) -> Optional[SparePartCategoryDTO]:
        pass

    @abstractmethod
    def get_all_spare_part_categories(self) -> List[SparePartCategoryDTO]:
        pass

    @abstractmethod
    def update_spare_part_category(self, category_id: int, dto: SparePartCategoryUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_spare_part_category(self, category_id: int) -> bool:
        pass

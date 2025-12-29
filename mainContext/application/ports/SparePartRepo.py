from abc import ABC, abstractmethod
from typing import List, Optional

from mainContext.application.dtos.spare_part_dto import SparePartDTO, SparePartCreateDTO, SparePartUpdateDTO


class SparePartRepo(ABC):
    @abstractmethod
    def create_spare_part(self, dto: SparePartCreateDTO) -> int:
        pass

    @abstractmethod
    def get_spare_part_by_id(self, spare_part_id: int) -> Optional[SparePartDTO]:
        pass

    @abstractmethod
    def get_all_spare_parts(self) -> List[SparePartDTO]:
        pass

    @abstractmethod
    def update_spare_part(self, spare_part_id: int, dto: SparePartUpdateDTO) -> bool:
        pass

    @abstractmethod
    def delete_spare_part(self, spare_part_id: int) -> bool:
        pass

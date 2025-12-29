from typing import List, Optional

from mainContext.application.ports.SparePartRepo import SparePartRepo
from mainContext.application.dtos.spare_part_dto import SparePartDTO, SparePartCreateDTO, SparePartUpdateDTO


class CreateSparePart:
    def __init__(self, repo: SparePartRepo):
        self.repo = repo

    def execute(self, dto: SparePartCreateDTO) -> int:
        return self.repo.create_spare_part(dto)


class GetSparePartById:
    def __init__(self, repo: SparePartRepo):
        self.repo = repo

    def execute(self, spare_part_id: int) -> Optional[SparePartDTO]:
        return self.repo.get_spare_part_by_id(spare_part_id)


class GetAllSpareParts:
    def __init__(self, repo: SparePartRepo):
        self.repo = repo

    def execute(self) -> List[SparePartDTO]:
        return self.repo.get_all_spare_parts()


class UpdateSparePart:
    def __init__(self, repo: SparePartRepo):
        self.repo = repo

    def execute(self, spare_part_id: int, dto: SparePartUpdateDTO) -> bool:
        return self.repo.update_spare_part(spare_part_id, dto)


class DeleteSparePart:
    def __init__(self, repo: SparePartRepo):
        self.repo = repo

    def execute(self, spare_part_id: int) -> bool:
        return self.repo.delete_spare_part(spare_part_id)

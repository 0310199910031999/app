from mainContext.application.ports.Formats.fo_le_01_repo import FOLE01Repo
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01CreateDTO
from mainContext.domain.models.Formats.fo_le_01 import FOLE01
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01UpdateDTO, FOLE01TableRowDTO, FOLE01SignatureDTO
from typing import List

class CreateFOLE01:
    def __init__(self, repo : FOLE01Repo):
        self.repo = repo

    def execute(self, dto : FOLE01CreateDTO) -> int:
        return self.repo.create_fole01(dto)

class GetFOLE01ById:
    def __init__(self, repo : FOLE01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOLE01:
        return self.repo.get_fole01_by_id(id)

class DeleteFOLE01:
    def __init__(self, repo : FOLE01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_fole01(id)

class UpdateFOLE01:
    def __init__(self, repo : FOLE01Repo):
        self.repo = repo

    def execute(self, fole01_id: int, dto: FOLE01UpdateDTO) -> bool:
        return self.repo.update_fole01(fole01_id, dto)


class GetListFOLE01ByEquipmentId:
    def __init__(self, repo : FOLE01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOLE01]:
        return self.repo.get_list_fole01_by_equipment_id(equipment_id)

class GetListFOLE01Table:
    def __init__(self, repo : FOLE01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOLE01TableRowDTO]:
        return self.repo.get_list_fole01_table(equipment_id)


class SignFOLE01:
    def __init__(self, repo: FOLE01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOLE01SignatureDTO) -> bool:
        return self.repo.sign_fole01(id, dto)
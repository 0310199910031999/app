from mainContext.application.ports.Formats.fo_sp_01_repo import FOSP01Repo
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO
from mainContext.domain.models.Formats.fo_sp_01 import FOSP01
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01UpdateDTO, FOSP01TableRowDTO, FOSP01SignatureDTO
from typing import List

class CreateFOSP01:
    def __init__(self, repo : FOSP01Repo):
        self.repo = repo

    def execute(self, dto : FOSP01CreateDTO) -> FOSP01:
        return self.repo.create_fosp01(dto)

class GetFOSP01ById:
    def __init__(self, repo : FOSP01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOSP01:
        return self.repo.get_fosp01_by_id(id)

class DeleteFOSP01:
    def __init__(self, repo : FOSP01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_fosp01(id)

class UpdateFOSP01:
    def __init__(self, repo : FOSP01Repo):
        self.repo = repo

    def execute(self, fosp01_id: int, dto: FOSP01UpdateDTO) -> FOSP01:
        return self.repo.update_fosp01(fosp01_id, dto)


class GetListFOSP01ByEquipmentId:
    def __init__(self, repo : FOSP01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOSP01]:
        return self.repo.get_list_fosp01_by_equipment_id(equipment_id)

class GetListFOSP01Table:
    def __init__(self, repo : FOSP01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOSP01TableRowDTO]:
        return self.repo.get_list_fosp01_table(equipment_id)


class SignFOSP01:
    def __init__(self, repo: FOSP01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOSP01SignatureDTO):
        return self.repo.sign_fosp01(id, dto)
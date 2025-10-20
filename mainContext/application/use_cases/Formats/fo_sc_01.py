from mainContext.application.ports.Formats.fo_sc_01_repo import FOSC01Repo
from mainContext.application.dtos.Formats.fo_sc_01_dto import FOSC01CreateDTO
from mainContext.domain.models.Formats.fo_sc_01 import FOSC01
from mainContext.application.dtos.Formats.fo_sc_01_dto import FOSC01UpdateDTO, FOSC01TableRowDTO, FOSC01SignatureDTO
from typing import List

class CreateFOSC01:
    def __init__(self, repo : FOSC01Repo):
        self.repo = repo

    def execute(self, dto : FOSC01CreateDTO) -> int:
        return self.repo.create_fosc01(dto)

class GetFOSC01ById:
    def __init__(self, repo : FOSC01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOSC01:
        return self.repo.get_fosc01_by_id(id)

class DeleteFOSC01:
    def __init__(self, repo : FOSC01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_fosc01(id)

class UpdateFOSC01:
    def __init__(self, repo : FOSC01Repo):
        self.repo = repo

    def execute(self, fosc01_id: int, dto: FOSC01UpdateDTO) -> bool:
        return self.repo.update_fosc01(fosc01_id, dto)


class GetListFOSC01ByEquipmentId:
    def __init__(self, repo : FOSC01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOSC01]:
        return self.repo.get_list_fosc01_by_equipment_id(equipment_id)

class GetListFOSC01Table:
    def __init__(self, repo : FOSC01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOSC01TableRowDTO]:
        return self.repo.get_list_fosc01_table(equipment_id)


class SignFOSC01:
    def __init__(self, repo: FOSC01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOSC01SignatureDTO) -> bool:
        return self.repo.sign_fosc01(id, dto)
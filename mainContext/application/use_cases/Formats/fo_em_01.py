from mainContext.application.ports.Formats.fo_em_01_repo import FOEM01Repo
from mainContext.application.dtos.Formats.fo_em_01_dto import FOEM01CreatedDTO, FOEM01TableRowDTO, FOEM01SignatureDTO, FOEM01UpdateDTO

from mainContext.domain.models.Formats.fo_em_01 import FOEM01

from typing import List

class CreateFOEM01:
    def __init__(self, repo : FOEM01Repo):
        self.repo = repo

    def execute(self, dto : FOEM01CreatedDTO) -> int:
        return self.repo.create_foem01(dto)

class GetFOEM01ById:
    def __init__(self, repo : FOEM01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOEM01:
        return self.repo.get_foem01_by_id(id)

class DeleteFOEM01:
    def __init__(self, repo : FOEM01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_foem01(id)

class UpdateFOEM01:
    def __init__(self, repo : FOEM01Repo):
        self.repo = repo

    def execute(self, foem01_id: int, dto: FOEM01UpdateDTO) -> bool:
        return self.repo.update_foem01(foem01_id, dto)

class GetListFOEM01ByEquipmentId:
    def __init__(self, repo : FOEM01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOEM01]:
        return self.repo.get_list_foem01_by_equipment_id(equipment_id)

class GetListFOEM01Table:
    def __init__(self, repo : FOEM01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOEM01TableRowDTO]:
        return self.repo.get_list_foem01_table(equipment_id)

class SignFOEM01:
    def __init__(self, repo: FOEM01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOEM01SignatureDTO) -> bool:
        return self.repo.sign_foem01(id, dto)
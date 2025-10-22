from mainContext.application.ports.Formats.fo_bc_01_repo import FOBC01Repo
from mainContext.application.dtos.Formats.fo_bc_01_dto import FOBC01CreateDTO, FOBC01UpdateDTO, FOBC01SignatureDTO

from mainContext.domain.models.Formats.fo_bc_01 import FOBC01

from typing import List

class CreateFOBC01:
    def __init__(self, repo : FOBC01Repo):
        self.repo = repo

    def execute(self, dto : FOBC01CreateDTO) -> int:
        return self.repo.create_fobc01(dto)

class GetFOBC01ById:
    def __init__(self, repo : FOBC01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOBC01:
        return self.repo.get_fobc01_by_id(id)

class DeleteFOBC01:
    def __init__(self, repo : FOBC01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_fobc01(id)

class UpdateFOBC01:
    def __init__(self, repo : FOBC01Repo):
        self.repo = repo

    def execute(self, fobc01_id: int, dto: FOBC01UpdateDTO) -> bool:
        return self.repo.update_fobc01(fobc01_id, dto)

class GetListFOBC01ByEquipmentId:
    def __init__(self, repo : FOBC01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOBC01]:
        return self.repo.get_list_fobc01_by_equipment_id(equipment_id)

class GetListFOBC01Table:
    def __init__(self, repo : FOBC01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOBC01]:
        return self.repo.get_list_fobc01_table(equipment_id)

class SignFOBC01:
    def __init__(self, repo: FOBC01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOBC01SignatureDTO) -> bool:
        return self.repo.sign_fobc0
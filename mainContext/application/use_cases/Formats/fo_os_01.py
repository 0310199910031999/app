from mainContext.application.ports.Formats.fo_os_01_repo import FOOS01Repo
from mainContext.application.dtos.Formats.fo_os_01_dto import FOOS01CreateDTO
from mainContext.domain.models.Formats.fo_os_01 import FOOS01
from mainContext.application.dtos.Formats.fo_os_01_dto import FOOS01UpdateDTO, FOOS01TableRowDTO, FOOS01SignatureDTO
from typing import List

class CreateFOOS01:
    def __init__(self, repo : FOOS01Repo):
        self.repo = repo

    def execute(self, dto : FOOS01CreateDTO) -> int:
        return self.repo.create_foos01(dto)

class GetFOOS01ById:
    def __init__(self, repo : FOOS01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOOS01:
        return self.repo.get_foos01_by_id(id)

class DeleteFOOS01:
    def __init__(self, repo : FOOS01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_foos01(id)

class UpdateFOOS01:
    def __init__(self, repo : FOOS01Repo):
        self.repo = repo

    def execute(self, foos01_id: int, dto: FOOS01UpdateDTO) -> bool:
        return self.repo.update_foos01(foos01_id, dto)


class GetListFOOS01ByEquipmentId:
    def __init__(self, repo : FOOS01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOOS01]:
        return self.repo.get_list_foos01_by_equipment_id(equipment_id)

class GetListFOOS01Table:
    def __init__(self, repo : FOOS01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOOS01TableRowDTO]:
        return self.repo.get_list_foos01_table(equipment_id)


class SignFOOS01:
    def __init__(self, repo: FOOS01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOOS01SignatureDTO) -> bool:
        return self.repo.sign_foos01(id, dto)
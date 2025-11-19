from mainContext.application.ports.Formats.fo_pc_02_repo import FOPC02Repo
from mainContext.application.dtos.Formats.fo_pc_02_dto import CreateFOPC02DTO
from mainContext.domain.models.Formats.fo_pc_02 import FOPC02
from mainContext.application.dtos.Formats.fo_pc_02_dto import UpdateFOPc02DTO, FOPC02TableRowDTO, FOPC02SignatureDTO
from typing import List

class CreateFOPC02:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, dto: CreateFOPC02DTO) -> int:
        return self.repo.create_fopc02(dto)

class GetFOPC02ById:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, id: int) -> FOPC02:
        return self.repo.get_fopc02_by_id(id)

class DeleteFOPC02:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_fopc02(id)

class UpdateFOPC02:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, fopc02_id: int, dto: UpdateFOPc02DTO) -> bool:
        return self.repo.update_fopc02(fopc02_id, dto)

class GetListFOPC02ByEquipmentId:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, equipment_id: int) -> List[FOPC02]:
        return self.repo.get_list_fopc02_by_equipment_id(equipment_id)

class GetListFOPC02Table:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, equipment_id: int) -> List[FOPC02TableRowDTO]:
        return self.repo.get_list_fopc02_table(equipment_id)

class SignFOPC02Departure:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOPC02SignatureDTO) -> bool:
        return self.repo.sign_fopc02_departure(id, dto)

class SignFOPC02Return:
    def __init__(self, repo: FOPC02Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOPC02SignatureDTO) -> bool:
        return self.repo.sign_fopc02_return(id, dto)

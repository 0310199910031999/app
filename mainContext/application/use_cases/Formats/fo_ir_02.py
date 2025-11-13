from mainContext.domain.models.Formats.fo_ir_02 import FOIR02
from mainContext.application.dtos.Formats.fo_ir_02_dto import CreateFOIR02DTO, UpdateFOIR02DTO, FOIR02SignatureDTO, FOIR02TableRowDTO, FOIR02RequieredEquipment
from mainContext.application.ports.Formats.fo_ir_02_repo import FOIR02Repo
from typing import List

class CreateFOIR02:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self, dto: CreateFOIR02DTO) -> int:
        return self.repo.create_foir02(dto)

class GetFOIR02ById:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self, id: int) -> FOIR02:
        return self.repo.get_foir02_by_id(id)
    
class DeleteFOIR02:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_foir02(id)

class UpdateFOIR02:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self, foir02_id: int, dto: UpdateFOIR02DTO) -> bool:
        return self.repo.update_foir02(foir02_id, dto)

class GetListFOIR02Table:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self) -> List[FOIR02TableRowDTO]:
        return self.repo.get_list_foir02_table()

class SignFOIR02:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOIR02SignatureDTO) -> bool:
        return self.repo.sign_foir02(id, dto)

class GetFOIR02RequiredEquipment:
    def __init__(self, repo: FOIR02Repo):
        self.repo = repo

    def execute(self) -> List[FOIR02RequieredEquipment]:
        return self.repo.get_foir02_required_equipment()

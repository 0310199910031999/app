from typing import List
from mainContext.application.ports.Formats.fo_pp_02_repo import FOPP02Repo
from mainContext.application.dtos.Formats.fo_pp_02_dto import (
    FOPP02CreateDTO,
    FOPP02UpdateDTO,
    FOPP02SignatureDTO,
    FOPP02TableRowDTO,
    GetFOPP02ByFOPCDTO,
    FOPP02ByFOPCResponseDTO
)
from mainContext.domain.models.Formats.fo_pp_02 import FOPP02


class CreateFOPP02:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, dto: FOPP02CreateDTO) -> int:
        return self.repo.create_fopp02(dto)


class GetFOPP02ById:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, id: int) -> FOPP02:
        return self.repo.get_fopp02_by_id(id)


class DeleteFOPP02:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_fopp02(id)


class UpdateFOPP02:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, id: int, dto: FOPP02UpdateDTO) -> bool:
        return self.repo.update_fopp02(id, dto)


class GetListFOPP02ByFOPCId:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, fopc_id: int) -> List[FOPP02]:
        return self.repo.get_list_fopp02_by_fopc_id(fopc_id)


class GetListFOPP02Table:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, equipment_id: int) -> List[FOPP02TableRowDTO]:
        return self.repo.get_list_fopp02_table(equipment_id)


class SignFOPP02Departure:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, id: int, dto: FOPP02SignatureDTO) -> bool:
        return self.repo.sign_fopp02_departure(id, dto)


class SignFOPP02Delivery:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, id: int, dto: FOPP02SignatureDTO) -> bool:
        return self.repo.sign_fopp02_delivery(id, dto)


class GetFOPP02ByFOPC:
    def __init__(self, repo: FOPP02Repo):
        self.repo = repo
    
    def execute(self, dto: GetFOPP02ByFOPCDTO) -> List[FOPP02ByFOPCResponseDTO]:
        return self.repo.get_fopp02_by_fopc(dto)

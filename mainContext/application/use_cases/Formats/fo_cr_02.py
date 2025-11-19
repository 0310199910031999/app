from mainContext.application.ports.Formats.fo_cr_02_repo import FOCR02Repo
from mainContext.application.dtos.Formats.fo_cr_02_dto import (
    CreateFOCR02DTO, UpdateFOCR02DTO, FOCR02SignatureDTO, FOCR02TableRowDTO, FOCRAddEquipmentDTO
)


class CreateFOCR02:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self, dto: CreateFOCR02DTO) -> int:
        return self.repo.create_focr02(dto)


class GetFOCR02ById:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self, id: int):
        return self.repo.get_focr02_by_id(id)


class GetFOCR02Table:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self):
        return self.repo.get_focr02_table()


class UpdateFOCR02:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self, id: int, dto: UpdateFOCR02DTO) -> bool:
        return self.repo.update_focr02(id, dto)


class DeleteFOCR02:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_focr02(id)


class SignFOCR02:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self, id: int, dto: FOCR02SignatureDTO) -> bool:
        return self.repo.sign_focr02(id, dto)


class GetFOCRAdditionalEquipment:
    def __init__(self, repo: FOCR02Repo):
        self.repo = repo
    
    def execute(self):
        return self.repo.get_focr_additional_equipment()

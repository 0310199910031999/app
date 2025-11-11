from mainContext.domain.models.Formats.fo_ro_05 import FORO05
from mainContext.application.dtos.Formats.fo_ro_05_dto import FORO05CreateDTO, FORO05UpdateDTO, FORO05SignatureDTO, FORO05TableRowDTO
from mainContext.application.ports.Formats.fo_ro_05_repo import FORO05Repo
from typing import List

class CreateFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, dto: FORO05CreateDTO) -> int:
        return self.repo.create_foro05(dto)

class GetFORO05ById:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, id: int) -> FORO05:
        return self.repo.get_foro05_by_id(id)

class DeleteFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_foro05(id)

class UpdateFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, foro05_id: int, dto: FORO05UpdateDTO) -> bool:
        return self.repo.update_foro05(foro05_id, dto)

class GetListFORO05Table:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self) -> List[FORO05TableRowDTO]:
        return self.repo.get_list_foro05_table()

class SignFORO05:
    def __init__(self, repo: FORO05Repo):
        self.repo = repo

    def execute(self, id: int, dto: FORO05SignatureDTO) -> bool:
        return self.repo.sign_foro05(id, dto)



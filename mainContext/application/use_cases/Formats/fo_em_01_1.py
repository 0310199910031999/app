from typing import List

from mainContext.application.ports.Formats.fo_em_01_1_repo import FOEM011Repo
from mainContext.application.dtos.Formats.fo_em_01_1_dto import FOEM011CreateDTO, FOEM011TableRowDTO, FOEM011SignatureDTO, FOEM011UpdateDTO
from mainContext.domain.models.Formats.fo_em_01_1 import FOEM011


class CreateFOEM011:
    def __init__(self, repo : FOEM011Repo):
        self.repo = repo

    def execute(self, dto : FOEM011CreateDTO) -> int:
        return self.repo.create_foem01_1(dto)


class GetFOEM011ById:
    def __init__(self, repo : FOEM011Repo):
        self.repo = repo

    def execute(self, id : int) -> FOEM011:
        return self.repo.get_foem01_1_by_id(id)


class DeleteFOEM011:
    def __init__(self, repo : FOEM011Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_foem01_1(id)


class UpdateFOEM011:
    def __init__(self, repo : FOEM011Repo):
        self.repo = repo

    def execute(self, foem01_1_id: int, dto: FOEM011UpdateDTO) -> bool:
        return self.repo.update_foem01_1(foem01_1_id, dto)


class GetListFOEM011ByClientId:
    def __init__(self, repo : FOEM011Repo):
        self.repo = repo

    def execute(self, client_id : int) -> List[FOEM011]:
        return self.repo.get_list_foem01_1_by_client_id(client_id)


class GetListFOEM011Table:
    def __init__(self, repo : FOEM011Repo):
        self.repo = repo

    def execute(self, client_id : int) -> List[FOEM011TableRowDTO]:
        return self.repo.get_list_foem01_1_table(client_id)


class SignFOEM011:
    def __init__(self, repo: FOEM011Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOEM011SignatureDTO) -> bool:
        return self.repo.sign_foem01_1(id, dto)
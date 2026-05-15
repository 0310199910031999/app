from typing import List, Optional

from mainContext.application.dtos.Formats.fo_bc_01_dto import (
    FOBC01CreateDTO,
    FOBC01QuestionCreateDTO,
    FOBC01QuestionDTO,
    FOBC01QuestionUpdateDTO,
    FOBC01SignatureDTO,
    FOBC01UpdateDTO,
)
from mainContext.application.ports.Formats.fo_bc_01_repo import FOBC01Repo
from mainContext.domain.models.Formats.fo_bc_01 import FOBC01


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
        return self.repo.sign_fobc01(id, dto)


class CreateFOBC01Question:
    def __init__(self, repo: FOBC01Repo):
        self.repo = repo

    def execute(self, dto: FOBC01QuestionCreateDTO) -> int:
        return self.repo.create_fobc01_question(dto)


class GetFOBC01QuestionById:
    def __init__(self, repo: FOBC01Repo):
        self.repo = repo

    def execute(self, id: int) -> Optional[FOBC01QuestionDTO]:
        return self.repo.get_fobc01_question_by_id(id)


class GetAllFOBC01Questions:
    def __init__(self, repo: FOBC01Repo):
        self.repo = repo

    def execute(self) -> List[FOBC01QuestionDTO]:
        return self.repo.get_all_fobc01_questions()


class UpdateFOBC01Question:
    def __init__(self, repo: FOBC01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOBC01QuestionUpdateDTO) -> bool:
        return self.repo.update_fobc01_question(id, dto)


class DeleteFOBC01Question:
    def __init__(self, repo: FOBC01Repo):
        self.repo = repo

    def execute(self, id: int) -> bool:
        return self.repo.delete_fobc01_question(id)
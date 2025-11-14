from mainContext.application.ports.Formats.fo_im_01_repo import FOIM01Repo
from mainContext.application.dtos.Formats.fo_im_01_dto import FOIM01CreateDTO
from mainContext.domain.models.Formats.fo_im_01 import FOIM01
from mainContext.application.dtos.Formats.fo_im_01_dto import FOIM01UpdateDTO, FOIM01TableRowDTO, FOIM01SignatureDTO
from mainContext.application.dtos.Formats.fo_im_question_dto import FOIMQuestionDTO
from typing import List

class CreateFOIM01:
    def __init__(self, repo : FOIM01Repo):
        self.repo = repo

    def execute(self, dto : FOIM01CreateDTO) -> int:
        return self.repo.create_foim01(dto)

class GetFOIM01ById:
    def __init__(self, repo : FOIM01Repo):
        self.repo = repo

    def execute(self, id : int) -> FOIM01:
        return self.repo.get_foim01_by_id(id)

class DeleteFOIM01:
    def __init__(self, repo : FOIM01Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_foim01(id)

class UpdateFOIM01:
    def __init__(self, repo : FOIM01Repo):
        self.repo = repo

    def execute(self, foim01_id: int, dto: FOIM01UpdateDTO) -> bool:
        return self.repo.update_foim01(foim01_id, dto)


class GetListFOIM01ByEquipmentId:
    def __init__(self, repo : FOIM01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOIM01]:
        return self.repo.get_list_foim01_by_equipment_id(equipment_id)

class GetListFOIM01Table:
    def __init__(self, repo : FOIM01Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOIM01TableRowDTO]:
        return self.repo.get_list_foim01_table(equipment_id)


class SignFOIM01:
    def __init__(self, repo: FOIM01Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOIM01SignatureDTO) -> bool:
        return self.repo.sign_foim01(id, dto)

class GetFOIMQuestions:
    def __init__(self, repo: FOIM01Repo):
        self.repo = repo

    def execute(self) -> List[FOIMQuestionDTO]:
        return self.repo.get_foim_questions()
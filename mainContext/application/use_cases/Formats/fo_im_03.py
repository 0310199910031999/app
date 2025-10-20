from mainContext.application.ports.Formats.fo_im_03_repo import FOIM03Repo
from mainContext.domain.models.Formats.fo_im_03 import FOIM03
from mainContext.application.dtos.Formats.fo_im_03_dto import FOIM03CreateDTO, FOIM03TableRowDTO, FOIM03ChangeStatusDTO
from typing import List

class CreateFOIM03:
    def __init__(self, repo : FOIM03Repo):
        self.repo = repo

    def execute(self, dto : FOIM03CreateDTO) -> int:
        return self.repo.create_foim03(dto)

class GetFOIM03ById:
    def __init__(self, repo : FOIM03Repo):
        self.repo = repo

    def execute(self, id : int) -> FOIM03:
        return self.repo.get_foim03_by_id(id)

class DeleteFOIM03:
    def __init__(self, repo : FOIM03Repo):
        self.repo = repo

    def execute(self, id : int) -> bool:
        return self.repo.delete_foim03(id)

class GetListFOIM03ByEquipmentId:
    def __init__(self, repo : FOIM03Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOIM03]:
        return self.repo.get_list_foim03_by_equipment_id(equipment_id)

class GetListFOIM03Table:
    def __init__(self, repo : FOIM03Repo):
        self.repo = repo

    def execute(self, equipment_id : int) -> List[FOIM03TableRowDTO]:
        return self.repo.get_list_foim03_table(equipment_id)


class ChangeStatusFOIM03:
    def __init__(self, repo: FOIM03Repo):
        self.repo = repo

    def execute(self, id: int, dto: FOIM03ChangeStatusDTO) -> bool:
        return self.repo.change_status_foim03(id, dto)
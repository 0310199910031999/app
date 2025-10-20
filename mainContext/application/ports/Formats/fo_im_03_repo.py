from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_im_03 import FOIM03
from mainContext.application.dtos.Formats.fo_im_03_dto import FOIM03CreateDTO, FOIM03TableRowDTO, FOIM03ChangeStatusDTO
from typing import List

class FOIM03Repo(ABC):
    @abstractmethod
    def create_foim03(self, foim03: FOIM03CreateDTO) -> int:
        pass
    @abstractmethod
    def get_foim03_by_id(self, id: int) -> FOIM03:
        pass
    @abstractmethod
    def delete_foim03(self, id: int) -> bool:
        pass
    @abstractmethod
    def get_list_foim03_by_equipment_id(self, equipment_id: int) -> List[FOIM03]:
        pass
    @abstractmethod
    def get_list_foim03_table(self, equipment_id: int) -> List[FOIM03TableRowDTO]:
        pass
    @abstractmethod
    def change_status_foim03(self, id: int, foim03: FOIM03ChangeStatusDTO) -> bool:
        pass




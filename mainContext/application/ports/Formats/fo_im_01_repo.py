from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_im_01 import FOIM01
from mainContext.application.dtos.Formats.fo_im_01_dto import FOIM01CreateDTO, FOIM01UpdateDTO, FOIM01SignatureDTO, FOIM01TableRowDTO
from mainContext.application.dtos.Formats.fo_im_question_dto import FOIMQuestionDTO
from typing import List

class FOIM01Repo(ABC):
    @abstractmethod
    def create_foim01(self, foim01: FOIM01CreateDTO) -> int:
        pass
    @abstractmethod
    def get_foim01_by_id(self, id: int) -> FOIM01:
        pass
    @abstractmethod
    def delete_foim01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_foim01(self, id: int, foim01: FOIM01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_foim01_by_equipment_id(self, equipment_id: int) -> List[FOIM01]:
        pass
    @abstractmethod
    def get_list_foim01_table(self, equipment_id: int) -> List[FOIM01TableRowDTO]:
        pass
    @abstractmethod
    def sign_foim01(self, id: int, foim01: FOIM01SignatureDTO) -> bool:
        pass
    @abstractmethod
    def get_foim_questions(self) -> List[FOIMQuestionDTO]:
        pass



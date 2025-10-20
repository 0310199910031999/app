from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_em_01 import FOEM01
from mainContext.application.dtos.Formats.fo_em_01_dto import FOEM01CreatedDTO, FOEM01UpdateDTO, FOEM01SignatureDTO, FOEM01TableRowDTO
from typing import List

class FOEM01Repo(ABC):
    @abstractmethod
    def create_foem01(self, foem01: FOEM01CreatedDTO) -> int:
        pass
    @abstractmethod
    def get_foem01_by_id(self, id: int) -> FOEM01:
        pass
    @abstractmethod
    def delete_foem01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_foem01(self, id: int, foem01: FOEM01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_foem01_by_equipment_id(self, equipment_id: int) -> List[FOEM01]:
        pass
    @abstractmethod
    def get_list_foem01_table(self, equipment_id: int) -> List[FOEM01TableRowDTO]:
        pass
    @abstractmethod
    def sign_foem01(self, id: int, foem01: FOEM01SignatureDTO) -> bool:
        pass
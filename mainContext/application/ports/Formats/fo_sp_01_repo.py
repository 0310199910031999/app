from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_sp_01 import FOSP01
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO, FOSP01UpdateDTO, FOSP01SignatureDTO, FOSP01TableRowDTO
from typing import List

class FOSP01Repo(ABC):
    @abstractmethod
    def create_fosp01(self, fosp01: FOSP01CreateDTO) -> int:
        pass
    @abstractmethod
    def get_fosp01_by_id(self, id: int) -> FOSP01:
        pass
    @abstractmethod
    def delete_fosp01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_fosp01(self, id: int, fosp01: FOSP01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_fosp01_by_equipment_id(self, equipment_id: int) -> List[FOSP01]:
        pass
    @abstractmethod
    def get_list_fosp01_table(self, equipment_id: int) -> List[FOSP01TableRowDTO]:
        pass
    @abstractmethod
    def sign_fosp01(self, id: int, fosp01: FOSP01SignatureDTO) -> bool:
        pass



from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_sc_01 import FOSC01
from mainContext.application.dtos.Formats.fo_sc_01_dto import FOSC01CreateDTO, FOSC01UpdateDTO, FOSC01SignatureDTO, FOSC01TableRowDTO
from typing import List

class FOSC01Repo(ABC):
    @abstractmethod
    def create_fosc01(self, fosc01: FOSC01CreateDTO) -> int:
        pass
    @abstractmethod
    def get_fosc01_by_id(self, id: int) -> FOSC01:
        pass
    @abstractmethod
    def delete_fosc01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_fosc01(self, id: int, fosc01: FOSC01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_fosc01_by_equipment_id(self, equipment_id: int) -> List[FOSC01]:
        pass
    @abstractmethod
    def get_list_fosc01_table(self, equipment_id: int) -> List[FOSC01TableRowDTO]:
        pass
    @abstractmethod
    def sign_fosc01(self, id: int, fosc01: FOSC01SignatureDTO) -> bool:
        pass



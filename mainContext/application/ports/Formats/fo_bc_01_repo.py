from abc import ABC, abstractmethod
from typing import List
from mainContext.domain.models.Formats.fo_bc_01 import FOBC01
from mainContext.application.dtos.Formats.fo_bc_01_dto import FOBC01CreateDTO, FOBC01UpdateDTO, FOBC01SignatureDTO, FOBC01TableRowDTO


class FOBC01Repo(ABC):
    @abstractmethod
    def create_fobc01(self, fobc01: FOBC01CreateDTO) -> int:
        pass
    @abstractmethod
    def get_fobc01_by_id(self, id: int) -> FOBC01:
        pass
    @abstractmethod
    def delete_fobc01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_fobc01(self, id: int, fobc01: FOBC01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_fobc01_by_equipment_id(self, equipment_id: int) -> List[FOBC01]:
        pass
    @abstractmethod
    def get_list_fobc01_table(self, equipment_id: int) -> List[FOBC01TableRowDTO]:
        pass
    @abstractmethod
    def sign_fobc01(self, id: int, fobc01: FOBC01SignatureDTO) -> bool:
        pass
        
    

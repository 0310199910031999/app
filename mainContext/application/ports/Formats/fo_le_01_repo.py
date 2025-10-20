from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_le_01 import FOLE01
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01CreateDTO, FOLE01UpdateDTO, FOLE01TableRowDTO, FOLE01SignatureDTO
from typing import List


class FOLE01Repo(ABC):
    @abstractmethod
    def create_fole01(self, fole01: FOLE01CreateDTO) -> int:
        pass
    @abstractmethod
    def get_fole01_by_id(self, id: int) -> FOLE01:
        pass
    @abstractmethod
    def delete_fole01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_fole01(self, id: int, fole01: FOLE01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_fole01_by_equipment_id(self, equipment_id: int) -> List[FOLE01]:
        pass
    @abstractmethod
    def get_list_fole01_table(self, equipment_id: int) -> List[FOLE01TableRowDTO]:
        pass
    @abstractmethod
    def sign_fole01(self, id: int, fole01: FOLE01SignatureDTO) -> bool:
        pass

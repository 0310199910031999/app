from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_os_01 import FOOS01
from mainContext.application.dtos.Formats.fo_os_01_dto import FOOS01CreateDTO, FOOS01UpdateDTO, FOOS01SignatureDTO, FOOS01TableRowDTO
from typing import List

class FOOS01Repo(ABC):
    @abstractmethod
    def create_foos01(self, foos01: FOOS01CreateDTO) -> int:
        pass
    @abstractmethod
    def get_foos01_by_id(self, id: int) -> FOOS01:
        pass
    @abstractmethod
    def delete_foos01(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_foos01(self, id: int, foos01: FOOS01UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_foos01_by_equipment_id(self, equipment_id: int) -> List[FOOS01]:
        pass
    @abstractmethod
    def get_list_foos01_table(self, equipment_id: int) -> List[FOOS01TableRowDTO]:
        pass
    @abstractmethod
    def sign_foos01(self, id: int, foos01: FOOS01SignatureDTO) -> bool:
        pass



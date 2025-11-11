from abc import ABC, abstractmethod
from typing import List 
from mainContext.application.dtos.Formats.fo_ro_05_dto import FORO05CreateDTO, FORO05UpdateDTO, FORO05SignatureDTO, FORO05TableRowDTO
from mainContext.domain.models.Formats.fo_ro_05 import FORO05


class FORO05Repo(ABC): 
    @abstractmethod
    def create_foro05(self, foro05: FORO05CreateDTO) -> int:
        pass
    @abstractmethod
    def get_foro05_by_id(self, id: int) -> FORO05:
        pass
    @abstractmethod
    def delete_foro05(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_foro05(self, id: int, foro05: FORO05UpdateDTO) -> bool:
        pass
    @abstractmethod
    def get_list_foro05_table(self) -> List[FORO05TableRowDTO]:
        pass
    @abstractmethod
    def sign_foro05(self, id: int, foro05: FORO05SignatureDTO) -> bool:
        pass

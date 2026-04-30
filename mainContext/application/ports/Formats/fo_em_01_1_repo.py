from abc import ABC, abstractmethod
from typing import List

from mainContext.domain.models.Formats.fo_em_01_1 import FOEM011
from mainContext.application.dtos.Formats.fo_em_01_1_dto import FOEM011CreateDTO, FOEM011UpdateDTO, FOEM011SignatureDTO, FOEM011TableRowDTO


class FOEM011Repo(ABC):
    @abstractmethod
    def create_foem01_1(self, foem01_1: FOEM011CreateDTO) -> int:
        pass

    @abstractmethod
    def get_foem01_1_by_id(self, id: int) -> FOEM011:
        pass

    @abstractmethod
    def delete_foem01_1(self, id: int) -> bool:
        pass

    @abstractmethod
    def update_foem01_1(self, id: int, foem01_1: FOEM011UpdateDTO) -> bool:
        pass

    @abstractmethod
    def get_list_foem01_1_by_client_id(self, client_id: int) -> List[FOEM011]:
        pass

    @abstractmethod
    def get_list_foem01_1_table(self, client_id: int) -> List[FOEM011TableRowDTO]:
        pass

    @abstractmethod
    def sign_foem01_1(self, id: int, foem01_1: FOEM011SignatureDTO) -> bool:
        pass
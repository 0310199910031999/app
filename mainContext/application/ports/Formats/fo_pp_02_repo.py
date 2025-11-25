from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_pp_02 import FOPP02
from mainContext.application.dtos.Formats.fo_pp_02_dto import (
    FOPP02CreateDTO,
    FOPP02UpdateDTO,
    FOPP02SignatureDTO,
    FOPP02TableRowDTO,
    GetFOPP02ByFOPCDTO,
    FOPP02ByFOPCResponseDTO
)
from typing import List


class FOPP02Repo(ABC):
    
    @abstractmethod
    def create_fopp02(self, dto: FOPP02CreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_fopp02_by_id(self, id: int) -> FOPP02:
        pass
    
    @abstractmethod
    def delete_fopp02(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def update_fopp02(self, id: int, dto: FOPP02UpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def get_list_fopp02_by_fopc_id(self, fopc_id: int) -> List[FOPP02]:
        pass
    
    @abstractmethod
    def get_list_fopp02_table(self, equipment_id: int) -> List[FOPP02TableRowDTO]:
        pass
    
    @abstractmethod
    def sign_fopp02_departure(self, id: int, dto: FOPP02SignatureDTO) -> bool:
        pass
    
    @abstractmethod
    def sign_fopp02_delivery(self, id: int, dto: FOPP02SignatureDTO) -> bool:
        pass
    
    @abstractmethod
    def get_fopp02_by_fopc(self, dto: GetFOPP02ByFOPCDTO) -> List[FOPP02ByFOPCResponseDTO]:
        pass

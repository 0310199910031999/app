from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_pc_02 import FOPC02
from mainContext.application.dtos.Formats.fo_pc_02_dto import (
    CreateFOPC02DTO,
    UpdateFOPc02DTO,
    FOPC02SignatureDTO,
    FOPC02TableRowDTO,
    GetFOPC02ByDocumentDTO,
    FOPC02ByDocumentResponseDTO
)
from typing import List

class FOPC02Repo(ABC):
    @abstractmethod
    def create_fopc02(self, fopc02: CreateFOPC02DTO) -> int:
        pass
    
    @abstractmethod
    def get_fopc02_by_id(self, id: int) -> FOPC02:
        pass
    
    @abstractmethod
    def delete_fopc02(self, id: int) -> bool:
        pass
    
    @abstractmethod
    def update_fopc02(self, id: int, fopc02: UpdateFOPc02DTO) -> bool:
        pass
    
    @abstractmethod
    def get_list_fopc02_by_equipment_id(self, equipment_id: int) -> List[FOPC02]:
        pass
    
    @abstractmethod
    def get_list_fopc02_table(self, equipment_id: int) -> List[FOPC02TableRowDTO]:
        pass
    
    @abstractmethod
    def sign_fopc02_departure(self, id: int, fopc02: FOPC02SignatureDTO) -> bool:
        pass
    
    @abstractmethod
    def sign_fopc02_return(self, id: int, fopc02: FOPC02SignatureDTO) -> bool:
        pass
    
    @abstractmethod
    def get_fopc02_by_document(self, dto: GetFOPC02ByDocumentDTO) -> List[FOPC02ByDocumentResponseDTO]:
        pass

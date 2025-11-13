from abc import ABC, abstractmethod
from mainContext.domain.models.Formats.fo_ir_02 import FOIR02
from mainContext.application.dtos.Formats.fo_ir_02_dto import CreateFOIR02DTO, UpdateFOIR02DTO, FOIR02SignatureDTO, FOIR02TableRowDTO, FOIR02RequieredEquipment
from typing import List

class FOIR02Repo(ABC):
    @abstractmethod
    def create_foir02(self, foir02: CreateFOIR02DTO) -> int:
        pass
    @abstractmethod
    def get_foir02_by_id(self, id: int) -> FOIR02:
        pass
    @abstractmethod
    def delete_foir02(self, id: int) -> bool:
        pass
    @abstractmethod
    def update_foir02(self, id: int, foir02: UpdateFOIR02DTO) -> bool:
        pass
    @abstractmethod
    def get_list_foir02_table(self) -> List[FOIR02TableRowDTO]:
        pass
    @abstractmethod
    def sign_foir02(self, id: int, foir02: FOIR02SignatureDTO) -> bool:
        pass
    @abstractmethod
    def get_foir02_required_equipment(self) -> List[FOIR02RequieredEquipment]:
        pass
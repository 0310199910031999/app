from abc import ABC, abstractmethod
from typing import List, Optional
from mainContext.application.dtos.vendor_dto import VendorDTO, VendorCreateDTO, VendorUpdateDTO

class VendorRepo(ABC):
    @abstractmethod
    def create_vendor(self, dto: VendorCreateDTO) -> int:
        pass
    
    @abstractmethod
    def get_vendor_by_id(self, id: int) -> Optional[VendorDTO]:
        pass
    
    @abstractmethod
    def get_all_vendors(self) -> List[VendorDTO]:
        pass
    
    @abstractmethod
    def update_vendor(self, id: int, dto: VendorUpdateDTO) -> bool:
        pass
    
    @abstractmethod
    def delete_vendor(self, id: int) -> bool:
        pass

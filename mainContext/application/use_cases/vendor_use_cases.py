from mainContext.application.ports.VendorRepo import VendorRepo
from mainContext.application.dtos.vendor_dto import VendorDTO, VendorCreateDTO, VendorUpdateDTO
from typing import List, Optional

class CreateVendor:
    def __init__(self, repo: VendorRepo):
        self.repo = repo
    
    def execute(self, dto: VendorCreateDTO) -> int:
        return self.repo.create_vendor(dto)

class GetVendorById:
    def __init__(self, repo: VendorRepo):
        self.repo = repo
    
    def execute(self, id: int) -> Optional[VendorDTO]:
        return self.repo.get_vendor_by_id(id)

class GetAllVendors:
    def __init__(self, repo: VendorRepo):
        self.repo = repo
    
    def execute(self) -> List[VendorDTO]:
        return self.repo.get_all_vendors()

class UpdateVendor:
    def __init__(self, repo: VendorRepo):
        self.repo = repo
    
    def execute(self, id: int, dto: VendorUpdateDTO) -> bool:
        return self.repo.update_vendor(id, dto)

class DeleteVendor:
    def __init__(self, repo: VendorRepo):
        self.repo = repo
    
    def execute(self, id: int) -> bool:
        return self.repo.delete_vendor(id)

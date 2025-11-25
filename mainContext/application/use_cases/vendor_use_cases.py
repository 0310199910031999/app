from mainContext.application.ports.VendorRepo import VendorRepo
from mainContext.application.dtos.vendor_dto import VendorDTO
from typing import List

class GetAllVendors:
    def __init__(self, repo: VendorRepo):
        self.repo = repo

    def execute(self) -> List[VendorDTO]:
        vendors = self.repo.get_all_vendors()
        return [
            VendorDTO(
                id=vendor.id,
                name=vendor.name,
                rfc=vendor.rfc,
                contact_person=vendor.contact_person,
                phone_number=vendor.phone_number,
                email=vendor.email
            )
            for vendor in vendors
        ]

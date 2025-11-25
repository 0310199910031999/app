from abc import ABC, abstractmethod
from typing import List
from mainContext.domain.models.Vendor import Vendor

class VendorRepo(ABC):
    @abstractmethod
    def get_all_vendors(self) -> List[Vendor]:
        pass

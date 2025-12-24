from abc import ABC, abstractmethod
from typing import List
from mainContext.application.dtos.service_record_dto import ServiceRecordDTO


class ServiceRecordRepo(ABC):
    @abstractmethod
    def list_service_records(self, equipment_id: int) -> List[ServiceRecordDTO]:
        pass

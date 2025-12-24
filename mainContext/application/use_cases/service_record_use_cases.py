from typing import List
from mainContext.application.dtos.service_record_dto import ServiceRecordDTO
from mainContext.application.ports.ServiceRecordRepo import ServiceRecordRepo


class ListServiceRecords:
    def __init__(self, repo: ServiceRecordRepo):
        self.repo = repo

    def execute(self, equipment_id: int) -> List[ServiceRecordDTO]:
        return self.repo.list_service_records(equipment_id)

from typing import List
from fastapi import APIRouter, Depends
from api.v1.schemas.service_record import ServiceRecordSchema
from mainContext.application.use_cases.service_record_use_cases import ListServiceRecords
from mainContext.infrastructure.dependencies import get_service_record_repo
from mainContext.infrastructure.adapters.ServiceRecordRepo import ServiceRecordRepoImpl


serviceRecordRouter = APIRouter(prefix="/service-records", tags=["Service Records"])


@serviceRecordRouter.get("/{equipment_id}", response_model=List[ServiceRecordSchema])
def list_service_records(equipment_id: int, repo: ServiceRecordRepoImpl = Depends(get_service_record_repo)):
    use_case = ListServiceRecords(repo)
    return use_case.execute(equipment_id)

from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from shared.db import get_db
from api.v1.schemas.service_record import ServiceRecordSchema
from mainContext.application.use_cases.service_record_use_cases import ListServiceRecords
from mainContext.infrastructure.adapters.ServiceRecordRepo import ServiceRecordRepoImpl


serviceRecordRouter = APIRouter(prefix="/service-records", tags=["Service Records"])


@serviceRecordRouter.get("/{equipment_id}", response_model=List[ServiceRecordSchema])
def list_service_records(equipment_id: int, db: Session = Depends(get_db)):
    repo = ServiceRecordRepoImpl(db)
    use_case = ListServiceRecords(repo)
    return use_case.execute(equipment_id)

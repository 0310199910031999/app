from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shared.db import get_db
from mainContext.application.dtos.app_request_dto import (
    AppRequestCreateDTO,
    AppRequestUpdateDTO,
    AppRequestCloseDTO,
    AppRequestStatusDTO,
)
from mainContext.application.use_cases.app_request_use_cases import (
    CreateAppRequest,
    GetAppRequestById,
    GetAllAppRequests,
    GetAppRequestsByEquipment,
    GetAppRequestsWithService,
    GetAppRequestsWithSparePart,
    GetAppRequestsByEquipmentWithService,
    GetAppRequestsByEquipmentWithSparePart,
    UpdateAppRequest,
    DeleteAppRequest,
    CloseAppRequest,
    UpdateAppRequestStatus,
)
from mainContext.infrastructure.adapters.AppRequestRepo import AppRequestRepoImpl
from api.v1.schemas.app_request import (
    AppRequestSchema,
    AppRequestCreateSchema,
    AppRequestUpdateSchema,
    AppRequestCloseSchema,
    AppRequestStatusSchema,
    AppRequestWithServiceSchema,
    AppRequestWithSparePartSchema,
)
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

AppRequestsRouter = APIRouter(prefix="/app-requests", tags=["App Requests"])


@AppRequestsRouter.post("/create", response_model=ResponseIntModel)
def create_app_request(dto: AppRequestCreateSchema, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = CreateAppRequest(repo)
    app_request_id = use_case.execute(AppRequestCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=app_request_id)


@AppRequestsRouter.get("/get/{id}", response_model=AppRequestSchema)
def get_app_request_by_id(id: int, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAppRequestById(repo)
    app_request = use_case.execute(id)
    if not app_request:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return app_request


@AppRequestsRouter.get("/get_all", response_model=List[AppRequestSchema])
def get_all_app_requests(db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAllAppRequests(repo)
    return use_case.execute()


@AppRequestsRouter.get("/equipment/{equipment_id}", response_model=List[AppRequestSchema])
def get_app_requests_by_equipment(equipment_id: int, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAppRequestsByEquipment(repo)
    return use_case.execute(equipment_id)


@AppRequestsRouter.get("/equipment/{equipment_id}/with-service", response_model=List[AppRequestWithServiceSchema])
def get_app_requests_by_equipment_with_service(equipment_id: int, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAppRequestsByEquipmentWithService(repo)
    return use_case.execute(equipment_id)


@AppRequestsRouter.get("/equipment/{equipment_id}/with-spare-part", response_model=List[AppRequestWithSparePartSchema])
def get_app_requests_by_equipment_with_spare_part(equipment_id: int, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAppRequestsByEquipmentWithSparePart(repo)
    return use_case.execute(equipment_id)


@AppRequestsRouter.get("/with-service", response_model=List[AppRequestWithServiceSchema])
def get_app_requests_with_service(db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAppRequestsWithService(repo)
    return use_case.execute()


@AppRequestsRouter.get("/with-spare-part", response_model=List[AppRequestWithSparePartSchema])
def get_app_requests_with_spare_part(db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = GetAppRequestsWithSparePart(repo)
    return use_case.execute()


@AppRequestsRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_app_request(id: int, dto: AppRequestUpdateSchema, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = UpdateAppRequest(repo)
    updated = use_case.execute(id, AppRequestUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return ResponseBoolModel(result=updated)


@AppRequestsRouter.put("/close/{id}", response_model=ResponseBoolModel)
def close_app_request(id: int, dto: AppRequestCloseSchema, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = CloseAppRequest(repo)
    closed = use_case.execute(id, AppRequestCloseDTO(**dto.model_dump(exclude_none=True)))
    if not closed:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return ResponseBoolModel(result=closed)


@AppRequestsRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_app_request(id: int, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = DeleteAppRequest(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return ResponseBoolModel(result=deleted)


@AppRequestsRouter.put("/status/{id}", response_model=ResponseBoolModel)
def update_app_request_status(id: int, dto: AppRequestStatusSchema, db: Session = Depends(get_db)):
    repo = AppRequestRepoImpl(db)
    use_case = UpdateAppRequestStatus(repo)
    updated = use_case.execute(id, AppRequestStatusDTO(**dto.model_dump()))
    if not updated:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada")
    return ResponseBoolModel(result=updated)

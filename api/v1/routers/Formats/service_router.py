from fastapi import APIRouter, Depends, HTTPException
from mainContext.infrastructure.dependencies import get_formats_service_repo
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.service_dto import ServiceCreateDTO, ServiceUpdateDTO, ServiceTableRowDTO, ServicesFormatList
## Importing Use Cases
from mainContext.application.use_cases.Formats.service import CreateService, UpdateService, GetServiceById, DeleteService, GetListServices, GetSPServices, GetSCServices, GetOSServices

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.service_repo import ServiceRepoImpl

#Importing Schemas
from api.v1.schemas.Formats.service import ServiceCreateSchema, ServiceUpdateSchema, ServiceSchema, ServiceTableRowSchema, ServicesFormatListSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


ServiceRouter = APIRouter(prefix="/services", tags=["Services"])


@ServiceRouter.post("create", response_model=ResponseIntModel)
def create_service(dto: ServiceCreateSchema, repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = CreateService(repo)
    created = use_case.execute(ServiceCreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@ServiceRouter.get("get_by_id/{id}", response_model=ServiceSchema)
def get_service_by_id(id : int, repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = GetServiceById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="Service not found")
    return get

@ServiceRouter.get("get_list", response_model=List[ServiceTableRowSchema])
def get_list_services(repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = GetListServices(repo)
    return use_case.execute()

@ServiceRouter.put("update/{service_id}")
def update_service(service_id: int, dto: ServiceUpdateSchema, repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = UpdateService(repo)
    updated = use_case.execute(service_id, ServiceUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")
    return ResponseBoolModel(result=updated)

@ServiceRouter.delete("delete/{id}")
def delete_service(id: int, repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = DeleteService(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@ServiceRouter.get("get_sp_services", response_model=List[ServicesFormatListSchema])
def get_sp_services(repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = GetSPServices(repo)
    return use_case.execute()

@ServiceRouter.get("get_sc_services", response_model=List[ServicesFormatListSchema])
def get_sc_services(repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = GetSCServices(repo)
    return use_case.execute()

@ServiceRouter.get("get_os_services", response_model=List[ServicesFormatListSchema])
def get_os_services(repo: ServiceRepoImpl = Depends(get_formats_service_repo)):
    use_case = GetOSServices(repo)
    return use_case.execute()
    
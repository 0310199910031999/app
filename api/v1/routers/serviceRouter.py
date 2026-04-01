from fastapi import APIRouter, Depends, HTTPException
from typing import List

from mainContext.application.dtos.service_dto import ServiceCreateDTO, ServiceUpdateDTO
from mainContext.application.use_cases.service_use_cases import (
    CreateService,
    GetServiceById,
    GetAllServices,
    UpdateService,
    DeleteService
)
from mainContext.infrastructure.dependencies import get_service_repo
from mainContext.infrastructure.adapters.ServiceRepo import ServiceRepoImpl

from api.v1.schemas.service import ServiceSchema, ServiceCreateSchema, ServiceUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

ServiceRouter = APIRouter(prefix="/services", tags=["Services"])


@ServiceRouter.post("/create", response_model=ResponseIntModel)
def create_service(dto: ServiceCreateSchema, repo: ServiceRepoImpl = Depends(get_service_repo)):
    """
    Crea un nuevo servicio
    
    Campos requeridos:
    - code: Código del servicio
    - name: Nombre del servicio
    - description: Descripción (opcional)
    - type: Tipo de servicio (opcional)
    """
    use_case = CreateService(repo)
    service_id = use_case.execute(ServiceCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=service_id)


@ServiceRouter.get("/get/{id}", response_model=ServiceSchema)
def get_service_by_id(id: int, repo: ServiceRepoImpl = Depends(get_service_repo)):
    """
    Obtiene un servicio por su ID
    """
    use_case = GetServiceById(repo)
    service = use_case.execute(id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@ServiceRouter.get("/get_all", response_model=List[ServiceSchema])
def get_all_services(repo: ServiceRepoImpl = Depends(get_service_repo)):
    """
    Obtiene todos los servicios
    """
    use_case = GetAllServices(repo)
    return use_case.execute()


@ServiceRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_service(id: int, dto: ServiceUpdateSchema, repo: ServiceRepoImpl = Depends(get_service_repo)):
    """
    Actualiza los datos de un servicio
    
    Campos actualizables:
    - code: Código del servicio
    - name: Nombre del servicio
    - description: Descripción
    - type: Tipo de servicio
    """
    use_case = UpdateService(repo)
    updated = use_case.execute(id, ServiceUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")
    return ResponseBoolModel(result=updated)


@ServiceRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_service(id: int, repo: ServiceRepoImpl = Depends(get_service_repo)):
    """
    Elimina un servicio
    """
    use_case = DeleteService(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found")
    return ResponseBoolModel(result=deleted)

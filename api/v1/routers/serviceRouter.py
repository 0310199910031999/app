from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.service_dto import ServiceCreateDTO, ServiceUpdateDTO
from mainContext.application.use_cases.service_use_cases import (
    CreateService,
    GetServiceById,
    GetAllServices,
    UpdateService,
    DeleteService
)
from mainContext.infrastructure.adapters.ServiceRepo import ServiceRepoImpl

from api.v1.schemas.service import ServiceSchema, ServiceCreateSchema, ServiceUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

ServiceRouter = APIRouter(prefix="/services", tags=["Services"])


@ServiceRouter.post("/create", response_model=ResponseIntModel)
def create_service(dto: ServiceCreateSchema, db: Session = Depends(get_db)):
    """
    Crea un nuevo servicio
    
    Campos requeridos:
    - code: Código del servicio
    - name: Nombre del servicio
    - description: Descripción (opcional)
    - type: Tipo de servicio (opcional)
    """
    repo = ServiceRepoImpl(db)
    use_case = CreateService(repo)
    service_id = use_case.execute(ServiceCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=service_id)


@ServiceRouter.get("/get/{id}", response_model=ServiceSchema)
def get_service_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un servicio por su ID
    """
    repo = ServiceRepoImpl(db)
    use_case = GetServiceById(repo)
    service = use_case.execute(id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@ServiceRouter.get("/get_all", response_model=List[ServiceSchema])
def get_all_services(db: Session = Depends(get_db)):
    """
    Obtiene todos los servicios
    """
    repo = ServiceRepoImpl(db)
    use_case = GetAllServices(repo)
    return use_case.execute()


@ServiceRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_service(id: int, dto: ServiceUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un servicio
    
    Campos actualizables:
    - code: Código del servicio
    - name: Nombre del servicio
    - description: Descripción
    - type: Tipo de servicio
    """
    repo = ServiceRepoImpl(db)
    use_case = UpdateService(repo)
    updated = use_case.execute(id, ServiceUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Service not found")
    return ResponseBoolModel(result=updated)


@ServiceRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_service(id: int, db: Session = Depends(get_db)):
    """
    Elimina un servicio
    """
    repo = ServiceRepoImpl(db)
    use_case = DeleteService(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Service not found")
    return ResponseBoolModel(result=deleted)

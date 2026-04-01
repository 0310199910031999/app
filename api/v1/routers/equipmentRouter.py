from fastapi import APIRouter, Depends, HTTPException
from typing import List

# Importing Application Layer
from mainContext.application.dtos.Equipment.create_equipment_dto import CreateEquipmentDTO
from mainContext.application.use_cases.Equipment.list_equipment_by_client import ListEquipmentByClient
from mainContext.application.use_cases.Equipment.get_equipment_by_id import GetEquipmentById
from mainContext.application.use_cases.Equipment.create_equipment import CreateEquipment
from mainContext.application.use_cases.Equipment.delete_equipment import DeleteEquipment
from mainContext.application.dtos.Equipment.update_equipment_dto import UpdateEquipmentDTO
from mainContext.application.use_cases.Equipment.update_equipment import UpdateEquipmentUseCase
from mainContext.application.use_cases.Equipment.get_brands_and_types import GetBrandsAndTypes
from mainContext.application.use_cases.Equipment.get_equipment_by_property import GetEquipmentByProperty
from mainContext.application.use_cases.Equipment.update_equipment_status import UpdateEquipmentStatus
from mainContext.application.use_cases.Equipment.end_equipment_rental import EndEquipmentRental
from mainContext.application.use_cases.Equipment.update_equipment_hourometer import UpdateEquipmentHourometer


# Importing Infrastructure Layer
from mainContext.infrastructure.dependencies import get_equipment_repo
from mainContext.infrastructure.adapters.EquipmentRepo import EquipmentRepoImpl

# Importing Schemas 
from api.v1.schemas.equipment import EquipmentSchema, BrandsTypesSchema, EquipmentByPropertySchema, UpdateStatusSchema, UpdateHourometerSchema




equipmentRouter = APIRouter(prefix="/equipment", tags=["Equipment"])

@equipmentRouter.get("/byClient/{client_id}", response_model=List[EquipmentSchema])
def list_equipment_by_client(client_id: int, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    use_case = ListEquipmentByClient(repo)
    return use_case.execute(client_id)

@equipmentRouter.get("/brandsAndTypes", response_model=BrandsTypesSchema)
def get_brands_and_types(repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    use_case = GetBrandsAndTypes(repo)
    return use_case.execute()

@equipmentRouter.get("/byProperty/{property}", response_model=List[EquipmentByPropertySchema])
def get_equipment_by_property(property: str, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    """
    Obtiene equipos por propiedad (Arrendamiento/Propio)
    
    Incluye el nombre del cliente asociado al equipo
    """
    use_case = GetEquipmentByProperty(repo)
    return use_case.execute(property)


@equipmentRouter.get("/{equipment_id}", response_model=EquipmentSchema)
def get_equipment_by_id(equipment_id: int, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    use_case = GetEquipmentById(repo)
    return use_case.execute(equipment_id)

@equipmentRouter.post("/", response_model=EquipmentSchema)
def create_equipment(dto: CreateEquipmentDTO, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    use_case = CreateEquipment(repo)
    return use_case.execute(dto)

@equipmentRouter.delete("/{equipment_id}", response_model=bool)
def delete_equipment(equipment_id: int, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    use_case = DeleteEquipment(repo)
    return use_case.execute(equipment_id)

@equipmentRouter.put("/{equipment_id}", response_model=EquipmentSchema)
def update_equipment(equipment_id: int, dto: UpdateEquipmentDTO, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    use_case = UpdateEquipmentUseCase(repo)
    update = use_case.execute(equipment_id, dto)
    if not update:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return update

@equipmentRouter.patch("/{equipment_id}/status", response_model=bool)
def update_equipment_status(equipment_id: int, dto: UpdateStatusSchema, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    """
    Actualiza el status de un equipo
    """
    use_case = UpdateEquipmentStatus(repo)
    result = use_case.execute(equipment_id, dto.status)
    if not result:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return result

@equipmentRouter.patch("/{equipment_id}/hourometer", response_model=bool)
def update_equipment_hourometer(equipment_id: int, dto: UpdateHourometerSchema, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    """
    Actualiza únicamente el horómetro de un equipo
    """
    use_case = UpdateEquipmentHourometer(repo)
    result = use_case.execute(equipment_id, dto.hourometer)
    if not result:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return result

@equipmentRouter.post("/{equipment_id}/end-rental", response_model=bool)
def end_equipment_rental(equipment_id: int, repo: EquipmentRepoImpl = Depends(get_equipment_repo)):
    """
    Termina el arrendamiento de un equipo actualizando su client_id a 11
    """
    use_case = EndEquipmentRental(repo)
    result = use_case.execute(equipment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return result

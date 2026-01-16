from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from shared.db import get_db
from mainContext.application.dtos.vehicle_dto import VehicleCreateDTO, VehicleUpdateDTO
from mainContext.application.use_cases.vehicle import (
    CreateVehicle,
    DeleteVehicle,
    GetVehicleById,
    ListVehicles,
    ListVehiclesTable,
    UpdateVehicle,
)
from mainContext.infrastructure.adapters.vehicle_repo import VehicleRepoImpl
from api.v1.schemas.vehicle import (
    VehicleCreateSchema,
    VehicleSchema,
    VehicleTableRowSchema,
    VehicleUpdateSchema,
    VehicleListSchema,
)
from api.v1.schemas.responses import ResponseIntModel, ResponseBoolModel


VehicleRouter = APIRouter(prefix="/vehicles", tags=["Vehicles"])


@VehicleRouter.post("/create", response_model=ResponseIntModel)
def create_vehicle(dto: VehicleCreateSchema, db: Session = Depends(get_db)):
    repo = VehicleRepoImpl(db)
    use_case = CreateVehicle(repo)
    new_id = use_case.execute(VehicleCreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=new_id)


@VehicleRouter.get("/get_by_id/{vehicle_id}", response_model=VehicleSchema)
def get_vehicle_by_id(vehicle_id: int, db: Session = Depends(get_db)):
    repo = VehicleRepoImpl(db)
    use_case = GetVehicleById(repo)
    vehicle = use_case.execute(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@VehicleRouter.get("/list", response_model=VehicleListSchema)
def list_vehicles(db: Session = Depends(get_db)):
    repo = VehicleRepoImpl(db)
    use_case = ListVehicles(repo)
    vehicles = use_case.execute()
    return {"vehicles": vehicles}


@VehicleRouter.get("/table", response_model=List[VehicleTableRowSchema])
def list_vehicles_table(db: Session = Depends(get_db)):
    repo = VehicleRepoImpl(db)
    use_case = ListVehiclesTable(repo)
    return use_case.execute()


@VehicleRouter.put("/update/{vehicle_id}", response_model=ResponseBoolModel)
def update_vehicle(vehicle_id: int, dto: VehicleUpdateSchema, db: Session = Depends(get_db)):
    repo = VehicleRepoImpl(db)
    use_case = UpdateVehicle(repo)
    updated = use_case.execute(vehicle_id, VehicleUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return ResponseBoolModel(result=updated)


@VehicleRouter.delete("/delete/{vehicle_id}", response_model=ResponseBoolModel)
def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    repo = VehicleRepoImpl(db)
    use_case = DeleteVehicle(repo)
    deleted = use_case.execute(vehicle_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return ResponseBoolModel(result=deleted)

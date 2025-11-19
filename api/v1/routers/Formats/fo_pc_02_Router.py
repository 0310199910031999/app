from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_pc_02_dto import CreateFOPC02DTO, UpdateFOPc02DTO, FOPC02SignatureDTO, FOPC02TableRowDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_pc_02 import (
    CreateFOPC02, 
    UpdateFOPC02, 
    GetFOPC02ById, 
    GetListFOPC02ByEquipmentId, 
    DeleteFOPC02, 
    SignFOPC02Departure,
    SignFOPC02Return,
    GetListFOPC02Table
)

# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_pc_02_repo import FOPC02RepoImpl

# Importing Schemas
from api.v1.schemas.Formats.fo_pc_02 import (
    FOPC02UpdateSchema, 
    FOPC02Schema, 
    FOPC02TableRowSchema, 
    FOPC02CreateSchema,
    FOPC02SignatureSchema
)
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel


FOPC02Router = APIRouter(prefix="/fopc02", tags=["FOPC02"])


@FOPC02Router.post("/create", response_model=ResponseIntModel)
def create_fopc02(dto: FOPC02CreateSchema, db: Session = Depends(get_db)):
    repo = FOPC02RepoImpl(db)
    use_case = CreateFOPC02(repo)
    created = use_case.execute(CreateFOPC02DTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOPC02Router.get("/get_by_id/{id}", response_model=FOPC02Schema)
def get_fopc02_by_id(id: int, db: Session = Depends(get_db)):
    repo = FOPC02RepoImpl(db)
    use_case = GetFOPC02ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return get

@FOPC02Router.get("/get_table/{equipment_id}", response_model=List[FOPC02TableRowSchema])
def get_list_fopc02_table(equipment_id: int, db: Session = Depends(get_db)):
    repo = FOPC02RepoImpl(db)
    use_case = GetListFOPC02Table(repo)
    return use_case.execute(equipment_id)

@FOPC02Router.put("/update/{fopc02_id}", response_model=ResponseBoolModel)
def update_fopc02(fopc02_id: int, dto: FOPC02UpdateSchema, db: Session = Depends(get_db)):
    repo = FOPC02RepoImpl(db)
    use_case = UpdateFOPC02(repo)
    updated = use_case.execute(fopc02_id, UpdateFOPc02DTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return ResponseBoolModel(result=updated)

@FOPC02Router.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_fopc02(id: int, db: Session = Depends(get_db)):
    repo = FOPC02RepoImpl(db)
    use_case = DeleteFOPC02(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOPC02Router.put("/sign_departure/{fopc02_id}", response_model=ResponseBoolModel)
def sign_fopc02_departure(fopc02_id: int, dto: FOPC02SignatureSchema, db: Session = Depends(get_db)):
    """
    Firma de salida (departure)
    - is_employee=True: firma del empleado (TecExt)
    - is_employee=False: firma del cliente (CliExt)
    """
    repo = FOPC02RepoImpl(db)
    use_case = SignFOPC02Departure(repo)
    signed = use_case.execute(fopc02_id, FOPC02SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return ResponseBoolModel(result=signed)

@FOPC02Router.put("/sign_return/{fopc02_id}", response_model=ResponseBoolModel)
def sign_fopc02_return(fopc02_id: int, dto: FOPC02SignatureSchema, db: Session = Depends(get_db)):
    """
    Firma de retorno (return)
    - is_employee=True: firma del empleado (TecRet)
    - is_employee=False: firma del cliente (CliRet)
    """
    repo = FOPC02RepoImpl(db)
    use_case = SignFOPC02Return(repo)
    signed = use_case.execute(fopc02_id, FOPC02SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return ResponseBoolModel(result=signed)

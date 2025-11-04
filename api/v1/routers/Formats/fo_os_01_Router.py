from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_os_01_dto import FOOS01CreateDTO, FOOS01UpdateDTO, FOOS01SignatureDTO, FOOS01TableRowDTO, FOOS01ServiceDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_os_01 import CreateFOOS01, UpdateFOOS01, GetFOOS01ById, GetListFOOS01ByEquipmentId, DeleteFOOS01, SignFOOS01, GetListFOOS01Table

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_os_01_repo import FOOS01RepoImpl

#Importing Schemas
from api.v1.schemas.Formats.fo_os_01 import FOOS01UpdateSchema, FOOS01Schema, FOOS01TableRowSchema, FOOS01CreateSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


FOOS01Router = APIRouter(prefix="/foos01", tags=["FOOS01"])


@FOOS01Router.post("create", response_model=ResponseIntModel)
def create_foos01(dto: FOOS01CreateSchema, db: Session = Depends(get_db)):
    repo = FOOS01RepoImpl(db)
    use_case = CreateFOOS01(repo)
    created = use_case.execute(FOOS01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOOS01Router.get("get_by_id/{id}", response_model=FOOS01Schema)
def get_foos01_by_id(id : int, db: Session = Depends(get_db)):
    repo = FOOS01RepoImpl(db)
    use_case = GetFOOS01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOOS01 not found")
    return get


@FOOS01Router.get("get_table/{equipment_id}", response_model=List[FOOS01TableRowSchema])
def get_list_foos01_table(equipment_id: int, db: Session = Depends(get_db)):
    repo = FOOS01RepoImpl(db)
    use_case = GetListFOOS01Table(repo)
    return use_case.execute(equipment_id)

@FOOS01Router.put("update/{foos01_id}")
def update_foos01(foos01_id: int, dto: FOOS01UpdateSchema, db: Session = Depends(get_db)):
    repo = FOOS01RepoImpl(db)
    use_case = UpdateFOOS01(repo)
    updated = use_case.execute(foos01_id, FOOS01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOOS01 not found")
    return ResponseBoolModel(result=updated)



@FOOS01Router.delete("delete/{id}")
def delete_foos01(id: int, db: Session = Depends(get_db)):
    repo = FOOS01RepoImpl(db)
    use_case = DeleteFOOS01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOOS01Router.put("sign/{foos01_id}")
def sign_foos01(foos01_id: int, dto: FOOS01SignatureDTO, db: Session = Depends(get_db)):
    repo = FOOS01RepoImpl(db)
    use_case = SignFOOS01(repo)
    signed = use_case.execute(foos01_id, FOOS01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOOS01 not found")
    return ResponseBoolModel(result=signed)


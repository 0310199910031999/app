from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO, FOSP01UpdateDTO, FOSP01SignatureDTO, FOSP01TableRowDTO, FOSP01ServiceDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_sp_01 import CreateFOSP01, UpdateFOSP01, GetFOSP01ById, GetListFOSP01ByEquipmentId, DeleteFOSP01, SignFOSP01, GetListFOSP01Table

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_sp_01_repo import FOSP01RepoImpl

#Importing Schemas
from api.v1.schemas.Formats.fo_sp_01 import FOSP01UpdateSchema, FOSP01Schema, FOSP01TableRowSchema, FOSP01CreateSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


FOSP01Router = APIRouter(prefix="/fosp01", tags=["FOSP01"])


@FOSP01Router.post("create", response_model=ResponseIntModel)
def create_fosp01(dto: FOSP01CreateSchema, db: Session = Depends(get_db)):
    repo = FOSP01RepoImpl(db)
    use_case = CreateFOSP01(repo)
    created = use_case.execute(FOSP01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOSP01Router.get("get_by_id/{id}", response_model=FOSP01Schema)
def get_fosp01_by_id(id : int, db: Session = Depends(get_db)):
    repo = FOSP01RepoImpl(db)
    use_case = GetFOSP01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOSP01 not found")
    return get


@FOSP01Router.get("get_table/{equipment_id}", response_model=List[FOSP01TableRowSchema])
def get_list_fosp01_table(equipment_id: int, db: Session = Depends(get_db)):
    repo = FOSP01RepoImpl(db)
    use_case = GetListFOSP01Table(repo)
    return use_case.execute(equipment_id)

@FOSP01Router.put("update/{fosp01_id}")
def update_fosp01(fosp01_id: int, dto: FOSP01UpdateSchema, db: Session = Depends(get_db)):
    repo = FOSP01RepoImpl(db)
    use_case = UpdateFOSP01(repo)
    updated = use_case.execute(fosp01_id, FOSP01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOSP01 not found")
    return ResponseBoolModel(result=updated)



@FOSP01Router.delete("delete/{id}")
def delete_fosp01(id: int, db: Session = Depends(get_db)):
    repo = FOSP01RepoImpl(db)
    use_case = DeleteFOSP01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOSP01Router.put("sign/{fosp01_id}")
def sign_fosp01(fosp01_id: int, dto: FOSP01SignatureDTO, db: Session = Depends(get_db)):
    repo = FOSP01RepoImpl(db)
    use_case = SignFOSP01(repo)
    signed = use_case.execute(fosp01_id, FOSP01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOSP01 not found")
    return ResponseBoolModel(result=signed)



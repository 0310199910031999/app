from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_sc_01_dto import FOSC01CreateDTO, FOSC01UpdateDTO, FOSC01SignatureDTO, FOSC01TableRowDTO, FOSC01ServiceDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_sc_01 import CreateFOSC01, UpdateFOSC01, GetFOSC01ById, GetListFOSC01ByEquipmentId, DeleteFOSC01, SignFOSC01, GetListFOSC01Table

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_sc_01_repo import FOSC01RepoImpl

#Importing Schemas
from api.v1.schemas.Formats.fo_sc_01 import FOSC01UpdateSchema, FOSC01Schema, FOSC01TableRowSchema, FOSC01CreateSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


FOSC01Router = APIRouter(prefix="/fosc01", tags=["FOSC01"])


@FOSC01Router.post("create", response_model=ResponseIntModel)
def create_fosc01(dto: FOSC01CreateSchema, db: Session = Depends(get_db)):
    repo = FOSC01RepoImpl(db)
    use_case = CreateFOSC01(repo)
    created = use_case.execute(FOSC01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOSC01Router.get("get_by_id/{id}", response_model=FOSC01Schema)
def get_fosc01_by_id(id : int, db: Session = Depends(get_db)):
    repo = FOSC01RepoImpl(db)
    use_case = GetFOSC01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOSC01 not found")
    return get


@FOSC01Router.get("get_table/{equipment_id}", response_model=List[FOSC01TableRowSchema])
def get_list_fosc01_table(equipment_id: int, db: Session = Depends(get_db)):
    repo = FOSC01RepoImpl(db)
    use_case = GetListFOSC01Table(repo)
    return use_case.execute(equipment_id)

@FOSC01Router.put("update/{fosc01_id}")
def update_fosc01(fosc01_id: int, dto: FOSC01UpdateSchema, db: Session = Depends(get_db)):
    repo = FOSC01RepoImpl(db)
    use_case = UpdateFOSC01(repo)
    updated = use_case.execute(fosc01_id, FOSC01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOSC01 not found")
    return ResponseBoolModel(result=updated)



@FOSC01Router.delete("delete/{id}")
def delete_fosc01(id: int, db: Session = Depends(get_db)):
    repo = FOSC01RepoImpl(db)
    use_case = DeleteFOSC01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOSC01Router.put("sign/{fosc01_id}")
def sign_fosc01(fosc01_id: int, dto: FOSC01SignatureDTO, db: Session = Depends(get_db)):
    repo = FOSC01RepoImpl(db)
    use_case = SignFOSC01(repo)
    signed = use_case.execute(fosc01_id, FOSC01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOSC01 not found")
    return ResponseBoolModel(result=signed)



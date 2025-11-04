from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List


from mainContext.application.dtos.Formats.fo_em_01_dto import FOEM01CreatedDTO, FOEM01UpdateDTO, FOEM01SignatureDTO, FOEM01TableRowDTO

## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_em_01 import CreateFOEM01, UpdateFOEM01, GetFOEM01ById, DeleteFOEM01, SignFOEM01, GetListFOEM01Table

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_em_01_repo import FOEM01RepoImpl

#Importing Schemas
from api.v1.schemas.Formats.fo_em_01 import FOEM01UpdateSchema, FOEM01Schema, FOEM01TableRowSchema, FOEM01CreatedSchema, FOEM01SignatureSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


FOEM01Router = APIRouter(prefix="/foem01", tags=["FOEM01"])


@FOEM01Router.post("create", response_model=ResponseIntModel)
def create_foem01(dto: FOEM01CreatedSchema, db: Session = Depends(get_db)):
    repo = FOEM01RepoImpl(db)
    use_case = CreateFOEM01(repo)
    created = use_case.execute(FOEM01CreatedDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOEM01Router.get("get_by_id/{id}", response_model=FOEM01Schema)
def get_foem01_by_id(id : int, db: Session = Depends(get_db)):
    repo = FOEM01RepoImpl(db)
    use_case = GetFOEM01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOEM01 not found")
    return get


@FOEM01Router.get("get_table/{equipment_id}", response_model=List[FOEM01TableRowSchema])
def get_list_foem01_table(equipment_id: int, db: Session = Depends(get_db)):
    repo = FOEM01RepoImpl(db)
    use_case = GetListFOEM01Table(repo)
    return use_case.execute(equipment_id)

@FOEM01Router.put("update/{foem01_id}")
def update_foem01(foem01_id: int, dto: FOEM01UpdateSchema, db: Session = Depends(get_db)):
    repo = FOEM01RepoImpl(db)
    use_case = UpdateFOEM01(repo)
    updated = use_case.execute(foem01_id, FOEM01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOEM01 not found")
    return ResponseBoolModel(result=updated)



@FOEM01Router.delete("delete/{id}")
def delete_foem01(id: int, db: Session = Depends(get_db)):
    repo = FOEM01RepoImpl(db)
    use_case = DeleteFOEM01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOEM01Router.put("sign/{foem01_id}")
def sign_foem01(foem01_id: int, dto: FOEM01SignatureSchema, db: Session = Depends(get_db)):
    repo = FOEM01RepoImpl(db)
    use_case = SignFOEM01(repo)
    signed = use_case.execute(foem01_id, FOEM01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOEM01 not found")
    return ResponseBoolModel(result=signed)
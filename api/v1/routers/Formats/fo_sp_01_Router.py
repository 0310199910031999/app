from fastapi import APIRouter, Depends, HTTPException, Response
from mainContext.infrastructure.dependencies import get_fosp01_repo
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_sp_01_dto import FOSP01CreateDTO, FOSP01UpdateDTO, FOSP01SignatureDTO, FOSP01TableRowDTO, FOSP01ServiceDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_sp_01 import CreateFOSP01, UpdateFOSP01, GetFOSP01ById, GetListFOSP01ByEquipmentId, DeleteFOSP01, SignFOSP01, GetListFOSP01Table
from mainContext.application.use_cases.Formats.generate_fosp01_pdf_use_case import GenerateFoSp01PdfUseCase

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_sp_01_repo import FOSP01RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter

#Importing Schemas
from api.v1.schemas.Formats.fo_sp_01 import FOSP01UpdateSchema, FOSP01Schema, FOSP01TableRowSchema, FOSP01CreateSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


FOSP01Router = APIRouter(prefix="/fosp01", tags=["FOSP01"])


@FOSP01Router.post("create", response_model=ResponseIntModel)
def create_fosp01(dto: FOSP01CreateSchema, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    use_case = CreateFOSP01(repo)
    created = use_case.execute(FOSP01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOSP01Router.get("get_by_id/{id}", response_model=FOSP01Schema)
def get_fosp01_by_id(id : int, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    use_case = GetFOSP01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOSP01 not found")
    return get


@FOSP01Router.get("get_table/{equipment_id}", response_model=List[FOSP01TableRowSchema])
def get_list_fosp01_table(equipment_id: int, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    use_case = GetListFOSP01Table(repo)
    return use_case.execute(equipment_id)

@FOSP01Router.put("update/{fosp01_id}")
def update_fosp01(fosp01_id: int, dto: FOSP01UpdateSchema, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    use_case = UpdateFOSP01(repo)
    updated = use_case.execute(fosp01_id, FOSP01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOSP01 not found")
    return ResponseBoolModel(result=updated)



@FOSP01Router.delete("delete/{id}")
def delete_fosp01(id: int, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    use_case = DeleteFOSP01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOSP01Router.put("sign/{fosp01_id}")
def sign_fosp01(fosp01_id: int, dto: FOSP01SignatureDTO, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    use_case = SignFOSP01(repo)
    signed = use_case.execute(fosp01_id, FOSP01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOSP01 not found")
    return ResponseBoolModel(result=signed)


@FOSP01Router.get(
    "generate_pdf/{fosp01_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_fosp01_pdf(fosp01_id: int, repo: FOSP01RepoImpl = Depends(get_fosp01_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoSp01PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(fosp01_id)
    return Response(content=pdf_bytes, media_type="application/pdf")



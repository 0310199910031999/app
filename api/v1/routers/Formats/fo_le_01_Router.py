from fastapi import APIRouter, Depends, HTTPException, Response
from mainContext.infrastructure.dependencies import get_fole01_repo
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_le_01_dto import FOLE01CreateDTO, FOLE01UpdateDTO, FOLE01SignatureDTO, FOLE01ServiceDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_le_01 import CreateFOLE01, UpdateFOLE01, GetFOLE01ById, GetListFOLE01ByEquipmentId, DeleteFOLE01, SignFOLE01, GetListFOLE01Table
from mainContext.application.use_cases.Formats.generate_fole01_pdf_use_case import GenerateFoLe01PdfUseCase

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_le_01_repo import FOLE01RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter

#Importing Schemas
from api.v1.schemas.Formats.fo_le_01 import FOLE01UpdateSchema, FOLE01Schema, FOLE01TableRowSchema, FOLE01CreateSchema, FOLE01SignatureSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel

FOLE01Router = APIRouter(prefix="/fole01", tags=["FOLE01"])


@FOLE01Router.post("create", response_model=ResponseIntModel)
def create_fole01(dto: FOLE01CreateSchema, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    use_case = CreateFOLE01(repo)
    created = use_case.execute(FOLE01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOLE01Router.get("get_by_id/{id}", response_model=FOLE01Schema)
def get_fole01_by_id(id : int, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    use_case = GetFOLE01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOLE01 not found")
    return get


@FOLE01Router.get("get_table/{equipment_id}", response_model=List[FOLE01TableRowSchema])
def get_list_fole01_table(equipment_id: int, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    use_case = GetListFOLE01Table(repo)
    return use_case.execute(equipment_id)

@FOLE01Router.put("update/{fole01_id}")
def update_fole01(fole01_id: int, dto: FOLE01UpdateSchema, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    use_case = UpdateFOLE01(repo)
    updated = use_case.execute(fole01_id, FOLE01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOLE01 not found")
    return ResponseBoolModel(result=updated)



@FOLE01Router.delete("delete/{id}")
def delete_fole01(id: int, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    use_case = DeleteFOLE01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOLE01Router.put("sign/{fole01_id}")
def sign_fole01(fole01_id: int, dto: FOLE01SignatureSchema, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    use_case = SignFOLE01(repo)
    signed = use_case.execute(fole01_id, FOLE01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOLE01 not found")
    return ResponseBoolModel(result=signed)

@FOLE01Router.get(
    "generate_pdf/{fole01_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_fole01_pdf(fole01_id: int, repo: FOLE01RepoImpl = Depends(get_fole01_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoLe01PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(fole01_id)
    return Response(content=pdf_bytes, media_type="application/pdf")
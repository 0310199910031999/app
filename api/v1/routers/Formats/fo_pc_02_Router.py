from fastapi import APIRouter, Depends, HTTPException, Response
from mainContext.infrastructure.dependencies import get_fopc02_repo
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_pc_02_dto import (
    CreateFOPC02DTO,
    UpdateFOPc02DTO,
    FOPC02SignatureDTO,
    FOPC02TableRowDTO,
    GetFOPC02ByDocumentDTO,
    FOPC02ByDocumentResponseDTO
)
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_pc_02 import (
    CreateFOPC02, 
    UpdateFOPC02, 
    GetFOPC02ById, 
    GetListFOPC02ByEquipmentId, 
    DeleteFOPC02, 
    SignFOPC02Departure,
    SignFOPC02Return,
    GetListFOPC02Table,
    GetFOPC02ByDocument
)
from mainContext.application.use_cases.Formats.generate_fopc02_pdf_use_case import GenerateFoPc02PdfUseCase

# Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_pc_02_repo import FOPC02RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter

# Importing Schemas
from api.v1.schemas.Formats.fo_pc_02 import (
    FOPC02UpdateSchema, 
    FOPC02Schema, 
    FOPC02TableRowSchema, 
    FOPC02CreateSchema,
    FOPC02SignatureSchema,
    GetFOPC02ByDocumentSchema,
    FOPC02ByDocumentResponseSchema
)
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel


FOPC02Router = APIRouter(prefix="/fopc02", tags=["FOPC02"])


@FOPC02Router.post("/create", response_model=ResponseIntModel)
def create_fopc02(dto: FOPC02CreateSchema, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    use_case = CreateFOPC02(repo)
    created = use_case.execute(CreateFOPC02DTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOPC02Router.get("/get_by_id/{id}", response_model=FOPC02Schema)
def get_fopc02_by_id(id: int, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    use_case = GetFOPC02ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return get

@FOPC02Router.get("/get_table/{equipment_id}", response_model=List[FOPC02TableRowSchema])
def get_list_fopc02_table(equipment_id: int, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    use_case = GetListFOPC02Table(repo)
    return use_case.execute(equipment_id)

@FOPC02Router.put("/update/{fopc02_id}", response_model=ResponseBoolModel)
def update_fopc02(fopc02_id: int, dto: FOPC02UpdateSchema, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    use_case = UpdateFOPC02(repo)
    updated = use_case.execute(fopc02_id, UpdateFOPc02DTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return ResponseBoolModel(result=updated)

@FOPC02Router.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_fopc02(id: int, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    use_case = DeleteFOPC02(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOPC02Router.put("/sign_departure/{fopc02_id}", response_model=ResponseBoolModel)
def sign_fopc02_departure(fopc02_id: int, dto: FOPC02SignatureSchema, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    """
    Firma de salida (departure)
    - is_employee=True: firma del empleado (TecExt)
    - is_employee=False: firma del cliente (CliExt)
    """
    use_case = SignFOPC02Departure(repo)
    signed = use_case.execute(fopc02_id, FOPC02SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return ResponseBoolModel(result=signed)

@FOPC02Router.put("/sign_return/{fopc02_id}", response_model=ResponseBoolModel)
def sign_fopc02_return(fopc02_id: int, dto: FOPC02SignatureSchema, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    """
    Firma de retorno (return)
    - is_employee=True: firma del empleado (TecRet)
    - is_employee=False: firma del cliente (CliRet)
    """
    use_case = SignFOPC02Return(repo)
    signed = use_case.execute(fopc02_id, FOPC02SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOPC02 not found")
    return ResponseBoolModel(result=signed)


@FOPC02Router.post("/get_fopc02_by_document", response_model=List[FOPC02ByDocumentResponseSchema])
def get_fopc02_by_document(dto: GetFOPC02ByDocumentSchema, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    """
    Obtiene todos los FOPC02 asociados a un documento (FOOS01, FOSP01 o FOSC01)
    Retorna: id, date_created, status, file_id de cada FOPC02
    """
    use_case = GetFOPC02ByDocument(repo)
    try:
        result = use_case.execute(GetFOPC02ByDocumentDTO(**dto.model_dump()))
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@FOPC02Router.get(
    "generate_pdf/{fopc02_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_fopc02_pdf(fopc02_id: int, repo: FOPC02RepoImpl = Depends(get_fopc02_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoPc02PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(fopc02_id)
    return Response(content=pdf_bytes, media_type="application/pdf")

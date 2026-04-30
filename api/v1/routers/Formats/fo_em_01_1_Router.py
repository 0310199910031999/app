from fastapi import APIRouter, Depends, HTTPException, Response
from typing import List

from api.v1.schemas.Formats.fo_em_01_1 import FOEM011UpdateSchema, FOEM011Schema, FOEM011TableRowSchema, FOEM011CreatedSchema, FOEM011SignatureSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel
from mainContext.application.dtos.Formats.fo_em_01_1_dto import FOEM011CreateDTO, FOEM011UpdateDTO, FOEM011SignatureDTO
from mainContext.application.use_cases.Formats.fo_em_01_1 import CreateFOEM011, UpdateFOEM011, GetFOEM011ById, DeleteFOEM011, SignFOEM011, GetListFOEM011Table
from mainContext.application.use_cases.Formats.generate_foem01_1_pdf_use_case import GenerateFoEm011PdfUseCase
from mainContext.infrastructure.adapters.Formats.fo_em_01_1_repo import FOEM011RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter
from mainContext.infrastructure.dependencies import get_foem01_1_repo


FOEM011Router = APIRouter(prefix="/foem01_1", tags=["FOEM011"])


@FOEM011Router.post("create", response_model=ResponseIntModel)
def create_foem01_1(dto: FOEM011CreatedSchema, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    use_case = CreateFOEM011(repo)
    created = use_case.execute(FOEM011CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)


@FOEM011Router.get("get_by_id/{id}", response_model=FOEM011Schema)
def get_foem01_1_by_id(id: int, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    use_case = GetFOEM011ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOEM011 not found")
    return get


@FOEM011Router.get("get_table/{client_id}", response_model=List[FOEM011TableRowSchema])
def get_list_foem01_1_table(client_id: int, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    use_case = GetListFOEM011Table(repo)
    return use_case.execute(client_id)


@FOEM011Router.put("update/{foem01_1_id}")
def update_foem01_1(foem01_1_id: int, dto: FOEM011UpdateSchema, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    use_case = UpdateFOEM011(repo)
    updated = use_case.execute(foem01_1_id, FOEM011UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOEM011 not found")
    return ResponseBoolModel(result=updated)


@FOEM011Router.delete("delete/{id}")
def delete_foem01_1(id: int, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    use_case = DeleteFOEM011(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)


@FOEM011Router.put("sign/{foem01_1_id}")
def sign_foem01_1(foem01_1_id: int, dto: FOEM011SignatureSchema, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    use_case = SignFOEM011(repo)
    signed = use_case.execute(foem01_1_id, FOEM011SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOEM011 not found")
    return ResponseBoolModel(result=signed)


@FOEM011Router.get(
    "generate_pdf/{foem01_1_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_foem01_1_pdf(foem01_1_id: int, repo: FOEM011RepoImpl = Depends(get_foem01_1_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoEm011PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(foem01_1_id)
    return Response(content=pdf_bytes, media_type="application/pdf")
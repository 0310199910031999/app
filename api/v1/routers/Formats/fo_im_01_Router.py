from fastapi import APIRouter, Depends, HTTPException, Response
from mainContext.infrastructure.dependencies import get_foim01_repo
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_im_01_dto import FOIM01CreateDTO, FOIM01UpdateDTO, FOIM01SignatureDTO, FOIM01TableRowDTO, FOIM01AnswerDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_im_01 import CreateFOIM01, UpdateFOIM01, GetFOIM01ById, GetListFOIM01ByEquipmentId, DeleteFOIM01, SignFOIM01, GetListFOIM01Table, GetFOIMQuestions
from mainContext.application.use_cases.Formats.generate_foim01_pdf_use_case import GenerateFoIm01PdfUseCase

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_im_01_repo import FOIM01RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter

#Importing Schemas
from api.v1.schemas.Formats.fo_im_01 import FOIM01UpdateSchema, FOIM01Schema, FOIM01TableRowSchema, FOIM01CreateSchema, FOIM01SignatureSchema
from api.v1.schemas.Formats.fo_im_questions import FOIMQuestionSchema
from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel


FOIM01Router = APIRouter(prefix="/foim01", tags=["FOIM01"])


@FOIM01Router.post("create", response_model=ResponseIntModel)
def create_foim01(dto: FOIM01CreateSchema, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = CreateFOIM01(repo)
    created = use_case.execute(FOIM01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOIM01Router.get("get_by_id/{id}", response_model=FOIM01Schema)
def get_foim01_by_id(id : int, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = GetFOIM01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOIM01 not found")
    return get


@FOIM01Router.get("get_table/{equipment_id}", response_model=List[FOIM01TableRowSchema])
def get_list_foim01_table(equipment_id: int, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = GetListFOIM01Table(repo)
    return use_case.execute(equipment_id)

@FOIM01Router.put("update/{foim01_id}")
def update_foim01(foim01_id: int, dto: FOIM01UpdateSchema, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = UpdateFOIM01(repo)
    updated = use_case.execute(foim01_id, FOIM01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOIM01 not found")
    return ResponseBoolModel(result=updated)



@FOIM01Router.delete("delete/{id}")
def delete_foim01(id: int, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = DeleteFOIM01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOIM01Router.put("sign/{foim01_id}")
def sign_foim01(foim01_id: int, dto: FOIM01SignatureSchema, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = SignFOIM01(repo)
    signed = use_case.execute(foim01_id, FOIM01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOIM01 not found")
    return ResponseBoolModel(result=signed)


@FOIM01Router.get("/questions", response_model=List[FOIMQuestionSchema])
def get_foim_questions(repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    use_case = GetFOIMQuestions(repo)
    return use_case.execute()


@FOIM01Router.get(
    "generate_pdf/{foim01_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_foim01_pdf(foim01_id: int, repo: FOIM01RepoImpl = Depends(get_foim01_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoIm01PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(foim01_id)
    return Response(content=pdf_bytes, media_type="application/pdf")


from fastapi import APIRouter, Depends, HTTPException, Response
from mainContext.infrastructure.dependencies import get_fobc01_repo
from typing import List

from mainContext.application.dtos.Formats.fo_bc_01_dto import (
    FOBC01CreateDTO,
    FOBC01QuestionCreateDTO,
    FOBC01QuestionUpdateDTO,
    FOBC01SignatureDTO,
    FOBC01UpdateDTO,
)

from mainContext.application.use_cases.Formats.fo_bc_01 import (
    CreateFOBC01,
    CreateFOBC01Question,
    DeleteFOBC01,
    DeleteFOBC01Question,
    GetAllFOBC01Questions,
    GetFOBC01ById,
    GetFOBC01QuestionById,
    GetListFOBC01Table,
    SignFOBC01,
    UpdateFOBC01,
    UpdateFOBC01Question,
)
from mainContext.application.use_cases.Formats.generate_fobc01_pdf_use_case import GenerateFoBc01PdfUseCase

from mainContext.infrastructure.adapters.Formats.fo_bc_01_repo import FOBC01RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter
from api.v1.schemas.Formats.fo_bc_01 import (
    FOBC01CreateSchema,
    FOBC01QuestionCreateSchema,
    FOBC01QuestionSchema,
    FOBC01QuestionUpdateSchema,
    FOBC01Schema,
    FOBC01SignatureSchema,
    FOBC01TableRowSchema,
    FOBC01UpdateSchema,
)

from api.v1.schemas.responses   import ResponseBoolModel, ResponseIntModel

FOBC01Router = APIRouter(prefix="/fobc01", tags=["FOBC01"])

@FOBC01Router.post("create", response_model=ResponseIntModel)
def create_fobc01(dto: FOBC01CreateSchema, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = CreateFOBC01(repo)
    created = use_case.execute(FOBC01CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOBC01Router.get("get_by_id/{id}", response_model=FOBC01Schema)
def get_fobc01_by_id(id : int, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = GetFOBC01ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOBC01 not found")
    return get

@FOBC01Router.get("get_table/{equipment_id}", response_model=List[FOBC01TableRowSchema])
def get_list_fobc01_table(equipment_id: int, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = GetListFOBC01Table(repo)
    return use_case.execute(equipment_id)

@FOBC01Router.put("update/{fobc01_id}")
def update_fobc01(fobc01_id: int, dto: FOBC01UpdateSchema, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = UpdateFOBC01(repo)
    updated = use_case.execute(fobc01_id, FOBC01UpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOBC01 not found")
    return ResponseBoolModel(result=updated)

@FOBC01Router.delete("delete/{id}")
def delete_fobc01(id: int, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = DeleteFOBC01(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)

@FOBC01Router.put("sign/{fobc01_id}")
def sign_fobc01(fobc01_id: int, dto: FOBC01SignatureSchema, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = SignFOBC01(repo)
    signed = use_case.execute(fobc01_id, FOBC01SignatureDTO(**dto.model_dump(exclude_none=True)))
    if not signed:
        raise HTTPException(status_code=404, detail="FOBC01 not found")
    return ResponseBoolModel(result=signed)


@FOBC01Router.post("/questions/create", response_model=ResponseIntModel)
def create_fobc01_question(dto: FOBC01QuestionCreateSchema, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = CreateFOBC01Question(repo)
    created = use_case.execute(FOBC01QuestionCreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(result=created)


@FOBC01Router.get("/questions/get/{id}", response_model=FOBC01QuestionSchema)
def get_fobc01_question_by_id(id: int, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = GetFOBC01QuestionById(repo)
    question = use_case.execute(id)
    if not question:
        raise HTTPException(status_code=404, detail="FOBC01 question not found")
    return question


@FOBC01Router.get("/questions/get_all", response_model=List[FOBC01QuestionSchema])
def get_all_fobc01_questions(repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = GetAllFOBC01Questions(repo)
    return use_case.execute()


@FOBC01Router.put("/questions/update/{id}", response_model=ResponseBoolModel)
def update_fobc01_question(id: int, dto: FOBC01QuestionUpdateSchema, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = UpdateFOBC01Question(repo)
    updated = use_case.execute(id, FOBC01QuestionUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOBC01 question not found")
    return ResponseBoolModel(result=updated)


@FOBC01Router.delete("/questions/delete/{id}", response_model=ResponseBoolModel)
def delete_fobc01_question(id: int, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    use_case = DeleteFOBC01Question(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FOBC01 question not found")
    return ResponseBoolModel(result=deleted)


@FOBC01Router.get(
    "generate_pdf/{fobc01_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_fobc01_pdf(fobc01_id: int, repo: FOBC01RepoImpl = Depends(get_fobc01_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoBc01PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(fobc01_id)
    return Response(content=pdf_bytes, media_type="application/pdf")
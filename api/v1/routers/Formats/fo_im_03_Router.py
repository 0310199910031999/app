from fastapi import APIRouter, Depends, HTTPException, Response
from mainContext.infrastructure.dependencies import get_foim03_repo
from typing import List

# Importing Application Layer
## Importing DTOs
from mainContext.application.dtos.Formats.fo_im_03_dto import FOIM03CreateDTO, FOIM03ChangeStatusDTO, FOIM03TableRowDTO, FOIM03AnswerDTO
## Importing Use Cases
from mainContext.application.use_cases.Formats.fo_im_03 import CreateFOIM03, GetFOIM03ById, GetListFOIM03ByEquipmentId, DeleteFOIM03, GetListFOIM03Table, ChangeStatusFOIM03, GetAllFOIM03
from mainContext.application.use_cases.Formats.generate_foim03_pdf_use_case import GenerateFoIm03PdfUseCase

#Importing Infrastructure Layer
from mainContext.infrastructure.adapters.Formats.fo_im_03_repo import FOIM03RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter

#Importing Schemas
from api.v1.schemas.Formats.fo_im_03 import FOIM03AnswerSchema, FOIM03Schema, FOIM03TableRowSchema, FOIM03CreateSchema, FOIM03ListItemSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel


FOIM03Router = APIRouter(prefix="/foim03", tags=["FOIM03"])


@FOIM03Router.post("create", response_model=ResponseIntModel)
def create_foim03(dto: FOIM03CreateSchema, repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    use_case = CreateFOIM03(repo)
    created = use_case.execute(FOIM03CreateDTO(**dto.model_dump(exclude_none=True)))
    return ResponseIntModel(id=created)

@FOIM03Router.get("get_by_id/{id}", response_model=FOIM03Schema)
def get_foim03_by_id(id : int, repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    use_case = GetFOIM03ById(repo)
    get = use_case.execute(id)
    if not get:
        raise HTTPException(status_code=404, detail="FOIM03 not found")
    return get


@FOIM03Router.get("get_table/{equipment_id}", response_model=List[FOIM03TableRowSchema])
def get_list_foim03_table(equipment_id: int, repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    use_case = GetListFOIM03Table(repo)
    return use_case.execute(equipment_id)


@FOIM03Router.get("get_all", response_model=List[FOIM03ListItemSchema])
def get_all_foim03(repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    use_case = GetAllFOIM03(repo)
    return use_case.execute()

@FOIM03Router.put("change_status/{id}")
def change_status_foim03(id: int, dto: FOIM03ChangeStatusDTO, repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    use_case = ChangeStatusFOIM03(repo)
    updated = use_case.execute(id, FOIM03ChangeStatusDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOIM03 not found or status not changed")
    return ResponseBoolModel(result=updated)
    

@FOIM03Router.delete("delete/{id}")
def delete_foim03(id: int, repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    use_case = DeleteFOIM03(repo)
    deleted = use_case.execute(id)
    return ResponseBoolModel(result=deleted)


@FOIM03Router.get(
    "generate_pdf/{foim03_id}",
    responses={200: {"content": {"application/pdf": {}}, "description": "PDF generado correctamente"}},
    response_class=Response,
)
def generate_foim03_pdf(foim03_id: int, repo: FOIM03RepoImpl = Depends(get_foim03_repo)):
    pdf_generator = WeasyPrintPdfAdapter()
    use_case = GenerateFoIm03PdfUseCase(pdf_generator, repo)
    pdf_bytes = use_case.execute(foim03_id)
    return Response(content=pdf_bytes, media_type="application/pdf")



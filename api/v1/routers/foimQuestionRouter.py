from fastapi import APIRouter, Depends, HTTPException
from typing import List

from mainContext.application.dtos.foim_question_dto import FoimQuestionCreateDTO, FoimQuestionUpdateDTO
from mainContext.application.use_cases.foim_question_use_cases import (
    CreateFoimQuestion,
    GetFoimQuestionById,
    GetAllFoimQuestions,
    UpdateFoimQuestion,
    DeleteFoimQuestion
)
from mainContext.infrastructure.dependencies import get_foim_question_repo
from mainContext.infrastructure.adapters.FoimQuestionRepo import FoimQuestionRepoImpl

from api.v1.schemas.foim_question import FoimQuestionSchema, FoimQuestionCreateSchema, FoimQuestionUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

FoimQuestionRouter = APIRouter(prefix="/foim-questions", tags=["FOIM Questions"])


@FoimQuestionRouter.post("/create", response_model=ResponseIntModel)
def create_foim_question(dto: FoimQuestionCreateSchema, repo: FoimQuestionRepoImpl = Depends(get_foim_question_repo)):
    """
    Crea una nueva pregunta FOIM
    
    Campos requeridos:
    - function: Función asociada
    - question: Pregunta
    - target: Objetivo (opcional)
    """
    use_case = CreateFoimQuestion(repo)
    foim_question_id = use_case.execute(FoimQuestionCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=foim_question_id)


@FoimQuestionRouter.get("/get/{id}", response_model=FoimQuestionSchema)
def get_foim_question_by_id(id: int, repo: FoimQuestionRepoImpl = Depends(get_foim_question_repo)):
    """
    Obtiene una pregunta FOIM por su ID
    """
    use_case = GetFoimQuestionById(repo)
    foim_question = use_case.execute(id)
    if not foim_question:
        raise HTTPException(status_code=404, detail="FOIM Question not found")
    return foim_question


@FoimQuestionRouter.get("/get_all", response_model=List[FoimQuestionSchema])
def get_all_foim_questions(repo: FoimQuestionRepoImpl = Depends(get_foim_question_repo)):
    """
    Obtiene todas las preguntas FOIM
    """
    use_case = GetAllFoimQuestions(repo)
    return use_case.execute()


@FoimQuestionRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_foim_question(id: int, dto: FoimQuestionUpdateSchema, repo: FoimQuestionRepoImpl = Depends(get_foim_question_repo)):
    """
    Actualiza los datos de una pregunta FOIM
    
    Campos actualizables:
    - function: Función asociada
    - question: Pregunta
    - target: Objetivo
    """
    use_case = UpdateFoimQuestion(repo)
    updated = use_case.execute(id, FoimQuestionUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOIM Question not found")
    return ResponseBoolModel(result=updated)


@FoimQuestionRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_foim_question(id: int, repo: FoimQuestionRepoImpl = Depends(get_foim_question_repo)):
    """
    Elimina una pregunta FOIM
    """
    use_case = DeleteFoimQuestion(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FOIM Question not found")
    return ResponseBoolModel(result=deleted)

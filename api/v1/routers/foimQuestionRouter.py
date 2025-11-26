from fastapi import APIRouter, Depends, HTTPException
from shared.db import get_db
from sqlalchemy.orm import Session
from typing import List

from mainContext.application.dtos.foim_question_dto import FoimQuestionCreateDTO, FoimQuestionUpdateDTO
from mainContext.application.use_cases.foim_question_use_cases import (
    CreateFoimQuestion,
    GetFoimQuestionById,
    GetAllFoimQuestions,
    UpdateFoimQuestion,
    DeleteFoimQuestion
)
from mainContext.infrastructure.adapters.FoimQuestionRepo import FoimQuestionRepoImpl

from api.v1.schemas.foim_question import FoimQuestionSchema, FoimQuestionCreateSchema, FoimQuestionUpdateSchema
from api.v1.schemas.responses import ResponseBoolModel, ResponseIntModel

FoimQuestionRouter = APIRouter(prefix="/foim-questions", tags=["FOIM Questions"])


@FoimQuestionRouter.post("/create", response_model=ResponseIntModel)
def create_foim_question(dto: FoimQuestionCreateSchema, db: Session = Depends(get_db)):
    """
    Crea una nueva pregunta FOIM
    
    Campos requeridos:
    - function: Función asociada
    - question: Pregunta
    - target: Objetivo (opcional)
    """
    repo = FoimQuestionRepoImpl(db)
    use_case = CreateFoimQuestion(repo)
    foim_question_id = use_case.execute(FoimQuestionCreateDTO(**dto.model_dump()))
    return ResponseIntModel(result=foim_question_id)


@FoimQuestionRouter.get("/get/{id}", response_model=FoimQuestionSchema)
def get_foim_question_by_id(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una pregunta FOIM por su ID
    """
    repo = FoimQuestionRepoImpl(db)
    use_case = GetFoimQuestionById(repo)
    foim_question = use_case.execute(id)
    if not foim_question:
        raise HTTPException(status_code=404, detail="FOIM Question not found")
    return foim_question


@FoimQuestionRouter.get("/get_all", response_model=List[FoimQuestionSchema])
def get_all_foim_questions(db: Session = Depends(get_db)):
    """
    Obtiene todas las preguntas FOIM
    """
    repo = FoimQuestionRepoImpl(db)
    use_case = GetAllFoimQuestions(repo)
    return use_case.execute()


@FoimQuestionRouter.put("/update/{id}", response_model=ResponseBoolModel)
def update_foim_question(id: int, dto: FoimQuestionUpdateSchema, db: Session = Depends(get_db)):
    """
    Actualiza los datos de una pregunta FOIM
    
    Campos actualizables:
    - function: Función asociada
    - question: Pregunta
    - target: Objetivo
    """
    repo = FoimQuestionRepoImpl(db)
    use_case = UpdateFoimQuestion(repo)
    updated = use_case.execute(id, FoimQuestionUpdateDTO(**dto.model_dump(exclude_none=True)))
    if not updated:
        raise HTTPException(status_code=404, detail="FOIM Question not found")
    return ResponseBoolModel(result=updated)


@FoimQuestionRouter.delete("/delete/{id}", response_model=ResponseBoolModel)
def delete_foim_question(id: int, db: Session = Depends(get_db)):
    """
    Elimina una pregunta FOIM
    """
    repo = FoimQuestionRepoImpl(db)
    use_case = DeleteFoimQuestion(repo)
    deleted = use_case.execute(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FOIM Question not found")
    return ResponseBoolModel(result=deleted)

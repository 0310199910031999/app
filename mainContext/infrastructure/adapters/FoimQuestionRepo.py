from mainContext.application.ports.FoimQuestionRepo import FoimQuestionRepo
from mainContext.application.dtos.foim_question_dto import FoimQuestionDTO, FoimQuestionCreateDTO, FoimQuestionUpdateDTO
from mainContext.infrastructure.models import FoimQuestions as FoimQuestionModel
from typing import List, Optional
from sqlalchemy.orm import Session

class FoimQuestionRepoImpl(FoimQuestionRepo):
    def __init__(self, db: Session):
        self.db = db

    def create_foim_question(self, dto: FoimQuestionCreateDTO) -> int:
        try:
            model = FoimQuestionModel(
                function=dto.function,
                question=dto.question,
                target=dto.target
            )
            
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            
            if not model.id or model.id <= 0:
                raise Exception("Error al registrar pregunta FOIM en la base de datos")
            
            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear pregunta FOIM: {str(e)}")

    def get_foim_question_by_id(self, id: int) -> Optional[FoimQuestionDTO]:
        try:
            model = self.db.query(FoimQuestionModel).filter_by(id=id).first()
            
            if not model:
                return None
            
            return FoimQuestionDTO(
                id=model.id,
                function=model.function,
                question=model.question,
                target=model.target
            )
        except Exception as e:
            raise Exception(f"Error al obtener pregunta FOIM: {str(e)}")

    def get_all_foim_questions(self) -> List[FoimQuestionDTO]:
        try:
            models = self.db.query(FoimQuestionModel).all()
            
            return [
                FoimQuestionDTO(
                    id=model.id,
                    function=model.function,
                    question=model.question,
                    target=model.target
                )
                for model in models
            ]
        except Exception as e:
            raise Exception(f"Error al obtener preguntas FOIM: {str(e)}")

    def update_foim_question(self, id: int, dto: FoimQuestionUpdateDTO) -> bool:
        try:
            model = self.db.query(FoimQuestionModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.function is not None:
                model.function = dto.function
            if dto.question is not None:
                model.question = dto.question
            if dto.target is not None:
                model.target = dto.target

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar pregunta FOIM: {str(e)}")

    def delete_foim_question(self, id: int) -> bool:
        try:
            model = self.db.query(FoimQuestionModel).filter_by(id=id).first()
            if not model:
                return False

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar pregunta FOIM: {str(e)}")

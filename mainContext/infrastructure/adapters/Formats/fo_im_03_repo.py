from mainContext.domain.models.Formats.fo_im_03 import FOIM03

from mainContext.application.ports.Formats.fo_im_03_repo import FOIM03Repo

from mainContext.application.dtos.Formats.fo_im_03_dto import FOIM03CreateDTO, FOIM03ChangeStatusDTO, FOIM03TableRowDTO

from mainContext.infrastructure.models import Foim03Answers as FOIM03AnswerModel, Foim03 as FOIM03Model, Equipment as EquipmentModel

from typing import List
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError

class FOIM03RepoImpl(FOIM03Repo):
    def __init__(self, db: Session):
        self.db = db
    
    
    def create_foim03(self, dto: FOIM03CreateDTO) -> int:
        try: 
            client_id = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first().client_id

            model = FOIM03Model(
                employee_id=dto.employee_id,
                app_user_id=dto.app_user_id,
                equipment_id=dto.equipment_id,
                client_id = client_id,
                date_created=dto.date_created,
                status=dto.status
            )
            self.db.add(model)
            self.db.flush()  # ensure model.id is available before inserting answers

            if dto.foim03_answers:
                for answer in dto.foim03_answers:
                    answer_model = FOIM03AnswerModel(
                        foim_question_id=answer.foim_question_id,
                        foim03_id=model.id,
                        answer=answer.answer,
                        description=answer.description,
                        status=answer.status or "Nuevo",
                    )
                    self.db.add(answer_model)

            self.db.commit()
            self.db.refresh(model)

            if not model.id or model.id <= 0:
                raise Exception("Error al registrar FO-IM-03 en la base de datos")
            return model.id
        except Exception as e: 
            self.db.rollback()
            raise Exception(f"Error al registrar FO-IM-03 en la base de datos: {str(e)}") 
    
    
    def get_foim03_by_id(self, id: int) -> FOIM03:
        model = self.db.query(FOIM03Model).filter_by(id=id).first()
        return FOIM03(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                app_user= model.app_user,
                client = model.client,
                date_created = model.date_created,
                status = model.status,
                answers = model.foim03_answers,
            )if model else None
    

    def delete_foim03(self, id: int) -> bool:
        model = self.db.query(FOIM03Model).filter_by(id=id).first()
        if not model:
            return False
        answers = self.db.query(FOIM03AnswerModel).filter_by(foim03_id=id).all()
        for answer in answers:
            self.db.delete(answer)
        self.db.delete(model)
        self.db.commit()
        return True
    
        
    def get_list_foim03_by_equipment_id(self, equipment_id: int) -> List[FOIM03]:
        models = self.db.query(FOIM03Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOIM03(
                id = model.id,
                app_user = model.app_user,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                status = model.status,
                date_created = model.date_created,
                answers= model.foim03_answers
            ) 
            for model in models
        ]
    
    def get_list_foim03_table(self, equipment_id: int) -> List[FOIM03TableRowDTO]:
        models = self.db.query(FOIM03Model).filter_by(equipment_id=equipment_id).order_by(desc(FOIM03Model.id)).all()
        
        if not models:
            return []
        
        result = []
        for m in models:
            
            employee_name = 'N/A'
            if m.employee:
                name = m.employee.name or ''  
                lastname = m.employee.lastname or '' 
                employee_name = f"{name} {lastname}".strip()
                if not employee_name: 
                    employee_name = 'N/A'
            app_user_name = 'N/A'
            if m.app_user:
                name = m.app_user.name or ''
                lastname = m.app_user.lastname or ''
                app_user_name = f"{name} {lastname}".strip()
                if not app_user_name:
                    app_user_name = 'N/A'
                    
            result.append(
                FOIM03TableRowDTO(
                    id=m.id,
                    date_created=m.date_created.date() if m.date_created else None,
                    employee_name=employee_name,
                    app_user_name=app_user_name,
                    status=m.status
                )
            )
            
        return result
    
    
    def change_status_foim03(self, id: int, dto: FOIM03ChangeStatusDTO) -> bool:
        try:
            model = self.db.query(FOIM03Model).filter_by(id=id).first()
            if not model:
                return None
            model.status = "Cerrado"

            existing_answers = model.foim03_answers or []
            incoming_answers = dto.foim03_answers or []

            for i, incoming in enumerate(incoming_answers):
                if i < len(existing_answers):
                    existing = existing_answers[i]
                    existing.status = incoming.status

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e: 
            self.db.rollback()
            return False
            




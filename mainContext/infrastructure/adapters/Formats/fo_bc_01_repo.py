from typing import List, Optional
from datetime import date, datetime
import base64
import glob
import os

from sqlalchemy import desc
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, joinedload, selectinload

from mainContext.application.dtos.Formats.fo_bc_01_dto import (
    FOBC01BatteryCellDTO,
    FOBC01CreateDTO,
    FOBC01QuestionCreateDTO,
    FOBC01QuestionDTO,
    FOBC01QuestionUpdateDTO,
    FOBC01SignatureDTO,
    FOBC01TableRowDTO,
    FOBC01UpdateDTO,
)
from mainContext.application.ports.Formats.fo_bc_01_repo import FOBC01Repo
from mainContext.application.services.file_generator import FileService
from mainContext.domain.models.Formats.fo_bc_01 import FOBC01
from mainContext.infrastructure.adapters.Formats.file_cleanup_helper import cleanup_file_if_orphaned
from mainContext.infrastructure.models import (
    Equipment as EquipmentModel,
    Fobc01 as FOBC01Model,
    Fobc01Answers as FOBC01AnswerModel,
    Fobc01BatteryCells as FOBC01BatteryCellModel,
    Fobc01Questions as FOBC01QuestionModel,
)

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_CONTEXT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(CURRENT_FILE_DIR)))

SIGNATURE_SAVE_DIR = os.path.join(MAIN_CONTEXT_ROOT, "static", "img", "signatures", "fo-bc-01")
SIGNATURE_URL_BASE = "/static/img/signatures/fo-bc-01"
os.makedirs(SIGNATURE_SAVE_DIR, exist_ok=True)


def build_fobc01_initial_model(*, employee_id: int, equipment_id: int, client_id: int, file_id: Optional[str], date_created, status: str) -> FOBC01Model:
    return FOBC01Model(
        employee_id=employee_id,
        equipment_id=equipment_id,
        client_id=client_id,
        file_id=file_id,
        date_created=date_created,
        status=status,
        hourometer=0.0,
        observations="",
        reception_name="",
        signature_path="",
        date_signed=None,
        doh=0.0,
        rating=0,
        rating_comment="",
        battery="",
        cells_x=None,
        cells_y=None,
    )

class FOBC01RepoImpl(FOBC01Repo):
    def __init__(self, db: Session):
        self.db = db

    def _delete_existing_signature(self, model_id: int) -> None:
        try:
            search_pattern = os.path.join(SIGNATURE_SAVE_DIR, f"fobc-{model_id}.*")
            for file_path in glob.glob(search_pattern):
                os.remove(file_path)
        except Exception as e:
            print(f"Error al eliminar firma anterior para ID {model_id}: {e}")
            raise

    def _save_signature_base64(self, base64_string: str, model_id: int) -> str | None:
        try:
            try:
                header, data = base64_string.split(",", 1)
            except ValueError:
                header = ""
                data = base64_string

            image_data = base64.b64decode(data)

            file_ext = ".png"
            if "image/jpeg" in header:
                file_ext = ".jpeg"
            elif "image/jpg" in header:
                file_ext = ".jpg"

            filename = f"fobc-{model_id}{file_ext}"
            save_path = os.path.join(SIGNATURE_SAVE_DIR, filename)

            with open(save_path, "wb") as file_handle:
                file_handle.write(image_data)

            return f"{SIGNATURE_URL_BASE}/{filename}"
        except Exception as e:
            print(f"Error al guardar firma Base64 de FOBC01: {e}")
            return None

    def _sync_answers(self, model: FOBC01Model, incoming_answers) -> None:
        if incoming_answers is None:
            return

        existing_by_question_id = {
            answer.question_id: answer
            for answer in model.fobc01_answers
            if answer.question_id is not None
        }
        incoming_question_ids: set[int] = set()

        for incoming in incoming_answers:
            incoming_question_ids.add(incoming.question_id)
            existing = existing_by_question_id.get(incoming.question_id)
            if existing:
                existing.answer = incoming.answer
                continue

            self.db.add(
                FOBC01AnswerModel(
                    fobc01_id=model.id,
                    question_id=incoming.question_id,
                    answer=incoming.answer,
                )
            )

        for answer in list(model.fobc01_answers):
            if answer.question_id not in incoming_question_ids:
                self.db.delete(answer)

    def _sync_battery_cells(self, model: FOBC01Model, incoming_cells: Optional[List[FOBC01BatteryCellDTO]]) -> None:
        if incoming_cells is None:
            return

        existing_by_cell_number = {
            cell.cell_number: cell
            for cell in model.fobc01_battery_cells
            if cell.cell_number is not None
        }
        incoming_cell_numbers: set[int] = set()

        for incoming in sorted(incoming_cells, key=lambda item: item.cell_number):
            incoming_cell_numbers.add(incoming.cell_number)
            existing = existing_by_cell_number.get(incoming.cell_number)
            if existing:
                existing.voltage = incoming.voltage
                existing.density = incoming.density
                existing.status = incoming.status
                continue

            self.db.add(
                FOBC01BatteryCellModel(
                    fobc01_id=model.id,
                    cell_number=incoming.cell_number,
                    voltage=incoming.voltage,
                    density=incoming.density,
                    status=incoming.status,
                )
            )

        for cell in list(model.fobc01_battery_cells):
            if cell.cell_number not in incoming_cell_numbers:
                self.db.delete(cell)
    
    def create_fobc01(self, dto: FOBC01CreateDTO) -> int:
        try:
            equipment = self.db.query(EquipmentModel).filter_by(id=dto.equipment_id).first()
            if not equipment:
                raise Exception("El equipo asociado a FO-BC-01 no existe")

            client_id = equipment.client_id

            file_model = FileService.create_file(self.db, client_id)

            model = build_fobc01_initial_model(
                employee_id=dto.employee_id,
                equipment_id=dto.equipment_id,
                client_id=client_id,
                file_id=file_model.id,
                date_created=date.today(),
                status="Abierto",
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)
            if model.id is None:
                raise Exception("Error al registrar FO-BC-01 en la base de datos")
            return model.id
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f"Error al registrar FO-BC-01 en la base de datos: {str(e)}")

    def get_fobc01_by_id(self, id: int) -> FOBC01:
        model = (
            self.db.query(FOBC01Model)
            .options(
                joinedload(FOBC01Model.employee),
                joinedload(FOBC01Model.equipment).joinedload(EquipmentModel.brand),
                joinedload(FOBC01Model.equipment).joinedload(EquipmentModel.type),
                joinedload(FOBC01Model.client),
                joinedload(FOBC01Model.file),
                selectinload(FOBC01Model.fobc01_answers).joinedload(FOBC01AnswerModel.fobc01_question),
                selectinload(FOBC01Model.fobc01_battery_cells),
            )
            .filter_by(id=id)
            .first()
        )

        sorted_answers = (
            sorted(model.fobc01_answers, key=lambda answer: ((answer.question_id or 0), answer.id))
            if model else None
        )
        sorted_battery_cells = (
            sorted(model.fobc01_battery_cells, key=lambda cell: ((cell.cell_number or 0), cell.id))
            if model else None
        )

        return FOBC01(
            id = model.id,
            employee = model.employee,
            equipment = model.equipment,
            client = model.client,
            file=model.file,
            date_created = model.date_created,
            hourometer = model.hourometer,
            observations = model.observations,
            status = model.status,
            reception_name =model.reception_name,
            signature_path = model.signature_path,
            date_signed = model.date_signed,
            doh = model.doh,
            rating = model.rating,
            rating_comment = model.rating_comment,
            battery = model.battery,
            cells_x = model.cells_x,
            cells_y = model.cells_y,
            answers = sorted_answers,
            battery_cells = sorted_battery_cells,
        ) if model else None

    def delete_fobc01(self, id: int) -> bool:
        model = self.db.query(FOBC01Model).filter_by(id=id).first()
        if not model:
            return False
        
        file_id = model.file_id
        self.db.delete(model)
        self.db.flush()
        
        # Eliminar file solo si no hay otros documentos relacionados
        cleanup_file_if_orphaned(self.db, file_id)
        
        self.db.commit()
        return True

    def update_fobc01(self, fobc01_id: int, dto: FOBC01UpdateDTO) -> bool:
        try:
            model = (
                self.db.query(FOBC01Model)
                .options(
                    selectinload(FOBC01Model.fobc01_answers),
                    selectinload(FOBC01Model.fobc01_battery_cells),
                )
                .filter_by(id=fobc01_id)
                .first()
            )
            if not model:
                return False

            model.hourometer = dto.hourometer
            model.observations = dto.observations
            model.reception_name = dto.reception_name
            model.employee_id = dto.employee_id

            if dto.battery is not None:
                model.battery = dto.battery
            if dto.cells_x is not None:
                model.cells_x = dto.cells_x
            if dto.cells_y is not None:
                model.cells_y = dto.cells_y

            self._sync_answers(model, dto.fobc01_answers)
            self._sync_battery_cells(model, dto.fobc01_battery_cells)

            self.db.commit()
            self.db.refresh(model)
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False

    def get_list_fobc01_by_equipment_id(self, equipment_id: int) -> List[FOBC01]:
        models = self.db.query(FOBC01Model).filter_by(equipment_id=equipment_id).all()
        return [
            FOBC01(
                id = model.id,
                employee = model.employee,
                equipment = model.equipment,
                client = model.client,
                file = model.file,
                date_created = model.date_created,
                hourometer = model.hourometer,
                observations = model.observations,
                status = model.status,
                reception_name = model.reception_name,
                signature_path = model.signature_path,
                date_signed = model.date_signed,
                doh = model.doh,
                rating = model.rating,
                rating_comment = model.rating_comment,
                battery = model.battery,
                cells_x = model.cells_x,
                cells_y = model.cells_y,
                answers = None,
                battery_cells = None,
            )
            for model in models
        ]

    def get_list_fobc01_table(self, equipment_id: int) -> List[FOBC01TableRowDTO]:
        models = self.db.query(FOBC01Model).filter_by(equipment_id=equipment_id).order_by(desc(FOBC01Model.id)).all()
        
        if not models:
            return []
        
        def get_full_name(model_rel):
            if model_rel:
                full_name = f"{model_rel.name or ''} {model_rel.lastname or ''}".strip()
                return full_name if full_name else 'N/A'
            return 'N/A'
        
        return [
            FOBC01TableRowDTO(
                id=m.id,
                file_id=m.file.folio if m.file else None, 
                date_created=m.date_created,
                observations = m.observations,
                employee_name=get_full_name(m.employee),
                status=m.status,
                rating=m.rating,
                rating_comment=m.rating_comment,
            )
            for m in models
        ]

    def sign_fobc01(self, id: int, dto: FOBC01SignatureDTO) -> bool:
        try:
            model = self.db.query(FOBC01Model).filter_by(id=id).first()
            if not model:
                return False

            if dto.signature_base64:
                self._delete_existing_signature(model.id)
                signature_url = self._save_signature_base64(dto.signature_base64, model.id)
                if not signature_url:
                    raise Exception(f"Fallo crítico al guardar la firma para el ID {model.id}")
                model.signature_path = signature_url

            model.status = dto.status
            model.date_signed = datetime.now()
            model.rating = dto.rating
            model.rating_comment = dto.rating_comment
            model.employee_id = dto.employee_id

            self.db.commit()
            self.db.refresh(model)
            
            # Verificar y cerrar file si todos los documentos están cerrados
            if model.file_id and dto.status == "Cerrado":
                from mainContext.application.services.file_generator import FileService
                try:
                    FileService.check_and_close_file(self.db, model.file_id)
                except Exception as e:
                    print(f"[FOBC01] Advertencia: No se pudo verificar el file: {str(e)}")
            
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            return False

    def create_fobc01_question(self, dto: FOBC01QuestionCreateDTO) -> int:
        try:
            model = FOBC01QuestionModel(
                description=dto.description,
                type=dto.type,
            )
            self.db.add(model)
            self.db.commit()
            self.db.refresh(model)

            if not model.id or model.id <= 0:
                raise Exception("Error al registrar pregunta FOBC01 en la base de datos")

            return model.id
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al crear pregunta FOBC01: {str(e)}")

    def get_fobc01_question_by_id(self, id: int) -> Optional[FOBC01QuestionDTO]:
        model = self.db.query(FOBC01QuestionModel).filter_by(id=id).first()
        if not model:
            return None

        return FOBC01QuestionDTO(
            id=model.id,
            description=model.description,
            type=model.type,
        )

    def get_all_fobc01_questions(self) -> List[FOBC01QuestionDTO]:
        models = self.db.query(FOBC01QuestionModel).order_by(FOBC01QuestionModel.id).all()
        return [
            FOBC01QuestionDTO(
                id=model.id,
                description=model.description,
                type=model.type,
            )
            for model in models
        ]

    def update_fobc01_question(self, id: int, dto: FOBC01QuestionUpdateDTO) -> bool:
        try:
            model = self.db.query(FOBC01QuestionModel).filter_by(id=id).first()
            if not model:
                return False

            if dto.description is not None:
                model.description = dto.description
            if dto.type is not None:
                model.type = dto.type

            self.db.commit()
            self.db.refresh(model)
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al actualizar pregunta FOBC01: {str(e)}")

    def delete_fobc01_question(self, id: int) -> bool:
        try:
            model = self.db.query(FOBC01QuestionModel).filter_by(id=id).first()
            if not model:
                return False

            answers = self.db.query(FOBC01AnswerModel).filter_by(question_id=id).all()
            for answer in answers:
                self.db.delete(answer)

            self.db.delete(model)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al eliminar pregunta FOBC01: {str(e)}")
            



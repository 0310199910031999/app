import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from mainContext.application.dtos.export_dto import ExportDocumentRowDTO, ExportJobDTO
from mainContext.infrastructure.models import (
    AppUsers,
    Equipment,
    Focr02,
    Foem01,
    Foim01,
    Foim03,
    Fole01,
    Foos01,
    Fopc02,
    Fopp02,
    Fosc01,
    Fosp01,
)


class ExportDocumentCollectorRepoImpl:
    FORMAT_LABELS = {
        'fo_cr_02': 'FO-CR-02',
        'fo_em_01': 'FO-EM-01',
        'fo_im_01': 'FO-IM-01',
        'fo_im_03': 'FO-IM-03',
        'fo_le_01': 'FO-LE-01',
        'fo_os_01': 'FO-OS-01',
        'fo_pc_02': 'FO-PC-02',
        'fo_pp_02': 'FO-PP-02',
        'fo_sc_01': 'FO-SC-01',
        'fo_sp_01': 'FO-SP-01',
    }
    FORMAT_NAMES = {
        'fo_cr_02': 'Carta Responsiva Entrega de Equipo',
        'fo_em_01': 'Entrega de Materiales',
        'fo_im_01': 'Inspeccion de Montacargas',
        'fo_im_03': 'Inspeccion de Montacargas',
        'fo_le_01': 'Orden de Levantamiento',
        'fo_os_01': 'Otros Servicios',
        'fo_pc_02': 'Propiedad del Cliente',
        'fo_pp_02': 'Identificacion Propiedad Cliente a Proveedor',
        'fo_sc_01': 'Servicio Correctivo',
        'fo_sp_01': 'Servicio Preventivo',
    }

    def __init__(self, db: Session):
        self.db = db

    def collect_documents(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        documents: List[ExportDocumentRowDTO] = []
        filters = job.format_filters or {}

        if filters.get('fo_cr_02'):
            documents.extend(self._collect_focr02(job))
        if filters.get('fo_em_01'):
            documents.extend(self._collect_foem01(job))
        if filters.get('fo_im_01'):
            documents.extend(self._collect_foim01(job))
        if filters.get('fo_im_03'):
            documents.extend(self._collect_foim03(job))
        if filters.get('fo_le_01'):
            documents.extend(self._collect_fole01(job))
        if filters.get('fo_os_01'):
            documents.extend(self._collect_foos01(job))
        if filters.get('fo_pc_02'):
            documents.extend(self._collect_fopc02(job))
        if filters.get('fo_pp_02'):
            documents.extend(self._collect_fopp02(job))
        if filters.get('fo_sc_01'):
            documents.extend(self._collect_fosc01(job))
        if filters.get('fo_sp_01'):
            documents.extend(self._collect_fosp01(job))

        return sorted(documents, key=lambda item: (item.date_created, item.format_key, item.document_id))

    def _date_only(self, value) -> datetime.date:
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        return datetime.date.today()

    def _full_name(self, person) -> str:
        if not person:
            return ''
        full_name = f"{person.name or ''} {person.lastname or ''}".strip()
        return full_name

    def _aggregate(self, values) -> str:
        result = []
        seen = set()
        for value in values:
            if not value:
                continue
            text_value = str(value).strip()
            if not text_value or text_value in seen:
                continue
            seen.add(text_value)
            result.append(text_value)
        return ', '.join(result)

    def _closed_status_filter(self, column):
        return func.upper(func.coalesce(column, '')) == 'CERRADO'

    def _equipment_name(self, equipment, fallback_id: int) -> str:
        if not equipment:
            return f'Equipo {fallback_id}'

        economic_number = str(equipment.economic_number).strip() if equipment.economic_number else ''
        brand_name = equipment.brand.name.strip() if equipment.brand and equipment.brand.name else ''
        model_name = equipment.model.strip() if equipment.model else ''

        descriptive_name = ' '.join(part for part in [brand_name, model_name] if part).strip()
        if economic_number and descriptive_name:
            return f'{economic_number} - {descriptive_name}'
        if economic_number:
            return economic_number
        if descriptive_name:
            return descriptive_name
        return f'Equipo {fallback_id}'

    def _format_folder_name(self, format_key: str) -> str:
        return f"{self.FORMAT_LABELS[format_key]} {self.FORMAT_NAMES[format_key]}"

    def _filename(self, document_date: datetime.date, format_label: str, format_name: str, document_id: int) -> str:
        return f"{document_date.strftime('%d-%m-%Y')} {format_label} {format_name} {document_id}.pdf"

    def _build_row(
        self,
        *,
        format_key: str,
        document_id: int,
        equipment_id: int,
        client_id: int,
        document_date: datetime.date,
        equipment_name: str,
        services: str,
        technician: str,
        reception_name: str,
        defects: str,
    ) -> ExportDocumentRowDTO:
        format_label = self.FORMAT_LABELS[format_key]
        format_name = self.FORMAT_NAMES[format_key]
        return ExportDocumentRowDTO(
            format_key=format_key,
            format_label=format_label,
            format_name=format_name,
            format_folder_name=self._format_folder_name(format_key),
            document_id=document_id,
            equipment_id=equipment_id,
            client_id=client_id,
            date_created=document_date,
            folder_equipment_name=equipment_name,
            filename=self._filename(document_date, format_label, format_name, document_id),
            excel_row={
                'ID': document_id,
                'Equipo': equipment_name,
                'Fecha': document_date.strftime('%d/%m/%Y'),
                'Tipo de servicio / Nombre de Formato': f'{format_label} {format_name}',
                'Servicios realizados': services,
                'Técnico / Empleado': technician,
                'Nombre de Recepción del Servicio': reception_name,
                'Desperfectos': defects,
            },
        )

    def _collect_focr02(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Focr02)
            .options(
                joinedload(Focr02.employee),
                joinedload(Focr02.equipment).joinedload(Equipment.brand),
            )
            .filter(
                Focr02.client_id == job.client_id,
                Focr02.equipment_id == job.equipment_id,
                self._closed_status_filter(Focr02.status),
                func.date(Focr02.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            document_date = self._date_only(model.date_created)
            reception_name = ' / '.join(
                value for value in [model.reception_name, model.return_reception_name] if value
            )
            documents.append(
                self._build_row(
                    format_key='fo_cr_02',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=document_date,
                    equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                    services='',
                    technician=self._full_name(model.employee),
                    reception_name=reception_name,
                    defects='',
                )
            )
        return documents

    def _collect_foem01(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Foem01)
            .options(
                joinedload(Foem01.employee),
                joinedload(Foem01.equipment).joinedload(Equipment.brand),
                joinedload(Foem01.foem01_materials),
            )
            .filter(
                Foem01.client_id == job.client_id,
                Foem01.equipment_id == job.equipment_id,
                self._closed_status_filter(Foem01.status),
                func.date(Foem01.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        return [
            self._build_row(
                format_key='fo_em_01',
                document_id=model.id,
                equipment_id=model.equipment_id or job.equipment_id,
                client_id=model.client_id or job.client_id,
                document_date=self._date_only(model.date_created),
                equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                services=self._aggregate(material.description for material in model.foem01_materials),
                technician=self._full_name(model.employee),
                reception_name=model.reception_name or '',
                defects='',
            )
            for model in models
        ]

    def _collect_foim01(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Foim01)
            .options(
                joinedload(Foim01.employee),
                joinedload(Foim01.equipment).joinedload(Equipment.brand),
                joinedload(Foim01.foim01_answers),
            )
            .filter(
                Foim01.client_id == job.client_id,
                Foim01.equipment_id == job.equipment_id,
                self._closed_status_filter(Foim01.status),
                func.date(Foim01.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        return [
            self._build_row(
                format_key='fo_im_01',
                document_id=model.id,
                equipment_id=model.equipment_id or job.equipment_id,
                client_id=model.client_id or job.client_id,
                document_date=self._date_only(model.date_created),
                equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                services='',
                technician=self._full_name(model.employee),
                reception_name=model.reception_name or '',
                defects=self._aggregate(answer.description for answer in model.foim01_answers),
            )
            for model in models
        ]

    def _collect_foim03(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Foim03)
            .options(
                joinedload(Foim03.employee),
                joinedload(Foim03.app_user),
                joinedload(Foim03.equipment).joinedload(Equipment.brand),
                joinedload(Foim03.foim03_answers),
            )
            .filter(
                Foim03.client_id == job.client_id,
                Foim03.equipment_id == job.equipment_id,
                self._closed_status_filter(Foim03.status),
                func.date(Foim03.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            technician = self._full_name(model.employee)
            if not technician:
                technician = self._full_name(model.app_user)

            documents.append(
                self._build_row(
                    format_key='fo_im_03',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=self._date_only(model.date_created),
                    equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                    services='',
                    technician=technician,
                    reception_name='',
                    defects=self._aggregate(answer.description for answer in model.foim03_answers),
                )
            )
        return documents

    def _collect_fole01(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Fole01)
            .options(
                joinedload(Fole01.employee),
                joinedload(Fole01.equipment).joinedload(Equipment.brand),
                joinedload(Fole01.fole01_services),
            )
            .filter(
                Fole01.client_id == job.client_id,
                Fole01.equipment_id == job.equipment_id,
                self._closed_status_filter(Fole01.status),
                func.date(Fole01.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            services = self._aggregate(
                (service.service.code if service.service and service.service.code else None)
                or (service.service.name if service.service else None)
                or service.description_service
                for service in model.fole01_services
            )
            documents.append(
                self._build_row(
                    format_key='fo_le_01',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=self._date_only(model.date_created),
                    equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                    services=services,
                    technician=self._full_name(model.employee),
                    reception_name=model.reception_name or '',
                    defects='',
                )
            )
        return documents

    def _collect_foos01(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Foos01)
            .options(
                joinedload(Foos01.employee),
                joinedload(Foos01.equipment).joinedload(Equipment.brand),
                joinedload(Foos01.foos01_services),
            )
            .filter(
                Foos01.client_id == job.client_id,
                Foos01.equipment_id == job.equipment_id,
                self._closed_status_filter(Foos01.status),
                func.date(Foos01.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            services = self._aggregate(
                service.service_description
                or (service.service.code if service.service and service.service.code else None)
                or (service.service.name if service.service else None)
                for service in model.foos01_services
            )
            documents.append(
                self._build_row(
                    format_key='fo_os_01',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=self._date_only(model.date_created),
                    equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                    services=services,
                    technician=self._full_name(model.employee),
                    reception_name=model.reception_name or '',
                    defects='',
                )
            )
        return documents

    def _collect_fopc02(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Fopc02)
            .options(
                joinedload(Fopc02.employee),
                joinedload(Fopc02.equipment).joinedload(Equipment.brand),
                joinedload(Fopc02.property),
            )
            .filter(
                Fopc02.client_id == job.client_id,
                Fopc02.equipment_id == job.equipment_id,
                self._closed_status_filter(Fopc02.status),
                func.date(func.coalesce(Fopc02.departure_date, Fopc02.date_created)).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            equipment_name = self._equipment_name(model.equipment, job.equipment_id)
            if not equipment_name and model.property:
                equipment_name = model.property.property or f'Equipo {job.equipment_id}'

            document_date = self._date_only(model.departure_date or model.date_created)
            documents.append(
                self._build_row(
                    format_key='fo_pc_02',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=document_date,
                    equipment_name=equipment_name,
                    services='',
                    technician=self._full_name(model.employee),
                    reception_name=model.name_recipient or '',
                    defects='',
                )
            )
        return documents

    def _collect_fopp02(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Fopp02)
            .join(Fopc02, Fopp02.fopc_id == Fopc02.id)
            .options(
                joinedload(Fopp02.employee),
                joinedload(Fopp02.property),
                joinedload(Fopp02.fopc).joinedload(Fopc02.equipment).joinedload(Equipment.brand),
            )
            .filter(
                Fopc02.client_id == job.client_id,
                Fopc02.equipment_id == job.equipment_id,
                self._closed_status_filter(Fopp02.status),
                func.date(func.coalesce(Fopp02.departure_date, Fopp02.date_created)).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            linked_equipment = model.fopc.equipment if model.fopc else None
            equipment_name = self._equipment_name(linked_equipment, job.equipment_id)
            if not equipment_name and model.property:
                equipment_name = model.property.property or f'Equipo {job.equipment_id}'

            documents.append(
                self._build_row(
                    format_key='fo_pp_02',
                    document_id=model.id,
                    equipment_id=job.equipment_id,
                    client_id=job.client_id,
                    document_date=self._date_only(model.departure_date or model.date_created),
                    equipment_name=equipment_name,
                    services='',
                    technician=self._full_name(model.employee),
                    reception_name=model.name_delivery or '',
                    defects='',
                )
            )
        return documents

    def _collect_fosc01(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Fosc01)
            .options(
                joinedload(Fosc01.employee),
                joinedload(Fosc01.equipment).joinedload(Equipment.brand),
                joinedload(Fosc01.fosc01_services),
            )
            .filter(
                Fosc01.client_id == job.client_id,
                Fosc01.equipment_id == job.equipment_id,
                self._closed_status_filter(Fosc01.status),
                func.date(Fosc01.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            services = self._aggregate(
                service.service_description
                or (service.service.code if service.service and service.service.code else None)
                or (service.service.name if service.service else None)
                for service in model.fosc01_services
            )
            documents.append(
                self._build_row(
                    format_key='fo_sc_01',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=self._date_only(model.date_created),
                    equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                    services=services,
                    technician=self._full_name(model.employee),
                    reception_name=model.reception_name or '',
                    defects='',
                )
            )
        return documents

    def _collect_fosp01(self, job: ExportJobDTO) -> List[ExportDocumentRowDTO]:
        models = (
            self.db.query(Fosp01)
            .options(
                joinedload(Fosp01.employee),
                joinedload(Fosp01.equipment).joinedload(Equipment.brand),
                joinedload(Fosp01.fosp01_services),
            )
            .filter(
                Fosp01.client_id == job.client_id,
                Fosp01.equipment_id == job.equipment_id,
                self._closed_status_filter(Fosp01.status),
                func.date(Fosp01.date_created).between(job.start_date, job.end_date),
            )
            .all()
        )

        documents = []
        for model in models:
            services = self._aggregate(
                service.service_description
                or (service.service.code if service.service and service.service.code else None)
                or (service.service.name if service.service else None)
                for service in model.fosp01_services
            )
            documents.append(
                self._build_row(
                    format_key='fo_sp_01',
                    document_id=model.id,
                    equipment_id=model.equipment_id or job.equipment_id,
                    client_id=model.client_id or job.client_id,
                    document_date=self._date_only(model.date_created),
                    equipment_name=self._equipment_name(model.equipment, job.equipment_id),
                    services=services,
                    technician=self._full_name(model.employee),
                    reception_name=model.reception_name or '',
                    defects='',
                )
            )
        return documents

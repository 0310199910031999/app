from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from sqlalchemy import desc

from mainContext.application.ports.FileRepo import FileRepo
from mainContext.application.dtos.file_dto import FileTableClosedDTO, FileTableOpenDTO, FileInvoiceDTO

from mainContext.infrastructure.models import (
    Files as FileModel,
    Clients as ClientModel,
    Foos01 as FOOS01Model,
    Fosp01 as FOSP01Model,
    Fosc01 as FOSC01Model,
    Foos01Services as FOOS01ServiceModel,
    Fosp01Services as FOSP01ServiceModel,
    Fosc01Services as FOSC01ServiceModel,
    Services as ServiceModel
)


class FileRepoImpl(FileRepo):
    def __init__(self, db: Session):
        self.db = db
    
    def get_table_closed(self) -> List[FileTableClosedDTO]:
        """
        Obtiene todos los files con status 'Cerrado'
        """
        try:
            files = (
                self.db.query(FileModel)
                .filter(FileModel.status == "Cerrado")
                .options(joinedload(FileModel.client))
                .order_by(desc(FileModel.date_closed))
                .all()
            )
            
            return [
                FileTableClosedDTO(
                    folio=file.folio,
                    client_name=file.client.name if file.client else "N/A",
                    date_closed=file.date_closed,
                    date_invoiced=file.date_invoiced,
                    uuid=file.uuid or "",
                    status=file.status
                )
                for file in files
            ]
        except Exception as e:
            raise Exception(f"Error al obtener files cerrados: {str(e)}")
    
    def get_table_open(self) -> List[FileTableOpenDTO]:
        """
        Obtiene todos los files con status 'Abierto' 
        e incluye los códigos únicos de servicios de FOOS01, FOSP01, FOSC01
        """
        try:
            files = (
                self.db.query(FileModel)
                .filter(FileModel.status == "Abierto")
                .options(joinedload(FileModel.client))
                .order_by(desc(FileModel.date_created))
                .all()
            )
            
            result = []
            for file in files:
                # Obtener códigos de servicios únicos desde FOOS01
                foos01_services = (
                    self.db.query(ServiceModel.code)
                    .join(FOOS01ServiceModel, FOOS01ServiceModel.service_id == ServiceModel.id)
                    .join(FOOS01Model, FOOS01Model.id == FOOS01ServiceModel.foos01_id)
                    .filter(FOOS01Model.file_id == file.id)
                    .distinct()
                    .all()
                )
                
                # Obtener códigos de servicios únicos desde FOSP01
                fosp01_services = (
                    self.db.query(ServiceModel.code)
                    .join(FOSP01ServiceModel, FOSP01ServiceModel.service_id == ServiceModel.id)
                    .join(FOSP01Model, FOSP01Model.id == FOSP01ServiceModel.fosp01_id)
                    .filter(FOSP01Model.file_id == file.id)
                    .distinct()
                    .all()
                )
                
                # Obtener códigos de servicios únicos desde FOSC01
                fosc01_services = (
                    self.db.query(ServiceModel.code)
                    .join(FOSC01ServiceModel, FOSC01ServiceModel.service_id == ServiceModel.id)
                    .join(FOSC01Model, FOSC01Model.id == FOSC01ServiceModel.fosc01_id)
                    .filter(FOSC01Model.file_id == file.id)
                    .distinct()
                    .all()
                )
                
                # Combinar todos los códigos y eliminar duplicados
                all_service_codes = set()
                for (code,) in foos01_services:
                    if code:
                        all_service_codes.add(code)
                for (code,) in fosp01_services:
                    if code:
                        all_service_codes.add(code)
                for (code,) in fosc01_services:
                    if code:
                        all_service_codes.add(code)
                
                result.append(
                    FileTableOpenDTO(
                        folio=file.folio,
                        client_name=file.client.name if file.client else "N/A",
                        date_created=file.date_created,
                        services=sorted(list(all_service_codes))  # Ordenar alfabéticamente
                    )
                )
            
            return result
        except Exception as e:
            raise Exception(f"Error al obtener files abiertos: {str(e)}")
    
    def invoice_file(self, file_id: str, dto: FileInvoiceDTO) -> bool:
        """
        Marca un file como facturado:
        - Actualiza uuid
        - Establece date_invoiced con fecha actual
        - Cambia status a 'Facturado'
        """
        try:
            file = self.db.query(FileModel).filter_by(id=file_id).first()
            
            if not file:
                raise Exception(f"File con ID {file_id} no encontrado")
            
            # Verificar que el file esté cerrado antes de facturar
            if file.status != "Cerrado":
                raise Exception(f"El file debe estar cerrado antes de facturarse. Estado actual: {file.status}")
            
            # Actualizar campos
            file.uuid = dto.uuid
            file.date_invoiced = datetime.now()
            file.status = "Facturado"
            
            self.db.commit()
            self.db.refresh(file)
            
            return True
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error al facturar file: {str(e)}")

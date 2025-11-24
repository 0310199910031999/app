from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from shared.db import get_db
from api.v1.schemas.file import (
    FileTableClosedSchema,
    FileTableOpenSchema,
    FileInvoiceSchema,
    FileInvoiceResponseSchema
)
from mainContext.infrastructure.adapters.FileRepo import FileRepoImpl
from mainContext.application.use_cases.file_use_cases import (
    GetTableClosed,
    GetTableOpen,
    InvoiceFile
)
from mainContext.application.dtos.file_dto import FileInvoiceDTO

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)


@router.get("/closed", response_model=List[FileTableClosedSchema])
def get_files_closed(db: Session = Depends(get_db)):
    """
    Obtiene todos los files con status 'Cerrado'
    
    Retorna:
    - folio: Folio del file
    - client_name: Nombre del cliente
    - date_closed: Fecha de cierre
    - date_invoiced: Fecha de facturación (si aplica)
    - uuid: UUID de la factura
    - status: Estado del file
    """
    try:
        repo = FileRepoImpl(db)
        use_case = GetTableClosed(repo)
        files = use_case.execute()
        
        return [
            FileTableClosedSchema(
                folio=file.folio,
                client_name=file.client_name,
                date_closed=file.date_closed,
                date_invoiced=file.date_invoiced,
                uuid=file.uuid,
                status=file.status
            )
            for file in files
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/open", response_model=List[FileTableOpenSchema])
def get_files_open(db: Session = Depends(get_db)):
    """
    Obtiene todos los files con status 'Abierto' 
    incluyendo los servicios asociados (FOOS01, FOSP01, FOSC01)
    
    Retorna:
    - folio: Folio del file
    - client_name: Nombre del cliente
    - date_created: Fecha de creación
    - services: Array de códigos de servicios únicos
    """
    try:
        repo = FileRepoImpl(db)
        use_case = GetTableOpen(repo)
        files = use_case.execute()
        
        return [
            FileTableOpenSchema(
                folio=file.folio,
                client_name=file.client_name,
                date_created=file.date_created,
                services=file.services
            )
            for file in files
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/invoice/{file_id}", response_model=FileInvoiceResponseSchema)
def invoice_file(file_id: str, invoice_data: FileInvoiceSchema, db: Session = Depends(get_db)):
    """
    Marca un file como facturado
    
    Parámetros:
    - file_id: ID del file a facturar
    - uuid: UUID de la factura
    
    Actualiza:
    - uuid: UUID proporcionado
    - date_invoiced: Fecha actual
    - status: Cambia a 'Facturado'
    
    Requisitos:
    - El file debe estar en status 'Cerrado'
    """
    try:
        dto = FileInvoiceDTO(uuid=invoice_data.uuid)
        
        repo = FileRepoImpl(db)
        use_case = InvoiceFile(repo)
        success = use_case.execute(file_id, dto)
        
        if success:
            return FileInvoiceResponseSchema(
                success=True,
                message=f"File {file_id} facturado exitosamente"
            )
        else:
            raise HTTPException(status_code=400, detail="No se pudo facturar el file")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

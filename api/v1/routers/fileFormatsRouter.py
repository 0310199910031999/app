from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from shared.db import get_db
from api.v1.schemas.file_formats import FileFormatSchema
from mainContext.infrastructure.adapters.FileFormatsRepo import FileFormatsRepoImpl
from mainContext.application.use_cases.file_formats_use_cases import GetFormatsByFile

router = APIRouter(
    prefix="/file-formats",
    tags=["File Formats"]
)


@router.get("/{file_id}", response_model=List[FileFormatSchema])
def get_formats_by_file(file_id: str, db: Session = Depends(get_db)):
    """
    Obtiene todos los formatos asociados a un file_id específico.
    
    Retorna una lista con los siguientes datos de cada formato:
    - id: ID del formato en su propia tabla
    - format: Nombre del formato (FO-SP-01, FO-SC-01, FO-OS-01, etc.)
    - file_id: ID del file para corroborar en el cliente
    - equipment: Marca y número económico del equipo (si aplica)
    - date_created: Fecha de creación del formato
    - employee: Nombre y apellido del empleado
    - status: Estado del formato
    
    Los formatos se devuelven en el siguiente orden:
    FO-SP-01, FO-SC-01, FO-OS-01, FO-EM-01, FO-BC-01, FO-PC-02, FO-PP-02, FO-CR-02
    """
    try:
        repo = FileFormatsRepoImpl(db)
        use_case = GetFormatsByFile(repo)
        formats = use_case.execute(file_id)
        
        return [
            FileFormatSchema(
                id=format.id,
                format=format.format,
                file_id=format.file_id,
                equipment=format.equipment,
                date_created=format.date_created,
                employee=format.employee,
                status=format.status
            )
            for format in formats
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al obtener formatos del file: {str(e)}"
        )

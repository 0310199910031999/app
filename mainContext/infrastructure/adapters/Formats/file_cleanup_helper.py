"""
Helper para la limpieza automática de files cuando se eliminan documentos
"""
from sqlalchemy.orm import Session
from mainContext.infrastructure.models import (
    Files as FilesModel,
    Fobc01 as FOBC01Model,
    Focr02 as FOCR02Model,
    Foem01 as FOEM01Model,
    Foem011 as FOEM011Model,
    Foos01 as FOOS01Model,
    Fopc02 as FOPC02Model,
    Fosc01 as FOSC01Model,
    Fosp01 as FOSP01Model,
    Foro05Services as FORO05ServicesModel
)


def cleanup_file_if_orphaned(db: Session, file_id: str | None) -> bool:
    """
    Elimina un file si no tiene ningún documento relacionado.
    
    Args:
        db: Sesión de base de datos
        file_id: ID del file a verificar y potencialmente eliminar
        
    Returns:
        True si el file fue eliminado, False si no fue eliminado o no existe
    """
    if not file_id:
        return False
    
    try:
        # Verificar si el file existe
        file_model = db.query(FilesModel).filter_by(id=file_id).first()
        if not file_model:
            return False
        
        # Verificar si hay documentos relacionados con este file_id
        has_fobc01 = db.query(FOBC01Model).filter_by(file_id=file_id).first() is not None
        has_focr02 = db.query(FOCR02Model).filter_by(file_id=file_id).first() is not None
        has_foem01 = db.query(FOEM01Model).filter_by(file_id=file_id).first() is not None
        has_foem011 = db.query(FOEM011Model).filter_by(file_id=file_id).first() is not None
        has_foos01 = db.query(FOOS01Model).filter_by(file_id=file_id).first() is not None
        has_fopc02 = db.query(FOPC02Model).filter_by(file_id=file_id).first() is not None
        has_fosc01 = db.query(FOSC01Model).filter_by(file_id=file_id).first() is not None
        has_fosp01 = db.query(FOSP01Model).filter_by(file_id=file_id).first() is not None
        has_foro05 = db.query(FORO05ServicesModel).filter_by(file_id=file_id).first() is not None
        
        # Si no hay ningún documento relacionado, eliminar el file
        if not (has_fobc01 or has_focr02 or has_foem01 or has_foem011 or 
                has_foos01 or has_fopc02 or has_fosc01 or has_fosp01 or has_foro05):
            db.delete(file_model)
            db.flush()
            print(f"File {file_id} eliminado por no tener documentos relacionados")
            return True
        
        return False
        
    except Exception as e:
        print(f"Error al verificar/eliminar file {file_id}: {e}")
        return False

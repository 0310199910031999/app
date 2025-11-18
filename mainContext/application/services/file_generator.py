
from datetime import datetime
from sqlalchemy.orm import Session
from mainContext.infrastructure.models import Files as File # Asegúrate de importar tu modelo correctamente

class FileService:
    @staticmethod
    def create_file(db: Session, client_id: int, status: str = "Abierto") -> File:
        now = datetime.now()
        year = now.year % 100
        month = now.month

        # Obtener el último File por fecha de creación
        last_file = db.query(File).order_by(File.date_created.desc()).first()

        if last_file and last_file.folio.startswith("DALM"):
            last_number = int(last_file.folio[8:])  # Extrae el número del folio
            next_number = last_number + 1
        else:
            next_number = 1

        folio_new = f"DALM{year:02d}{month:02d}{next_number:03d}"

        file_model = File(
            id = folio_new,
            client_id=client_id,
            date_created=now,
            status=status,
            date_closed=None,
            date_invoiced=None,
            folio_invoice="",
            uuid="",
            folio=folio_new
        )

        db.add(file_model)
        db.flush()
        return file_model
    
    @staticmethod
    def check_and_close_file(db: Session, file_id: str) -> bool:
        """
        Verifica si todos los documentos asociados a un file están cerrados.
        Si todos están cerrados, cierra el file automáticamente.
        
        Args:
            db: Sesión de base de datos
            file_id: ID del file a verificar
            
        Returns:
            bool: True si el file fue cerrado, False si se mantiene abierto
            
        Raises:
            Exception: Si hay un error al verificar o actualizar el file
        """
        try:
            # Obtener el file
            file = db.query(File).filter_by(id=file_id).first()
            
            if not file:
                raise Exception(f"File con ID {file_id} no encontrado")
            
            # Si el file ya está cerrado, no hacer nada
            if file.status == "Cerrado":
                return False
            
            # Verificar documentos asociados
            # Importar modelos necesarios
            from mainContext.infrastructure.models import Foos01, Fosc01, Fosp01, Fobc01, Foem01, Focr02
            
            has_open_documents = False
            
            # Verificar FOOS01
            open_foos01 = db.query(Foos01).filter(
                Foos01.file_id == file_id,
                Foos01.status == "Abierto"
            ).first()
            if open_foos01:
                has_open_documents = True
            
            # Verificar FOSC01
            if not has_open_documents:
                open_fosc01 = db.query(Fosc01).filter(
                    Fosc01.file_id == file_id,
                    Fosc01.status == "Abierto"
                ).first()
                if open_fosc01:
                    has_open_documents = True
            
            # Verificar FOSP01
            if not has_open_documents:
                open_fosp01 = db.query(Fosp01).filter(
                    Fosp01.file_id == file_id,
                    Fosp01.status == "Abierto"
                ).first()
                if open_fosp01:
                    has_open_documents = True
            
            # Verificar FOBC01
            if not has_open_documents:
                open_fobc01 = db.query(Fobc01).filter(
                    Fobc01.file_id == file_id,
                    Fobc01.status == "Abierto"
                ).first()
                if open_fobc01:
                    has_open_documents = True
            
            # Verificar FOEM01
            if not has_open_documents:
                open_foem01 = db.query(Foem01).filter(
                    Foem01.file_id == file_id,
                    Foem01.status == "Abierto"
                ).first()
                if open_foem01:
                    has_open_documents = True
            
            # Verificar FOCR02
            if not has_open_documents:
                open_focr02 = db.query(Focr02).filter(
                    Focr02.file_id == file_id,
                    Focr02.status == "Abierto"
                ).first()
                if open_focr02:
                    has_open_documents = True
            
            # Si no hay documentos abiertos, cerrar el file
            if not has_open_documents:
                # Verificar que al menos haya un documento asociado
                total_docs = (
                    db.query(Foos01).filter(Foos01.file_id == file_id).count() +
                    db.query(Fosc01).filter(Fosc01.file_id == file_id).count() +
                    db.query(Fosp01).filter(Fosp01.file_id == file_id).count() +
                    db.query(Fobc01).filter(Fobc01.file_id == file_id).count() +
                    db.query(Foem01).filter(Foem01.file_id == file_id).count() +
                    db.query(Focr02).filter(Focr02.file_id == file_id).count()
                )
                
                # Solo cerrar si hay documentos y todos están cerrados
                if total_docs > 0:
                    file.status = "Cerrado"
                    file.date_closed = datetime.now()
                    db.commit()
                    print(f"[FILE SERVICE] File {file_id} cerrado automáticamente - todos los documentos están cerrados")
                    return True
            else:
                print(f"[FILE SERVICE] File {file_id} se mantiene abierto - hay documentos abiertos")
            
            return False
            
        except Exception as e:
            print(f"[FILE SERVICE ERROR] Error al verificar file {file_id}: {str(e)}")
            raise Exception(f"Error al verificar y cerrar file: {str(e)}")

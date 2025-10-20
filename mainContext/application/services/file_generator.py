
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


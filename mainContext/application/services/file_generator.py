
import re
from datetime import datetime

from sqlalchemy import not_, or_
from sqlalchemy.orm import Session

from mainContext.infrastructure.models import Files as File

class FileService:
    CONSECUTIVE_FILE_PATTERN = re.compile(r"^(?P<base>.+)-(?P<consecutive>\d+)$")

    @staticmethod
    def get_base_file_id(file_id: str | None) -> str | None:
        if not file_id:
            return file_id

        match = FileService.CONSECUTIVE_FILE_PATTERN.match(file_id)
        if not match:
            return file_id

        return match.group("base")

    @staticmethod
    def is_consecutive_file_id(file_id: str | None) -> bool:
        if not file_id:
            return False

        return FileService.CONSECUTIVE_FILE_PATTERN.match(file_id) is not None

    @staticmethod
    def build_related_file_filter(column, file_id: str):
        base_file_id = FileService.get_base_file_id(file_id)
        return or_(column == base_file_id, column.like(f"{base_file_id}-%"))

    @staticmethod
    def create_file(db: Session, client_id: int, status: str = "Abierto") -> File:
        # Si el cliente es 11, retornar None
        if client_id == 11 or client_id == 90:
            return None
        
        now = datetime.now()
        year = now.year % 100
        month = now.month

        # Obtener el último file base por fecha de creación, ignorando consecutivos.
        last_file = (
            db.query(File)
            .filter(not_(File.id.like("%-%")))
            .order_by(File.date_created.desc())
            .first()
        )

        if last_file and last_file.folio and last_file.folio.startswith("DALM"):
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
    def create_consecutive_file(db: Session, file_id: str, status: str = "Abierto") -> File:
        base_file_id = FileService.get_base_file_id(file_id)
        base_file = db.query(File).filter_by(id=base_file_id).first()

        if not base_file:
            raise Exception(f"File base con ID {base_file_id} no encontrado")

        related_file_ids = (
            db.query(File.id)
            .filter(FileService.build_related_file_filter(File.id, base_file_id))
            .all()
        )

        next_consecutive = 1
        for (related_file_id,) in related_file_ids:
            match = FileService.CONSECUTIVE_FILE_PATTERN.match(related_file_id)
            if not match or match.group("base") != base_file_id:
                continue
            next_consecutive = max(next_consecutive, int(match.group("consecutive")) + 1)

        consecutive_file_id = f"{base_file_id}-{next_consecutive}"
        consecutive_file = File(
            id=consecutive_file_id,
            client_id=base_file.client_id,
            date_created=datetime.now(),
            status=status,
            date_closed=None,
            date_invoiced=None,
            folio_invoice="",
            uuid="",
            folio=consecutive_file_id,
        )

        db.add(consecutive_file)
        db.flush()
        return consecutive_file

    @staticmethod
    def _has_related_consecutive_files(db: Session, file_id: str) -> bool:
        return (
            db.query(File.id)
            .filter(File.id.like(f"{file_id}-%"))
            .first()
            is not None
        )

    @staticmethod
    def _has_open_documents(db: Session, filter_factory) -> bool:
        from mainContext.infrastructure.models import Foos01, Fosc01, Fosp01, Fobc01, Foem01, Focr02, Fopc02, Fopp02

        if db.query(Foos01).filter(filter_factory(Foos01.file_id), Foos01.status == "Abierto").first():
            return True
        if db.query(Fosc01).filter(filter_factory(Fosc01.file_id), Fosc01.status == "Abierto").first():
            return True
        if db.query(Fosp01).filter(filter_factory(Fosp01.file_id), Fosp01.status == "Abierto").first():
            return True
        if db.query(Fobc01).filter(filter_factory(Fobc01.file_id), Fobc01.status == "Abierto").first():
            return True
        if db.query(Foem01).filter(filter_factory(Foem01.file_id), Foem01.status == "Abierto").first():
            return True
        if db.query(Focr02).filter(filter_factory(Focr02.file_id), Focr02.status.in_(["Abierto", "En Renta"])).first():
            return True
        if db.query(Fopc02).filter(filter_factory(Fopc02.file_id), Fopc02.status == "Abierto").first():
            return True
        if db.query(Fopp02).filter(filter_factory(Fopp02.file_id), Fopp02.status == "Abierto").first():
            return True

        return False

    @staticmethod
    def _count_documents(db: Session, filter_factory) -> int:
        from mainContext.infrastructure.models import Foos01, Fosc01, Fosp01, Fobc01, Foem01, Focr02, Fopc02, Fopp02

        return (
            db.query(Foos01).filter(filter_factory(Foos01.file_id)).count()
            + db.query(Fosc01).filter(filter_factory(Fosc01.file_id)).count()
            + db.query(Fosp01).filter(filter_factory(Fosp01.file_id)).count()
            + db.query(Fobc01).filter(filter_factory(Fobc01.file_id)).count()
            + db.query(Foem01).filter(filter_factory(Foem01.file_id)).count()
            + db.query(Focr02).filter(filter_factory(Focr02.file_id)).count()
            + db.query(Fopc02).filter(filter_factory(Fopc02.file_id)).count()
            + db.query(Fopp02).filter(filter_factory(Fopp02.file_id)).count()
        )

    @staticmethod
    def check_and_close_exact_file(db: Session, file_id: str) -> bool:
        try:
            file = db.query(File).filter_by(id=file_id).first()

            if not file:
                raise Exception(f"File con ID {file_id} no encontrado")

            if file.status == "Cerrado":
                return False

            if (
                not FileService.is_consecutive_file_id(file_id)
                and FileService._has_related_consecutive_files(db, file_id)
            ):
                print(
                    f"[FILE SERVICE] File base {file_id} tiene consecutivos relacionados; "
                    "su cierre grupal se evalua desde FOCR02"
                )
                return False

            file_filter = lambda column: column == file_id
            has_open_documents = FileService._has_open_documents(db, file_filter)

            if not has_open_documents:
                total_docs = FileService._count_documents(db, file_filter)

                if total_docs > 0:
                    file.status = "Cerrado"
                    file.date_closed = datetime.now()
                    db.commit()
                    print(f"[FILE SERVICE] File {file_id} cerrado automaticamente - todos sus documentos estan cerrados")
                    return True
            else:
                print(f"[FILE SERVICE] File {file_id} se mantiene abierto - hay documentos abiertos")

            return False

        except Exception as e:
            print(f"[FILE SERVICE ERROR] Error al verificar file exacto {file_id}: {str(e)}")
            raise Exception(f"Error al verificar y cerrar file exacto: {str(e)}")

    @staticmethod
    def check_and_close_group_file(db: Session, file_id: str) -> bool:
        try:
            base_file_id = FileService.get_base_file_id(file_id)
            file = db.query(File).filter_by(id=base_file_id).first()

            if not file:
                raise Exception(f"File base con ID {base_file_id} no encontrado")

            if file.status == "Cerrado":
                return False

            file_filter = lambda column: FileService.build_related_file_filter(column, base_file_id)
            has_open_documents = FileService._has_open_documents(db, file_filter)

            if not has_open_documents:
                total_docs = FileService._count_documents(db, file_filter)

                if total_docs > 0:
                    file.status = "Cerrado"
                    file.date_closed = datetime.now()
                    db.commit()
                    print(
                        f"[FILE SERVICE] File base {base_file_id} cerrado automaticamente - "
                        "todos los documentos base y consecutivos estan cerrados"
                    )
                    return True
            else:
                print(
                    f"[FILE SERVICE] File base {base_file_id} se mantiene abierto - "
                    "hay documentos abiertos en el grupo"
                )

            return False

        except Exception as e:
            print(f"[FILE SERVICE ERROR] Error al verificar grupo de file {file_id}: {str(e)}")
            raise Exception(f"Error al verificar y cerrar grupo de file: {str(e)}")
    
    @staticmethod
    def check_and_close_file(db: Session, file_id: str) -> bool:
        return FileService.check_and_close_exact_file(db, file_id)

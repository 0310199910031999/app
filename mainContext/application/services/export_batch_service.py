import datetime
import hashlib
import re
import secrets
import shutil
import zipfile
from pathlib import Path
from typing import Optional

from config import settings
from mainContext.application.dtos.export_dto import (
    ExportDocumentRowDTO,
    ExportJobCompleteDTO,
    ExportJobDTO,
    ExportJobProgressDTO,
)
from mainContext.infrastructure.adapters.AppUserRepo import AppUserRepoImpl
from mainContext.infrastructure.adapters.ExportDocumentCollectorRepo import ExportDocumentCollectorRepoImpl
from mainContext.infrastructure.adapters.ExportJobRepo import ExportJobRepoImpl
from mainContext.infrastructure.adapters.Formats.fo_cr_02_repo import FOCR02RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_em_01_repo import FOEM01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_im_01_repo import FOIM01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_im_03_repo import FOIM03RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_le_01_repo import FOLE01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_os_01_repo import FOOS01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_pc_02_repo import FOPC02RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_pp_02_repo import FOPP02RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_sc_01_repo import FOSC01RepoImpl
from mainContext.infrastructure.adapters.Formats.fo_sp_01_repo import FOSP01RepoImpl
from mainContext.infrastructure.adapters.weasyprint_pdf_adapter import WeasyPrintPdfAdapter
from shared.email_service import EmailService


class ExportBatchService:
    MONTH_NAMES = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }
    STATUS_MESSAGES = {
        'queued': 'La exportación está en cola.',
        'collecting': 'Recolectando documentos para la exportación.',
        'rendering_pdfs': 'Generando archivos PDF.',
        'building_excel': 'Construyendo el Excel consolidado.',
        'compressing': 'Comprimiendo el lote en ZIP.',
        'notifying': 'Enviando la notificación por correo.',
        'completed': 'La exportación está lista.',
        'expired': 'El enlace de descarga ha expirado.',
        'failed': 'La exportación falló.',
    }

    def __init__(
        self,
        job_repo: ExportJobRepoImpl,
        collector: ExportDocumentCollectorRepoImpl,
        app_user_repo: AppUserRepoImpl,
    ):
        self.job_repo = job_repo
        self.collector = collector
        self.app_user_repo = app_user_repo
        self.pdf_generator = WeasyPrintPdfAdapter()
        self._renderer_registry = {
            'fo_cr_02': (FOCR02RepoImpl, 'get_focr02_by_id', self.pdf_generator.generate_focr02_pdf),
            'fo_em_01': (FOEM01RepoImpl, 'get_foem01_by_id', self.pdf_generator.generate_foem01_pdf),
            'fo_im_01': (FOIM01RepoImpl, 'get_foim01_by_id', self.pdf_generator.generate_foim01_pdf),
            'fo_im_03': (FOIM03RepoImpl, 'get_foim03_by_id', self.pdf_generator.generate_foim03_pdf),
            'fo_le_01': (FOLE01RepoImpl, 'get_fole01_by_id', self.pdf_generator.generate_fole01_pdf),
            'fo_os_01': (FOOS01RepoImpl, 'get_foos01_by_id', self.pdf_generator.generate_foos01_pdf),
            'fo_pc_02': (FOPC02RepoImpl, 'get_fopc02_by_id', self.pdf_generator.generate_fopc02_pdf),
            'fo_pp_02': (FOPP02RepoImpl, 'get_fopp02_by_id', self.pdf_generator.generate_fopp02_pdf),
            'fo_sc_01': (FOSC01RepoImpl, 'get_fosc01_by_id', self.pdf_generator.generate_fosc01_pdf),
            'fo_sp_01': (FOSP01RepoImpl, 'get_fosp01_by_id', self.pdf_generator.generate_fosp01_pdf),
        }

    @classmethod
    def status_message(cls, stage: str, status: str, error_message: Optional[str] = None) -> str:
        if status == 'failed' and error_message:
            return error_message
        return cls.STATUS_MESSAGES.get(stage) or cls.STATUS_MESSAGES.get(status) or 'Estado de exportación actualizado.'

    @staticmethod
    def cleanup_job_artifacts(zip_path: Optional[str]):
        if not zip_path:
            return

        zip_file = Path(zip_path)
        if zip_file.exists():
            job_dir = zip_file.parent.parent
            shutil.rmtree(job_dir, ignore_errors=True)

    def process_job(self, job_id: str):
        job = self.job_repo.get_job_by_id(job_id)
        if not job:
            raise ValueError(f'No se encontró el export job con id {job_id}')

        started_at = datetime.datetime.now()
        self.job_repo.update_job_progress(
            job_id,
            ExportJobProgressDTO(
                status='processing',
                stage='collecting',
                progress_pct=0,
                processed_documents=0,
                total_documents=0,
                started_at=started_at,
            ),
        )

        work_dir = None
        try:
            documents = self.collector.collect_documents(job)
            total_documents = len(documents)

            self.job_repo.update_job_progress(
                job_id,
                ExportJobProgressDTO(
                    status='processing',
                    stage='rendering_pdfs',
                    progress_pct=5 if total_documents else 20,
                    processed_documents=0,
                    total_documents=total_documents,
                    started_at=started_at,
                ),
            )

            work_dir, bundle_dir = self._prepare_job_dirs(job_id)
            excel_rows = []

            for index, document in enumerate(documents, start=1):
                pdf_bytes = self._render_pdf(document)
                pdf_path = self._pdf_output_path(work_dir, document)
                pdf_path.parent.mkdir(parents=True, exist_ok=True)
                pdf_path.write_bytes(pdf_bytes)
                excel_rows.append(document.excel_row)

                progress_pct = 10 + int((index / max(total_documents, 1)) * 70)
                self.job_repo.update_job_progress(
                    job_id,
                    ExportJobProgressDTO(
                        status='processing',
                        stage='rendering_pdfs',
                        progress_pct=min(progress_pct, 80),
                        processed_documents=index,
                        total_documents=total_documents,
                        started_at=started_at,
                    ),
                )

            self.job_repo.update_job_progress(
                job_id,
                ExportJobProgressDTO(
                    status='processing',
                    stage='building_excel',
                    progress_pct=85,
                    processed_documents=total_documents,
                    total_documents=total_documents,
                    started_at=started_at,
                ),
            )

            excel_path = work_dir / 'reporte_consolidado.xlsx'
            self._build_excel(excel_rows, excel_path)

            self.job_repo.update_job_progress(
                job_id,
                ExportJobProgressDTO(
                    status='processing',
                    stage='compressing',
                    progress_pct=95,
                    processed_documents=total_documents,
                    total_documents=total_documents,
                    started_at=started_at,
                ),
            )

            zip_filename = f'export_{job_id}.zip'
            zip_path = bundle_dir / zip_filename
            self._build_zip(work_dir, zip_path)

            raw_token = secrets.token_urlsafe(32)
            token_hash = self._hash_token(raw_token)
            expires_at = datetime.datetime.now() + datetime.timedelta(minutes=settings.EXPORT_URL_TTL_MINUTES)

            self.job_repo.update_job_progress(
                job_id,
                ExportJobProgressDTO(
                    status='processing',
                    stage='notifying',
                    progress_pct=98,
                    processed_documents=total_documents,
                    total_documents=total_documents,
                    started_at=started_at,
                ),
            )

            self.job_repo.complete_job(
                job_id,
                ExportJobCompleteDTO(
                    zip_filename=zip_filename,
                    zip_path=str(zip_path.resolve()),
                    zip_size_bytes=zip_path.stat().st_size,
                    download_token_hash=token_hash,
                    token_expires_at=expires_at,
                    processed_documents=total_documents,
                    total_documents=total_documents,
                ),
            )

            email_sent = self._send_completion_email(job, raw_token, expires_at)
            if not email_sent:
                self.job_repo.update_job_progress(
                    job_id,
                    ExportJobProgressDTO(
                        status='completed',
                        stage='completed',
                        progress_pct=100,
                        processed_documents=total_documents,
                        total_documents=total_documents,
                        error_message='No se pudo enviar el correo de exportación.',
                    ),
                )

            shutil.rmtree(work_dir, ignore_errors=True)
        except Exception as e:
            if work_dir is not None:
                shutil.rmtree(work_dir.parent, ignore_errors=True)
            self.job_repo.fail_job(job_id, str(e))
            raise

    def _prepare_job_dirs(self, job_id: str):
        root_dir = Path(settings.EXPORT_TMP_DIR).resolve() / job_id
        work_dir = root_dir / 'work'
        bundle_dir = root_dir / 'bundle'
        work_dir.mkdir(parents=True, exist_ok=True)
        bundle_dir.mkdir(parents=True, exist_ok=True)
        return work_dir, bundle_dir

    def _sanitize_path_segment(self, value: str) -> str:
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', '_', value or '').strip(' .')
        return sanitized or 'sin_nombre'

    def _pdf_output_path(self, work_dir: Path, document: ExportDocumentRowDTO) -> Path:
        month_name = self.MONTH_NAMES[document.date_created.month]
        return (
            work_dir
            / self._sanitize_path_segment(document.folder_equipment_name)
            / document.date_created.strftime('%Y')
            / self._sanitize_path_segment(month_name)
            / self._sanitize_path_segment(document.format_folder_name)
            / self._sanitize_path_segment(document.filename)
        )

    def _render_pdf(self, document: ExportDocumentRowDTO) -> bytes:
        if document.format_key not in self._renderer_registry:
            raise ValueError(f'Formato no soportado para PDF: {document.format_key}')

        repo_cls, detail_method, pdf_method = self._renderer_registry[document.format_key]
        repo = repo_cls(self.collector.db)
        detail = getattr(repo, detail_method)(document.document_id)
        if not detail:
            raise ValueError(f'No se encontró el detalle del documento {document.document_id} para {document.format_label}')
        return pdf_method(detail.__dict__)

    def _build_excel(self, rows, output_path: Path):
        try:
            from openpyxl import Workbook
        except ImportError as exc:
            raise RuntimeError('openpyxl es requerido para generar el Excel consolidado') from exc

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = 'Export'

        headers = [
            'ID',
            'Equipo',
            'Fecha',
            'Tipo de servicio / Nombre de Formato',
            'Servicios realizados',
            'Técnico / Empleado',
            'Nombre de Recepción del Servicio',
            'Desperfectos',
        ]
        worksheet.append(headers)

        for row in rows:
            worksheet.append([row.get(header, '') for header in headers])

        for column_cells in worksheet.columns:
            max_length = max(len(str(cell.value or '')) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 50)

        workbook.save(output_path)

    def _build_zip(self, source_dir: Path, zip_path: Path):
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for file_path in source_dir.rglob('*'):
                if file_path.is_file():
                    archive.write(file_path, file_path.relative_to(source_dir))

    def _hash_token(self, raw_token: str) -> str:
        return hashlib.sha256(raw_token.encode('utf-8')).hexdigest()

    def _send_completion_email(self, job: ExportJobDTO, raw_token: str, expires_at: datetime.datetime) -> bool:
        app_user = self.app_user_repo.get_app_user_by_id(job.requested_by_user_id)
        if not app_user or not app_user.email:
            return False

        export_base_url = (settings.EXPORT_BASE_URL or settings.BASE_URL).rstrip('/')
        download_url = f"{export_base_url}/exports/download/{raw_token}"
        subject = f'Exportación lista {job.id}'
        message = f"""
        <html>
        <body style=\"font-family: Arial, sans-serif;\">
            <div style=\"max-width: 600px; margin: 0 auto; padding: 20px;\">
                <h3>Tu exportación está lista</h3>
                <p>Se generó correctamente el archivo ZIP solicitado.</p>
                <p><strong>Job:</strong> {job.id}</p>
                <p><strong>Expira:</strong> {expires_at.strftime('%d/%m/%Y %H:%M:%S')}</p>
                <p>
                    <a href=\"{download_url}\" style=\"display: inline-block; padding: 10px 16px; background: #0066cc; color: #fff; text-decoration: none; border-radius: 4px;\">
                        Descargar ZIP
                    </a>
                </p>
            </div>
        </body>
        </html>
        """
        return EmailService.send_email(
            to=app_user.email,
            subject=subject,
            message=message,
            company_id=90,
            html=True,
        )

import os
import sys

# WeasyPrint 68 docs (first_steps.html):
# En Windows necesita WEASYPRINT_DLL_DIRECTORIES para localizar las DLLs de Pango/GTK.
# En Linux las librerías se instalan como paquetes del sistema y se encuentran automáticamente.
if sys.platform == "win32":
    os.environ.setdefault("WEASYPRINT_DLL_DIRECTORIES", r"C:\msys64\ucrt64\bin")

from pathlib import Path
import base64
import glob as glob_module
from datetime import date, datetime

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from weasyprint.text.fonts import FontConfiguration

from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort


class WeasyPrintPdfAdapter(PDFGeneratorPort):
    def __init__(self):
        # mainContext/infrastructure/
        infra_dir = Path(__file__).resolve().parent.parent

        # Templates Jinja2: mainContext/infrastructure/templates/
        self.template_dir = infra_dir / "templates"
        self.env = Environment(loader=FileSystemLoader(str(self.template_dir)))

        # Assets locales (fonts/): mainContext/infrastructure/static/
        # El @font-face usa url('fonts/tahoma.ttf') relativo a este directorio.
        self.assets_dir = infra_dir / "static"

        # Imágenes servidas por FastAPI: mainContext/static/
        # Aquí están evidence y signatures guardadas por el repo.
        self.static_root = infra_dir.parent / "static"
        self.logo_path = self.static_root / "img" / "logos" / "Logo DAL.png"

    def _file_to_base64_uri(self, file_path: Path) -> str | None:
        try:
            if not file_path.exists():
                return None
            mime = "image/png" if file_path.suffix.lower() == ".png" else "image/jpeg"
            encoded = base64.b64encode(file_path.read_bytes()).decode("utf-8")
            return f"data:{mime};base64,{encoded}"
        except Exception:
            return None

    def _load_signature(self, signature_path: str) -> str | None:
        if not signature_path:
            return None
        relative = signature_path.removeprefix("/static/")
        return self._file_to_base64_uri(self.static_root / relative)

    def _load_evidence_images(self, fole01_id: int) -> list:
        evidence_dir = self.static_root / "img" / "evidence" / "fo-le-01"
        pattern = str(evidence_dir / f"{fole01_id}-*")
        image_files = sorted(glob_module.glob(pattern))
        return [uri for path in image_files if (uri := self._file_to_base64_uri(Path(path)))]

    def _load_fosp01_evidence_images(self, fosp01_id: int, photo_type: str) -> list:
        evidence_dir = self.static_root / "img" / "evidence" / "fo-sp-01"
        pattern = str(evidence_dir / f"{fosp01_id}-fosp-{photo_type}-*")
        image_files = sorted(glob_module.glob(pattern))
        return [uri for path in image_files if (uri := self._file_to_base64_uri(Path(path)))]

    def _load_fosc01_evidence_images(self, fosc01_id: int, photo_type: str) -> list:
        evidence_dir = self.static_root / "img" / "evidence" / "fo-sc-01"
        pattern = str(evidence_dir / f"{fosc01_id}-fosc-{photo_type}-*")
        image_files = sorted(glob_module.glob(pattern))
        return [uri for path in image_files if (uri := self._file_to_base64_uri(Path(path)))]

    def _load_foos01_evidence_images(self, foos01_id: int, photo_type: str) -> list:
        evidence_dir = self.static_root / "img" / "evidence" / "fo-os-01"
        pattern = str(evidence_dir / f"{foos01_id}-foos-{photo_type}-*")
        image_files = sorted(glob_module.glob(pattern))
        return [uri for path in image_files if (uri := self._file_to_base64_uri(Path(path)))]

    def _group_foir02_checklist(self, equipment_checklist: list) -> list:
        grouped_items = {}
        desired_order = [
            "Caja #1",
            "Caja #2 (insumos electricos nuevos)",
            "Caja #3 (equipo de seguridad personal)",
            "Caja #4 (herramienta)",
            "Papelería",
            "Otra Herramienta",
            "Equipo Opcional",
        ]

        for item in equipment_checklist or []:
            required_equipment = getattr(item, "required_equipment", None)
            group_name = getattr(required_equipment, "type", None)
            grouped_items.setdefault(group_name, []).append(item)

        return [
            {"type": group_type, "items": grouped_items[group_type]}
            for group_type in desired_order
            if group_type in grouped_items
        ]

    def _load_logo(self) -> str | None:
        return self._file_to_base64_uri(self.logo_path)

    def _format_document_date(self, value) -> str:
        if not value:
            return ""

        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y")

        if isinstance(value, date):
            return value.strftime("%d/%m/%Y")

        if isinstance(value, str):
            sanitized_value = value.strip()
            if not sanitized_value:
                return ""

            normalized_value = sanitized_value.replace("Z", "+00:00")
            for parser in (datetime.fromisoformat, date.fromisoformat):
                try:
                    parsed_value = parser(normalized_value)
                    return parsed_value.strftime("%d/%m/%Y")
                except ValueError:
                    continue

            return sanitized_value

        return str(value)

    def generate_fole01_pdf(self, data: dict) -> bytes:
        """
        WeasyPrint 68 API (api_reference.html):
        font_config = FontConfiguration()
        HTML(string=..., base_url=...).write_pdf(font_config=font_config)

        FontConfiguration() reúne las fuentes del sistema al crearse.
        El mismo objeto debe usarse para todos los CSS del mismo documento.
        base_url apunta a assets_dir para que url('fonts/tahoma.ttf') resuelva.
        """
        try:
            template = self.env.get_template("fole01_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            evidence_images = self._load_evidence_images(data.get("id", 0))
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
                evidence_images=evidence_images,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_foim01_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("foim01_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_foim03_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("foim03_template.html")
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_fosp01_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("fosp01_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            before_images = self._load_fosp01_evidence_images(data.get("id", 0), "antes")
            after_images = self._load_fosp01_evidence_images(data.get("id", 0), "despues")
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
                before_images=before_images,
                after_images=after_images,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_fosc01_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("fosc01_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            before_images = self._load_fosc01_evidence_images(data.get("id", 0), "antes")
            after_images = self._load_fosc01_evidence_images(data.get("id", 0), "despues")
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
                before_images=before_images,
                after_images=after_images,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_foos01_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("foos01_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            before_images = self._load_foos01_evidence_images(data.get("id", 0), "antes")
            after_images = self._load_foos01_evidence_images(data.get("id", 0), "despues")
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
                before_images=before_images,
                after_images=after_images,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_foem01_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("foem01_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_fopc02_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("fopc02_template.html")
            logo_base64 = self._load_logo()

            render_data = dict(data)
            render_data["departure_date"] = self._format_document_date(data.get("departure_date", ""))
            render_data["return_date"] = self._format_document_date(data.get("return_date", ""))

            html_content = template.render(
                data=render_data,
                logo_base64=logo_base64,
                departure_signature_base64=self._load_signature(data.get("departure_signature_path", "")),
                departure_employee_signature_base64=self._load_signature(data.get("departure_employee_signature_path", "")),
                return_signature_base64=self._load_signature(data.get("return_signature_path", "")),
                return_employee_signature_base64=self._load_signature(data.get("return_employee_signature_path", "")),
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_fopp02_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("fopp02_template.html")
            logo_base64 = self._load_logo()

            render_data = dict(data)
            render_data["departure_date"] = self._format_document_date(data.get("departure_date", ""))
            render_data["delivery_date"] = self._format_document_date(data.get("delivery_date", ""))

            html_content = template.render(
                data=render_data,
                logo_base64=logo_base64,
                departure_signature_base64=self._load_signature(data.get("departure_signature_path", "")),
                departure_employee_signature_base64=self._load_signature(data.get("departure_employee_signature_path", "")),
                delivery_signature_base64=self._load_signature(data.get("delivery_signature_path", "")),
                delivery_employee_signature_base64=self._load_signature(data.get("delivery_employee_signature_path", "")),
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_focr02_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("focr02_template.html")
            signature_base64 = self._load_signature(data.get("signature_path", ""))
            return_signature_base64 = self._load_signature(data.get("return_signature_path", "")) if data.get("return_signature_path") else None
            logo_base64 = self._load_logo()
            formatted_date_signed = self._format_document_date(
                data.get("date_signed", data.get("date_created", ""))
            )
            formatted_return_date_signed = self._format_document_date(
                data.get("return_date_signed", "")
            ) if data.get("return_date_signed") else None
            html_content = template.render(
                data=data,
                date_signed=formatted_date_signed,
                return_date_signed=formatted_return_date_signed,
                logo_base64=logo_base64,
                signature_base64=signature_base64,
                return_signature_base64=return_signature_base64,
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_foir02_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("foir02_template.html")
            logo_base64 = self._load_logo()
            formatted_date_route = self._format_document_date(data.get("date_route", ""))
            grouped_checklist = self._group_foir02_checklist(data.get("equipment_checklist", []))

            html_content = template.render(
                data=data,
                date_route=formatted_date_route,
                logo_base64=logo_base64,
                grouped_checklist=grouped_checklist,
                employee_signature_base64=self._load_signature(data.get("employee_signature_path", "")),
                supervisor_signature_base64=self._load_signature(data.get("supervisor_signature_path", "")),
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def generate_foro05_pdf(self, data: dict) -> bytes:
        try:
            template = self.env.get_template("foro05_template.html")
            logo_base64 = self._load_logo()
            formatted_route_date = self._format_document_date(data.get("route_date", ""))

            html_content = template.render(
                data=data,
                route_date=formatted_route_date,
                logo_base64=logo_base64,
                employee_signature_base64=self._load_signature(data.get("signature_path_employee", "")),
                supervisor_signature_base64=self._load_signature(data.get("signature_path_supervisor", "")),
            )

            font_config = FontConfiguration()

            pdf_bytes = HTML(
                string=html_content,
                base_url=str(self.assets_dir),
            ).write_pdf(font_config=font_config)

            return pdf_bytes
        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

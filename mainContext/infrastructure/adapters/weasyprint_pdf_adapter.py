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
            html_content = template.render(
                data=data,
                date_signed=data.get("date_signed", data.get("date_created", "")),
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

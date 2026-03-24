from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_sp_01_repo import FOSP01Repo


class GenerateFoSp01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, fosp01_repo: FOSP01Repo):
        self.pdf_generator = pdf_generator
        self.fosp01_repo = fosp01_repo

    def execute(self, fosp01_id: int) -> bytes:
        fosp01_data = self.fosp01_repo.get_fosp01_by_id(fosp01_id)

        if not fosp01_data:
            raise ValueError(f"No se encontró el reporte FO-SP-01 con ID {fosp01_id}")

        return self.pdf_generator.generate_fosp01_pdf(data=fosp01_data.__dict__)
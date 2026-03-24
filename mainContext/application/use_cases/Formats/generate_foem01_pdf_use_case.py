from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_em_01_repo import FOEM01Repo


class GenerateFoEm01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foem01_repo: FOEM01Repo):
        self.pdf_generator = pdf_generator
        self.foem01_repo = foem01_repo

    def execute(self, foem01_id: int) -> bytes:
        foem01_data = self.foem01_repo.get_foem01_by_id(foem01_id)

        if not foem01_data:
            raise ValueError(f"No se encontró el reporte FO-EM-01 con ID {foem01_id}")

        return self.pdf_generator.generate_foem01_pdf(data=foem01_data.__dict__)
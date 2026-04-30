from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_em_01_1_repo import FOEM011Repo


class GenerateFoEm011PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foem01_1_repo: FOEM011Repo):
        self.pdf_generator = pdf_generator
        self.foem01_1_repo = foem01_1_repo

    def execute(self, foem01_1_id: int) -> bytes:
        foem01_1_data = self.foem01_1_repo.get_foem01_1_by_id(foem01_1_id)

        if not foem01_1_data:
            raise ValueError(f"No se encontró el reporte FO-EM-01_1 con ID {foem01_1_id}")

        return self.pdf_generator.generate_foem01_1_pdf(data=foem01_1_data.__dict__)
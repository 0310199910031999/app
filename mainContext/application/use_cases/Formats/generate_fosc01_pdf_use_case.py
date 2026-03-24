from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_sc_01_repo import FOSC01Repo


class GenerateFoSc01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, fosc01_repo: FOSC01Repo):
        self.pdf_generator = pdf_generator
        self.fosc01_repo = fosc01_repo

    def execute(self, fosc01_id: int) -> bytes:
        fosc01_data = self.fosc01_repo.get_fosc01_by_id(fosc01_id)

        if not fosc01_data:
            raise ValueError(f"No se encontró el reporte FO-SC-01 con ID {fosc01_id}")

        return self.pdf_generator.generate_fosc01_pdf(data=fosc01_data.__dict__)
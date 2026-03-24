from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_im_01_repo import FOIM01Repo


class GenerateFoIm01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foim01_repo: FOIM01Repo):
        self.pdf_generator = pdf_generator
        self.foim01_repo = foim01_repo

    def execute(self, foim01_id: int) -> bytes:
        foim01_data = self.foim01_repo.get_foim01_by_id(foim01_id)

        if not foim01_data:
            raise ValueError(f"No se encontró el reporte FO-IM-01 con ID {foim01_id}")

        return self.pdf_generator.generate_foim01_pdf(data=foim01_data.__dict__)
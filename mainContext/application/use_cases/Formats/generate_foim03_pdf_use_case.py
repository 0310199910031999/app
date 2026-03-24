from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_im_03_repo import FOIM03Repo


class GenerateFoIm03PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foim03_repo: FOIM03Repo):
        self.pdf_generator = pdf_generator
        self.foim03_repo = foim03_repo

    def execute(self, foim03_id: int) -> bytes:
        foim03_data = self.foim03_repo.get_foim03_by_id(foim03_id)

        if not foim03_data:
            raise ValueError(f"No se encontró el reporte FO-IM-03 con ID {foim03_id}")

        return self.pdf_generator.generate_foim03_pdf(data=foim03_data.__dict__)
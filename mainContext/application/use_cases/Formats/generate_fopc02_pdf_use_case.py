from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_pc_02_repo import FOPC02Repo


class GenerateFoPc02PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, fopc02_repo: FOPC02Repo):
        self.pdf_generator = pdf_generator
        self.fopc02_repo = fopc02_repo

    def execute(self, fopc02_id: int) -> bytes:
        fopc02_data = self.fopc02_repo.get_fopc02_by_id(fopc02_id)
        if not fopc02_data:
            raise ValueError("FOPC02 no encontrado")

        return self.pdf_generator.generate_fopc02_pdf(data=fopc02_data.__dict__)
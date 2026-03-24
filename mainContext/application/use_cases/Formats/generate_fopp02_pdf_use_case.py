from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_pp_02_repo import FOPP02Repo


class GenerateFoPp02PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, fopp02_repo: FOPP02Repo):
        self.pdf_generator = pdf_generator
        self.fopp02_repo = fopp02_repo

    def execute(self, fopp02_id: int) -> bytes:
        fopp02_data = self.fopp02_repo.get_fopp02_by_id(fopp02_id)
        if not fopp02_data:
            raise ValueError("FOPP02 no encontrado")

        return self.pdf_generator.generate_fopp02_pdf(data=fopp02_data.__dict__)
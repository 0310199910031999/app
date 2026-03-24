from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_ro_05_repo import FORO05Repo


class GenerateFoRo05PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foro05_repo: FORO05Repo):
        self.pdf_generator = pdf_generator
        self.foro05_repo = foro05_repo

    def execute(self, foro05_id: int) -> bytes:
        foro05_data = self.foro05_repo.get_foro05_by_id(foro05_id)
        if not foro05_data:
            raise ValueError("FORO05 no encontrado")

        return self.pdf_generator.generate_foro05_pdf(data=foro05_data.__dict__)
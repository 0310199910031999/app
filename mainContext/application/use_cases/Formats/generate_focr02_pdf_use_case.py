from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_cr_02_repo import FOCR02Repo


class GenerateFoCr02PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, focr02_repo: FOCR02Repo):
        self.pdf_generator = pdf_generator
        self.focr02_repo = focr02_repo

    def execute(self, focr02_id: int) -> bytes:
        focr02_data = self.focr02_repo.get_focr02_by_id(focr02_id)
        if not focr02_data:
            raise ValueError("FOCR02 no encontrado")

        return self.pdf_generator.generate_focr02_pdf(data=focr02_data)
from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_ir_02_repo import FOIR02Repo


class GenerateFoIr02PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foir02_repo: FOIR02Repo):
        self.pdf_generator = pdf_generator
        self.foir02_repo = foir02_repo

    def execute(self, foir02_id: int) -> bytes:
        foir02_data = self.foir02_repo.get_foir02_by_id(foir02_id)
        if not foir02_data:
            raise ValueError("FOIR02 no encontrado")

        return self.pdf_generator.generate_foir02_pdf(data=foir02_data.__dict__)
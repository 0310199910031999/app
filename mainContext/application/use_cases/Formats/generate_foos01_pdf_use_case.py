from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_os_01_repo import FOOS01Repo


class GenerateFoOs01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, foos01_repo: FOOS01Repo):
        self.pdf_generator = pdf_generator
        self.foos01_repo = foos01_repo

    def execute(self, foos01_id: int) -> bytes:
        foos01_data = self.foos01_repo.get_foos01_by_id(foos01_id)

        if not foos01_data:
            raise ValueError(f"No se encontró el reporte FO-OS-01 con ID {foos01_id}")

        return self.pdf_generator.generate_foos01_pdf(data=foos01_data.__dict__)
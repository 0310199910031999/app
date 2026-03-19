from mainContext.application.ports.pdf_generator_port import PDFGeneratorPort
from mainContext.application.ports.Formats.fo_le_01_repo import FOLE01Repo

class GenerateFoLe01PdfUseCase:
    def __init__(self, pdf_generator: PDFGeneratorPort, fole01_repo: FOLE01Repo):
        self.pdf_generator = pdf_generator
        self.fole01_repo = fole01_repo

    def execute(self, fole01_id: int) -> bytes:
        # 1. Obtener los datos usando tu puerto existente
        fole01_data = self.fole01_repo.get_fole01_by_id(fole01_id)
        
        if not fole01_data:
            raise ValueError(f"No se encontró el reporte FO-LE-01 con ID {fole01_id}")

        pdf_bytes = self.pdf_generator.generate_fole01_pdf(data=fole01_data.__dict__)  # O data_dict si usas un Mapper
        
        return pdf_bytes
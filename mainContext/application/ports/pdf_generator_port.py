from abc import ABC, abstractmethod
from typing import Dict, Any

class PDFGeneratorPort(ABC):

    @abstractmethod
    def generate_fole01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF a partir de los datos proporcionados.
        """
        pass
from abc import ABC, abstractmethod
from typing import Dict, Any

class PDFGeneratorPort(ABC):

    @abstractmethod
    def generate_fole01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foim01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-IM-01 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foim03_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-IM-03 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_fosp01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-SP-01 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_fosc01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-SC-01 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foos01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-OS-01 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foem01_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-EM-01 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foem01_1_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-EM-01_1 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_fopc02_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-PC-02 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_fopp02_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-PP-02 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_focr02_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-CR-02 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foir02_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-IR-02 a partir de los datos proporcionados.
        """
        pass

    @abstractmethod
    def generate_foro05_pdf(self, data: Dict[str, Any]) -> bytes:
        """
        Genera un PDF FO-RO-05 a partir de los datos proporcionados.
        """
        pass
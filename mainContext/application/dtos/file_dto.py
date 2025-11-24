from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List


@dataclass
class FileTableClosedDTO:
    """DTO para files cerrados en tabla"""
    folio: str
    client_name: str
    date_closed: Optional[datetime]
    date_invoiced: Optional[datetime]
    uuid: str
    status: str


@dataclass
class FileTableOpenDTO:
    """DTO para files abiertos en tabla"""
    folio: str
    client_name: str
    date_created: datetime
    services: List[str]  # Códigos de servicios únicos


@dataclass
class FileInvoiceDTO:
    """DTO para facturar un file"""
    uuid: str

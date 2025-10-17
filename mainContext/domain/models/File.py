from dataclasses import dataclass
from datetime import date
from mainContext.domain.models import Client

@dataclass
class File:
    id: str
    client : Client
    date_created: date
    status : str
    date_closed : date
    date_invoiced : date
    folio_invoice : str
    uuid : str
    folio : str
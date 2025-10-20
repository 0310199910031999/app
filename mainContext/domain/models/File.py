from dataclasses import dataclass
from datetime import date, datetime
from mainContext.domain.models import Client

@dataclass
class File:
    id: int
    client : Client
    date_created: datetime
    status : str
    date_closed : datetime
    date_invoiced : datetime
    folio_invoice : str
    uuid : str
    folio : str
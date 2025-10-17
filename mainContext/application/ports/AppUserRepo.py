from abc import ABC, abstractmethod
from typing import List, Optional

class AppUserRepo(ABC):
    @abstractmethod
    def listWithClientName(self) -> List[dict]:
        pass
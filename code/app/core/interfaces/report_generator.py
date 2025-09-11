from abc import ABC, abstractmethod
from typing import List
from app.core.entities.repository import Repository

class ReportGenerator(ABC):
    @abstractmethod
    def generate(self, repos: List[Repository], file_path: str) -> None:
        ...

from abc import ABC, abstractmethod
from typing import Dict

class StaticAnalyzer(ABC):
    @abstractmethod
    def analyze(self, repo_path: str) -> Dict[str, float]:
        ...
from abc import ABC, abstractmethod
from contextlib import contextmanager

class RepositoryCloner(ABC):
    @abstractmethod
    @contextmanager
    def clone(self, repo_url: str, local_path: str):
        pass
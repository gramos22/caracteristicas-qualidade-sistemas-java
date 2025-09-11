from abc import ABC, abstractmethod

class RepositoryCloner(ABC):
    @abstractmethod
    def clone(self, repo_url: str, local_path: str) -> bool:
        ...
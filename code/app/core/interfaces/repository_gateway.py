from abc import ABC, abstractmethod
from typing import List
from app.core.entities.repository import Repository

class RepositoryGateway(ABC):
    @abstractmethod
    def get_popular_java_repos(self, count: int) -> List[Repository]:
        pass
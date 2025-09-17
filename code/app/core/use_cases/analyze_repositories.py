import os
from typing import List
from app.core.entities.repository import Repository
from app.core.interfaces.repository_gateway import RepositoryGateway
from app.core.interfaces.repository_cloner import RepositoryCloner
from app.core.interfaces.static_analyzer import StaticAnalyzer

class AnalyzeRepositories:
    def __init__(
        self,
        repository_gateway: RepositoryGateway,
        repository_cloner: RepositoryCloner,
        static_analyzer: StaticAnalyzer,
    ):
        self.repository_gateway = repository_gateway
        self.repository_cloner = repository_cloner
        self.static_analyzer = static_analyzer

    def execute(self, repo_count: int, temp_clone_path: str) -> List[Repository]:
        repositories = self.repository_gateway.get_popular_java_repos(repo_count)
        analyzed_repos = []

        for i, repo in enumerate(repositories):
            repo_local_path = os.path.join(temp_clone_path, repo.name)
            try:
                with self.repository_cloner.clone(repo.url, repo_local_path) as path:
                    metrics = self.static_analyzer.analyze(path)
                    if metrics:
                        repo.total_loc = metrics.get("total_loc")
                        repo.total_comments = metrics.get("total_comments")
                        repo.java_files = metrics.get("java_files")
                        repo.avg_loc_per_file = metrics.get("avg_loc_per_file")
                        repo.avg_comments_per_file = metrics.get("avg_comments_per_file")
                        repo.cbo_avg = metrics.get("cbo_avg")
                        repo.dit_avg = metrics.get("dit_avg")
                        repo.lcom_avg = metrics.get("lcom_avg")
                        repo.cbo_total = metrics.get("cbo_total")
                        repo.dit_total = metrics.get("dit_total")
                        repo.lcom_total = metrics.get("lcom_total")
                analyzed_repos.append(repo)
            except Exception:
                if os.path.exists(repo_local_path):
                    try:
                        import shutil
                        shutil.rmtree(repo_local_path, ignore_errors=True)
                    except Exception:
                        pass
        return analyzed_repos
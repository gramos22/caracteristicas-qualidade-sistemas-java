import tempfile
from typing import List, Dict, Any
from app.core.entities.repository import Repository


class ListPopularRepos:
    def __init__(self, github_gateway, report_generator, cloner, analyzer):
        self.github = github_gateway
        self.report = report_generator
        self.cloner = cloner
        self.analyzer = analyzer

    def _node_to_entity(self, node: Dict[str, Any]) -> Repository:
        return Repository(
            name=node.get("name"),
            stargazer_count=node.get("stargazerCount", 0),
            url=node.get("url"),
            created_at=node.get("createdAt"),
            updated_at=node.get("updatedAt"),
            releases_count=node.get("releases", {}).get("totalCount", 0),
            primary_language=node.get("primaryLanguage", {}).get("name") if node.get("primaryLanguage") else None,
            merged_pull_requests=node.get("mergedPullRequests", {}).get("totalCount", 0),
            total_issues=node.get("totalIssues", {}).get("totalCount", 0),
            closed_issues=node.get("closedIssues", {}).get("totalCount", 0),
        )

    def execute(self, number_of_repos: int, file_path: str, batch_size: int = 25) -> str:
        q = "language:Java sort:stars-desc"
        repos: List[Repository] = []
        after = None

        while len(repos) < number_of_repos:
            first = min(batch_size, number_of_repos - len(repos))

            data = self.github.search_repositories(q, first=first, after=after)
            search = data.get("search", {})
            edges = search.get("edges", [])

            for edge in edges:
                repo_entity = self._node_to_entity(edge["node"])

                with tempfile.TemporaryDirectory() as temp_dir:
                    print(f"Clonando {repo_entity.name}...")
                    clone_success = self.cloner.clone(repo_entity.url, temp_dir)
                    if clone_success:
                        print(f"Analisando {repo_entity.name} com CK...")
                        metrics = self.analyzer.analyze(temp_dir)
                        repo_entity.cbo = metrics.get("cbo")
                        repo_entity.dit = metrics.get("dit")
                        repo_entity.lcom = metrics.get("lcom")
                    else:
                        print(f"Falha ao clonar {repo_entity.name}")

                repos.append(repo_entity)

            page_info = search.get("pageInfo", {})
            if not page_info.get("hasNextPage"):
                break

            after = page_info.get("endCursor")

        self.report.generate(repos, file_path)
        return file_path

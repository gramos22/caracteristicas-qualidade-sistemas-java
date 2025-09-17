import requests
from typing import List, Dict, Any
from app.core.entities.repository import Repository
from app.core.interfaces.repository_gateway import RepositoryGateway
from app.infrastructure.config.settings import Settings
from app.infrastructure.graphql.queries import SEARCH_REPOS_PAGINATED

class GithubGateway(RepositoryGateway):
    def __init__(self):
        self.api_url = Settings.API_URL
        self.token = Settings.GITHUB_TOKEN
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN not set in settings")

    def _execute_query(self, query: str, variables: dict) -> Dict[str, Any]:
        resp = requests.post(
            self.api_url,
            json={"query": query, "variables": variables},
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=Settings.TIMEOUT
        )
        resp.raise_for_status()
        payload = resp.json()
        if "errors" in payload:
            raise RuntimeError(payload["errors"])
        return payload["data"]

    def _get_releases_count(self, owner: str, repo: str) -> int:
        url = f"https://api.github.com/repos/{owner}/{repo}/releases"
        headers = {"Authorization": f"Token {self.token}"}
        page = 1
        releases = []
        while True:
            response = requests.get(f"{url}?page={page}&per_page=100", headers=headers)
            if response.status_code == 200:
                page_releases = response.json()
                if not page_releases:
                    break
                releases.extend(page_releases)
                page += 1
            else:
                break
        return len(releases)

    def get_popular_java_repos(self, count: int) -> List[Repository]:
        all_repos = []
        cursor = None
        has_next_page = True

        while has_next_page and len(all_repos) < count:
            first = min(100, count - len(all_repos))
            variables = {
                "q": "language:java sort:stars-desc",
                "first": first,
                "after": cursor
            }
            
            data = self._execute_query(SEARCH_REPOS_PAGINATED, variables)
            search_data = data['search']
            
            for node in search_data['nodes']:
                if not node: continue
                owner = node['url'].split('/')[-2]
                repo_name = node['name']
                releases_count = self._get_releases_count(owner, repo_name)
                repo_data = {
                    'name': node['name'],
                    'url': node['url'],
                    'stargazerCount': node['stargazerCount'],
                    'createdAt': node['createdAt'],
                    'releases': releases_count
                }
                all_repos.append(Repository.model_validate(repo_data))

            page_info = search_data['pageInfo']
            cursor = page_info['endCursor']
            has_next_page = page_info['hasNextPage']
            
        return all_repos
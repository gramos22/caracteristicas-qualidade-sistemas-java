import requests
from typing import Optional, Dict, Any
from app.infrastructure.config.settings import Settings
from app.infrastructure.graphql.queries import SEARCH_REPOS_PAGINATED

class GitHubGateway:
    def __init__(self):
        self.api_url = Settings.API_URL
        self.token = Settings.GITHUB_TOKEN
        if not self.token:
            raise RuntimeError("GITHUB_TOKEN not set")

    def execute_query(self, query: str, variables: dict) -> Dict[str, Any]:
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

    def search_repositories(self, q: str, first: int, after: Optional[str] = None):
        vars_ = {"q": q, "first": first, "after": after}
        return self.execute_query(SEARCH_REPOS_PAGINATED, vars_)

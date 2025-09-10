from dataclasses import dataclass
from typing import Optional

@dataclass
class Repository:
    name: str
    stargazer_count: int
    url: str
    created_at: str
    updated_at: str
    releases_count: int
    primary_language: Optional[str]
    merged_pull_requests: int
    total_issues: int
    closed_issues: int
    cbo: Optional[float] = None
    dit: Optional[float] = None
    lcom: Optional[float] = None

    @property
    def closed_issues_percentage(self) -> float:
        if self.total_issues == 0:
            return 0.0
        return (self.closed_issues / self.total_issues) * 100

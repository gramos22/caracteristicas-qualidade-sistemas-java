from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class Repository(BaseModel):
    name: str
    url: str
    stars: int = Field(..., alias='stargazerCount')
    created_at: datetime = Field(..., alias='createdAt')
    releases: int
    total_loc: Optional[int] = 0
    total_comments: Optional[int] = 0
    java_files: Optional[int] = 0
    avg_loc_per_file: Optional[float] = 0.0
    avg_comments_per_file: Optional[float] = 0.0
    cbo_avg: Optional[float] = 0.0
    dit_avg: Optional[float] = 0.0
    lcom_avg: Optional[float] = 0.0
    cbo_total: Optional[int] = 0
    dit_total: Optional[int] = 0
    lcom_total: Optional[float] = 0.0

    @property
    def age_in_years(self) -> int:
        if self.created_at.tzinfo is None:
            return (datetime.now() - self.created_at).days // 365
        return (datetime.now(timezone.utc) - self.created_at).days // 365
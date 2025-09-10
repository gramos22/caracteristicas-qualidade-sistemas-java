from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    BATCH_SIZE: int = int(os.getenv("BATCH_SIZE", "25"))
    API_URL: str = os.getenv("GITHUB_API_URL", "https://api.github.com/graphql")
    TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "30"))

settings = Settings()